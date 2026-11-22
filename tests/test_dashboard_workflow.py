import json
import subprocess
from pathlib import Path
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.app import app


ROOT = Path(__file__).resolve().parents[1]
APP_SOURCE = (ROOT / "DASHBOARD" / "app.js").read_text(encoding="utf-8")
THEME_GUARD_SOURCE = (ROOT / "DASHBOARD" / "theme_guard.js").read_text(encoding="utf-8")
CSS_SOURCE = (ROOT / "DASHBOARD" / "dashboard.css").read_text(encoding="utf-8")
INDEX_SOURCE = (ROOT / "DASHBOARD" / "index.html").read_text(encoding="utf-8")


def background_checks_source():
    start = APP_SOURCE.index("async function runBackgroundChecks")
    end = APP_SOURCE.index("async function preflightSelected", start)
    return APP_SOURCE[start:end]


def preflight_source():
    start = APP_SOURCE.index("async function preflightSelected")
    end = APP_SOURCE.index("async function retryCheck", start)
    return APP_SOURCE[start:end]


def page_show_source():
    start = APP_SOURCE.index("function handlePageShowRestore")
    end = APP_SOURCE.index('window.addEventListener("pageshow"', start)
    return APP_SOURCE[start:end]


def theme_guard_css_source():
    return CSS_SOURCE[CSS_SOURCE.index("@layer dreamerol-guard"):]


def apply_operation_source():
    start = APP_SOURCE.index("function applyOperation")
    end = APP_SOURCE.index("function setConnectionState", start)
    return APP_SOURCE[start:end]


def update_stats_source():
    start = APP_SOURCE.index("function updateStats")
    end = APP_SOURCE.index("function filteredRepos", start)
    return APP_SOURCE[start:end]


def run_node(script):
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = result.stdout.strip()
    return json.loads(stdout) if stdout else None


def test_three_selected_repositories_are_ready_then_confirmed():
    out = run_node(
        """
        import {isReadyCandidate,isSyncConfirmedRepository} from './DASHBOARD/utils.js';
        const names=['u/a','u/b','u/c'];
        const ready=names.map(repository=>({repository,fork:true,status:'pending',check_status:'pending',ahead_by:0,behind_by:1}));
        const confirmed=ready.map(repo=>({...repo,status:'behind',check_status:'ok'}));
        console.log(JSON.stringify({
            ready:ready.filter(isReadyCandidate).map(r=>r.repository),
            confirmed:confirmed.filter(isSyncConfirmedRepository).map(r=>r.repository),
        }));
        """
    )
    assert out == {
        "ready": ["u/a", "u/b", "u/c"],
        "confirmed": ["u/a", "u/b", "u/c"],
    }


def test_repo_display_order_groups_ready_before_synced_before_unsyncable():
    out = run_node(
        """
        import {sortReposForDisplay} from './DASHBOARD/utils.js';
        const repos=[
            {repository:'u/synced-first',fork:true,status:'up-to-date',ahead_by:0,behind_by:0},
            {repository:'u/ready-first',fork:true,status:'behind',ahead_by:0,behind_by:2},
            {repository:'u/unsyncable',fork:true,status:'diverged',ahead_by:1,behind_by:1},
            {repository:'u/ready-second',fork:true,status:'behind',ahead_by:0,behind_by:1},
            {repository:'u/synced-second',fork:true,status:'up-to-date',ahead_by:0,behind_by:0},
            {repository:'u/pending',fork:true,status:'pending'},
        ];
        console.log(JSON.stringify(sortReposForDisplay(repos).map(r=>r.repository)));
        """
    )
    assert out == [
        "u/ready-first",
        "u/ready-second",
        "u/synced-first",
        "u/synced-second",
        "u/unsyncable",
        "u/pending",
    ]
    assert "return sortReposForDisplay(repositories.filter((r) => {" in APP_SOURCE


def test_ready_to_sync_is_visible_before_background_checks_finish():
    out = run_node(
        """
        import {isReadyCandidate,isSyncableRepository,isSyncConfirmedRepository} from './DASHBOARD/utils.js';
        const repo={repository:'u/fast',fork:true,status:'pending',check_status:'pending',ahead_by:0,behind_by:2};
        console.log(JSON.stringify({
            ready:isReadyCandidate(repo),
            syncable:isSyncableRepository(repo),
            confirmed:isSyncConfirmedRepository(repo),
        }));
        """
    )
    assert out == {"ready": True, "syncable": False, "confirmed": False}
    assert "const selectableCount = repositories.filter((r) => isSelectableCandidate(r)).length;" in APP_SOURCE
    assert "Background checks continue" in APP_SOURCE


def test_sync_can_start_while_background_checks_continue():
    assert "if (syncInFlight || operationLock) return;" in APP_SOURCE
    assert "if (syncInFlight || previewInFlight) return;" not in APP_SOURCE
    assert "await preview();" not in APP_SOURCE
    assert "if (operationLockedNames.has(name)) continue;" in APP_SOURCE
    assert "Background checks continue." in APP_SOURCE
    assert "operationLock = true;" in APP_SOURCE
    assert "operationLock = false;" in APP_SOURCE
    assert 'syncButton.addEventListener("click", () => runSync("chosen"));' in APP_SOURCE
    assert 'syncAllButton.addEventListener("click", () => runSync("all"));' in APP_SOURCE


