const brokerLoginButton = document.getElementById("broker-login-button");
const brokerLink = document.getElementById("broker-link");
const authStatus = document.getElementById("auth-status");

const PENDING_AUTH_STATES = new Set(["PENDING", "PROCESSING", "TOKEN_READY"]);
const TERMINAL_AUTH_STATES = new Set(["FAILED", "CANCELLED", "EXPIRED", "ACKNOWLEDGED"]);
const LOGIN_POLL_MS = 2000;
const LOGIN_TIMEOUT_MS = 5 * 60 * 1000;
const DASHBOARD_URL = `${window.location.origin}/dashboard`;

let loginTimer = null;
let loginStartedAt = 0;
let loginPollGeneration = 0;

function setAuthStatus(message, state = "") {
    if (!authStatus) return;
    authStatus.textContent = message;
    authStatus.dataset.state = state;
}

function stopLoginPolling() {
    loginPollGeneration += 1;
    if (loginTimer !== null) {
        window.clearTimeout(loginTimer);
        loginTimer = null;
    }
}

async function requestJson(url, options = {}, fallbackMessage = "The request failed.") {
    let response;
    try {
        response = await fetch(url, { credentials: "same-origin", ...options });
    } catch {
        throw new Error("Could not reach the server.");
    }
    let data = null;
    try {
        data = await response.json();
    } catch {
        data = null;
    }
    if (!response.ok) {
        const detail = data && typeof data.detail === "string" ? data.detail : fallbackMessage;
        const error = new Error(detail);
        error.status = response.status;
        throw error;
    }
    if (data === null) {
        throw new Error("The server returned an invalid response.");
    }
    return data;
}

function redirectToDashboard() {
    stopLoginPolling();
    window.location.assign(DASHBOARD_URL);
}

async function pollLoginStatus(gen) {
    loginTimer = null;
    if (gen !== loginPollGeneration) return;
    if (Date.now() - loginStartedAt > LOGIN_TIMEOUT_MS) {
        setAuthStatus("GitHub sign-in timed out. Try again.", "error");
        return;
    }
    try {
        const data = await requestJson("/api/auth/status", { cache: "no-store" }, "Could not check GitHub sign-in status.");
        if (gen !== loginPollGeneration) return;
        if (data.state === "AUTHENTICATED") {
            redirectToDashboard();
            return;
        }
        if (TERMINAL_AUTH_STATES.has(data.state)) {
            setAuthStatus("GitHub sign-in did not complete. Try again.", "error");
            return;
        }
        setAuthStatus("Waiting for GitHub authorization…", "pending");
    } catch (error) {
        if (gen !== loginPollGeneration) return;
        if (error.status === 401) {
            setAuthStatus("GitHub sign-in session expired. Try again.", "error");
            return;
        }
        setAuthStatus("Could not check GitHub sign-in yet. Retrying…", "error");
    }
    loginTimer = window.setTimeout(() => pollLoginStatus(gen), LOGIN_POLL_MS);
}

function startLoginPolling() {
    stopLoginPolling();
    const gen = loginPollGeneration;
    loginStartedAt = Date.now();
    setAuthStatus("Waiting for GitHub authorization…", "pending");
    loginTimer = window.setTimeout(() => pollLoginStatus(gen), LOGIN_POLL_MS);
}

async function restoreSession() {
    try {
        const data = await requestJson("/api/auth/status", { cache: "no-store" }, "Could not check GitHub sign-in status.");
        if (data.state === "AUTHENTICATED") {
            redirectToDashboard();
            return;
        }
        if (PENDING_AUTH_STATES.has(data.state)) {
            startLoginPolling();
            return;
        }
        setAuthStatus("Not signed in.", "muted");
    } catch (error) {
        if (error.status === 401) {
            setAuthStatus("Not signed in.", "muted");
            return;
        }
        setAuthStatus(error.message || "Could not check GitHub sign-in status.", "error");
    }
}

if (brokerLoginButton) {
    brokerLoginButton.addEventListener("click", async () => {
        stopLoginPolling();
        brokerLoginButton.disabled = true;
        if (brokerLink) brokerLink.hidden = true;
        try {
            const data = await requestJson("/api/auth/start", { method: "POST" }, "Could not start GitHub sign-in.");
            if (brokerLink) {
                brokerLink.href = data.authorization_url;
                brokerLink.hidden = false;
            }
            window.open(data.authorization_url, "_blank", "noopener,noreferrer");
            startLoginPolling();
        } catch (error) {
            setAuthStatus(error.message || "Could not start GitHub sign-in.", "error");
        } finally {
            brokerLoginButton.disabled = false;
        }
    });
}

restoreSession();
