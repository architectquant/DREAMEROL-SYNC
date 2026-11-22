import {
    requestJson,
    effectiveCountClass,
    formatLastSync,
    formatHistoryTimestamp,
    computeDashboardCounts,
    sortReposForDisplay,
    isReadyCandidate,
    isSelectableCandidate,
    listErrorMessage,
    isSyncableRepository,
    isSyncConfirmedRepository,
    isCheckError,
    computeProgress,
    finalizePreviewCounters,
    getPreviewProgressState,
    getSyncProgressState,
    dedupeRepositoriesByName,
    mergePreviewResult,
    mergePreviewError,
    mergeOperationResults,
    operationCountsAfter,
    getUnexpectedStates,
    getForkFlagErrors,
    getUpstreamLabel,
    summarizeSyncResults,
} from "./utils.js?v=20261121d";

const WELCOME_URL = `${window.location.origin}/?switch=1`;
const BATCH_CHECK_SIZE = 10;
const CHECK_TIMEOUT_MS = 8000;
const PREFLIGHT_TIMEOUT_MS = 30000;
const LAST_OPERATION_KEY_PREFIX = "dreamerol.lastOperation";
const SELECTION_KEY_PREFIX = "dreamerol.selection";
const DASHBOARD_SNAPSHOT_KEY_PREFIX = "dreamerol.dashboardSnapshot";
const el = (id) => document.getElementById(id);
const userName = el("user-name");
const userAvatar = el("user-avatar");
const connectionStatus = el("connection-status");
const signoutButton = el("signout-button");
const switchAccountButton = el("switch-account-button");
const syncButton = el("sync-button");
const syncAllButton = el("sync-all-button");
const syncEligibleCount = el("sync-eligible-count");
const searchInput = el("repo-search");
const filterSelect = el("status-filter");
const statusMessage = el("status-message");
const repoList = el("repo-list");
const historyList = el("sync-history");
const previewPanel = el("preview-progress");
const previewLabel = el("preview-progress-label");
const previewCount = el("preview-progress-count");
const previewSpinner = el("preview-spinner");
const syncPanel = el("sync-progress");
const syncLabel = el("sync-progress-label");
const syncCount = el("sync-progress-count");
const syncSpinner = el("sync-spinner");
const syncCurrent = el("sync-current-info");
const statsEls = {
    total: el("stat-total"),
    upToDate: el("stat-up-to-date"),
    toBeSynced: el("stat-to-be-synced"),
    unsyncable: el("stat-unsyncable"),
    aheadNote: el("ahead-note"),
};
const summaryEls = {
    status: el("summary-status"),
    total: el("summary-total"),
    upToDate: el("summary-up-to-date"),
    toBeSynced: el("summary-to-be-synced"),
    unsyncable: el("summary-unsyncable"),
    attention: el("summary-attention"),
};
let repositories = [];
let selected = new Set();
let history = [];
let initialized = false;
let sessionGeneration = 0;
let activePreviewControllers = new Set();
let previewInFlight = false;
let backgroundScanActive = false;
let listError = "";
let syncInFlight = false;
let checkingSet = new Set();
let checkedCount = 0;
let previewTotal = 0;
let forkFlagErrors = [];
let operationLock = false;
let lastOperation = null;
let operationLockedNames = new Set();
let operationCounts = null;
let operationStatusText = "";
let snapshotSuppressed = false;
let authoritativeOperations = [];
let currentAccount = "";
let sessionExpired = false;

function isCurrent(gen) { return gen === sessionGeneration; }

function normalizeOperation(raw, source = "live") {
    const results = Array.isArray(raw && raw.results)
        ? raw.results.filter((r) => r && typeof r === "object" && typeof r.repository === "string" && r.repository.includes("/"))
            .map((r) => ({
                repository: r.repository,
                status: r.status || "unknown",
                message: typeof r.message === "string" ? r.message : "",
                ahead_by: Number.isInteger(r.ahead_by) ? r.ahead_by : null,
                behind_by: Number.isInteger(r.behind_by) ? r.behind_by : null,
                last_successful_sync: typeof r.last_successful_sync === "string" ? r.last_successful_sync : null,
            }))
        : [];
    const targets = Array.isArray(raw && raw.targets) && raw.targets.length
        ? raw.targets.filter((name) => typeof name === "string")
        : results.map((r) => r.repository);
    const countsBeforeRaw = raw && (raw.counts_before || raw.countsBefore);
    return {
        operationId: (raw && (raw.operation_id || raw.operationId)) || "",
        createdAt: (raw && (raw.created_at || raw.createdAt)) || new Date().toISOString(),
        targets,
        results,
        summary: (raw && raw.summary) || summarizeSyncResults(results),
        countsBefore: countsBeforeRaw && Number.isFinite(countsBeforeRaw.total) ? { ...countsBeforeRaw } : null,
        source: source === "restored" ? "restored" : "live",
    };
}

function lastOperationStorageKey(account = currentAccount) {
    if (typeof account !== "string" || !account.trim()) return "";
    return `${LAST_OPERATION_KEY_PREFIX}.${account.trim().toLowerCase()}`;
}

function saveLastOperation(operation, account = currentAccount) {
    const key = lastOperationStorageKey(account);
    if (!key) return;
    try {
        window.localStorage.setItem(key, JSON.stringify(operation));
    } catch {}
}

function loadLastOperation(account = currentAccount) {
    const key = lastOperationStorageKey(account);
    if (!key) return null;
    try {
        const raw = window.localStorage.getItem(key);
        return raw ? normalizeOperation(JSON.parse(raw), "restored") : null;
    } catch {
        return null;
    }
}

function selectionStorageKey(account = currentAccount) {
    if (typeof account !== "string" || !account.trim()) return "";
    return `${SELECTION_KEY_PREFIX}.${account.trim().toLowerCase()}`;
}

function saveSelection() {
    const key = selectionStorageKey();
    if (!key) return;
    try {
        window.sessionStorage.setItem(key, JSON.stringify([...selected]));
    } catch {}
}

function loadSelection() {
    const key = selectionStorageKey();
    if (!key) return new Set();
    try {
        const raw = window.sessionStorage.getItem(key);
        const names = raw ? JSON.parse(raw) : [];
        return new Set(Array.isArray(names) ? names.filter((name) => typeof name === "string" && name.includes("/")) : []);
    } catch {
        return new Set();
    }
}