def test_one_success_and_one_failure_keep_per_repository_results():
    out = run_node(
        """
        import {summarizeSyncResults} from './DASHBOARD/utils.js';
        const results=[
            {repository:'u/ok',status:'synced',message:'Synced 1 upstream commit.'},
            {repository:'u/fail',status:'error',message:'HTTP 403'},
        ];
        console.log(JSON.stringify({summary:summarizeSyncResults(results),results}));
        """
    )
    assert out["summary"] == {"success": 1, "skipped": 0, "failed": 1, "manual": 1}
    assert [item["repository"] for item in out["results"]] == ["u/ok", "u/fail"]
    assert "renderResults(authoritative, historyList);" in APP_SOURCE


def test_timeout_and_retry_do_not_make_repository_ready():
    out = run_node(
        """
        import {isReadyCandidate} from './DASHBOARD/utils.js';
        const base={repository:'u/slow',fork:true,status:'pending',ahead_by:0,behind_by:1};
        console.log(JSON.stringify({
            timeout:isReadyCandidate({...base,check_status:'timeout'}),
            error:isReadyCandidate({...base,check_status:'error'}),
            retryable:isReadyCandidate(base),
        }));
        """
    )
    assert out == {"timeout": False, "error": False, "retryable": True}
    assert "CHECK_TIMEOUT_MS = 8000" in APP_SOURCE
    assert '"Check timeout"' in APP_SOURCE
    assert "retryCheck(repo.repository)" in APP_SOURCE


def test_preflight_uses_longer_timeout_than_batch_checks():
    assert "PREFLIGHT_TIMEOUT_MS = 30000" in APP_SOURCE
    assert "}, CHECK_TIMEOUT_MS * activeNames.length);" in background_checks_source()
    assert "}, PREFLIGHT_TIMEOUT_MS);" in preflight_source()
    assert "}, CHECK_TIMEOUT_MS);" not in preflight_source()


def test_refresh_restores_operation_without_returning_to_zero_counters():
    assert 'LAST_OPERATION_KEY_PREFIX = "dreamerol.lastOperation"' in APP_SOURCE
    assert "applyOperation(storedOperation, { source: \"restored\" });" in APP_SOURCE
    assert "renderHistory();" in APP_SOURCE
    assert "await restoreAuthoritativeOperation(gen);" in APP_SOURCE
    assert 'requestJson("/api/history"' in APP_SOURCE
    assert "if (clearOperation) {" in APP_SOURCE
    assert 'window.addEventListener("pageshow", handlePageShowRestore);' in APP_SOURCE
    assert "if (lastOperation && lastOperation.operationId === latest.operation_id && lastOperation.source !== \"restored\") return;" in APP_SOURCE
    assert "operationLockedNames = new Set();" in APP_SOURCE
    assert "Last recorded sync result:" in APP_SOURCE


def test_refresh_keeps_last_sync_counters_until_fresh_checks_finish():
    apply_source = apply_operation_source()
    stats_source = update_stats_source()
    assert "operationCounts = next.countsBefore" in apply_source
    assert "operationCountsAfter(next.countsBefore, next.summary, next.results, next.createdAt)" in apply_source
    assert "const snapshotActive = operationCounts" in stats_source
    assert "repositories.length === 0 || previewInFlight || backgroundScanActive || !liveCounts.complete" in stats_source
    assert "const counts = snapshotActive ? operationCounts : liveCounts;" in stats_source
    assert "if (computeDashboardCounts(repositories).complete) {" in APP_SOURCE


def test_reload_restores_saved_dashboard_without_rechecking_repositories():
    init_source = APP_SOURCE[APP_SOURCE.index("async function initDashboard"):APP_SOURCE.index("function toWelcome")]
    snapshot_source = APP_SOURCE[APP_SOURCE.index("function saveDashboardSnapshot"):APP_SOURCE.index("function loadDashboardSnapshot")]
    restore_source = APP_SOURCE[APP_SOURCE.index("function restoreDashboardSnapshot"):APP_SOURCE.index("function applyOperation")]
    assert 'DASHBOARD_SNAPSHOT_KEY_PREFIX = "dreamerol.dashboardSnapshot"' in APP_SOURCE
    assert "const savedSnapshot = loadDashboardSnapshot(currentAccount);" in init_source
    assert "if (savedSnapshot && snapshotOperationId === storedOperationId) {" in init_source
    assert "restoreDashboardSnapshot(savedSnapshot);" in init_source
    assert init_source.index("restoreDashboardSnapshot(savedSnapshot);") < init_source.index("await preview({ auto: true });")
    assert "if (!force && (previewInFlight || backgroundScanActive || syncInFlight || operationLock || sessionExpired)) return;" in snapshot_source
    assert 'statusFilter: filterSelect ? filterSelect.value : "all",' in snapshot_source
    assert 'searchText: searchInput ? searchInput.value : "",' in snapshot_source
    assert "filterSelect.value = snapshot.statusFilter;" in restore_source
    assert "searchInput.value = snapshot.searchText;" in restore_source
    assert 'window.addEventListener("pagehide", () => saveDashboardSnapshot({ force: true }));' in APP_SOURCE
    assert "previewInFlight = false;" in restore_source
    assert "backgroundScanActive = false;" in restore_source
    assert "preview(" not in restore_source
    assert "saveDashboardSnapshot();" in APP_SOURCE
    assert "clearDashboardSnapshot();" in APP_SOURCE


