import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_node(script: str):
    p = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    out = p.stdout.strip()
    return json.loads(out) if out else None


def test_compute_progress_reflects_real_counts():
    out = run_node(
        "import {computeProgress} from './DASHBOARD/utils.js';"
        "console.log(JSON.stringify(["
        "computeProgress(0,5),"
        "computeProgress(2,5),"
        "computeProgress(5,5),"
        "computeProgress(7,5),"
        "computeProgress(1,0)"
        "]));"
    )
    assert out[0] == {"checked": 0, "total": 5, "percent": 0}
    assert out[1] == {"checked": 2, "total": 5, "percent": 40}
    assert out[2] == {"checked": 5, "total": 5, "percent": 100}
    assert out[3]["checked"] == 5 and out[3]["total"] == 5 and out[3]["percent"] == 100
    assert out[4] == {"checked": 1, "total": 0, "percent": 0}


def test_all_real_statuses_classified_and_counted():
    out = run_node(
        "import {computeDashboardCounts,effectiveCountClass} from './DASHBOARD/utils.js';"
        "const repos=["
        " {repository:'a/1',status:'behind',fork:true},"
        " {repository:'a/2',status:'ahead',fork:true},"
        " {repository:'a/3',status:'diverged',fork:true},"
        " {repository:'a/4',status:'error',fork:true},"
        " {repository:'a/5',status:'unknown',fork:true},"
        " {repository:'a/6',status:'pending',fork:true},"
        " {repository:'a/7',status:'up-to-date',fork:true,preview_error:'temporary'}"
        "];"
        "console.log(JSON.stringify({counts:computeDashboardCounts(repos),classes:repos.map(r=>effectiveCountClass(r))}));"
    )
    assert out["classes"] == ["behind", "ahead", "diverged", "error", "unknown", "pending", "synced"]
    assert out["counts"]["total"] == 7
    assert out["counts"]["up_to_date"] == 1
    assert out["counts"]["to_be_synced"] == 1
    assert out["counts"]["unsyncable"] == 2
    assert out["counts"]["ahead"] == 1
    assert out["counts"]["diverged"] == 1
    assert out["counts"]["errors"] == 3
    assert out["counts"]["check_errors"] == 3
    assert out["counts"]["pending"] == 1
    assert out["counts"]["complete"] is False


def test_non_fork_repositories_excluded_from_dashboard_counters():
    out = run_node(
        "import {computeDashboardCounts} from './DASHBOARD/utils.js';"
        "const repos=["
        " {repository:'demo/fork',status:'behind',fork:true},"
        " {repository:'demo/original',status:'behind',fork:false}"
        "];"
        "console.log(JSON.stringify(computeDashboardCounts(repos)));"
    )
    assert out["total"] == 1
    assert out["to_be_synced"] == 1
    assert out["unsyncable"] == 0


def test_ahead_counted_as_unsyncable_subcategory_and_status_preserved():
    out = run_node(
        "import {computeDashboardCounts,effectiveCountClass} from './DASHBOARD/utils.js';"
        "const repos=[{repository:'a/1',status:'ahead',fork:true},{repository:'a/2',status:'behind',fork:true}];"
        "console.log(JSON.stringify({counts:computeDashboardCounts(repos),cls:effectiveCountClass(repos[0]),status:repos[0].status}));"
    )
    assert out["cls"] == "ahead"
    assert out["status"] == "ahead"
    assert out["counts"]["up_to_date"] == 0
    assert out["counts"]["to_be_synced"] == 1
    assert out["counts"]["unsyncable"] == 1
    assert out["counts"]["ahead"] == 1
    assert out["counts"]["complete"] is True
    assert out["counts"]["up_to_date"] + out["counts"]["to_be_synced"] + out["counts"]["unsyncable"] == out["counts"]["total"]


def test_preview_error_preserves_last_known_status():
    out = run_node(
        "import {mergePreviewError,effectiveCountClass,computeDashboardCounts} from './DASHBOARD/utils.js';"
        "const repo=mergePreviewError({repository:'o/r',status:'up-to-date',fork:true},'API timeout','o/r');"
        "console.log(JSON.stringify({repo,cls:effectiveCountClass(repo),counts:computeDashboardCounts([repo])}));"
    )
    assert out["repo"]["status"] == "up-to-date"
    assert out["repo"]["preview_error"] == "API timeout"
    assert out["cls"] == "synced"
    assert out["counts"]["total"] == 1
    assert out["counts"]["up_to_date"] == 1
    assert out["counts"]["unsyncable"] == 0
    assert out["counts"]["check_errors"] == 1
    assert out["counts"]["complete"] is False