function dashboardSnapshotKey(account = currentAccount) {
    if (typeof account !== "string" || !account.trim()) return "";
    return `${DASHBOARD_SNAPSHOT_KEY_PREFIX}.${account.trim().toLowerCase()}`;
}

function clearDashboardSnapshot(account = currentAccount) {
    const key = dashboardSnapshotKey(account);
    if (!key) return;
    try { window.sessionStorage.removeItem(key); } catch {}
}

function saveDashboardSnapshot({ force = false } = {}) {
    const key = dashboardSnapshotKey();
    if (snapshotSuppressed || !key || repositories.length === 0) return;
    if (!force && (previewInFlight || backgroundScanActive || syncInFlight || operationLock || sessionExpired)) return;
    try {
        window.sessionStorage.setItem(key, JSON.stringify({
            account: currentAccount,
            savedAt: Date.now(),
            repositories,
            selected: [...selected],
            statusText: statusMessage ? statusMessage.textContent : "",
            statusClass: statusMessage ? statusMessage.className : "",
            lastOperation,
            operationCounts,
            operationStatusText,
            operationLockedNames: [...operationLockedNames],
            authoritativeOperations,
            history,
            checkedCount,
            previewTotal,
            forkFlagErrors,
            listError,
            statusFilter: filterSelect ? filterSelect.value : "all",
            searchText: searchInput ? searchInput.value : "",
        }));
    } catch {}
}

function loadDashboardSnapshot(account = currentAccount) {
    const key = dashboardSnapshotKey(account);
    if (!key) return null;
    try {
        const raw = window.sessionStorage.getItem(key);
        if (!raw) return null;
        const snapshot = JSON.parse(raw);
        if (!snapshot || typeof snapshot.account !== "string") return null;
        if (snapshot.account.trim().toLowerCase() !== account.trim().toLowerCase()) return null;
        if (!Array.isArray(snapshot.repositories) || snapshot.repositories.length === 0) return null;
        return snapshot;
    } catch {
        return null;
    }
}

function restoreDashboardSnapshot(snapshot) {
    previewInFlight = false;
    backgroundScanActive = false;
    checkingSet = new Set();
    sessionExpired = false;
    listError = typeof snapshot.listError === "string" ? snapshot.listError : "";
    repositories = snapshot.repositories.filter((repo) => repo && typeof repo.repository === "string");
    selected = new Set((Array.isArray(snapshot.selected) ? snapshot.selected : []).filter((name) => typeof name === "string"));
    lastOperation = snapshot.lastOperation ? normalizeOperation(snapshot.lastOperation, "restored") : null;
    operationCounts = snapshot.operationCounts && Number.isFinite(snapshot.operationCounts.total)
        ? { ...snapshot.operationCounts }
        : null;
    operationStatusText = typeof snapshot.operationStatusText === "string" ? snapshot.operationStatusText : "";
    operationLockedNames = new Set(Array.isArray(snapshot.operationLockedNames) ? snapshot.operationLockedNames : []);
    authoritativeOperations = Array.isArray(snapshot.authoritativeOperations) ? snapshot.authoritativeOperations : [];
    history = Array.isArray(snapshot.history) ? snapshot.history : [];
    checkedCount = Number.isFinite(snapshot.checkedCount) ? snapshot.checkedCount : repositories.length;
    previewTotal = Number.isFinite(snapshot.previewTotal) ? snapshot.previewTotal : repositories.length;
    forkFlagErrors = Array.isArray(snapshot.forkFlagErrors) ? snapshot.forkFlagErrors : [];
    if (statusMessage) {
        statusMessage.textContent = typeof snapshot.statusText === "string" ? snapshot.statusText : "";
        statusMessage.className = typeof snapshot.statusClass === "string" ? snapshot.statusClass : "";
    }
    if (filterSelect && typeof snapshot.statusFilter === "string"
        && [...filterSelect.options].some((option) => option.value === snapshot.statusFilter)) {
        filterSelect.value = snapshot.statusFilter;
    }
    if (searchInput && typeof snapshot.searchText === "string") searchInput.value = snapshot.searchText;
    renderPreviewProgress(false);
    setBusyUI();
    updateStats();
    renderRepos();
    updateSelectionUI();
    renderHistory();
    if (lastOperation) {
        renderSyncProgress({
            total: lastOperation.results.length,
            processed: lastOperation.results.length,
            active: false,
            current: `Recorded at ${lastOperation.createdAt}`,
        });
    }
}

function applyOperation(raw, options = {}) {
    const opts = typeof options === "boolean" ? { persist: options, source: "live" } : (options || {});
    const source = opts.source === "restored" ? "restored" : "live";
    const persist = !!opts.persist;
    const restored = source === "restored";
    if (!raw || !Array.isArray(raw.results)) return;
    const next = normalizeOperation(raw, source);
    if (lastOperation && lastOperation.operationId && lastOperation.operationId !== next.operationId
        && lastOperation.createdAt > next.createdAt) return;
    if (!next.countsBefore && lastOperation && lastOperation.operationId === next.operationId) {
        next.countsBefore = lastOperation.countsBefore;
    }
    if (restored && lastOperation && lastOperation.operationId === next.operationId && lastOperation.source !== "restored") return;
    lastOperation = next;
    if (restored) {
        operationLockedNames = new Set();
        operationCounts = next.countsBefore
            ? operationCountsAfter(next.countsBefore, next.summary, next.results, next.createdAt)
            : null;
        operationStatusText = `Last recorded sync result: ${next.summary.success} synchronized, ${next.summary.failed} failed. Running fresh checks.`;
    } else {
        operationLockedNames = new Set(next.targets);
        const merged = mergeOperationResults(repositories, next.results, next.createdAt);
        repositories = merged.repositories;
        operationCounts = next.countsBefore
            ? operationCountsAfter(next.countsBefore, next.summary, next.results, next.createdAt)
            : null;
        operationStatusText = next.countsBefore
            ? `Last sync result: ${next.summary.success} synchronized, ${next.summary.failed} failed. Fresh checks continue.`
            : "";
    }
    if (persist) saveLastOperation(lastOperation);
    renderSyncProgress({
        total: lastOperation.results.length,
        processed: lastOperation.results.length,
        active: false,
        current: `${restored ? "Recorded" : "Completed"} at ${lastOperation.createdAt}`,
    });
    updateStats();
    renderRepos();
    updateSelectionUI();
    renderHistory();
}

