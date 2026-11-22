import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COUNT_SCRIPT = (
    "import {computeDashboardCounts} from './DASHBOARD/utils.js';"
    "const repos=JSON.parse(process.argv[1]);"
    "console.log(JSON.stringify(computeDashboardCounts(repos)));"
)


def run_node(script, *args):
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = result.stdout.strip()
    return json.loads(stdout) if stdout else None


def count(repos):
    return run_node(COUNT_SCRIPT, json.dumps(repos))


def fork(name, ahead, behind, status=None, **extra):
    item = {
        "repository": name,
        "fork": True,
        "ahead_by": ahead,
        "behind_by": behind,
        "status": status or "pending",
    }
    item.update(extra)
    return item


def original(name, **extra):
    item = {"repository": name, "fork": False, "status": "behind", "ahead_by": 0, "behind_by": 5}
    item.update(extra)
    return item


def test_original_repositories_are_excluded_and_forks_included():
    repos = [
        original("acme/fork-looking-original"),
        fork("acme/copy", 0, 0, "up-to-date"),
        original("acme/another-original"),
    ]
    out = count(repos)
    assert out["total"] == 1
    assert out["up_to_date"] == 1
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 0


def test_up_to_date_fork_is_counted_from_numeric_compare_values():
    out = count([fork("f/up", 0, 0, "up-to-date")])
    assert out["up_to_date"] == 1
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 0


def test_behind_only_fork_is_counted_as_to_be_synced():
    out = count([fork("f/behind", 0, 3, "behind")])
    assert out["up_to_date"] == 0
    assert out["to_be_synced"] == 1
    assert out["unsyncable"] == 0


def test_ahead_only_fork_is_counted_as_unsyncable():
    out = count([fork("f/ahead", 2, 0, "ahead")])
    assert out["up_to_date"] == 0
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 1
    assert out["ahead"] == 1


def test_diverged_fork_is_counted_as_unsyncable():
    out = count([fork("f/diverged", 1, 3, "diverged")])
    assert out["up_to_date"] == 0
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 1
    assert out["diverged"] == 1


def test_repository_inspection_error_is_unverified_not_unsyncable():
    out = count([{"repository": "f/error", "fork": True, "status": "error", "message": "compare failed"}])
    assert out["unsyncable"] == 0
    assert out["errors"] == 1
    assert out["check_errors"] == 1
    assert out["complete"] is False


def test_missing_or_invalid_fork_flag_is_reported_and_excluded():
    repos = [
        {"repository": "f/no-flag", "status": "up-to-date", "ahead_by": 0, "behind_by": 0},
        {"repository": "f/bad-flag", "fork": "true", "status": "behind", "ahead_by": 0, "behind_by": 1},
    ]
    out = run_node(
        "import {computeDashboardCounts,getForkFlagErrors} from './DASHBOARD/utils.js';"
        "const repos=JSON.parse(process.argv[1]);"
        "console.log(JSON.stringify({counts:computeDashboardCounts(repos),errors:getForkFlagErrors(repos)}));",
        json.dumps(repos),
    )
    assert out["counts"]["total"] == 0
    assert out["counts"]["up_to_date"] == 0
    assert out["counts"]["to_be_synced"] == 0
    assert out["counts"]["unsyncable"] == 0
    assert out["counts"]["invalid_fork_flags"] == 2
    assert out["errors"] == ["f/no-flag", "f/bad-flag"]


def test_duplicate_fork_is_counted_once():
    row = fork("f/duplicate", 0, 0, "up-to-date")
    out = count([row, dict(row)])
    assert out["total"] == 1
    assert out["up_to_date"] == 1
    assert out["duplicates"] == 1


def test_four_counters_sum_to_total_with_mixed_data():
    repos = [
        original("owner/fork-looking-original"),
        original("owner/plain-original"),
        fork("f/up-1", 0, 0, "up-to-date"),
        fork("f/up-2", 0, 0, "up-to-date"),
        fork("f/behind-1", 0, 1, "behind"),
        fork("f/behind-2", 0, 2, "behind"),
        fork("f/behind-3", 0, 9, "behind"),
        fork("f/ahead", 1, 0, "ahead"),
        fork("f/diverged", 2, 2, "diverged"),
        fork("f/up-3", 0, 0, "up-to-date"),
        {"repository": "f/missing-flag", "status": "behind", "ahead_by": 0, "behind_by": 1},
        fork("f/up-1", 0, 0, "up-to-date"),
    ]
    out = count(repos)
    assert out["total"] == 8
    assert out["up_to_date"] == 3
    assert out["to_be_synced"] == 3
    assert out["unsyncable"] == 2
    assert out["invalid_fork_flags"] == 1
    assert out["duplicates"] == 1
    assert out["data_errors"] == 1
    assert out["total"] == out["up_to_date"] + out["to_be_synced"] + out["unsyncable"]


def test_unexpected_states_are_unverified_and_reported():
    repos = [
        fork("f/ok", 0, 0, "up-to-date"),
        {"repository": "f/weird", "fork": True, "status": "unexpected-state"},
        {"repository": "f/missing", "fork": True},
    ]
    out = run_node(
        "import {computeDashboardCounts,getUnexpectedStates} from './DASHBOARD/utils.js';"
        "const repos=JSON.parse(process.argv[1]);"
        "console.log(JSON.stringify({counts:computeDashboardCounts(repos),unexpected:getUnexpectedStates(repos)}));",
        json.dumps(repos),
    )
    assert out["counts"]["up_to_date"] == 1
    assert out["counts"]["unsyncable"] == 0
    assert out["counts"]["check_errors"] == 2
    assert out["counts"]["complete"] is False
    assert out["unexpected"] == ["unexpected-state", "unclassified"]