def test_only_behind_is_syncable():
    out = run_node(
        "import {isSyncableRepository} from './DASHBOARD/utils.js';"
        "const cases=['behind','diverged','error','ahead','up-to-date','unknown','pending'];"
        "const repos=cases.map(s=>({status:s,fork:true,ahead_by:0,behind_by:s==='behind'?1:0}));"
        "console.log(JSON.stringify(cases.map((s,i)=>({s,ok:isSyncableRepository(repos[i])}))));"
    )
    assert out == [
        {"s":"behind","ok":True},
        {"s":"diverged","ok":False},
        {"s":"error","ok":False},
        {"s":"ahead","ok":False},
        {"s":"up-to-date","ok":False},
        {"s":"unknown","ok":False},
        {"s":"pending","ok":False},
    ]


def test_unknown_pending_without_previous_status_not_misleadingly_counted():
    out = run_node(
        "import {mergePreviewError,computeDashboardCounts,isUnresolvedRepository} from './DASHBOARD/utils.js';"
        "const a={repository:'a/1',status:'pending',fork:true};"
        "const b=mergePreviewError({repository:'a/2',status:'pending',fork:true},'Network error','a/2');"
        "const counts=computeDashboardCounts([a,b]);"
        "console.log(JSON.stringify({counts,aUn:isUnresolvedRepository(a),bStatus:b.status,bUn:isUnresolvedRepository(b)}));"
    )
    assert out["aUn"] is True
    assert out["bStatus"] == "unknown"
    assert out["bUn"] is True
    assert out["counts"]["unsyncable"] == 0
    assert out["counts"]["errors"] == 1
    assert out["counts"]["check_errors"] == 1
    assert out["counts"]["pending"] == 1
    assert out["counts"]["up_to_date"] == 0
    assert out["counts"]["to_be_synced"] == 0
    assert out["counts"]["complete"] is False


def test_total_equals_four_mutually_exclusive_counters_after_classification():
    out = run_node(
        "import {computeDashboardCounts} from './DASHBOARD/utils.js';"
        "const repos=["
         " {repository:'a/1',status:'behind',fork:true},"
         " {repository:'a/2',status:'diverged',fork:true},"
         " {repository:'a/3',status:'up-to-date',fork:true},"
         " {repository:'a/4',status:'ahead',fork:true},"
         " {repository:'a/5',status:'up-to-date',fork:true}"
         "];"
         "const counts=computeDashboardCounts(repos);"
         "console.log(JSON.stringify(counts));"
     )
    assert out["complete"] is True
    assert out["pending"] == 0
    assert out["up_to_date"] == 2
    assert out["to_be_synced"] == 1
    assert out["unsyncable"] == 2
    assert out["ahead"] == 1
    assert out["total"] == out["up_to_date"] + out["to_be_synced"] + out["unsyncable"]


def test_sync_selected_excludes_forbidden_statuses_by_syncable_rule():
    out = run_node(
        "import {isSyncableRepository} from './DASHBOARD/utils.js';"
        "const selected=['a/1','a/2','a/3','a/4','a/5','a/6'];"
        "const repos=["
         " {repository:'a/1',status:'behind',fork:true,ahead_by:0,behind_by:1},"
         " {repository:'a/2',status:'diverged',fork:true},"
         " {repository:'a/3',status:'error',fork:true},"
        " {repository:'a/4',status:'ahead',fork:true},"
        " {repository:'a/5',status:'unknown',fork:true},"
        " {repository:'a/6',status:'pending',fork:true}"
        "];"
        "const toSync=selected.filter(name=>repos.find(r=>r.repository===name && isSyncableRepository(r)));"
        "console.log(JSON.stringify(toSync));"
    )
    assert out == ["a/1"]


def test_merge_preview_result_success_clears_preview_error():
    out = run_node(
        "import {mergePreviewResult} from './DASHBOARD/utils.js';"
        "const prev={repository:'o/r',status:'behind',behind_by:2,fork:true,preview_error:'timeout'};"
        "const res={repository:'o/r',status:'up-to-date',message:'ok'};"
        "const merged=mergePreviewResult(prev,res,'o/r');"
        "console.log(JSON.stringify(merged));"
    )
    assert out["status"] == "up-to-date"
    assert out["fork"] is True
    assert "preview_error" not in out