function setConnectionState(text, tone = "") {
    if (!connectionStatus) return;
    connectionStatus.textContent = text;
    connectionStatus.classList.remove("is-online", "is-error");
    if (tone) connectionStatus.classList.add(tone);
}

function setCounterText(node, value, loading = false) {
    if (!node) return;
    node.textContent = loading ? "CHECKING" : String(value);
    node.classList.toggle("is-loading", !!loading);
}

function renderFinalSummary(counts, statusText) {
    setCounterText(summaryEls.total, listError ? "—" : counts.total, false);
    setCounterText(summaryEls.upToDate, listError ? "—" : counts.up_to_date, false);
    setCounterText(summaryEls.toBeSynced, listError ? "—" : counts.to_be_synced, false);
    setCounterText(summaryEls.unsyncable, listError ? "—" : counts.unsyncable, false);
    if (summaryEls.status) summaryEls.status.textContent = statusText;
    const unexpected = getUnexpectedStates(repositories);
    const unverified = (counts.pending || 0) + (counts.check_errors || 0);
    const attention = [];
    if (listError) attention.push(listError);
    if (forkFlagErrors.length > 0) attention.push(`${forkFlagErrors.length} item(s) with missing/invalid fork flag excluded as data errors: ${forkFlagErrors.slice(0, 5).join(", ")}.`);
    if (counts.invalid_repositories > 0) attention.push(`${counts.invalid_repositories} fork row(s) with invalid repository name excluded.`);
    if (counts.duplicates > 0) attention.push(`${counts.duplicates} duplicate fork row(s) ignored.`);
    if (unverified > 0) attention.push(`${unverified} check(s) unverified; shown separately from verified counters.`);
    if (unexpected.length > 0) attention.push(`Unexpected or unclassified state(s): ${unexpected.join(", ")}. Excluded as unverified.`);
    if (summaryEls.attention) {
        summaryEls.attention.hidden = attention.length === 0;
        summaryEls.attention.textContent = attention.join(" ");
    }
}

function repoRowClass(repo, effective, checking) {
    if (checking) return "is-checking";
    if (repo && isCheckError(repo)) return "is-unverified";
    if (effective === "synced") return "is-up-to-date";
    if (effective === "behind") return "is-behind";
    if (effective === "ahead") return "is-ahead";
    if (effective === "diverged") return "is-diverged";
    if (effective === "pending") return "is-pending";
    return "is-unverified";
}

function abortActivePreview() {
    for (const c of activePreviewControllers) {
        try { c.abort(); } catch {}
    }
    activePreviewControllers.clear();
}

function invalidatePendingOperations() {
    sessionGeneration += 1;
    abortActivePreview();
    previewInFlight = false;
    backgroundScanActive = false;
    listError = "";
    syncInFlight = false;
    checkingSet = new Set();
    if (typeof renderPreviewProgress === "function") {
        try { renderPreviewProgress(false); } catch {}
    }
}

function setStatus(message, tone = "") {
    statusMessage.textContent = message;
    statusMessage.classList.remove("is-success", "is-warning", "is-error", "is-loading");
    if (tone === "success") statusMessage.classList.add("is-success");
    else if (tone === "warning") statusMessage.classList.add("is-warning");
    else if (tone === "error") statusMessage.classList.add("is-error");
    else if (tone === "loading") statusMessage.classList.add("is-loading");
}

function renderPreviewProgress(active) {
    const running = !!active && (previewInFlight || backgroundScanActive) && isCurrent(sessionGeneration);
    if (previewPanel) {
        previewPanel.hidden = !running;
        previewPanel.classList.toggle("is-active", running);
    }
    if (previewSpinner) previewSpinner.classList.toggle("is-stopped", !running);
    const loadingList = previewTotal === 0 && previewInFlight;
    const pendingCount = Math.max(0, previewTotal - checkedCount);
    if (previewLabel) previewLabel.textContent = loadingList ? "Loading fork list" : "Checking forks";
    if (previewCount) previewCount.textContent = loadingList ? "Loading fork list..." : `${checkedCount} / ${previewTotal} checked, ${pendingCount} pending`;
}

function handleCheckSessionExpired(gen) {
    if (!isCurrent(gen)) return;
    invalidatePendingOperations();
    clearDashboardSnapshot();
    sessionExpired = true;
    setConnectionState("GitHub Signed out", "is-error");
    setStatus("SESSION EXPIRED — PLEASE SIGN IN", "error");
    saveSelection();
    renderPreviewProgress(false);
    renderRepos();
    updateStats();
    updateSelectionUI();
}

function finalizePreviewUi(gen) {
    if (!isCurrent(gen)) return;
    previewInFlight = false;
    backgroundScanActive = false;
    checkingSet = new Set();
    const finalized = finalizePreviewCounters({ checked: checkedCount, total: previewTotal });
    checkedCount = finalized.checked;
    setBusyUI();
    renderPreviewProgress(false);
    renderRepos();
    if (computeDashboardCounts(repositories).complete) {
        operationCounts = null;
        operationStatusText = "";
    }
    updateStats();
    updateSelectionUI();
    saveDashboardSnapshot();
}

function renderSyncProgress({ total = 0, processed = 0, active = false, current = "" } = {}) {
    const state = getSyncProgressState({ total, processed, active });
    if (syncPanel) {
        syncPanel.hidden = !(active || total > 0);
        syncPanel.classList.toggle("is-active", !!active);
    }
    if (syncSpinner) syncSpinner.classList.toggle("is-stopped", !active);
    if (syncLabel) syncLabel.textContent = state.label;
    if (syncCount) syncCount.textContent = `${state.processed} / ${state.total}`;
    if (syncCurrent) syncCurrent.textContent = current || (active ? "Processing selected repositories..." : (total > 0 ? "Sync processing completed." : ""));
}

function setBusyUI() {
    const busy = syncInFlight || operationLock;
    if (switchAccountButton) switchAccountButton.disabled = busy;
    signoutButton.disabled = busy;
    if (busy) {
        syncButton.disabled = true;
        syncAllButton.disabled = true;
    }
}

