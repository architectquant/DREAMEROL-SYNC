from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from requests.exceptions import HTTPError, RequestException

from api.app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_healthz_reports_ok(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Pragma"] == "no-cache"


def test_html_pages_are_not_cached(client):
    for path in ("/", "/dashboard"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["Cache-Control"] == "no-store"
        assert response.headers["Pragma"] == "no-cache"


def make_github_client():
    github = Mock()
    github.session = Mock()
    github.get_authenticated_user.return_value = {"login": "demo-user"}
    return github


def make_fork(full_name):
    return {"full_name": full_name, "fork": True}


def github_http_error(status_code):
    response = Mock(status_code=status_code)
    return HTTPError(f"GitHub returned {status_code}", response=response)


def patch_github(monkeypatch, github):
    monkeypatch.setattr("api.routes.GitHubClient", lambda token: github)


def patch_synchronizer(monkeypatch, synchronizer):
    monkeypatch.setattr("api.routes.ForkSynchronizer", lambda client: synchronizer)


def post_sync(client, payload, token="test-token"):
    return client.post(
        "/api/sync",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )


def test_live_sync_processes_only_selected_forks_that_are_behind(
    client, monkeypatch
):
    github = make_github_client()
    patch_github(monkeypatch, github)

    behind_fork = make_fork("demo/behind")
    current_fork = make_fork("demo/current")
    unselected_fork = make_fork("demo/unselected")

    synchronizer = Mock()
    synchronizer.get_forks.return_value = [
        behind_fork,
        current_fork,
        unselected_fork,
    ]
    synchronizer.preview_fork.side_effect = [
        {"repository": "demo/behind", "status": "behind", "behind_by": 3},
        {"repository": "demo/current", "status": "up-to-date", "behind_by": 0},
    ]
    synchronizer.sync_all.return_value = [
        {
            "repository": "demo/behind",
            "status": "synced",
            "message": "Synced 3 upstream commits.",
            "behind_by": 3,
        }
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(
        client,
        {
            "dry_run": False,
            "confirmation": "SYNC",
            "repositories": ["demo/behind", "demo/current"],
        },
    )

    assert response.status_code == 200
    assert [item["repository"] for item in response.json()["results"]] == [
        "demo/behind",
        "demo/current",
    ]
    assert [item["status"] for item in response.json()["results"]] == [
        "synced",
        "up-to-date",
    ]

    assert synchronizer.preview_fork.call_count == 2
    synchronizer.preview_fork.assert_any_call(behind_fork)
    synchronizer.preview_fork.assert_any_call(current_fork)

    synchronizer.sync_all.assert_called_once_with(forks=[behind_fork])
    github.session.close.assert_called_once_with()

def test_live_sync_processes_multiple_selected_behind_forks(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)

    behind_a = make_fork("demo/behind-a")
    behind_b = make_fork("demo/behind-b")
    current = make_fork("demo/current")

    synchronizer = Mock()
    synchronizer.get_forks.return_value = [behind_a, behind_b, current]
    synchronizer.preview_fork.side_effect = [
        {"repository": "demo/behind-a", "status": "behind", "behind_by": 2},
        {"repository": "demo/behind-b", "status": "behind", "behind_by": 1},
        {"repository": "demo/current", "status": "up-to-date", "behind_by": 0},
    ]
    synchronizer.sync_all.return_value = [
        {"repository": "demo/behind-a", "status": "synced", "message": "Synced 2 upstream commits.", "behind_by": 2},
        {"repository": "demo/behind-b", "status": "synced", "message": "Synced 1 upstream commits.", "behind_by": 1},
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(
        client,
        {
            "dry_run": False,
            "confirmation": "SYNC",
            "repositories": ["demo/behind-a", "demo/behind-b", "demo/current"],
        },
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert [item["repository"] for item in results] == [
        "demo/behind-a",
        "demo/behind-b",
        "demo/current",
    ]
    assert [item["status"] for item in results] == ["synced", "synced", "up-to-date"]
    assert len(results) == 3
    synchronizer.sync_all.assert_called_once_with(forks=[behind_a, behind_b])
    github.session.close.assert_called_once_with()


def _use_temp_sync_history(client, tmp_path):
    from api.sync_history import SyncHistoryStore

    store = SyncHistoryStore(tmp_path / "sync_history.json")
    client.app.state.sync_history = store
    return store


def test_preview_includes_last_sync_and_does_not_persist(client, monkeypatch, tmp_path):
    github = make_github_client()
    patch_github(monkeypatch, github)
    store = _use_temp_sync_history(client, tmp_path)

    synchronizer = Mock()
    synchronizer.preview_all.return_value = [
        {"repository": "demo/a", "status": "behind", "message": "1 upstream commit(s) available.", "behind_by": 1}
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True})

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["repository"] == "demo/a"
    assert result["last_successful_sync"] is None
    assert store.get_map("demo-user") == {}
    assert not store.path.exists()


def test_preview_result_exposes_ahead_by_for_counter_calculation(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.preview_all.return_value = [
        {"repository": "demo/a", "status": "behind", "ahead_by": 0, "behind_by": 2}
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True})

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["ahead_by"] == 0
    assert result["behind_by"] == 2


def test_successful_sync_records_and_persists_last_sync(client, monkeypatch, tmp_path):
    github = make_github_client()
    patch_github(monkeypatch, github)
    store = _use_temp_sync_history(client, tmp_path)

    behind_fork = make_fork("demo/behind")
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [behind_fork]
    synchronizer.preview_fork.return_value = {
        "repository": "demo/behind", "status": "behind", "behind_by": 2
    }
    synchronizer.sync_all.return_value = [
        {"repository": "demo/behind", "status": "synced", "message": "Synced 2 upstream commits.", "behind_by": 2}
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(
        client,
        {"dry_run": False, "confirmation": "SYNC", "repositories": ["demo/behind"]},
    )

    assert response.status_code == 200
    ts = response.json()["results"][0]["last_successful_sync"]
    assert isinstance(ts, str) and ts.endswith("Z")
    assert store.get_map("demo-user") == {"demo/behind": ts}

    # Preview returns persisted timestamp and does not change it
    synchronizer.preview_all.return_value = [
        {"repository": "demo/behind", "status": "up-to-date", "behind_by": 0}
    ]
    preview = post_sync(client, {"dry_run": True})
    assert preview.status_code == 200
    assert preview.json()["results"][0]["last_successful_sync"] == ts
    assert store.get_map("demo-user") == {"demo/behind": ts}

    # Restart simulation: new store instance reading same file
    from api.sync_history import SyncHistoryStore

    reloaded = SyncHistoryStore(store.path)
    assert reloaded.get_map("demo-user") == {"demo/behind": ts}


def test_failed_sync_does_not_overwrite_last_successful(client, monkeypatch, tmp_path):
    github = make_github_client()
    patch_github(monkeypatch, github)
    store = _use_temp_sync_history(client, tmp_path)
    previous = store.record_success("demo-user", "demo/behind")

    behind_fork = make_fork("demo/behind")
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [behind_fork]
    synchronizer.preview_fork.return_value = {
        "repository": "demo/behind", "status": "behind", "behind_by": 1
    }
    synchronizer.sync_all.return_value = [
        {"repository": "demo/behind", "status": "error", "message": "HTTP 403: Resource not accessible by integration"}
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(
        client,
        {"dry_run": False, "confirmation": "SYNC", "repositories": ["demo/behind"]},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "error"
    assert result["last_successful_sync"] == previous
    assert store.get_map("demo-user") == {"demo/behind": previous}

def test_dry_run_list_mode_returns_pending_without_compare(client, monkeypatch, tmp_path):
    github = make_github_client()
    patch_github(monkeypatch, github)
    store = _use_temp_sync_history(client, tmp_path)
    store.record_success("demo-user", "demo/a")

    forks = [make_fork("demo/a"), make_fork("demo/b")]
    synchronizer = Mock()
    synchronizer.get_forks.return_value = forks
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    assert response.json() == {
        "account": "demo-user",
        "total": 2,
        "diagnostics": None,
        "results": [

            {"repository": "demo/a", "status": "pending", "message": "Not checked yet.", "ahead_by": None, "behind_by": None, "last_successful_sync": store.get_map("demo-user")["demo/a"], "fork": True},
            {"repository": "demo/b", "status": "pending", "message": "Not checked yet.", "ahead_by": None, "behind_by": None, "last_successful_sync": None, "fork": True},
        ],
    }
    synchronizer.preview_all.assert_not_called()
    synchronizer.preview_fork.assert_not_called()
    assert store.get_map("demo-user") == {"demo/a": store.get_map("demo-user")["demo/a"]}
    github.session.close.assert_called_once_with()


def test_dry_run_list_includes_read_only_diagnostics(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [make_fork("demo/a")]
    synchronizer.get_last_diagnostics.return_value = {
        "owned_repositories": 12,
        "fork_candidates": 4,
        "valid_forks": 3,
        "unavailable_forks": 1,
    }
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    assert response.json()["diagnostics"] == {
        "owned_repositories": 12,
        "fork_candidates": 4,
        "valid_forks": 3,
        "unavailable_forks": 1,
    }
    synchronizer.preview_all.assert_not_called()
    synchronizer.preview_fork.assert_not_called()


def test_dry_run_list_exposes_existing_fork_property(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [
        make_fork("demo/fork"),
        {"full_name": "demo/original", "fork": False},
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    assert [item["fork"] for item in response.json()["results"]] == [True, False]


def test_dry_run_list_keeps_missing_or_invalid_fork_flags_reportable(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [
        make_fork("demo/ok"),
        {"full_name": "demo/missing"},
        {"full_name": "demo/invalid", "fork": "true"},
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    results = response.json()["results"]
    assert results[0]["fork"] is True
    assert "fork" not in results[1]
    assert "fork" not in results[2]


@pytest.mark.parametrize("account", ["architectquant", "GabrielRules"])
def test_dry_run_list_exposes_fork_flag_for_account_repositories(client, monkeypatch, account):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [
        make_fork(f"{account}/fork"),
        {"full_name": f"{account}/original", "fork": False},
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    results = response.json()["results"]
    assert [item["repository"] for item in results] == [f"{account}/fork", f"{account}/original"]
    assert [item["fork"] for item in results] == [True, False]


def test_dry_run_subset_checks_only_requested_repositories(client, monkeypatch, tmp_path):

    github = make_github_client()
    patch_github(monkeypatch, github)
    store = _use_temp_sync_history(client, tmp_path)

    a, b, c = make_fork("demo/a"), make_fork("demo/b"), make_fork("demo/c")
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [a, b, c]

    def preview_side(fork):
        name = fork["full_name"]
        if name == "demo/a":
            return {"repository": name, "status": "behind", "message": "1 upstream commit(s) available.", "behind_by": 1}
        if name == "demo/c":
            return {"repository": name, "status": "error", "message": "compare failed"}
        raise AssertionError(f"unexpected preview for {name}")

    synchronizer.preview_fork.side_effect = preview_side
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "repositories": ["demo/a", "demo/c"]})

    assert response.status_code == 200
    results = response.json()["results"]
    assert [r["repository"] for r in results] == ["demo/a", "demo/c"]
    assert results[0]["status"] == "behind"
    assert results[1]["status"] == "error"
    assert all(r["last_successful_sync"] is None for r in results)
    synchronizer.preview_all.assert_not_called()
    assert [call.args[0]["full_name"] for call in synchronizer.preview_fork.call_args_list] == ["demo/a", "demo/c"]
    assert store.get_map("demo-user") == {}


def test_dry_run_subset_rejects_unknown_repository(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [make_fork("demo/a")]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "repositories": ["demo/missing"]})

    assert response.status_code == 400
    assert "Preview again" in response.json()["detail"]
    synchronizer.preview_fork.assert_not_called()


def test_default_dry_run_preview_still_compares_all(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.preview_all.return_value = [
        {"repository": "demo/a", "status": "up-to-date", "behind_by": 0}
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True})

    assert response.status_code == 200
    assert response.json()["results"][0]["repository"] == "demo/a"
    synchronizer.preview_all.assert_called_once_with()
    synchronizer.get_forks.assert_not_called()


def test_dry_run_list_dedupes_duplicate_forks(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    # duplicates by full_name (e.g. repeated pages/batches)
    synchronizer.get_forks.return_value = [
        make_fork("GabrielRules/DREAMEROL-SYNC"),
        make_fork("GabrielRules/DREAMEROL-SYNC"),
        make_fork("GabrielRules/Other"),
        make_fork("GabrielRules/Other"),
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert [r["repository"] for r in data["results"]] == [
        "GabrielRules/DREAMEROL-SYNC",
        "GabrielRules/Other",
    ]
    assert len(data["results"]) == len({r["repository"] for r in data["results"]})
    synchronizer.preview_all.assert_not_called()


def test_dry_run_list_36_unique_repositories_total_36(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    forks = [make_fork(f"user/repo{i}") for i in range(1, 37)]
    # inject duplicates interleaved (progressive/batch merge safety)
    duped = forks[:10] + [forks[0], forks[5]] + forks[10:] + [forks[35], forks[35]]
    synchronizer.get_forks.return_value = duped
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 36
    names = [r["repository"] for r in data["results"]]
    assert len(names) == 36
    assert len(set(names)) == 36
    assert names == [f"user/repo{i}" for i in range(1, 37)]


def test_dry_run_subset_dedupes_result_rows(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    a = make_fork("demo/a")
    synchronizer = Mock()
    synchronizer.get_forks.return_value = [a, a]
    synchronizer.preview_fork.return_value = {"repository": "demo/a", "status": "up-to-date", "behind_by": 0}
    patch_synchronizer(monkeypatch, synchronizer)

    # request unique repo but server-side fork list had dup entries; result must be single
    response = post_sync(client, {"dry_run": True, "repositories": ["demo/a"]})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert [r["repository"] for r in data["results"]] == ["demo/a"]


def test_preview_default_dedupes_results(client, monkeypatch):
    github = make_github_client()
    patch_github(monkeypatch, github)
    synchronizer = Mock()
    synchronizer.preview_all.return_value = [
        {"repository": "demo/a", "status": "up-to-date", "behind_by": 0},
        {"repository": "demo/a", "status": "up-to-date", "behind_by": 0},
        {"repository": "demo/b", "status": "behind", "behind_by": 1},
    ]
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert [r["repository"] for r in data["results"]] == ["demo/a", "demo/b"]


def test_dry_run_list_serializes_github_fork_flag_from_discovery(client, monkeypatch):
    github = Mock()
    github.session = Mock()
    github.get_authenticated_user.return_value = {"login": "GabrielRules"}
    repositories = [
        {
            "full_name": f"GabrielRules/fork-{index}",
            "fork": True,
            "default_branch": "main",
            "parent": {"full_name": "Dreamerol/upstream", "default_branch": "main"},
        }
        for index in range(34)
    ]
    repositories.extend(
        [
            {
                "full_name": "GabrielRules/original-a",
                "fork": False,
                "default_branch": "main",
            },
            {
                "full_name": "GabrielRules/original-b",
                "fork": False,
                "default_branch": "main",
            },
        ]
    )
    github.list_repositories.return_value = repositories
    monkeypatch.setattr("api.routes.GitHubClient", lambda token: github)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 200
    data = response.json()
    results = data["results"]
    assert data["total"] == 34
    assert len(results) == 34
    assert all(item["fork"] is True for item in results)
    assert all("original" not in item["repository"] for item in results)
    assert data["diagnostics"] == {
        "owned_repositories": 36,
        "fork_candidates": 34,
        "valid_forks": 34,
        "unavailable_forks": 0,
    }
    github.session.close.assert_called_once_with()


@pytest.mark.parametrize(
    "payload, detail",
    [
        (
            {"dry_run": False, "repositories": ["demo/behind"]},
            'Live synchronization requires confirmation="SYNC".',
        ),
        (
            {"dry_run": False, "confirmation": "sync", "repositories": ["demo/behind"]},
            'Live synchronization requires confirmation="SYNC".',
        ),
        (
            {"dry_run": False, "confirmation": "SYNC"},
            "Select at least one repository from the preview before syncing.",
        ),
        (
            {"dry_run": False, "confirmation": "SYNC", "repositories": []},
            "Select at least one repository from the preview before syncing.",
        ),
        (
            {
                "dry_run": False,
                "confirmation": "SYNC",
                "repositories": [f"demo/repo-{index}" for index in range(5001)],
            },
            "Too many repositories were selected.",
        ),
        (
            {"dry_run": False, "confirmation": "SYNC", "repositories": ["demo/a", "demo/a"]},
            "Duplicate repositories were selected.",
        ),
    ],
)
def test_live_sync_contract_rejections(client, payload, detail):
    response = post_sync(client, payload)

    assert response.status_code == 400
    assert response.json()["detail"] == detail


@pytest.mark.parametrize("status_code", [403, 429, 500])
def test_list_mode_reports_discovery_http_status(client, monkeypatch, status_code):
    patch_github(monkeypatch, make_github_client())
    synchronizer = Mock()
    synchronizer.get_forks.side_effect = github_http_error(status_code)
    patch_synchronizer(monkeypatch, synchronizer)

    response = post_sync(client, {"dry_run": True, "mode": "list"})

    assert response.status_code == 502
    assert response.json()["detail"] == (
        f"Could not load forks from GitHub (HTTP {status_code})."
    )