def test_temporary_error_does_not_change_known_counters():
    out = run_node(
        "import {mergePreviewError,computeDashboardCounts} from './DASHBOARD/utils.js';"
        "const repos=["
        " mergePreviewError({repository:'a/1',status:'up-to-date',fork:true},'e1','a/1'),"
        " mergePreviewError({repository:'a/2',status:'behind',fork:true},'e2','a/2'),"
        " mergePreviewError({repository:'a/3',status:'diverged',fork:true},'e3','a/3'),"
        " mergePreviewError({repository:'a/4',status:'ahead',fork:true},'e4','a/4')"
        "];"
        "console.log(JSON.stringify(computeDashboardCounts(repos)));"
    )
    assert out["total"] == 4
    assert out["up_to_date"] == 1
    assert out["to_be_synced"] == 1
    assert out["unsyncable"] == 2
    assert out["ahead"] == 1
    assert out["errors"] == 4
    assert out["check_errors"] == 4
    assert out["complete"] is False


def test_next_successful_preview_updates_after_temporary_error():
    out = run_node(
        "import {mergePreviewError,mergePreviewResult,computeDashboardCounts} from './DASHBOARD/utils.js';"
        "let repo={repository:'o/r',status:'behind',behind_by:3,fork:true};"
        "repo=mergePreviewError(repo,'temporary','o/r');"
        "const afterError=computeDashboardCounts([repo]);"
        "repo=mergePreviewResult(repo,{repository:'o/r',status:'up-to-date'},'o/r');"
        "console.log(JSON.stringify({afterError,afterSuccess:computeDashboardCounts([repo]),status:repo.status}));"
    )
    assert out["afterError"]["to_be_synced"] == 1
    assert out["afterError"]["check_errors"] == 1
    assert out["afterError"]["complete"] is False
    assert out["afterSuccess"]["up_to_date"] == 1
    assert out["afterSuccess"]["to_be_synced"] == 0
    assert out["status"] == "up-to-date"


def test_mismatched_or_missing_preview_result_preserves_known_status():
    out = run_node(
        "import {mergePreviewResult,computeDashboardCounts} from './DASHBOARD/utils.js';"
        "const prev={repository:'o/r',status:'up-to-date',fork:true};"
        "const r1=mergePreviewResult(prev,null,'o/r');"
        "const r2=mergePreviewResult(prev,{repository:'o/other',status:'behind'},'o/r');"
        "console.log(JSON.stringify({r1,r2,counts:computeDashboardCounts([r1,r2])}));"
    )
    assert out["r1"]["status"] == "up-to-date" and out["r1"]["preview_error"]
    assert out["r2"]["status"] == "up-to-date" and out["r2"]["preview_error"]
    assert out["counts"]["total"] == 1
    assert out["counts"]["up_to_date"] == 1 and out["counts"]["unsyncable"] == 0
    assert out["counts"]["check_errors"] == 1
    assert out["counts"]["complete"] is False


def test_preview_spinner_start_and_stop_visible_only_while_active_and_current():
    out = run_node(
        "import {getPreviewSpinnerUiState} from './DASHBOARD/utils.js';"
        "console.log(JSON.stringify(["
        "getPreviewSpinnerUiState({previewInFlight:true,isCurrent:true}),"
        "getPreviewSpinnerUiState({previewInFlight:true,isCurrent:false}),"
        "getPreviewSpinnerUiState({previewInFlight:false,isCurrent:true}),"
        "getPreviewSpinnerUiState({previewInFlight:false,isCurrent:false})"
        "]));"
    )
    assert out[0]["visible"] is True and out[0]["spinnerStopped"] is False
    assert out[1]["visible"] is False and out[1]["spinnerStopped"] is True
    assert out[2]["visible"] is False and out[2]["spinnerStopped"] is True
    assert out[3]["visible"] is False and out[3]["spinnerStopped"] is True


def test_preview_cancellation_and_old_preview_after_account_switch_cannot_mutate_state():
    out = run_node(
        "import {canApplyPreviewUpdate,getPreviewSpinnerUiState} from './DASHBOARD/utils.js';"
        "console.log(JSON.stringify({"
        "oldAfterSwitch: canApplyPreviewUpdate({updateGen:1,currentGen:2,targetName:'a/1',currentName:'a/1'}),"
        "cancelledUi: getPreviewSpinnerUiState({previewInFlight:false,isCurrent:false}),"
        "mismatch: canApplyPreviewUpdate({updateGen:2,currentGen:2,targetName:'a/1',currentName:'a/2'})"
        "}));"
    )
    assert out["oldAfterSwitch"] is False
    assert out["cancelledUi"]["visible"] is False
    assert out["mismatch"] is False