def test_bfcache_completed_batch_does_not_restart_or_reset_counters():
    source = page_show_source()
    assert "if (!event.persisted || syncInFlight || operationLock) return;" in source
    assert "if (initialized && !previewInFlight && !backgroundScanActive) {" in source
    assert "renderPreviewProgress(false);" in source
    assert "checkedCount = 0;" not in source
    assert "resetDashboardState(" not in source
    assert "initDashboard({ force: true });" in source
    assert source.index("if (initialized && !previewInFlight && !backgroundScanActive) {") < source.index("invalidatePendingOperations();")


def test_bfcache_active_batch_does_not_start_parallel_check():
    source = page_show_source()
    assert "if (previewInFlight || backgroundScanActive) {" in source
    assert "renderPreviewProgress(true);" in source
    assert source.index("if (previewInFlight || backgroundScanActive) {") < source.index("invalidatePendingOperations();")
    assert "preview(" not in source.replace("renderPreviewProgress", "")
    assert "void runBackgroundChecks(" not in source
    assert 'window.addEventListener("pageshow", handlePageShowRestore);' in APP_SOURCE
    assert "initDashboard();" in APP_SOURCE


def test_background_checks_never_overwrite_completed_operation():
    assert "if (operationLockedNames.has(name)) continue;" in APP_SOURCE
    assert "operationLockedNames = new Set(next.targets);" in APP_SOURCE
    assert "renderHistory();" in APP_SOURCE
    assert "applyOperation(storedOperation, { source: \"restored\" });" in APP_SOURCE


def test_background_checks_use_batched_requests():
    source = background_checks_source()
    assert "const BATCH_CHECK_SIZE = 10;" in APP_SOURCE
    assert "for (let i = 0; i < queue.length; i += BATCH_CHECK_SIZE)" in source
    assert "repositories: activeNames" in source
    assert "repositories: [targetName]" not in source
    assert "const byName = new Map();" in source
    assert "if (!isCurrent(gen)) return;" in source


def test_thirty_five_batched_results_keep_full_counter_set():
    out = run_node(
        """
        import {computeDashboardCounts, mergePreviewResult, mergePreviewError} from './DASHBOARD/utils.js';
        const names = Array.from({length:35}, (_, i) => `owner/repo-${i + 1}`);
        let repositories = names.map(repository => ({repository, fork:true, status:'pending', check_status:'pending', ahead_by:null, behind_by:null}));
        const results = names.map((repository, i) => ({repository, status:i === 0 ? 'behind' : 'up-to-date', ahead_by:0, behind_by:i === 0 ? 1 : 0}));
        const byName = new Map(results.map(result => [result.repository, result]));
        for (let i = 0; i < names.length; i += 10) {
            for (const name of names.slice(i, i + 10)) {
                const index = repositories.findIndex(r => r.repository === name);
                const result = byName.get(name) || null;
                if (result) {
                    repositories[index] = mergePreviewResult(repositories[index], result, name);
                    repositories[index].check_status = 'ok';
                } else {
                    repositories[index] = mergePreviewError(repositories[index], 'No matching result returned.', name);
                    repositories[index].check_status = 'error';
                }
            }
        }
        const counts = computeDashboardCounts(repositories);
        console.log(JSON.stringify({counts, checked:repositories.filter(r => r.check_status === 'ok').length}));
        """
    )
    assert out["counts"]["total"] == 35
    assert out["counts"]["up_to_date"] == 34
    assert out["counts"]["to_be_synced"] == 1
    assert out["counts"]["check_errors"] == 0
    assert out["checked"] == 35


def test_live_sync_requires_final_check_and_explicit_confirmation():
    assert "const preflight = await preflightSelected(requested);" in APP_SOURCE
    assert "const repos = preflight.filter((item) => item.ok).map((item) => item.name);" in APP_SOURCE
    assert "Excluded after safety check" in APP_SOURCE
    assert "if (!window.confirm(confirmMessage)) return;" in APP_SOURCE
    assert 'confirmation: "SYNC"' in APP_SOURCE
    assert "repositories: repos" in APP_SOURCE


