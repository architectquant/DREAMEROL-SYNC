import os
import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_serializer
from requests.exceptions import RequestException

from api.auth import (
    SESSION_COOKIE,
    TERMINAL_STATES,
    UnknownSession,
    WebAuthError,
    WebAuthManager,
)
from api.sync_history import SyncHistoryStore
from fork_sync.github import GitHubClient
from fork_sync.synchronizer import ForkSynchronizer

router = APIRouter(prefix="/api", tags=["sync"])


def _cookie_secure(request: Request) -> bool:
    setting = os.getenv("COOKIE_SECURE", "auto").strip().lower()
    if setting in {"1", "true", "yes", "on"}:
        return True
    if setting in {"0", "false", "no", "off"}:
        return False
    return request.url.scheme == "https"


def _github_discovery_error(error) -> str:
    response = getattr(error, "response", None)
    status = getattr(response, "status_code", None)
    if isinstance(status, int) and 400 <= status <= 599:
        return f"Could not load forks from GitHub (HTTP {status})."
    return "Could not load forks from GitHub."


class SyncRequest(BaseModel):
    dry_run: bool = True
    confirmation: str | None = None
    repositories: list[str] | None = None
    mode: str | None = None


class SyncResult(BaseModel):
    repository: str
    status: str
    message: str | None = None
    ahead_by: int | None = None
    behind_by: int | None = None
    last_successful_sync: str | None = None
    fork: bool | None = None

    @model_serializer
    def serialize_result(self) -> dict:
        data = {
            "repository": self.repository,
            "status": self.status,
            "message": self.message,
            "ahead_by": self.ahead_by,
            "behind_by": self.behind_by,
            "last_successful_sync": self.last_successful_sync,
        }
        if self.fork is not None:
            data["fork"] = self.fork
        return data


class SyncResponse(BaseModel):
    account: str
    total: int
    results: list[SyncResult]
    diagnostics: dict | None = None
    operation_id: str | None = None

    @model_serializer
    def serialize_response(self) -> dict:
        data = {
            "account": self.account,
            "total": self.total,
            "results": self.results,
            "diagnostics": self.diagnostics,
        }
        if self.operation_id:
            data["operation_id"] = self.operation_id
        return data


class HistoryResponse(BaseModel):
    account: str
    last_successful_sync: dict[str, str]
    operations: list[dict]


class AuthStartResponse(BaseModel):
    authorization_url: str


class AuthStatusResponse(BaseModel):
    state: str
    account: str | None = None
    avatar_url: str | None = None


class LogoutResponse(BaseModel):
    state: str


def get_web_auth_manager(request: Request) -> WebAuthManager:
    return request.app.state.auth_manager


def get_sync_history(request: Request) -> SyncHistoryStore:
    store = getattr(request.app.state, "sync_history", None)
    if store is None:
        store = SyncHistoryStore()
        request.app.state.sync_history = store
    return store


def _set_session_cookie(
    response: Response,
    request: Request,
    manager: WebAuthManager,
    session_id: str,
) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        session_id,
        max_age=max(1, int(manager.ttl_seconds)),
        httponly=True,
        samesite="lax",
        secure=_cookie_secure(request),
        path="/",
    )