def test_dedupe_repositories_by_name_unique():
    out = run_node(
        "import {dedupeRepositoriesByName} from './DASHBOARD/utils.js';"
        "const repos=[]; for(let i=1;i<=36;i++) repos.push({repository:`u/r${i}`,status:'pending'});"
        "const duped=[...repos.slice(0,10), repos[0], repos[5], ...repos.slice(10), repos[35]];"
        "const out=dedupeRepositoriesByName(duped);"
        "console.log(JSON.stringify({len:out.length,names:out.map(r=>r.repository)}));"
    )
    assert out["len"] == 36
    assert out["names"] == [f"u/r{i}" for i in range(1, 37)]


def test_api_error_object_cannot_be_shown_as_repository():
    out = run_node(
        "import {mergePreviewResult,mergePreviewError,isValidRepositoryResult,dedupeRepositoriesByName} from './DASHBOARD/utils.js';"
        "const apiErr={detail:'perm', account:'x'};"
        "const prev={repository:'owner/repo',status:'pending'};"
        "const r1=mergePreviewResult(prev, apiErr, 'owner/repo');"
        "const r3=mergePreviewError(prev, apiErr.detail, 'owner/repo');"
        "const list=dedupeRepositoriesByName([apiErr, {repository:'account',status:'error'}, {repository:'owner/real',status:'pending'}]);"
        "console.log(JSON.stringify({r1,r3,valid:isValidRepositoryResult(apiErr),list}));"
    )
    assert out["valid"] is False
    assert out["r1"]["repository"] == "owner/repo"
    assert out["r3"]["repository"] == "owner/repo"
    assert out["list"] == [{"repository": "owner/real", "status": "pending"}]


def test_finalize_preview_counters_clamps():
    out = run_node(
        "import {finalizePreviewCounters} from './DASHBOARD/utils.js';"
        "console.log(JSON.stringify([finalizePreviewCounters({checked:1,total:6}),finalizePreviewCounters({checked:9,total:6}),finalizePreviewCounters({checked:0,total:0})]));"
    )
    assert out[0] == {"checked": 1, "total": 6, "complete": False}
    assert out[1] == {"checked": 6, "total": 6, "complete": True}
    assert out[2] == {"checked": 0, "total": 0, "complete": True}


def test_ambiguous_sync_result_is_counted_as_failed():
    out = run_node(
        "import {classifyRepo,summarizeSyncResults} from './DASHBOARD/utils.js';"
        "console.log(JSON.stringify({"
        "classification:classifyRepo({status:'ambiguous'}),"
        "summary:summarizeSyncResults([{status:'ambiguous'}]),"
        "}));"
    )
    assert out == {
        "classification": "error",
        "summary": {"success": 0, "skipped": 0, "failed": 1, "manual": 1},
    }