def test_dry_run_does_not_create_operation_or_expose_operation_id(
    monkeypatch, tmp_path
):
    from api.sync_history import SyncHistoryStore

    client = TestClient(app)
    client.app.state.sync_history = SyncHistoryStore(tmp_path / "history.json")

    github = Mock()
    github.session = Mock()
    github.get_authenticated_user.return_value = {"login": "demo-user"}
    monkeypatch.setattr("api.routes.GitHubClient", lambda token: github)

    synchronizer = Mock()
    synchronizer.get_forks.return_value = [
        {"full_name": "demo/a", "fork": True},
    ]
    synchronizer.preview_fork.return_value = {
        "repository": "demo/a",
        "status": "behind",
        "ahead_by": 0,
        "behind_by": 1,
    }
    monkeypatch.setattr("api.routes.ForkSynchronizer", lambda client: synchronizer)

    response = client.post(
        "/api/sync",
        json={"dry_run": True, "mode": "list"},
        headers={"Authorization": "Bearer test-token"},
    )
    assert response.status_code == 200
    assert "operation_id" not in response.json()

    history = client.get("/api/history", headers={"Authorization": "Bearer test-token"})
    assert history.status_code == 200
    assert history.json()["operations"] == []


def test_live_sync_returns_backend_operation_id_and_authoritative_history(
    monkeypatch, tmp_path
):
    from api.sync_history import SyncHistoryStore

    client = TestClient(app)
    client.app.state.sync_history = SyncHistoryStore(tmp_path / "history.json")

    github = Mock()
    github.session = Mock()
    github.get_authenticated_user.return_value = {"login": "demo-user"}
    monkeypatch.setattr("api.routes.GitHubClient", lambda token: github)

    forks = [
        {"full_name": "demo/a", "fork": True},
        {"full_name": "demo/b", "fork": True},
        {"full_name": "demo/current", "fork": True},
    ]
    synchronizer = Mock()
    synchronizer.get_forks.return_value = forks
    synchronizer.preview_fork.side_effect = [
        {"repository": "demo/a", "status": "behind", "ahead_by": 0, "behind_by": 1},
        {"repository": "demo/b", "status": "behind", "ahead_by": 0, "behind_by": 2},
        {"repository": "demo/current", "status": "up-to-date", "ahead_by": 0, "behind_by": 0},
    ]
    synchronizer.sync_all.return_value = [
        {"repository": "demo/a", "status": "synced", "message": "Synced 1 upstream commit.", "behind_by": 1},
        {"repository": "demo/b", "status": "error", "message": "HTTP 403"},
    ]
    monkeypatch.setattr("api.routes.ForkSynchronizer", lambda client: synchronizer)

    response = client.post(
        "/api/sync",
        json={
            "dry_run": False,
            "confirmation": "SYNC",
            "repositories": ["demo/a", "demo/b", "demo/current"],
        },
        headers={"Authorization": "Bearer test-token"},
    )
    assert response.status_code == 200
    payload = response.json()
    operation_id = payload.get("operation_id")
    assert isinstance(operation_id, str) and len(operation_id) == 36
    assert [item["status"] for item in payload["results"]] == ["synced", "error", "up-to-date"]

    history = client.get("/api/history", headers={"Authorization": "Bearer test-token"})
    assert history.status_code == 200
    data = history.json()
    assert data["account"] == "demo-user"
    assert data["last_successful_sync"].get("demo/a")
    assert "demo/b" not in data["last_successful_sync"]
    assert len(data["operations"]) == 1
    operation = data["operations"][0]
    assert operation["operation_id"] == operation_id
    assert operation["targets"] == ["demo/a", "demo/b", "demo/current"]
    assert [item["repository"] for item in operation["results"]] == [
        "demo/a",
        "demo/b",
        "demo/current",
    ]
    assert operation["summary"] == {
        "success": 1,
        "skipped": 1,
        "failed": 1,
        "manual": 1,
    }


def test_completed_operation_moves_counters_from_ready_to_up_to_date():
    out = run_node(
        """
        import {mergeOperationResults,operationCountsAfter} from './DASHBOARD/utils.js';
        const before={total:4,up_to_date:1,to_be_synced:2,unsyncable:1,complete:true};
        const results=[
            {repository:'u/a',status:'synced',behind_by:1},
            {repository:'u/b',status:'error',message:'HTTP 403'},
        ];
        const summary={success:1,skipped:0,failed:1,manual:1};
        const repos=[
            {repository:'u/a',fork:true,status:'behind',ahead_by:0,behind_by:2,check_status:'ok'},
            {repository:'u/b',fork:true,status:'behind',ahead_by:0,behind_by:1,check_status:'ok'},
            {repository:'u/c',fork:true,status:'up-to-date',ahead_by:0,behind_by:0,check_status:'ok'},
            {repository:'u/d',fork:true,status:'ahead',ahead_by:1,behind_by:0,check_status:'ok'},
        ];
        const merged=mergeOperationResults(repos,results,'2026-11-19T23:00:00Z');
        console.log(JSON.stringify({
            synced:merged.repositories.find(r=>r.repository==='u/a'),
            counts:operationCountsAfter(before,summary,results,'2026-11-19T23:00:00Z'),
        }));
        """
    )
    assert out["synced"]["status"] == "synced"
    assert out["synced"]["behind_by"] == 0
    assert out["synced"]["last_successful_sync"] == "2026-11-19T23:00:00Z"
    assert out["counts"]["total"] == 4
    assert out["counts"]["up_to_date"] == 2
    assert out["counts"]["to_be_synced"] == 1
    assert out["counts"]["unsyncable"] == 1
    assert out["counts"]["from_operation"] is True