function renderedHistoryEntries() {
    const entries = [];
    for (const operation of authoritativeOperations.slice(0, 1)) {
        for (const result of Array.isArray(operation.results) ? operation.results : []) {
            if (!result || typeof result.repository !== "string") continue;
            entries.push({
                repository: result.repository,
                status: result.status || "unknown",
                message: typeof result.message === "string" ? result.message : "",
                timestamp: operation.created_at,
            });
        }
    }
    return entries;
}

function renderHistory() {
    const authoritative = renderedHistoryEntries();
    if (authoritative.length > 0) {
        renderResults(authoritative, historyList);
        return;
    }
    if (lastOperation) {
        renderResults(lastOperation.results.map((r) => ({
            repository: r.repository,
            status: r.status,
            message: r.message,
            timestamp: "",
        })), historyList);
        return;
    }
    renderResults(history.slice(0, 1).map((h) => ({
        repository: h.time,
        status: h.summary,
        message: "",
        timestamp: "",
    })), historyList);
}

function syncableRepositories() {
    return repositories.filter((r) => isSelectableCandidate(r));
}

function confirmedRepositories() {
    return repositories.filter((r) => isSyncConfirmedRepository(r));
}

function updateSelectionUI() {
    const syncable = syncableRepositories();
    const allowed = new Set(syncable.map((r) => r.repository));
    const allowedSelection = new Set([...selected].filter((name) => allowed.has(name)));
    if (allowedSelection.size !== selected.size) {
        selected = allowedSelection;
        saveSelection();
    }
    const selectedSyncable = syncable.filter((r) => selected.has(r.repository)).length;
    const checksRunning = previewInFlight || backgroundScanActive;
    const idle = !syncInFlight && !operationLock && !checksRunning && !sessionExpired;
    syncButton.disabled = !idle || selectedSyncable === 0;
    syncAllButton.disabled = !idle || syncable.length === 0;
    if (syncEligibleCount) {
        syncEligibleCount.textContent = syncable.length === 0
            ? "No SELECTABLE forks"
            : `${syncable.length} SELECTABLE fork${syncable.length === 1 ? "" : "s"} — checks continue`;
    }
    syncButton.setAttribute("aria-label", `SYNC CHOSEN ${selectedSyncable} selected fork(s)`);
    syncAllButton.setAttribute("aria-label", `SYNC ALL ${syncable.length} eligible fork(s)`);
}

function resetDashboardState({ clearOperation = false } = {}) {
    repositories = [];
    selected = new Set();
    checkedCount = 0;
    previewTotal = 0;
    previewInFlight = false;
    backgroundScanActive = false;
    listError = "";
    checkingSet = new Set();
    forkFlagErrors = [];
    operationLockedNames = new Set();
    operationCounts = null;
    operationStatusText = "";
    authoritativeOperations = [];
    if (clearOperation) {
        history = [];
        lastOperation = null;
        clearDashboardSnapshot();
        try {
            const key = lastOperationStorageKey();
            if (key) window.localStorage.removeItem(key);
            window.localStorage.removeItem("dreamerol.lastOperation");
        } catch {}
    }
    userName.textContent = "Loading...";
    userAvatar.hidden = true;
    userAvatar.removeAttribute("src");
    setConnectionState("Connecting...");
    renderPreviewProgress(false);
    renderSyncProgress({ total: 0, processed: 0, active: false, current: "" });
    if (syncPanel) syncPanel.hidden = true;
    updateStats();
    renderRepos();
    renderHistory();
    setBusyUI();
    updateSelectionUI();
}

function updateStats() {
    const liveCounts = computeDashboardCounts(repositories);
    const snapshotActive = operationCounts
        && (repositories.length === 0 || previewInFlight || backgroundScanActive || !liveCounts.complete);
    const counts = snapshotActive ? operationCounts : liveCounts;
    const unverified = (counts.pending || 0) + (counts.check_errors || 0);
    setCounterText(statsEls.total, listError ? "—" : counts.total, false);
    setCounterText(statsEls.upToDate, listError ? "—" : counts.up_to_date, false);
    setCounterText(statsEls.toBeSynced, listError ? "—" : counts.to_be_synced, false);
    setCounterText(statsEls.unsyncable, listError ? "—" : counts.unsyncable, false);
    if (statsEls.aheadNote) {
        statsEls.aheadNote.hidden = counts.ahead === 0;
        statsEls.aheadNote.textContent = counts.ahead > 0
            ? `${counts.ahead} AHEAD-only fork(s) included in UNSYNCABLE; not auto-synced.`
            : "";
    }
    const operationNote = lastOperation
        ? `; last sync ${lastOperation.summary.success} synchronized, ${lastOperation.summary.failed} failed`
        : "; no GitHub repositories were modified";
    let summaryText = "Checking starts automatically after sign-in.";
    if (listError) {
        summaryText = listError;
        setStatus(listError, "error");
    } else if ((previewInFlight || backgroundScanActive) && previewTotal > 0) {
        const pendingCount = Math.max(0, previewTotal - checkedCount);
        summaryText = `Checking forks: ${checkedCount} of ${previewTotal} complete, ${pendingCount} pending${operationNote}.`;
    } else if (previewInFlight) {
        summaryText = "Loading fork list — no repositories will be modified.";
    } else if (repositories.length) {
        summaryText = counts.complete
            ? `${counts.total} forks checked${operationNote}.`
            : `${counts.total} forks listed, ${unverified} check(s) unverified; verified counters shown separately${operationNote}.`;
    } else if (operationStatusText) {
        summaryText = operationStatusText;
    }
    renderFinalSummary(counts, summaryText);
}

function filteredRepos() {
    const q = (searchInput.value || "").toLowerCase();
    const f = filterSelect.value;
    return sortReposForDisplay(repositories.filter((r) => {
        if (!r || r.fork !== true) return false;
        const matchesQ = !q || (r.repository || "").toLowerCase().includes(q);
        const c = effectiveCountClass(r);
        let matchesF = false;
        if (f === "all") matchesF = true;
        else if (f === "up-to-date") matchesF = c === "synced";
        else if (f === "to-be-synced") matchesF = c === "behind";
        else if (f === "unsyncable") matchesF = c === "diverged" || c === "ahead";
        else if (f === "ahead-only") matchesF = c === "ahead";
        return matchesQ && matchesF;
    }));
}