def test_architectquant_reference_counts_are_calculated_from_response_data():
    repos = [original("architectquant/fork-looking-original")]
    repos += [fork(f"architectquant/repo-{i}", 0, 0, "up-to-date") for i in range(30)]
    repos += [fork(f"architectquant/behind-{i}", 0, 1, "behind") for i in range(4)]
    out = count(repos)
    assert out["total"] == 34
    assert out["up_to_date"] == 30
    assert out["to_be_synced"] == 4
    assert out["unsyncable"] == 0
    assert out["total"] == out["up_to_date"] + out["to_be_synced"] + out["unsyncable"]


def test_gabrielrules_reference_counts_are_calculated_from_response_data():
    repos = [original("GabrielRules/fork-looking-original")]
    repos += [fork(f"GabrielRules/repo-{i}", 0, 0, "up-to-date") for i in range(34)]
    repos += [fork(f"GabrielRules/diverged-{i}", 1, 1, "diverged") for i in range(2)]
    out = count(repos)
    assert out["total"] == 36
    assert out["up_to_date"] == 34
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 2
    assert out["diverged"] == 2
    assert out["total"] == out["up_to_date"] + out["to_be_synced"] + out["unsyncable"]


def test_failed_checks_are_not_counted_as_confirmed_unsyncable():
    repos = [
        {"repository": f"GabrielRules/failed-{i}", "fork": True, "status": "unknown", "preview_error": "Check failed."}
        for i in range(34)
    ]
    repos += [fork(f"GabrielRules/diverged-{i}", 1, 1, "diverged") for i in range(2)]
    out = count(repos)
    assert out["total"] == 36
    assert out["up_to_date"] == 0
    assert out["to_be_synced"] == 0
    assert out["unsyncable"] == 2
    assert out["check_errors"] == 34
    assert out["complete"] is False


def test_check_failure_with_last_known_status_withholds_final_counters():
    out = count([fork("f/last-known", 0, 0, "up-to-date", preview_error="Check failed.")])
    assert out["up_to_date"] == 1
    assert out["unsyncable"] == 0
    assert out["check_errors"] == 1
    assert out["complete"] is False


def test_sync_summary_distinguishes_success_skipped_failed_and_manual():
    out = run_node(
        "import {summarizeSyncResults} from './DASHBOARD/utils.js';"
        "const results=["
        " {status:'synced'},{status:'up-to-date'},{status:'ahead'},"
        " {status:'diverged'},{status:'error'},{status:'conflict'},{status:'mystery'}"
        "];"
        "console.log(JSON.stringify(summarizeSyncResults(results)));"
    )
    assert out == {"success": 1, "skipped": 3, "failed": 2, "manual": 5}


def test_reported_39_forks_37_unverified_2_up_to_date_are_consistent():
    out = run_node(
        """
        import {computeDashboardCounts,effectiveCountClass,isSelectableCandidate,isSyncConfirmedRepository} from './DASHBOARD/utils.js';
        const repos=[];
        for(let i=0;i<37;i++) repos.push({repository:`u/p${i}`,fork:true,status:'pending',check_status:'pending',ahead_by:null,behind_by:null});
        repos.push({repository:'u/ok1',fork:true,status:'up-to-date',check_status:'ok',ahead_by:0,behind_by:0});
        repos.push({repository:'u/ok2',fork:true,status:'synced',check_status:'ok',ahead_by:0,behind_by:0});
        const ok=repos.filter(r=>r.repository==='u/ok1'||r.repository==='u/ok2');
        console.log(JSON.stringify({
            counts:computeDashboardCounts(repos),
            ok:ok.map(r=>({
                repository:r.repository,
                effective:effectiveCountClass(r),
                selectable:isSelectableCandidate(r),
                confirmed:isSyncConfirmedRepository(r),
            })),
        }));
        """
    )
    assert out["counts"]["total"] == 39
    assert out["counts"]["up_to_date"] == 2
    assert out["counts"]["to_be_synced"] == 0
    assert out["counts"]["unsyncable"] == 0
    assert out["counts"]["pending"] == 37
    assert out["counts"]["check_errors"] == 0
    assert out["counts"]["complete"] is False
    assert out["ok"] == [
        {"repository": "u/ok1", "effective": "synced", "selectable": False, "confirmed": False},
        {"repository": "u/ok2", "effective": "synced", "selectable": False, "confirmed": False},
    ]


def test_upstream_label_uses_available_metadata_only():
    out = run_node(
        "import {getUpstreamLabel} from './DASHBOARD/utils.js';"
        "const values=["
        " getUpstreamLabel({parent:{full_name:'GabrielRules/Upstream'}}),"
        " getUpstreamLabel({upstream:'architectquant/Base'}),"
        " getUpstreamLabel({upstream_full_name:'Owner/Parent'}),"
        " getUpstreamLabel({repository:'f/only'})"
        "];"
        "console.log(JSON.stringify(values));"
    )
    assert out == ["GabrielRules/Upstream", "architectquant/Base", "Owner/Parent", ""]


def test_merge_preview_result_preserves_fork_and_upstream_metadata():
    out = run_node(
        "import {mergePreviewResult} from './DASHBOARD/utils.js';"
        "const prev={repository:'f/repo',status:'pending',fork:true,parent:{full_name:'Owner/Upstream'},last_successful_sync:'2026-11-17T10:00:00Z'};"
        "const merged=mergePreviewResult(prev,{repository:'f/repo',status:'up-to-date',ahead_by:0,behind_by:0},'f/repo');"
        "console.log(JSON.stringify(merged));"
    )
    assert out["fork"] is True
    assert out["parent"]["full_name"] == "Owner/Upstream"
    assert out["last_successful_sync"] == "2026-11-17T10:00:00Z"
    assert out["status"] == "up-to-date"