def test_operation_results_merge_without_overriding_live_verified_counters():
    assert "counts_before: countsBefore" in APP_SOURCE
    assert "repositories = mergeOperationResults(" in APP_SOURCE
    assert "applyRecordedOperation ? lastOperation.results : []" in APP_SOURCE
    assert "const applyRecordedOperation = !!(lastOperation && lastOperation.source !== \"restored\");" in APP_SOURCE
    assert "const counts = snapshotActive ? operationCounts : liveCounts;" in APP_SOURCE
    assert "verified counters shown separately" in APP_SOURCE


def test_dashboard_assets_are_cache_busted():
    html = (ROOT / "DASHBOARD" / "index.html").read_text(encoding="utf-8")
    assert "/dashboard/static/app.js?v=" in html
    assert "/dashboard/static/dashboard.css?v=" in html


def test_repo_status_does_not_display_checked_marker():
    assert "(CHECKED)" not in APP_SOURCE
    assert "status.textContent = confirmedLabel;" in APP_SOURCE
    assert "READY TO SYNC" in APP_SOURCE
    assert "UP TO DATE" in APP_SOURCE
    assert "UNSYNCABLE" in APP_SOURCE


def test_sync_results_section_removed_but_history_preserved():
    html = (ROOT / "DASHBOARD" / "index.html").read_text(encoding="utf-8")
    for marker in (
        "SYNC RESULTS",
        "SUCCESSFULLY SYNCHRONIZED",
        "SKIPPED",
        "FAILED",
        "MANUAL ATTENTION",
        'id="sync-summary"',
        'id="sync-success"',
        'id="sync-skipped"',
        'id="sync-failed"',
        'id="sync-manual"',
    ):
        assert marker not in html
    assert "Sync history and last result" in html
    assert 'id="sync-history"' in html
    assert "function renderHistory()" in APP_SOURCE
    assert "renderHistory();" in APP_SOURCE
    assert 'requestJson("/api/history"' in APP_SOURCE
    assert "renderSyncSummary" not in APP_SOURCE


def test_history_timestamp_uses_local_time_in_dd_mm_yyyy_hh_mm_format():
    out = run_node(
        """
        import {formatHistoryTimestamp} from './DASHBOARD/utils.js';
        const local = new Date(2026, 10, 21, 16, 42, 0, 0);
        console.log(JSON.stringify(formatHistoryTimestamp(local.toISOString())));
        """
    )
    assert out == "21.11.2026, 16:42"


def test_missing_history_timestamp_shows_placeholder():
    out = run_node(
        """
        import {formatHistoryTimestamp} from './DASHBOARD/utils.js';
        const values = [null, undefined, "", "   ", "not-a-date", 123, {}];
        console.log(JSON.stringify(values.map(formatHistoryTimestamp)));
        """
    )
    assert out == ["Time unavailable"] * 7


def test_history_uses_backend_operation_timestamps():
    assert "timestamp: operation.created_at" in APP_SOURCE
    assert "formatHistoryTimestamp(r.timestamp)" in APP_SOURCE
    assert "authoritativeOperations = data.operations.filter" in APP_SOURCE
    assert "await restoreAuthoritativeOperation(gen);" in APP_SOURCE
    assert 'from "./utils.js?v=20261121d";' in APP_SOURCE


def test_history_section_shows_only_latest_authoritative_operation():
    assert "for (const operation of authoritativeOperations.slice(0, 1)) {" in APP_SOURCE
    assert "for (const operation of authoritativeOperations) {" not in APP_SOURCE
    assert "history.slice(0, 1)" in APP_SOURCE
    assert "_MAX_OPERATIONS = 20" in (ROOT / "api" / "sync_history.py").read_text(encoding="utf-8")


def test_ahead_only_status_renders_as_plain_unsyncable():
    assert '"ahead": "UNSYNCABLE"' in APP_SOURCE
    assert "UNSYNCABLE (AHEAD-ONLY)" not in APP_SOURCE
    assert "AHEAD-ONLY is included in UNSYNCABLE" not in APP_SOURCE
    assert 'if (effective === "ahead") return "is-ahead";' in APP_SOURCE
    assert '"/dashboard/static/app.js?v=20261121l"' in (ROOT / "DASHBOARD" / "index.html").read_text(encoding="utf-8")


def test_null_compare_values_are_selectable_but_not_confirmed():
    out = run_node(
        """
        import {isSelectableCandidate,isReadyCandidate,isSyncConfirmedRepository,computeDashboardCounts} from './DASHBOARD/utils.js';
        const names=['u/a','u/b','u/c'];
        const repos=names.map(repository=>({repository,fork:true,status:'pending',check_status:'pending',ahead_by:null,behind_by:null}));
        console.log(JSON.stringify({
            selectable:repos.filter(isSelectableCandidate).map(r=>r.repository),
            ready:repos.filter(isReadyCandidate).map(r=>r.repository),
            confirmed:repos.filter(isSyncConfirmedRepository).map(r=>r.repository),
            counts:computeDashboardCounts(repos),
        }));
        """
    )
    assert out["selectable"] == ["u/a", "u/b", "u/c"]
    assert out["ready"] == []
    assert out["confirmed"] == []
    assert out["counts"]["total"] == 3
    assert out["counts"]["pending"] == 3