def test_dashboard_syncable_status_label_is_ready_to_sync():
    out = run_node(
        "import {readFileSync} from 'node:fs';"
        "const app = readFileSync('./DASHBOARD/app.js','utf8');"
        "const html = readFileSync('./DASHBOARD/index.html','utf8');"
        "const css = readFileSync('./DASHBOARD/dashboard.css','utf8');"
        r"const match = app.match(/const statusLabels = \{([\s\S]*?)\n    \};/);"
        "if (!match) throw new Error('statusLabels block not found');"
        "const labels = Function('return {' + match[1] + '}')();"
        "console.log(JSON.stringify({"
        " badge:labels.behind,"
        " unverifiedLabels:[labels.error,labels.conflict,labels.unknown,labels.skipped],"
        " hasUnverifiedBangLabel:app.includes('UNVERIFIED!!!'),"
        " oldCheckFailedBadgeInApp:app.includes('(CHECK FAILED)'),"
        " stat:html.includes('<span class=\"stat-label\">READY TO SYNC</span>'),"
        " filter:html.includes('<option value=\"to-be-synced\">READY TO SYNC</option>'),"
        " legend:html.includes('<span>READY TO SYNC</span><strong id=\"summary-to-be-synced\"'),"
        " internalValue:html.includes('value=\"to-be-synced\"'),"
        r" fixedSelectColumns:(css.match(/grid-template-columns: 17px /g) || []).length,"
        r" autoSelectColumns:(css.match(/\.repo-row\s*\{[^}]*grid-template-columns:\s*auto/g) || []).length,"
        " oldUpperInApp:app.includes('TO BE SYNCED'),"
        " oldTitleInApp:app.includes('Ready to Sync'),"
        " oldLowerInApp:app.includes('to be synced'),"
        " oldUpperInHtml:html.includes('TO BE SYNCED'),"
        " oldTitleInHtml:html.includes('Ready to Sync'),"
        "}));"
    )
    assert out == {
        "badge": "READY TO SYNC",
        "unverifiedLabels": ["UNVERIFIED!!!", "UNVERIFIED!!!", "UNVERIFIED!!!", "UNVERIFIED!!!"],
        "hasUnverifiedBangLabel": True,
        "oldCheckFailedBadgeInApp": False,
        "stat": True,
        "filter": True,
        "legend": True,
        "internalValue": True,
        "fixedSelectColumns": 3,
        "autoSelectColumns": 0,
        "oldUpperInApp": False,
        "oldTitleInApp": False,
        "oldLowerInApp": False,
        "oldUpperInHtml": False,
        "oldTitleInHtml": False,
    }


def test_dashboard_sync_action_group_has_purple_chosen_and_green_all():
    out = run_node(
        r"""
        import {readFileSync} from 'node:fs';
        const html = readFileSync('./DASHBOARD/index.html','utf8');
        const css = readFileSync('./DASHBOARD/dashboard.css','utf8');
        const actionMatch = css.match(/\.hero-action\s*\{([\s\S]*?)\}/);
        const baseMatch = css.match(/\.hero-sync-button\s*\{([\s\S]*?)\}/);
        const allMatch = css.match(/\.hero-sync-button--all\s*\{([\s\S]*?)\}/);
        const mediaMatch = css.match(/@media \(max-width: 700px\)\s*\{([\s\S]*?)\n\}/);
        const mobileMatch = mediaMatch && mediaMatch[1].match(/\.hero-sync-button\s*\{([\s\S]*?)\}/);
        const titleMatch = css.match(/\.sync-title\s*\{([\s\S]*?)\}/);
        const iconMatch = css.match(/\.button-icon\s*\{([\s\S]*?)\}/);
        const mobileIconMatch = mediaMatch && mediaMatch[1].match(/\.button-icon\s*\{([\s\S]*?)\}/);
        if (!actionMatch || !baseMatch || !allMatch || !mobileMatch || !titleMatch || !iconMatch || !mobileIconMatch) {
            throw new Error('sync action group CSS blocks not found');
        }
        const num = (block, prop) => {
            const m = block.match(new RegExp(prop + ':\\s*(\\d+(?:\\.\\d+)?)'));
            return m ? Number(m[1]) : null;
        };
        const shadow = (titleMatch[1].match(/text-shadow:\s*([\s\S]*?);/) || ['',''])[1];
        console.log(JSON.stringify({
            labels: html.includes('aria-label="SYNC CHOSEN"') && html.includes('<span class="sync-title">SYNC CHOSEN</span>')
                && html.includes('aria-label="SYNC ALL"') && html.includes('<span class="sync-title">SYNC ALL</span>'),
            order: html.indexOf('id="sync-button"') < html.indexOf('id="sync-all-button"'),
            countElement: html.includes('id="sync-eligible-count"'),
            desktopFontSize: num(baseMatch[1],'font-size'),
            desktopIconSize: num(iconMatch[1],'width'),
            fontWeight: num(baseMatch[1],'font-weight'),
            desktopLetterSpacing: num(baseMatch[1],'letter-spacing'),
            mobileFontSize: num(mobileMatch[1],'font-size'),
            mobileIconSize: num(mobileIconMatch[1],'width'),
            mobileLetterSpacing: num(mobileMatch[1],'letter-spacing'),
            flexWrap: actionMatch[1].includes('flex-wrap: wrap'),
            mobileFullWidth: mobileMatch[1].includes('flex: 1 1 100%'),
            purple: baseMatch[1].includes('#C93BFF'),
            green: allMatch[1].includes('#10EFA2'),
            stroke: (titleMatch[1].match(/-webkit-text-stroke:\s*\d+px\s*rgba?\([^)]*\)/) || [''])[0],
            shadowLayers: (shadow.match(/\b0\s+-?\d+px/g) || []).length,
        }));
        """
    )
    assert out == {
        "labels": True,
        "order": True,
        "countElement": True,
        "desktopFontSize": 26,
        "desktopIconSize": 27,
        "fontWeight": 750,
        "desktopLetterSpacing": 0.1,
        "mobileFontSize": 22,
        "mobileIconSize": 24,
        "mobileLetterSpacing": 0.08,
        "flexWrap": True,
        "mobileFullWidth": True,
        "purple": True,
        "green": True,
        "stroke": "",
        "shadowLayers": 1,
    }