function renderRepos() {
    repoList.replaceChildren();
    const checksRunning = previewInFlight || backgroundScanActive;
    const statusLabels = {
        "behind": "READY TO SYNC",
        "up-to-date": "UP TO DATE",
        "synced": "UP TO DATE",
        "ahead": "UNSYNCABLE",
        "diverged": "UNSYNCABLE",
        "error": "UNVERIFIED!!!",
        "conflict": "UNVERIFIED!!!",
        "unknown": "UNVERIFIED!!!",
        "pending": "PENDING",
        "skipped": "UNVERIFIED!!!",
    };
    for (const repo of filteredRepos()) {
        const li = document.createElement("li");
        const effective = effectiveCountClass(repo);
        const isChecking = (previewInFlight || backgroundScanActive) && checkingSet.has(repo.repository);
        const checkFailed = !isChecking && isCheckError(repo);
        const lastKnown = checkFailed && !!repo.preview_error && effective !== "error" && effective !== "unknown";
        const confirmedLabel = statusLabels[effective] || statusLabels[repo.status] || "PENDING";
        li.className = `repo-row ${repoRowClass(repo, effective, isChecking)}`;
        const selectCell = document.createElement("span");
        selectCell.className = "repo-select";
        if (isSelectableCandidate(repo)) {
            const cb = document.createElement("input");
            cb.type = "checkbox";
            cb.checked = selected.has(repo.repository);
            cb.disabled = checksRunning;
            if (checksRunning) cb.title = "Available after checks finish.";
            cb.setAttribute("aria-label", `Select ${repo.repository} for SYNC`);
            cb.addEventListener("change", () => {
                if (cb.checked) selected.add(repo.repository); else selected.delete(repo.repository);
                saveSelection();
                updateSelectionUI();
                saveDashboardSnapshot();
            });
            selectCell.appendChild(cb);
        }
        li.appendChild(selectCell);
        const name = document.createElement("span");
        name.className = "repo-name";
        name.textContent = repo.repository || "unknown";
        const status = document.createElement("span");
        status.className = "repo-status";
        if (isChecking) status.textContent = "CHECKING";
        else if (checkFailed) status.textContent = "UNVERIFIED!!!";
        else if (repo.check_status === "ok") status.textContent = confirmedLabel;
        else status.textContent = confirmedLabel;
        if (effective === "diverged") status.title = "DIVERGED forks are included in UNSYNCABLE and are never auto-synced.";
        else if (checkFailed) status.title = lastKnown
            ? "Check failed or unverified; showing last known classification."
            : "Check failed or unverified; excluded from confirmed sync.";
        const meta = document.createElement("span");
        meta.className = "repo-meta";
        const deltas = [];
        if (Number.isInteger(repo.ahead_by)) deltas.push(`${repo.ahead_by} ahead`);
        if (Number.isInteger(repo.behind_by)) deltas.push(`${repo.behind_by} behind`);
        const messageText = !isChecking ? (checkFailed ? repo.preview_error : (repo.message || "")) : "";
        meta.textContent = `${deltas.length ? `(${deltas.join(", ")})` : "—"}${messageText ? ` - ${messageText}` : ""}`;
        if (repo.check_status === "error" || repo.check_status === "timeout") {
            const retry = document.createElement("button");
            retry.type = "button";
            retry.className = "check-retry";
            retry.textContent = "Retry check";
            retry.addEventListener("click", () => retryCheck(repo.repository));
            meta.appendChild(retry);
        }
        const upstream = document.createElement("span");
        upstream.className = "repo-meta repo-upstream";
        upstream.textContent = getUpstreamLabel(repo) || "—";
        const syncInfo = document.createElement("span");
        syncInfo.className = "repo-meta repo-last-sync";
        syncInfo.textContent = formatLastSync(repo.last_successful_sync);
        li.append(name, status, meta, upstream, syncInfo);
        repoList.appendChild(li);
    }
    updateSelectionUI();
}

function renderResults(results, target) {
    target.replaceChildren();
    for (const r of results || []) {
        const li = document.createElement("li");
        li.textContent = `${r.repository}: ${r.status}${r.message ? ` - ${r.message}` : ""} (${formatHistoryTimestamp(r.timestamp)})`;
        target.appendChild(li);
    }
}

function addHistory(entry) {
    history.unshift({ time: new Date().toLocaleTimeString(), ...entry });
    renderHistory();
}

async function ensureAuth(gen = sessionGeneration) {
    try {
        const data = await requestJson("/api/auth/status", { cache: "no-store" }, "Not signed in.");
        if (!isCurrent(gen)) return null;
        if (data.state !== "AUTHENTICATED") throw new Error("Not authenticated");
        currentAccount = typeof data.account === "string" ? data.account.trim() : "";
        userName.textContent = currentAccount || "unknown";
        setConnectionState("GitHub Connected", "is-online");
        if (data.avatar_url) {
            userAvatar.src = data.avatar_url;
            userAvatar.hidden = false;
        } else {
            userAvatar.hidden = true;
            userAvatar.removeAttribute("src");
        }
        return data;
    } catch {
        snapshotSuppressed = true;
        clearDashboardSnapshot();
        setConnectionState("GitHub Signed out", "is-error");
        if (isCurrent(gen)) window.location.assign(WELCOME_URL);
        return null;
    }
}

