"""GitHub API client for repository management."""

import time

import requests


class GitHubClient:
    """Handles authenticated communication with the GitHub API."""

    BASE_URL = "https://api.github.com"
    GET_MAX_ATTEMPTS = 3
    GET_RETRY_BASE_DELAY = 0.5
    GET_RETRY_MAX_DELAY = 5.0

    def __init__(self, token: str):
        if not token:
            raise ValueError("A GitHub token is required.")

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    @staticmethod
    def _retryable_get_error(error):
        if isinstance(error, requests.exceptions.Timeout):
            return True
        if not isinstance(error, requests.exceptions.HTTPError):
            return False
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
        return isinstance(status, int) and (status == 429 or status >= 500)

    @classmethod
    def _retry_delay(cls, error, attempt):
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
        if status == 429:
            headers = getattr(response, "headers", None) or {}
            retry_after = headers.get("Retry-After")
            try:
                return min(max(float(retry_after), 0), cls.GET_RETRY_MAX_DELAY)
            except (TypeError, ValueError):
                pass
        return min(cls.GET_RETRY_BASE_DELAY * (2 ** attempt), cls.GET_RETRY_MAX_DELAY)

    def _request(self, method: str, endpoint: str, **kwargs):
        """Send an authenticated request to GitHub."""
        is_get = method.upper() == "GET"
        attempts = self.GET_MAX_ATTEMPTS if is_get else 1
        for attempt in range(attempts):
            try:
                response = self.session.request(
                    method,
                    f"{self.BASE_URL}{endpoint}",
                    timeout=30,
                    **kwargs,
                )
                response.raise_for_status()
            except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as error:
                can_retry = is_get and self._retryable_get_error(error)
                if not can_retry or attempt == attempts - 1:
                    raise
                time.sleep(self._retry_delay(error, attempt))
                continue

            if response.status_code == 204 or not response.content:
                return None

            return response.json()

    def compare_upstream_diagnostic(
        self,
        fork_full_name: str,
        upstream_full_name: str,
        upstream_branch: str,
        fork_branch: str,
        *,
        request_id: str | None = None,
    ):
        """Read-only compare with captured request/response metadata (no tokens)."""
        import uuid
        from datetime import datetime, timezone

        if not isinstance(fork_full_name, str) or not fork_full_name.strip():
            raise ValueError("Fork full_name is required.")
        if not isinstance(upstream_full_name, str) or not upstream_full_name.strip():
            raise ValueError("Upstream full_name is required.")
        if not isinstance(upstream_branch, str) or not upstream_branch.strip():
            raise ValueError("Upstream branch is required.")
        if not isinstance(fork_branch, str) or not fork_branch.strip():
            raise ValueError("Fork branch is required.")

        fork_full_name = fork_full_name.strip()
        upstream_full_name = upstream_full_name.strip()
        upstream_branch = upstream_branch.strip()
        fork_branch = fork_branch.strip()

        fork_owner, fork_name = fork_full_name.split("/", 1)
        upstream_owner, _ = upstream_full_name.split("/", 1)

        basehead = f"{upstream_owner}:{upstream_branch}...{fork_owner}:{fork_branch}"
        endpoint = f"/repos/{fork_owner}/{fork_name}/compare/{basehead}"
        url = f"{self.BASE_URL}{endpoint}"
        req_id = request_id or str(uuid.uuid4())

        start_dt = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        start_perf = time.perf_counter()
        meta = {
            "request_id": req_id,
            "method": "GET",
            "endpoint": endpoint,
            "url": url,
            "basehead": basehead,
            "http_status": None,
            "start_time": start_dt,
            "end_time": None,
            "duration_ms": None,
            "attempts": 0,
            "error": None,
            "response_fields": None,
        }

        attempts = self.GET_MAX_ATTEMPTS
        comparison = None
        for attempt in range(attempts):
            meta["attempts"] = attempt + 1
            try:
                response = self.session.request("GET", url, timeout=30)
                meta["http_status"] = getattr(response, "status_code", None)
                response.raise_for_status()
            except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as error:
                response_obj = getattr(error, "response", None)
                if response_obj is not None:
                    meta["http_status"] = getattr(response_obj, "status_code", meta["http_status"])
                can_retry = self._retryable_get_error(error)
                if not can_retry or attempt == attempts - 1:
                    meta["error"] = str(error)
                    if response_obj is not None:
                        try:
                            payload = response_obj.json()
                            if isinstance(payload, dict):
                                meta["response_fields"] = {
                                    "status": payload.get("status"),
                                    "ahead_by": payload.get("ahead_by"),
                                    "behind_by": payload.get("behind_by"),
                                    "total_commits": payload.get("total_commits"),
                                    "message": payload.get("message"),
                                }
                        except Exception:
                            meta["response_fields"] = None
                    break
                time.sleep(self._retry_delay(error, attempt))
                continue

            if response.status_code == 204 or not response.content:
                comparison = None
            else:
                comparison = response.json()
            if isinstance(comparison, dict):
                meta["response_fields"] = {
                    "status": comparison.get("status"),
                    "ahead_by": comparison.get("ahead_by"),
                    "behind_by": comparison.get("behind_by"),
                    "total_commits": comparison.get("total_commits"),
                }
            else:
                meta["response_fields"] = None
            meta["error"] = None
            break

        end_dt = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        meta["end_time"] = end_dt
        meta["duration_ms"] = round((time.perf_counter() - start_perf) * 1000, 3)
        return {"comparison": comparison, "meta": meta}

    def get_authenticated_user(self):
        """Return the authenticated GitHub account."""
        return self._request("GET", "/user")

    def get_repository(self, full_name: str):
        """Return complete repository metadata, including fork parent details."""
        if not isinstance(full_name, str) or full_name.count("/") != 1:
            raise ValueError("Repository full_name must be OWNER/REPO.")
        owner, name = full_name.split("/", 1)
        if not owner or not name:
            raise ValueError("Repository full_name must be OWNER/REPO.")
        return self._request("GET", f"/repos/{owner}/{name}")

    def list_repositories(self):
        """Return all repositories owned by the authenticated account."""
        repositories = []
        page = 1

        while True:
            batch = self._request(
                "GET",
                "/user/repos",
                params={
                    "type": "owner",
                    "sort": "updated",
                    "per_page": 100,
                    "page": page,
                },
            )

            repositories.extend(batch)

            if len(batch) < 100:
                break

            page += 1

        return repositories

    def compare_upstream(
        self,
        fork_full_name: str,
        upstream_full_name: str,
        upstream_branch: str,
        fork_branch: str,
    ):
        """Compare a fork branch with its upstream branch.

        GitHub compare API expects the `basehead` form:
        "UPSTREAM_OWNER:BRANCH...FORK_OWNER:BRANCH"
        when comparing a fork against its parent repository.
        """
        if not isinstance(fork_full_name, str) or not fork_full_name.strip():
            raise ValueError("Fork full_name is required.")
        if not isinstance(upstream_full_name, str) or not upstream_full_name.strip():
            raise ValueError("Upstream full_name is required.")
        if not isinstance(upstream_branch, str) or not upstream_branch.strip():
            raise ValueError("Upstream branch is required.")
        if not isinstance(fork_branch, str) or not fork_branch.strip():
            raise ValueError("Fork branch is required.")

        fork_owner, fork_name = fork_full_name.split("/", 1)
        upstream_owner, _ = upstream_full_name.split("/", 1)

        basehead = (
            f"{upstream_owner}:{upstream_branch.strip()}..."
            f"{fork_owner}:{fork_branch.strip()}"
        )

        return self._request(
            "GET",
            f"/repos/{fork_owner}/{fork_name}/compare/{basehead}",
        )

    def merge_upstream(self, full_name: str, branch: str):
        """Merge the upstream branch into a fork."""
        owner, name = full_name.split("/", 1)

        return self._request(
            "POST",
            f"/repos/{owner}/{name}/merge-upstream",
            json={"branch": branch},
        )