def test_sync_chosen_and_sync_all_use_only_eligible_repositories():
    out = run_node(
        """
        import {isSyncableRepository} from './DASHBOARD/utils.js';
        const behindFork = (name, extra = {}) => ({repository:name,ahead_by:0,behind_by:1,fork:true,...extra});
        const repos = [
            behindFork('u/behind',{status:'behind'}),
            behindFork('u/ready',{status:'to-be-synced'}),
            behindFork('u/ready2',{status:'to_be_synced'}),
            behindFork('u/private',{status:'behind',is_private:true}),
            behindFork('u/current',{status:'up-to-date',ahead_by:0,behind_by:0}),
            behindFork('u/ahead',{status:'ahead',ahead_by:1,behind_by:0}),
            behindFork('u/diverged',{status:'diverged',ahead_by:1,behind_by:1}),
            behindFork('u/error',{status:'error'}),
            behindFork('u/conflict',{status:'conflict'}),
            behindFork('u/unknown',{status:'unknown',ahead_by:undefined,behind_by:undefined}),
            behindFork('u/skipped',{status:'skipped',ahead_by:undefined,behind_by:undefined}),
            behindFork('u/nonfork',{status:'behind',fork:false}),
            {detail:'perm',account:'x'},
        ];
        const syncable = repos.filter(isSyncableRepository).map(r => r.repository);
        const selected = new Set(['u/behind','u/current','u/ready','u/error','missing/repo']);
        const chosen = [...selected].filter(name => syncable.some(repository => repository === name));
        const empty = [...new Set(['u/current','missing/repo'])].filter(name => syncable.some(repository => repository === name));
        console.log(JSON.stringify({syncable,chosen,empty}));
        """
    )
    assert out == {
        "syncable": ["u/behind", "u/ready", "u/ready2", "u/private"],
        "chosen": ["u/behind", "u/ready"],
        "empty": [],
    }


def test_sync_action_group_confirmations_and_payload_contract():
    out = run_node(
        """
        import {readFileSync} from 'node:fs';
        const app = readFileSync('./DASHBOARD/app.js','utf8');
        console.log(JSON.stringify({
            chosenConfirm: app.includes('Synchronize ${repos.length} selected READY TO SYNC fork(s)? Only READY TO SYNC forks can be auto-synced.'),
            allConfirm: app.includes('Synchronize ALL ${repos.length} eligible READY TO SYNC fork(s)? This affects all eligible repositories. Only READY TO SYNC forks can be auto-synced.'),
            payload: app.includes('JSON.stringify({ dry_run: false, confirmation: "SYNC", repositories: repos })'),
            chosenHandler: app.includes('runSync("chosen")'),
            allHandler: app.includes('runSync("all")'),
            busyDisablesBoth: app.includes('syncButton.disabled = true;') && app.includes('syncAllButton.disabled = true;'),
            chosenEmptyGuard: app.includes('Select at least one READY TO SYNC fork. UNSYNCABLE forks cannot be auto-synced.'),
            allEmptyGuard: app.includes('No READY TO SYNC forks are available. UNSYNCABLE forks cannot be auto-synced.'),
            eligibleCount: app.includes('syncEligibleCount.textContent = syncable.length === 0'),
            historyLabels: app.includes('const action = mode === "all" ? "SYNC ALL" : "SYNC CHOSEN";'),
        }));
        """
    )
    assert out == {
        "chosenConfirm": True,
        "allConfirm": True,
        "payload": True,
        "chosenHandler": True,
        "allHandler": True,
        "busyDisablesBoth": True,
        "chosenEmptyGuard": True,
        "allEmptyGuard": True,
        "eligibleCount": True,
        "historyLabels": True,
    }