def test_three_selected_repositories_enable_sync_chosen_before_checks_finish():
    out = run_node(
        """
        import {isSelectableCandidate,isSyncConfirmedRepository} from './DASHBOARD/utils.js';
        const names=['u/a','u/b','u/c'];
        const repos=names.map(repository=>({repository,fork:true,status:'pending',check_status:'pending',ahead_by:null,behind_by:null}));
        const selectable=repos.filter(isSelectableCandidate).map(r=>r.repository);
        const selected=new Set(['u/a','u/b','u/c']);
        const selectedSyncable=selectable.filter(name=>selected.has(name));
        console.log(JSON.stringify({
            selected:selectedSyncable,
            sync_chosen_enabled:selectedSyncable.length>0,
            confirmed:repos.filter(isSyncConfirmedRepository).map(r=>r.repository),
        }));
        """
    )
    assert out == {
        "selected": ["u/a", "u/b", "u/c"],
        "sync_chosen_enabled": True,
        "confirmed": [],
    }
    assert "syncButton.disabled = !idle || selectedSyncable === 0;" in APP_SOURCE
    assert "if (isSelectableCandidate(repo)) {" in APP_SOURCE
    assert "previewInFlight = false;" in APP_SOURCE
    assert "backgroundScanActive = true;" in APP_SOURCE
    assert "void runBackgroundChecks(gen, auto);" in APP_SOURCE
    assert "const running = !!active && (previewInFlight || backgroundScanActive)" in APP_SOURCE
    assert "const isChecking = (previewInFlight || backgroundScanActive) && checkingSet.has(repo.repository);" in APP_SOURCE


def test_list_403_is_shown_instead_of_zero_counters():
    out = run_node(
        """
        import {listErrorMessage} from './DASHBOARD/utils.js';
        console.log(JSON.stringify({
            message:listErrorMessage({status:403,message:'Could not load forks from GitHub (HTTP 403).'}),
            fallback:listErrorMessage({status:403}),
        }));
        """
    )
    assert out["message"] == "Could not load forks from GitHub (HTTP 403)."
    assert out["fallback"] == "Could not load forks from GitHub."
    assert "listError = listErrorMessage(e);" in APP_SOURCE
    assert 'setStatus(listError, "error");' in APP_SOURCE
    assert 'setCounterText(statsEls.total, listError ? "—" : counts.total, false);' in APP_SOURCE
    assert "if (listError) attention.push(listError);" in APP_SOURCE


def test_background_timeout_and_stale_response_do_not_block_selection():
    out = run_node(
        """
        import {isSelectableCandidate,mergePreviewError} from './DASHBOARD/utils.js';
        const base={repository:'u/a',fork:true,status:'pending',ahead_by:null,behind_by:null};
        const timeout={...base,check_status:'timeout'};
        const stale=mergePreviewError(base,'Unexpected check response for this repository.','u/other');
        console.log(JSON.stringify({
            timeoutSelectable:isSelectableCandidate(timeout),
            retryableSelectable:isSelectableCandidate(base),
            staleError:stale.preview_error||'',
        }));
        """
    )
    assert out["timeoutSelectable"] is False
    assert out["retryableSelectable"] is True
    assert "Unexpected check response" in out["staleError"]
    assert "function isCurrent(gen) { return gen === sessionGeneration; }" in APP_SOURCE
    assert "if (!isCurrent(gen)) return;" in APP_SOURCE
    assert '"Check timeout"' in APP_SOURCE


def test_preflight_failure_excludes_only_that_repository():
    out = run_node(
        """
        import {isSyncConfirmedRepository} from './DASHBOARD/utils.js';
        const repos={
            'u/a':{repository:'u/a',fork:true,status:'behind',ahead_by:0,behind_by:1,check_status:'ok'},
            'u/b':{repository:'u/b',fork:true,status:'error',ahead_by:0,behind_by:2,check_status:'error',preview_error:'HTTP 403'},
            'u/c':{repository:'u/c',fork:true,status:'behind',ahead_by:0,behind_by:3,check_status:'ok'},
        };
        console.log(JSON.stringify({
            accepted:Object.keys(repos).filter(name=>isSyncConfirmedRepository(repos[name])),
        }));
        """
    )
    assert out["accepted"] == ["u/a", "u/c"]
    assert "const failed = preflight.filter((item) => !item.ok);" in APP_SOURCE
    assert "const repos = preflight.filter((item) => item.ok).map((item) => item.name);" in APP_SOURCE
    assert "Excluded after safety check" in APP_SOURCE
    assert "if (repos.length === 0) {" in APP_SOURCE
    assert "if (!window.confirm(confirmMessage)) return;" in APP_SOURCE


