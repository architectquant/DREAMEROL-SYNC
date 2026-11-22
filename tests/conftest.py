import requests.sessions
import pytest


WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


@pytest.fixture(autouse=True)
def isolated_sync_history(tmp_path):
    from api.app import app
    from api.sync_history import SyncHistoryStore

    original = getattr(app.state, "sync_history", None)
    app.state.sync_history = SyncHistoryStore(tmp_path / "sync_history.json")
    try:
        yield
    finally:
        app.state.sync_history = original


@pytest.fixture(autouse=True)
def forbid_real_github_writes(monkeypatch):
    real_request = requests.sessions.Session.request

    def guarded_request(self, method, url, *args, **kwargs):
        target = str(url)
        if str(method).upper() in WRITE_METHODS and "github.com" in target:
            if "/login/oauth/access_token" not in target:
                raise AssertionError(f"Blocked real GitHub write request: {method} {target}")
        return real_request(self, method, url, *args, **kwargs)

    monkeypatch.setattr(requests.sessions.Session, "request", guarded_request)