async function preview({ auto = false } = {}) {
    if (syncInFlight) return false;
    if (previewInFlight) return false;
    const gen = sessionGeneration;
    previewInFlight = true;
    backgroundScanActive = false;
    listError = "";
    abortActivePreview();
    checkedCount = 0;
    previewTotal = 0;
    checkingSet = new Set();
    forkFlagErrors = [];
    if (repositories.length > 0) {
        const available = new Set(repositories.map((r) => r.repository));
        selected = new Set([...selected].filter((name) => available.has(name)));
    }
    setBusyUI();
    renderPreviewProgress(true);
    setStatus("Loading fork list — no repositories will be modified.", "loading");
    try {
        const listController = new AbortController();
        activePreviewControllers.add(listController);
        const listData = await requestJson(
            "/api/sync",
            { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ dry_run: true, mode: "list" }), signal: listController.signal },
            "Check failed.",
        );
        activePreviewControllers.delete(listController);
        if (!isCurrent(gen)) return false;

        const listRows = Array.isArray(listData.results) ? listData.results : [];
        forkFlagErrors = getForkFlagErrors(listRows);
        const listedRepositories = dedupeRepositoriesByName(
            listRows
                .filter((r) => r && r.fork === true && typeof r.repository === "string" && r.repository.includes("/"))
                .map((r) => ({
                    repository: r.repository,
                    status: "pending",
                    fork: r.fork,
                    ahead_by: r.ahead_by ?? null,
                    behind_by: r.behind_by ?? null,
                    message: r.message ?? null,
                    parent: r.parent ?? null,
                    upstream: r.upstream ?? null,
                    upstream_full_name: r.upstream_full_name ?? null,
                    last_successful_sync: r.last_successful_sync ?? null,
                    check_status: "pending",
                }))
        );
    const applyRecordedOperation = !!(lastOperation && lastOperation.source !== "restored");
    repositories = mergeOperationResults(
        listedRepositories,
        applyRecordedOperation ? lastOperation.results : [],
        lastOperation ? lastOperation.createdAt : null
    ).repositories.filter((r) => r && r.fork === true);
        previewTotal = repositories.length;
        const resolvedNames = applyRecordedOperation
            ? new Set(lastOperation.results.map((r) => r.repository))
            : new Set();
        checkedCount = repositories.filter((r) => resolvedNames.has(r.repository)).length;
        checkingSet = new Set();
        if (listData.account) userName.textContent = listData.account;
        selected = new Set([...selected].filter((name) => repositories.some((r) => r.repository === name && isSelectableCandidate(r))));
        updateStats();
        renderRepos();
        updateSelectionUI();
        const selectableCount = repositories.filter((r) => isSelectableCandidate(r)).length;
        setStatus(`${selectableCount} fork(s) listed and selectable. Background checks continue — no repositories were modified.`, "loading");
        previewInFlight = false;
        backgroundScanActive = true;
        renderPreviewProgress(true);
        void runBackgroundChecks(gen, auto);
        return true;
    } catch (e) {
        if (!isCurrent(gen)) return false;
        if (e && e.status === 401) { handleCheckSessionExpired(gen); return false; }
        listError = listErrorMessage(e);
        repositories = [];
        selected = new Set();
        previewTotal = 0;
        checkedCount = 0;
        checkingSet = new Set();
        updateStats();
        renderRepos();
        updateSelectionUI();
        renderPreviewProgress(false);
        setStatus(listError, "error");
        addHistory({ summary: `Check failed: ${listError}` });
        return false;
    } finally {
        if (previewInFlight) finalizePreviewUi(gen);
    }
}

async function runBackgroundChecks(gen, auto = false) {
    const queue = repositories
        .filter((r) => r && typeof r.repository === "string" && !operationLockedNames.has(r.repository))
        .map((r) => r.repository);
    const batches = [];
    for (let i = 0; i < queue.length; i += BATCH_CHECK_SIZE) {
        batches.push(queue.slice(i, i + BATCH_CHECK_SIZE));
    }

    async function checkBatch(names) {
        if (!isCurrent(gen) || !Array.isArray(names) || names.length === 0) return;
        const activeNames = names.filter((name) => !operationLockedNames.has(name));
        if (activeNames.length === 0) return;
        for (const name of activeNames) checkingSet.add(name);
        if (isCurrent(gen)) {
            updateStats();
            updateSelectionUI();
            renderPreviewProgress(true);
            renderRepos();
        }
        const controller = new AbortController();
        activePreviewControllers.add(controller);
        let timedOut = false;
        const timeoutId = setTimeout(() => { timedOut = true; controller.abort(); }, CHECK_TIMEOUT_MS * activeNames.length);
        try {
            const data = await requestJson(
                "/api/sync",
                { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ dry_run: true, repositories: activeNames }), signal: controller.signal },
                "Check failed.",
            );
            if (!isCurrent(gen)) return;
            const results = Array.isArray(data && data.results) ? data.results : [];
            const byName = new Map();
            for (const result of results) {
                if (result && typeof result.repository === "string" && !byName.has(result.repository)) byName.set(result.repository, result);
            }
            for (const name of activeNames) {
                if (operationLockedNames.has(name)) continue;
                const writeIndex = repositories.findIndex((r) => r && r.repository === name);
                if (writeIndex < 0) continue;
                const result = byName.get(name) || null;
                if (result) {
                    repositories[writeIndex] = mergePreviewResult(repositories[writeIndex], result, name);
                    if (repositories[writeIndex]) repositories[writeIndex].check_status = "ok";
                } else {
                    repositories[writeIndex] = mergePreviewError(repositories[writeIndex], "No matching result returned.", name);
                    if (repositories[writeIndex]) repositories[writeIndex].check_status = "error";
                }
            }
        } catch (e) {
            if (e && e.name === "AbortError") {
                if (!timedOut || !isCurrent(gen)) return;
                for (const name of activeNames) {
                    if (operationLockedNames.has(name)) continue;
                    const writeIndex = repositories.findIndex((r) => r && r.repository === name);
                    if (writeIndex < 0) continue;
                    repositories[writeIndex] = mergePreviewError(repositories[writeIndex], "Check timeout", name);
                    if (repositories[writeIndex]) repositories[writeIndex].check_status = "timeout";
                }
                return;
            }
            if (!isCurrent(gen)) return;
            if (e && e.status === 401) { handleCheckSessionExpired(gen); return; }
            for (const name of activeNames) {
                if (operationLockedNames.has(name)) continue;
                const writeIndex = repositories.findIndex((r) => r && r.repository === name);
                if (writeIndex < 0) continue;
                repositories[writeIndex] = mergePreviewError(repositories[writeIndex], (e && e.message) || "Check failed.", name);
                if (repositories[writeIndex]) repositories[writeIndex].check_status = "error";
            }
        } finally {
            clearTimeout(timeoutId);
            activePreviewControllers.delete(controller);
            if (!isCurrent(gen)) return;
            for (const name of activeNames) {
                checkingSet.delete(name);
                if (!operationLockedNames.has(name)) checkedCount += 1;
            }
            updateStats();
            updateSelectionUI();
            renderPreviewProgress(true);
            renderRepos();
        }
    }

    try {
        for (const batch of batches) {
            await checkBatch(batch);
            if (!isCurrent(gen)) return;
        }

        if (!isCurrent(gen)) return;
        const counts = computeDashboardCounts(repositories);
        const unverified = counts.pending + counts.check_errors;
        const dataErrors = counts.invalid_fork_flags + counts.invalid_repositories + counts.duplicates + forkFlagErrors.length;
        const needsAttention = counts.unsyncable > 0 || unverified > 0 || dataErrors > 0;
        const checkingIncomplete = unverified > 0 || checkedCount < previewTotal;
        const countSummary = checkingIncomplete
            ? `${counts.up_to_date} up to date, ${counts.to_be_synced} READY TO SYNC, ${counts.unsyncable} unsyncable, ${unverified} unverified`
            : `${counts.up_to_date} up to date, ${counts.to_be_synced} READY TO SYNC, ${counts.unsyncable} unsyncable`;
        const modificationNote = lastOperation
            ? ` Last sync result: ${lastOperation.summary.success} synchronized, ${lastOperation.summary.failed} failed.`
            : " No repositories were modified.";
        setStatus(
            checkingIncomplete
                ? `Check incomplete: ${checkedCount} of ${previewTotal} complete, ${unverified} check(s) unverified; verified counters shown separately.${modificationNote}`
                : `Check complete: ${counts.total} forks checked.${modificationNote}${dataErrors > 0 ? ` ${dataErrors} data error(s) reported in the summary.` : ""}`,
            checkingIncomplete || needsAttention ? "warning" : ""
        );
        addHistory({
            summary: `${checkingIncomplete ? "Check incomplete" : (auto ? "Automatic check" : "Check")}: ${checkedCount}/${previewTotal} complete, ${counts.total} forks, ${countSummary}${dataErrors > 0 ? `, ${dataErrors} data error(s)` : ""}`,
        });
    } finally {
        finalizePreviewUi(gen);
    }
}