def test_theme_guard_strips_only_external_theme_blocks():
    out = run_node(
        """
        import {stripExternalThemeStyle} from './DASHBOARD/theme_guard.js';
        console.log(JSON.stringify({
            mixed: stripExternalThemeStyle('color:red;/*startDM*/background:#222 !important;color:#eee !important;/*endDM*/padding:4px'),
            plain: stripExternalThemeStyle('color:red'),
            undefinedBlock: stripExternalThemeStyle('/*startDM*/undefined/*endDM*/'),
            multiple: stripExternalThemeStyle('/*startDM*/a:1/*endDM*/b:2;/*startDM*/c:3/*endDM*/'),
            nullValue: stripExternalThemeStyle(null),
        }));
        """
    )
    assert out == {
        "mixed": "color:red;padding:4px",
        "plain": "color:red",
        "undefinedBlock": "",
        "multiple": "b:2;",
        "nullValue": "",
    }


def test_theme_guard_is_scoped_debounced_and_accessibility_safe():
    assert 'const THEME_MARKER = "/*startDM*/";' in THEME_GUARD_SOURCE
    assert "attributeFilter: [\"style\"]" in THEME_GUARD_SOURCE
    assert "childList: true" in THEME_GUARD_SOURCE
    assert "new MutationObserver(schedule)" in THEME_GUARD_SOURCE
    assert "if (scheduled) return;" in THEME_GUARD_SOURCE
    assert "observer.disconnect()" in THEME_GUARD_SOURCE
    assert "observer.observe(root, observerOptions)" in THEME_GUARD_SOURCE
    assert "requestAnimationFrame(run)" in THEME_GUARD_SOURCE
    assert "(forced-colors: active)" in THEME_GUARD_SOURCE
    assert 'root.dataset.themeGuard = "off"' in THEME_GUARD_SOURCE
    assert 'root.dataset.themeGuard = "on"' in THEME_GUARD_SOURCE
    assert 'window.addEventListener("pageshow", schedule)' in THEME_GUARD_SOURCE

    guard_css = theme_guard_css_source()
    assert "@layer dreamerol-guard" in guard_css
    assert ':root[data-theme-guard="on"]' in guard_css
    assert "!important" in guard_css
    assert "display:" not in guard_css

    assert "dashboard.css?v=20261122s" in INDEX_SOURCE
    assert "theme_guard.js?v=20261121a" in INDEX_SOURCE
    assert INDEX_SOURCE.index("theme_guard.js") < INDEX_SOURCE.index("app.js?v=")


def test_welcome_uses_theme_guard_with_github_green_signin():
    welcome_html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    welcome_css = (ROOT / "web" / "style.css").read_text(encoding="utf-8")
    welcome_app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    assert "/static/style.css?v=20261122r" in welcome_html
    assert "/static/app.js?v=20261121k" in welcome_html
    assert "/static/assets/hero-welcome.jpg?v=20261122r" in welcome_html
    assert (ROOT / "web" / "assets" / "hero-welcome.jpg").is_file()
    assert 'width="1321" height="880"' in welcome_html
    assert "/dashboard/static/theme_guard.js?v=20261121a" in welcome_html
    assert 'href="/?switch=1&v=20261121j"' in INDEX_SOURCE
    assert welcome_html.index("theme_guard.js") < welcome_html.index("app.js?v=")
    assert "@layer dreamerol-guard" in welcome_css
    assert ':root[data-theme-guard="on"] .auth-block button' in welcome_css
    assert 'class="github-button"' in welcome_html
    assert 'class="github-icon"' in welcome_html
    assert "--welcome-action-width: min(400px, calc(100vw - 96px))" in welcome_css
    assert ".welcome-shell {\n    width: 100%;\n    max-width: 880px;" in welcome_css
    assert ".sync-panel {\n    width: 100%;\n    max-width: none;" in welcome_css
    assert "width: 100%;\n    max-width: none;\n    height: auto;\n    object-fit: contain;" in welcome_css
    assert "align-items: center" in welcome_css
    assert "mix-blend-mode: screen" in welcome_css
    assert "mask-image: radial-gradient(ellipse 78% 85% at 50% 50%, #000 60%, rgba(0, 0, 0, 0.85) 78%, transparent 100%)" in welcome_css
    assert 'class="brand-mark"' not in welcome_html
    assert ".heading-line:last-child" in welcome_css
    assert "font-size: 0.75em" in welcome_css
    assert "font-size: clamp(42px, 7.5vw, 60px)" in welcome_css
    assert "min-height: 92px" in welcome_css
    assert "font-size: 34px" in welcome_css
    assert ".button-label {\n    white-space: nowrap;\n}" in welcome_css
    assert "width: 34px;\n    height: 34px;" in welcome_css
    assert "margin: 15px 0 45px" in welcome_css
    assert "font-size: clamp(24px, 3.9vw, 27.5px)" in welcome_css
    assert "font-weight: 600" in welcome_css
    assert "padding-bottom: clamp(40px, 6vw, 56px)" in welcome_css
    assert "font-size: 21px" in welcome_css
    assert "color: #d0dcf2" in welcome_css
    assert welcome_html.count('class="heading-line"') == 2
    assert "background-color: #060913 !important" in welcome_css
    assert "radial-gradient(circle at 10% 5%, rgba(88, 28, 135, 0.32), transparent 34%)" in welcome_css
    assert "linear-gradient(180deg, #0b1020, #060913) !important" in welcome_css
    assert "background: linear-gradient(180deg, rgba(14, 20, 34, 0.96), rgba(8, 13, 27, 0.94)) !important" in welcome_css
    assert "background: #238636 !important" in welcome_css
    assert "background: #2ea043 !important" in welcome_css
    assert '<span class="heading-line">WELCOME TO</span>' in welcome_html
    assert '<span class="heading-line">DREAMEROL SYNC</span>' in welcome_html
    assert "Click. Any fork. Always up-to-date" in welcome_html
    assert "Click. Any fork. Always up-to-date." not in welcome_html
    assert "preview and synchronize" not in welcome_html
    assert "<footer>" not in welcome_html
    assert "choose a different account" not in welcome_app
    assert "switchIntent" not in welcome_app
    assert 'setAuthStatus("Not signed in.", "muted");' in welcome_app