def _resolve_github_credentials(
    request: Request,
    authorization: str | None,
    manager: WebAuthManager,
) -> tuple[str, str | None, str | None]:
    if authorization is not None:
        scheme, separator, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not separator or not token.strip():
            raise HTTPException(
                status_code=401,
                detail="Provide a GitHub token using the Bearer authorization scheme.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token.strip(), None, None

    session_id = request.cookies.get(SESSION_COOKIE)
    credentials = manager.credentials(session_id)
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Sign in through the Auth Broker or provide a GitHub token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token, account = credentials
    return token, session_id, account


def _github_http_status(error: RequestException) -> int | None:
    response = getattr(error, "response", None)
    status = getattr(response, "status_code", None)
    return status if isinstance(status, int) else None


@router.post("/auth/start", response_model=AuthStartResponse)
def start_web_authentication(
    request: Request,
    response: Response,
    manager: WebAuthManager = Depends(get_web_auth_manager),
):
    """Start a server-side Broker login for the browser session."""
    try:
        session_id, authorization_url = manager.start()
    except WebAuthError as error:
        raise HTTPException(status_code=502, detail=str(error)) from None

    _set_session_cookie(response, request, manager, session_id)
    return AuthStartResponse(authorization_url=authorization_url)


@router.get("/auth/status", response_model=AuthStatusResponse)
def web_authentication_status(
    request: Request,
    response: Response,
    manager: WebAuthManager = Depends(get_web_auth_manager),
):
    """Report whether the browser session has completed Broker login."""
    try:
        result = manager.status(request.cookies.get(SESSION_COOKIE))
    except UnknownSession:
        error_response = JSONResponse(
            status_code=401,
            content={"detail": "Sign in through the Auth Broker first."},
        )
        error_response.delete_cookie(SESSION_COOKIE, path="/")
        return error_response
    except WebAuthError as error:
        raise HTTPException(status_code=502, detail=str(error)) from None

    session_id = request.cookies.get(SESSION_COOKIE)
    if result["state"] in TERMINAL_STATES:
        response.delete_cookie(SESSION_COOKIE, path="/")
    elif session_id:
        _set_session_cookie(response, request, manager, session_id)
    return AuthStatusResponse(**result)


@router.post("/auth/logout", response_model=LogoutResponse)
def logout_web_authentication(
    request: Request,
    response: Response,
    manager: WebAuthManager = Depends(get_web_auth_manager),
):
    """Discard the server-side browser credential."""
    manager.logout(request.cookies.get(SESSION_COOKIE))
    response.delete_cookie(SESSION_COOKIE, path="/")
    return LogoutResponse(state="SIGNED_OUT")


@router.post("/auth/switch", response_model=LogoutResponse)
def switch_web_authentication(
    request: Request,
    response: Response,
    manager: WebAuthManager = Depends(get_web_auth_manager),
):
    """Terminate current server-side session so a different GitHub account can sign in."""
    manager.logout(request.cookies.get(SESSION_COOKIE))
    response.delete_cookie(SESSION_COOKIE, path="/")
    return LogoutResponse(state="SIGNED_OUT")


@router.post("/sync", response_model=SyncResponse)
def sync_repositories(
    request: SyncRequest,
    http_request: Request,
    response: Response,
    authorization: str | None = Header(default=None),
    manager: WebAuthManager = Depends(get_web_auth_manager),
    sync_history: SyncHistoryStore = Depends(get_sync_history),
):
    """Preview fork status or sync only the explicitly confirmed, lagging forks."""
    token, session_id, account = _resolve_github_credentials(
        http_request, authorization, manager
    )

    def _github_error(error: RequestException, *, discovery: bool = False) -> JSONResponse:
        status = _github_http_status(error)
        if status == 401:
            if session_id:
                manager.logout(session_id)
            error_response = JSONResponse(
                status_code=401,
                content={
                    "state": "REAUTH_REQUIRED",
                    "detail": "The GitHub token is invalid.",
                },
            )
            error_response.delete_cookie(SESSION_COOKIE, path="/")
            return error_response
        if discovery:
            return JSONResponse(
                status_code=502,
                content={"detail": _github_discovery_error(error)},
            )
        if status == 403:
            return JSONResponse(
                status_code=403,
                content={"detail": "The GitHub token does not have sufficient permissions."},
            )
        return JSONResponse(
            status_code=502,
            content={"detail": "Could not reach GitHub."},
        )

    if not request.dry_run:
        if request.confirmation != "SYNC":
            raise HTTPException(
                status_code=400,
                detail='Live synchronization requires confirmation="SYNC".',
            )
        if not request.repositories:
            raise HTTPException(
                status_code=400,
                detail="Select at least one repository from the preview before syncing.",
            )
        if len(request.repositories) > 5000:
            raise HTTPException(status_code=400, detail="Too many repositories were selected.")
        if len(set(request.repositories)) != len(request.repositories):
            raise HTTPException(status_code=400, detail="Duplicate repositories were selected.")

    operation_id = str(uuid.uuid4()) if not request.dry_run else None

    client = GitHubClient(token.strip())
    try:
        if not isinstance(account, str) or not account.strip():
            try:
                user = client.get_authenticated_user()
            except RequestException as error:
                return _github_error(error)
            account = user.get("login") if isinstance(user, dict) else None
            if not isinstance(account, str) or not account.strip():
                raise HTTPException(status_code=502, detail="GitHub returned an invalid account profile.")

        if session_id:
            _set_session_cookie(response, http_request, manager, session_id)

        def _dedupe_forks_by_name(forks):
            seen = set()
            unique = []
            for fork in forks or []:
                if not isinstance(fork, dict):
                    continue
                name = fork.get("full_name")
                if not isinstance(name, str) or not name.strip() or name in seen:
                    continue
                seen.add(name)
                unique.append(fork)
            return unique

        def _dedupe_results_by_repository(items):
            seen = set()
            unique = []
            for item in items or []:
                if not isinstance(item, dict):
                    continue
                name = item.get("repository")
                if not isinstance(name, str) or not name.strip() or name in seen:
                    continue
                seen.add(name)
                unique.append(item)
            return unique

        synchronizer = ForkSynchronizer(client)
        diagnostics = None
        if request.dry_run:
            if request.mode == "list":
                try:
                    current_forks = _dedupe_forks_by_name(synchronizer.get_forks())
                except RequestException as error:
                    return _github_error(error, discovery=True)
                get_last_diagnostics = getattr(synchronizer, "get_last_diagnostics", None)
                if callable(get_last_diagnostics):
                    candidate = get_last_diagnostics()
                    if isinstance(candidate, dict):
                        diagnostics = candidate
                results = _dedupe_results_by_repository([
                    {
                        "repository": fork.get("full_name"),
                        "status": "pending",
                        "message": "Not checked yet.",
                        "ahead_by": None,
                        "behind_by": None,
                        "fork": fork.get("fork") if isinstance(fork.get("fork"), bool) else None,
                    }
                    for fork in current_forks
                    if isinstance(fork, dict) and isinstance(fork.get("full_name"), str)
                ])
            elif request.repositories:
                if len(request.repositories) > 5000:
                    raise HTTPException(status_code=400, detail="Too many repositories were selected.")
                if len(set(request.repositories)) != len(request.repositories):
                    raise HTTPException(status_code=400, detail="Duplicate repositories were selected.")
                try:
                    current_forks = _dedupe_forks_by_name(synchronizer.get_forks())
                except RequestException as error:
                    return _github_error(error, discovery=True)
                forks_by_name = {
                    fork.get("full_name"): fork
                    for fork in current_forks
                    if isinstance(fork, dict) and isinstance(fork.get("full_name"), str)
                }
                missing = [name for name in request.repositories if name not in forks_by_name]
                if missing:
                    raise HTTPException(
                        status_code=400,
                        detail="A selected repository is no longer an available fork for this account. Preview again.",
                    )
                results = _dedupe_results_by_repository([
                    synchronizer.preview_fork(forks_by_name[name])
                    for name in request.repositories
                ])
            else:
                # This performs read-only comparisons; it never submits a merge request.
                results = _dedupe_results_by_repository(synchronizer.preview_all())
        else:
            try:
                current_forks = _dedupe_forks_by_name(synchronizer.get_forks())
            except RequestException as error:
                return _github_error(error, discovery=True)

            available = {
                fork.get("full_name")
                for fork in current_forks
                if isinstance(fork, dict) and isinstance(fork.get("full_name"), str)
            }
            if any(repository not in available for repository in request.repositories):
                raise HTTPException(
                    status_code=400,
                    detail="A selected repository is no longer an available fork for this account. Preview again.",
                )

            selected_names = set(request.repositories)
            selected_forks = [
                fork for fork in current_forks
                if fork.get("full_name") in selected_names
            ]

            # Recheck status on the server so stale or edited browser requests cannot
            # cause an up-to-date fork to be sent to the merge-upstream endpoint.
            preview_by_name = {
                result["repository"]: result
                for result in (
                    synchronizer.preview_fork(fork) for fork in selected_forks
                )
            }
            behind_forks = [
                fork for fork in selected_forks
                if preview_by_name[fork["full_name"]]["status"] == "behind"
            ]
            sync_results = synchronizer.sync_all(forks=behind_forks)
            sync_by_name = {result["repository"]: result for result in sync_results}

            results = []
            for repository in request.repositories:
                preview = preview_by_name[repository]
                if preview["status"] == "behind":
                    # If the second comparison changes state, sync_fork reports the
                    # final status; otherwise this is the per-repository sync result.
                    results.append(sync_by_name.get(repository, preview))
                else:
                    results.append(preview)

            # Persist timestamp only after an actually successful synchronization.
            for result in results:
                if result.get("status") == "synced":
                    sync_history.record_success(account, result["repository"])
            if operation_id:
                sync_history.record_operation(
                    account,
                    operation_id,
                    results,
                    targets=request.repositories,
                )

        last_map = sync_history.get_map(account)
        enriched = []
        for result in results:
            item = dict(result)
            repo_name = item.get("repository")
            if isinstance(repo_name, str):
                item["last_successful_sync"] = last_map.get(repo_name)
            else:
                item["last_successful_sync"] = None
            enriched.append(item)

        return SyncResponse(
            account=account,
            total=len(enriched),
            results=enriched,
            diagnostics=diagnostics,
            operation_id=operation_id,
        )
    except RequestException as error:
        return _github_error(error)
    finally:
        client.session.close()


@router.get("/history", response_model=HistoryResponse)
def read_sync_history(
    http_request: Request,
    response: Response,
    authorization: str | None = Header(default=None),
    manager: WebAuthManager = Depends(get_web_auth_manager),
    sync_history: SyncHistoryStore = Depends(get_sync_history),
):
    """Return authoritative persisted sync results for the current account."""
    token, session_id, account = _resolve_github_credentials(
        http_request, authorization, manager
    )
    if not isinstance(account, str) or not account.strip():
        client = GitHubClient(token.strip())
        try:
            user = client.get_authenticated_user()
        except RequestException as error:
            return _github_error(error)
        finally:
            client.session.close()
        account = user.get("login") if isinstance(user, dict) else None
        if not isinstance(account, str) or not account.strip():
            raise HTTPException(status_code=502, detail="GitHub returned an invalid account profile.")

    if session_id:
        _set_session_cookie(response, http_request, manager, session_id)
    snapshot = sync_history.get_snapshot(account)
    return HistoryResponse(
        account=account,
        last_successful_sync=snapshot["last_successful_sync"],
        operations=snapshot["operations"],
    )


class CompareDiagnosticsRequest(BaseModel):
    repositories: list[str]


@router.post("/debug/compare-forks")
def debug_compare_forks(
    request: CompareDiagnosticsRequest,
    http_request: Request,
    response: Response,
    authorization: str | None = Header(default=None),
    manager: WebAuthManager = Depends(get_web_auth_manager),
):
    """Read-only compare diagnostics for explicit repos (no sync/writes, no counters)."""
    if not isinstance(request.repositories, list) or not request.repositories:
        raise HTTPException(status_code=400, detail="Provide at least one repository.")
    if len(request.repositories) > 20:
        raise HTTPException(status_code=400, detail="Too many repositories requested.")

    token, session_id, account = _resolve_github_credentials(
        http_request, authorization, manager
    )

    def _gh_err(error: RequestException, *, discovery: bool = False) -> JSONResponse:
        status = _github_http_status(error)
        if status == 401:
            if session_id:
                manager.logout(session_id)
            error_response = JSONResponse(
                status_code=401,
                content={"state": "REAUTH_REQUIRED", "detail": "The GitHub token is invalid."},
            )
            error_response.delete_cookie(SESSION_COOKIE, path="/")
            return error_response
        if discovery:
            return JSONResponse(status_code=502, content={"detail": _github_discovery_error(error)})
        if status == 403:
            return JSONResponse(status_code=403, content={"detail": "The GitHub token does not have sufficient permissions."})
        return JSONResponse(status_code=502, content={"detail": "Could not reach GitHub."})

    client = GitHubClient(token.strip())
    try:
        if not isinstance(account, str) or not account.strip():
            try:
                user = client.get_authenticated_user()
            except RequestException as error:
                return _gh_err(error)
            account = user.get("login") if isinstance(user, dict) else None
            if not isinstance(account, str) or not account.strip():
                raise HTTPException(status_code=502, detail="GitHub returned an invalid account profile.")

        if session_id:
            _set_session_cookie(response, http_request, manager, session_id)

        synchronizer = ForkSynchronizer(client)
        try:
            current_forks = synchronizer.get_forks()
        except RequestException as error:
            return _gh_err(error, discovery=True)

        forks_by_name = {
            fork.get("full_name"): fork
            for fork in (current_forks or [])
            if isinstance(fork, dict) and isinstance(fork.get("full_name"), str)
        }

        diagnostics_get = getattr(synchronizer, "get_last_diagnostics", None)
        discovery_diagnostics = diagnostics_get() if callable(diagnostics_get) else None

        results = []
        for name in request.repositories:
            if not isinstance(name, str) or not name.strip():
                results.append({
                    "repository_full_name": name,
                    "result_state": "UNVERIFIED",
                    "origin": "error",
                    "message": "Invalid repository name.",
                })
                continue
            repo_name = name.strip()
            fork = forks_by_name.get(repo_name)
            if not isinstance(fork, dict):
                results.append({
                    "request_id": str(uuid.uuid4()),
                    "account_login": account,
                    "repository_full_name": repo_name,
                    "result_state": "UNVERIFIED",
                    "origin": "not_found_in_discovery",
                    "message": "Repository not found in fresh authenticated fork discovery.",
                })
                continue
            results.append(
                synchronizer.compare_fork_diagnostic(fork, account_login=account)
            )

        return {
            "account": account,
            "discovery_diagnostics": discovery_diagnostics,
            "total": len(results),
            "results": results,
        }
    except RequestException as error:
        return _gh_err(error)
    finally:
        client.session.close()