async function preflightSelected(names) {
    const gen = sessionGeneration;
    const outcomes = await Promise.all((names || []).map(async (name) => {
        if (repositories.findIndex((r) => r.repository === name) < 0) return { name, ok: false, message: "Repository is not available." };
        const controller = new AbortController();
        let timedOut = false;
        const timeoutId = setTimeout(() => { timedOut = true; controller.abort(); }, PREFLIGHT_TIMEOUT_MS);
        try {
            const data = await requestJson(
                "/api/sync",
                { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ dry_run: true, repositories: [name] }), signal: controller.signal },
                "Check failed.",
            );
            if (!isCurrent(gen)) return { name, ok: false, message: "Session changed." };
            if (operationLockedNames.has(name)) return { name, ok: false, message: "Locked by a completed operation." };
            const writeIndex = repositories.findIndex((r) => r.repository === name);
            if (writeIndex < 0) return { name, ok: false, message: "Repository is not available." };
            const res = (data.results && data.results[0]) ? data.results[0] : null;
            repositories[writeIndex] = mergePreviewResult(repositories[writeIndex], res, name);
            repositories[writeIndex].check_status = "ok";
            return {
                name,
                ok: isSyncConfirmedRepository(repositories[writeIndex]),
                message: repositories[writeIndex].message || "Safety check passed.",
            };
        } catch (e) {
            if (!isCurrent(gen)) return { name, ok: false, message: "Session changed." };
            const writeIndex = repositories.findIndex((r) => r.repository === name);
            if (writeIndex < 0) return { name, ok: false, message: "Repository is not available." };
            const message = e && e.name === "AbortError"
                ? "Check timeout"
                : (e && e.message) || "Check failed.";
            repositories[writeIndex] = mergePreviewError(repositories[writeIndex], message, name);
            repositories[writeIndex].check_status = e && e.name === "AbortError" ? "timeout" : "error";
            return { name, ok: false, message };
        } finally {
            clearTimeout(timeoutId);
        }
    }));
    updateStats();
    renderRepos();
    updateSelectionUI();
    return outcomes;
}

async function retryCheck(name) {
    if (syncInFlight || operationLock) return;
    const repo = repositories.find((r) => r.repository === name);
    if (!repo) return;
    repo.check_status = "running";
    renderRepos();
    await preflightSelected([name]);
    saveDashboardSnapshot();
}

async function runSync(mode) {
    if (syncInFlight || operationLock) return;
    const gen = sessionGeneration;
    operationCounts = null;
    operationStatusText = "";
    operationLock = true;
    setBusyUI();
    updateSelectionUI();
    try {
        const syncable = syncableRepositories();
        const requested = mode === "all"
            ? syncable.map((r) => r.repository)
            : Array.from(selected).filter((name) => syncable.some((r) => r.repository === name));
        if (requested.length === 0) {
            setStatus(mode === "all"
                ? "No READY TO SYNC forks are available. UNSYNCABLE forks cannot be auto-synced."
                : "Select at least one READY TO SYNC fork. UNSYNCABLE forks cannot be auto-synced.", "warning");
            return;
        }
        const preflight = await preflightSelected(requested);
        if (!isCurrent(gen)) return;
        const failed = preflight.filter((item) => !item.ok);
        const repos = preflight.filter((item) => item.ok).map((item) => item.name);
        if (repos.length === 0) {
            setStatus(`No selected repository passed the final safety check. ${failed.map((item) => `${item.name}: ${item.message}`).join("; ")}`, "error");
            return;
        }
        const details = repos.map((name) => {
            const repo = repositories.find((r) => r.repository === name);
            const upstream = repo ? getUpstreamLabel(repo) : "";
            const message = repo && repo.message ? repo.message : "Safety check passed.";
            return `${name}: ${message}${upstream ? ` (upstream: ${upstream})` : ""}`;
        }).join("\n");
        const baseConfirm = mode === "all"
            ? `Synchronize ALL ${repos.length} eligible READY TO SYNC fork(s)? This affects all eligible repositories. Only READY TO SYNC forks can be auto-synced.`
            : `Synchronize ${repos.length} selected READY TO SYNC fork(s)? Only READY TO SYNC forks can be auto-synced.`;
        const excluded = failed.length ? `\nExcluded after safety check: ${failed.map((item) => `${item.name} (${item.message})`).join(", ")}` : "";
        const confirmMessage = `${baseConfirm}${excluded}\n\n${details}\n\nConfirm live GitHub Sync?`;
        if (!window.confirm(confirmMessage)) return;
        syncInFlight = true;
        setBusyUI();
        updateSelectionUI();
        renderSyncProgress({ total: repos.length, processed: 0, active: true, current: mode === "all"
            ? `Processing all eligible forks (0 of ${repos.length})...`
            : `Processing selected forks (0 of ${repos.length})...` });
        setStatus(mode === "all"
            ? `SYNC ALL in progress: ${repos.length} eligible fork(s).`
            : `SYNC CHOSEN in progress: ${repos.length} selected fork(s).`, "loading");
        const countsBefore = computeDashboardCounts(repositories);
        const data = await requestJson("/api/sync", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ dry_run: false, confirmation: "SYNC", repositories: repos }) }, "Sync failed.");
        if (!isCurrent(gen)) return;
        if (lastOperation && data.operation_id && lastOperation.operationId === data.operation_id) return;
        const results = data.results || [];
        applyOperation({
            operation_id: data.operation_id || "",
            created_at: new Date().toISOString(),
            targets: repos,
            results,
            counts_before: countsBefore,
        }, true);
        const summary = lastOperation.summary;
        const action = mode === "all" ? "SYNC ALL" : "SYNC CHOSEN";
        const historySummary = `${action}: ${summary.success} synchronized, ${summary.skipped} skipped, ${summary.failed} failed, ${summary.manual} need attention`;
        addHistory({ summary: historySummary });
        await restoreAuthoritativeOperation(gen);
        setStatus(`${historySummary}. Background checks continue.`, summary.failed > 0 ? "error" : "success");
    } catch (e) {
        if (!isCurrent(gen)) return;
        if (e && e.status === 401) { window.location.assign(WELCOME_URL); return; }
        setStatus(`Sync failed: ${(e && e.message) || "error"}. No UNSYNCABLE forks were auto-synced.`, "error");
        addHistory({ summary: `Sync failed: ${(e && e.message) || "error"}` });
    } finally {
        syncInFlight = false;
        operationLock = false;
        if (isCurrent(gen)) {
            setBusyUI();
            updateSelectionUI();
            saveDashboardSnapshot();
        }
    }
}