def test_theme_guard_never_touches_sync_or_extension_stylesheet():
    assert "/api/sync" not in THEME_GUARD_SOURCE
    assert "fetch(" not in THEME_GUARD_SOURCE
    assert "dark-mode" not in THEME_GUARD_SOURCE
    assert "stylesheet" not in THEME_GUARD_SOURCE
    assert "disabled" not in THEME_GUARD_SOURCE
    assert "removeChild" not in THEME_GUARD_SOURCE
    assert "hidden" not in THEME_GUARD_SOURCE
    assert "THEME_BLOCK" in THEME_GUARD_SOURCE
    assert 'removeAttribute("style")' in THEME_GUARD_SOURCE


def test_checkboxes_lock_until_checks_finish_and_selection_is_persisted():
    assert "const SELECTION_KEY_PREFIX = \"dreamerol.selection\";" in APP_SOURCE
    assert "function selectionStorageKey(account = currentAccount)" in APP_SOURCE
    assert "function saveSelection()" in APP_SOURCE
    assert "function loadSelection()" in APP_SOURCE
    assert "selected = loadSelection();" in APP_SOURCE
    assert "if (repositories.length > 0) {" in APP_SOURCE
    assert "const available = new Set(repositories.map((r) => r.repository));" in APP_SOURCE
    assert "cb.disabled = checksRunning;" in APP_SOURCE
    assert 'if (checksRunning) cb.title = "Available after checks finish.";' in APP_SOURCE
    assert "if (cb.checked) selected.add(repo.repository); else selected.delete(repo.repository);" in APP_SOURCE
    assert "saveSelection();" in APP_SOURCE
    assert "const checksRunning = previewInFlight || backgroundScanActive;" in APP_SOURCE
    assert "const idle = !syncInFlight && !operationLock && !checksRunning && !sessionExpired;" in APP_SOURCE
    assert "void runBackgroundChecks(gen, auto);" in APP_SOURCE
    assert APP_SOURCE.count("void runBackgroundChecks(gen, auto);") == 1
    assert "location.reload(" not in APP_SOURCE


def test_check_401_cancels_batches_without_redirect_or_data_loss():
    start = APP_SOURCE.index("function handleCheckSessionExpired")
    end = APP_SOURCE.index("function finalizePreviewUi", start)
    helper = APP_SOURCE[start:end]
    assert "if (!isCurrent(gen)) return;" in helper
    assert "invalidatePendingOperations();" in helper
    assert "sessionExpired = true;" in helper
    assert "let sessionExpired = false;" in APP_SOURCE
    assert "sessionExpired = false;" in APP_SOURCE
    assert 'setStatus("SESSION EXPIRED — PLEASE SIGN IN", "error");' in helper
    assert "saveSelection();" in helper
    assert "renderRepos();" in helper
    assert "updateStats();" in helper
    assert "updateSelectionUI();" in helper
    assert "window.location.assign" not in helper
    assert "repositories = []" not in helper
    assert "selected = new Set()" not in helper
    assert "checkedCount = 0" not in helper
    assert "previewTotal = 0" not in helper
    assert APP_SOURCE.count("if (e && e.status === 401) { handleCheckSessionExpired(gen)") == 2
    assert APP_SOURCE.count("window.location.assign(WELCOME_URL)") == 3


def test_sync_requires_preflight_and_has_no_parallel_operations():
    assert "const preflight = await preflightSelected(requested);" in APP_SOURCE
    assert "const failed = preflight.filter((item) => !item.ok);" in APP_SOURCE
    assert "const repos = preflight.filter((item) => item.ok).map((item) => item.name);" in APP_SOURCE
    assert "if (repos.length === 0) {" in APP_SOURCE
    assert "if (!window.confirm(confirmMessage)) return;" in APP_SOURCE
    assert 'JSON.stringify({ dry_run: false, confirmation: "SYNC", repositories: repos })' in APP_SOURCE
    assert APP_SOURCE.count("if (syncInFlight || operationLock) return;") >= 3


def test_no_client_side_redirect_to_broker_healthz():
    client_files = [
        ROOT / "DASHBOARD" / "app.js",
        ROOT / "DASHBOARD" / "index.html",
        ROOT / "web" / "app.js",
        ROOT / "web" / "index.html",
    ]
    for path in client_files:
        assert "healthz" not in path.read_text(encoding="utf-8").lower()
