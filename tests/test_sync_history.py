import json
from pathlib import Path

import pytest

from api.sync_history import SyncHistoryStore


def test_history_isolated_by_account(tmp_path):
    store = SyncHistoryStore(tmp_path / "h.json")
    t1 = store.record_success("AccountA", "owner/repo1")
    t2 = store.record_success("AccountB", "owner/repo2")
    assert store.get_map("accounta") == {"owner/repo1": t1}
    assert store.get_map("accountb") == {"owner/repo2": t2}
    assert store.get_map("accounta") != store.get_map("accountb")


def test_latest_successful_is_last_recorded_and_preview_does_not_change(tmp_path):
    store = SyncHistoryStore(tmp_path / "h.json")
    t1 = store.record_success("demo-user", "demo/repo")
    # simulate later successful sync overwriting with newer timestamp (record_success is only called on actual success)
    t2 = store.record_success("demo-user", "demo/repo")
    assert t2 >= t1
    assert store.get_last_successful("demo-user", "demo/repo") == t2
    # "preview" path: reads only
    before = store.path.read_text(encoding="utf-8")
    assert store.get_map("demo-user") == {"demo/repo": t2}
    assert store.get_last_successful("demo-user", "demo/repo") == t2
    after = store.path.read_text(encoding="utf-8")
    assert before == after


def test_case_insensitive_account_read_tolerance_without_rewrite(tmp_path):
    path = tmp_path / "h.json"
    data = {
        "accounts": {
            "GabrielRules": {
                "repos": {
                    "GabrielRules/DREAMEROL-SYNC": {"last_successful_sync": "2026-11-10T10:00:00Z"}
                }
            }
        }
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    store = SyncHistoryStore(path)
    assert store.get_map("gabrielrules") == {"GabrielRules/DREAMEROL-SYNC": "2026-11-10T10:00:00Z"}
    assert store.get_last_successful("GabrielRules", "GabrielRules/DREAMEROL-SYNC") == "2026-11-10T10:00:00Z"
    assert path.read_text(encoding="utf-8") == before  # no rewrite/delete


def test_record_success_writes_canonical_account_key_without_deleting_others(tmp_path):
    path = tmp_path / "h.json"
    data = {
        "accounts": {
            "LegacyCase": {"repos": {"owner/a": {"last_successful_sync": "2026-01-01T00:00:00Z"}}},
            "other-user": {"repos": {"owner/b": {"last_successful_sync": "2026-01-02T00:00:00Z"}}},
        }
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    store = SyncHistoryStore(path)
    ts = store.record_success("legacycase", "owner/new")
    saved = json.loads(path.read_text(encoding="utf-8"))
    # existing unrelated account preserved; legacy key not deleted (we only add canonical)
    assert saved["accounts"]["other-user"]["repos"]["owner/b"]["last_successful_sync"] == "2026-01-02T00:00:00Z"
    assert "LegacyCase" in saved["accounts"]
    assert saved["accounts"]["legacycase"]["repos"]["owner/new"]["last_successful_sync"] == ts


def test_operations_survive_new_store_instance_and_keep_latest_twenty(tmp_path):
    path = tmp_path / "h.json"
    timestamps = iter([f"2026-11-19T20:{index:02d}:00Z" for index in range(21)])
    store = SyncHistoryStore(path, clock=lambda: next(timestamps))
    for index in range(21):
        store.record_operation(
            "Demo-User",
            f"op-{index:02d}",
            [{"repository": "owner/repo", "status": "synced", "message": "ok"}],
            targets=["owner/repo"],
        )
    reloaded = SyncHistoryStore(path)
    operations = reloaded.get_operations("demo-user")
    assert len(operations) == 20
    assert operations[0]["operation_id"] == "op-20"
    assert operations[-1]["operation_id"] == "op-01"
    assert operations[0]["targets"] == ["owner/repo"]
    assert operations[0]["results"] == [
        {"repository": "owner/repo", "status": "synced", "message": "ok"}
    ]
    assert operations[0]["summary"] == {
        "success": 1,
        "skipped": 0,
        "failed": 0,
        "manual": 0,
    }


def test_record_operation_dedupes_id_and_preserves_existing_success_map(tmp_path):
    path = tmp_path / "h.json"
    store = SyncHistoryStore(path)
    ts = store.record_success("demo-user", "owner/keep")
    store.record_operation(
        "demo-user",
        "same-id",
        [{"repository": "owner/a", "status": "error", "message": "HTTP 403"}],
        targets=["owner/a"],
    )
    store.record_operation(
        "DEMO-USER",
        "same-id",
        [{"repository": "owner/a", "status": "synced"}],
        targets=["owner/a"],
    )
    reloaded = SyncHistoryStore(path)
    operations = reloaded.get_operations("demo-user")
    assert len(operations) == 1
    assert operations[0]["operation_id"] == "same-id"
    assert operations[0]["results"][0]["status"] == "synced"
    assert reloaded.get_map("demo-user") == {"owner/keep": ts}
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["accounts"]["demo-user"]["repos"]["owner/keep"]["last_successful_sync"] == ts