async function restoreAuthoritativeOperation(gen) {
    const expectedAccount = currentAccount;
    try {
        const data = await requestJson("/api/history", { cache: "no-store" }, "History unavailable.");
        if (!isCurrent(gen) || currentAccount !== expectedAccount) return;
        if (data && typeof data.account === "string" && currentAccount && data.account.toLowerCase() !== currentAccount.toLowerCase()) return;
        if (!Array.isArray(data.operations) || data.operations.length === 0) return;
        authoritativeOperations = data.operations.filter((op) => op && typeof op === "object");
        renderHistory();
        const latest = authoritativeOperations.find((op) => typeof op.operation_id === "string");
        if (!latest) return;
        if (lastOperation && lastOperation.operationId === latest.operation_id && lastOperation.source !== "restored") return;
        applyOperation(latest, { persist: true, source: "restored" });
    } catch {
        return;
    }
}

async function initDashboard({ force = false } = {}) {
    if (syncInFlight || operationLock) return;
    if (previewInFlight && !force) return;
    if (initialized && !force) return;
    if (force) invalidatePendingOperations();
    initialized = true;
    const gen = sessionGeneration;
    resetDashboardState();
    setConnectionState("Connecting...");
    setStatus("Restoring session...", "loading");
    const auth = await ensureAuth(gen);
    if (!auth || !isCurrent(gen)) {
        if (isCurrent(gen)) {
            renderPreviewProgress(false);
            setBusyUI();
            updateSelectionUI();
        }
        return;
    }
    sessionExpired = false;
    snapshotSuppressed = false;
    const storedOperation = loadLastOperation(currentAccount);
    const savedSnapshot = loadDashboardSnapshot(currentAccount);
    const snapshotOperationId = savedSnapshot && savedSnapshot.lastOperation
        ? (savedSnapshot.lastOperation.operationId || savedSnapshot.lastOperation.operation_id || "")
        : "";
    const storedOperationId = storedOperation ? storedOperation.operationId : "";
    if (savedSnapshot && snapshotOperationId === storedOperationId) {
        restoreDashboardSnapshot(savedSnapshot);
        return;
    }
    if (savedSnapshot) clearDashboardSnapshot();
    selected = loadSelection();
    applyOperation(storedOperation, { source: "restored" });
    await restoreAuthoritativeOperation(gen);
    await preview({ auto: true });
}

function toWelcome() {
    snapshotSuppressed = true;
    invalidatePendingOperations();
    initialized = false;
    resetDashboardState({ clearOperation: true });
    currentAccount = "";
    window.location.assign(WELCOME_URL);
}

signoutButton.addEventListener("click", async () => {
    invalidatePendingOperations();
    try { await requestJson("/api/auth/logout", { method: "POST" }, "Sign out failed."); } catch {}
    toWelcome();
});

if (switchAccountButton) {
    switchAccountButton.addEventListener("click", async () => {
        switchAccountButton.disabled = true;
        setStatus("Switching account...", "loading");
        invalidatePendingOperations();
        initialized = false;
        resetDashboardState({ clearOperation: true });
        currentAccount = "";
        try { await requestJson("/api/auth/switch", { method: "POST" }, "Switch account failed."); } catch {}
        toWelcome();
    });
}

syncButton.addEventListener("click", () => runSync("chosen"));
syncAllButton.addEventListener("click", () => runSync("all"));
searchInput.addEventListener("input", () => { renderRepos(); saveDashboardSnapshot(); });
filterSelect.addEventListener("change", () => { renderRepos(); saveDashboardSnapshot(); });
function handlePageShowRestore(event) {
    if (!event.persisted || syncInFlight || operationLock) return;
    if (initialized && !previewInFlight && !backgroundScanActive) {
        renderPreviewProgress(false);
        updateStats();
        renderRepos();
        updateSelectionUI();
        return;
    }
    if (previewInFlight || backgroundScanActive) {
        renderPreviewProgress(true);
        updateStats();
        renderRepos();
        updateSelectionUI();
        return;
    }
    invalidatePendingOperations();
    initDashboard({ force: true });
}

window.addEventListener("pageshow", handlePageShowRestore);
window.addEventListener("pagehide", () => saveDashboardSnapshot({ force: true }));

initDashboard();
