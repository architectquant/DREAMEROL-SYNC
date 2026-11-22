"""GitHub Fork discovery and upstream synchronization."""

import requests


class ForkSynchronizer:
    """Synchronize GitHub forks with their upstream repositories."""

    def __init__(self, github_client):
        self.github = github_client
        self.last_diagnostics = {
            "owned_repositories": 0,
            "fork_candidates": 0,
            "valid_forks": 0,
            "unavailable_forks": 0,
        }

    def get_forks(self):
        """Find valid forks belonging to the authenticated account."""
        repositories = self.github.list_repositories()
        if not isinstance(repositories, list):
            raise ValueError("Invalid repository list returned by GitHub.")

        owned_repositories = len(repositories)
        fork_candidates = sum(
            1 for repository in repositories
            if isinstance(repository, dict) and repository.get("fork") is True
        )
        unavailable_forks = 0
        forks = []
        for repository in repositories:
            if not isinstance(repository, dict) or repository.get("fork") is not True:
                continue

            parent = repository.get("parent")
            upstream_full_name = parent.get("full_name") if isinstance(parent, dict) else None
            upstream_branch = parent.get("default_branch") if isinstance(parent, dict) else None

            # The /user/repos listing may omit parent metadata. Fetch the
            # individual repository resource before deciding it is not a fork.
            if (
                (not isinstance(upstream_full_name, str) or not upstream_full_name.strip())
                or (not isinstance(upstream_branch, str) or not upstream_branch.strip())
            ):
                full_name = repository.get("full_name")
                get_repository = getattr(self.github, "get_repository", None)
                if isinstance(full_name, str) and callable(get_repository):
                    try:
                        details = get_repository(full_name)
                    except requests.exceptions.HTTPError as error:
                        response = getattr(error, "response", None)
                        status_code = getattr(response, "status_code", None)
                        if status_code == 404:
                            unavailable_forks += 1
                            continue
                        raise
                    if isinstance(details, dict):
                        repository = details
                        parent = repository.get("parent")
                        upstream_full_name = parent.get("full_name") if isinstance(parent, dict) else None
                        upstream_branch = parent.get("default_branch") if isinstance(parent, dict) else None

            if (
                not isinstance(upstream_full_name, str)
                or not upstream_full_name.strip()
                or not isinstance(upstream_branch, str)
                or not upstream_branch.strip()
            ):
                continue

            forks.append(repository)

        self.last_diagnostics = {
            "owned_repositories": owned_repositories,
            "fork_candidates": fork_candidates,
            "valid_forks": len(forks),
            "unavailable_forks": unavailable_forks,
        }
        return forks

    def get_last_diagnostics(self):
        """Return read-only counters from the last fork discovery."""
        return dict(self.last_diagnostics)

    def compare_fork_diagnostic(self, repo, *, request_id: str | None = None, account_login: str | None = None):
        """Read-only compare diagnostic for one discovered fork (no state changes)."""
        import uuid

        req_id = request_id or str(uuid.uuid4())
        record = {
            "request_id": req_id,
            "account_login": account_login,
            "repository_full_name": repo.get("full_name") if isinstance(repo, dict) else None,
            "repository_id": repo.get("id") if isinstance(repo, dict) else None,
            "fork": repo.get("fork") if isinstance(repo, dict) else None,
            "owner_login": (repo.get("owner") or {}).get("login") if isinstance(repo, dict) and isinstance(repo.get("owner"), dict) else None,
            "parent_full_name": None,
            "parent_id": None,
            "source_full_name": None,
            "source_id": None,
            "fork_default_branch": repo.get("default_branch") if isinstance(repo, dict) else None,
            "upstream_default_branch": None,
            "upstream_full_name_arg": None,
            "fork_full_name_arg": None,
            "fork_branch_arg": None,
            "upstream_branch_arg": None,
            "compare_endpoint": None,
            "basehead": None,
            "base": None,
            "head": None,
            "http_status": None,
            "raw_status": None,
            "ahead_by": None,
            "behind_by": None,
            "total_commits": None,
            "request_start_time": None,
            "request_end_time": None,
            "duration_ms": None,
            "origin": "fresh_api",
            "result_state": "UNVERIFIED",
            "derived_status": None,
            "message": None,
        }

        if not isinstance(repo, dict):
            record["message"] = "Invalid repository data."
            record["origin"] = "error"
            return record

        parent = repo.get("parent")
        source = repo.get("source")
        record["parent_full_name"] = parent.get("full_name") if isinstance(parent, dict) else None
        record["parent_id"] = parent.get("id") if isinstance(parent, dict) else None
        record["source_full_name"] = source.get("full_name") if isinstance(source, dict) else None
        record["source_id"] = source.get("id") if isinstance(source, dict) else None
        record["upstream_default_branch"] = parent.get("default_branch") if isinstance(parent, dict) else None

        full_name = repo.get("full_name")
        fork_branch = repo.get("default_branch")
        upstream_full_name = parent.get("full_name") if isinstance(parent, dict) else None
        upstream_branch = parent.get("default_branch") if isinstance(parent, dict) else None

        try:
            if not isinstance(full_name, str) or not full_name.strip():
                raise ValueError("Missing or invalid repository full_name.")
            full_name = full_name.strip()
            if full_name.count("/") != 1 or not all(full_name.split("/", 1)):
                raise ValueError("Invalid repository full_name.")
            if not isinstance(fork_branch, str) or not fork_branch.strip():
                raise ValueError("Missing or invalid default branch.")
            if (
                not isinstance(upstream_full_name, str)
                or not upstream_full_name.strip()
                or upstream_full_name.count("/") != 1
                or not all(upstream_full_name.strip().split("/", 1))
                or not isinstance(upstream_branch, str)
                or not upstream_branch.strip()
            ):
                raise ValueError("Missing upstream branch information.")

            record["fork_full_name_arg"] = full_name
            record["upstream_full_name_arg"] = upstream_full_name.strip()
            record["fork_branch_arg"] = fork_branch.strip()
            record["upstream_branch_arg"] = upstream_branch.strip()

            diag = self.github.compare_upstream_diagnostic(
                fork_full_name=full_name,
                upstream_full_name=upstream_full_name.strip(),
                upstream_branch=upstream_branch.strip(),
                fork_branch=fork_branch.strip(),
                request_id=req_id,
            )
            comparison = diag.get("comparison") if isinstance(diag, dict) else None
            meta = diag.get("meta") if isinstance(diag, dict) else {}
            if not isinstance(meta, dict):
                meta = {}

            basehead = meta.get("basehead")
            record["compare_endpoint"] = meta.get("endpoint")
            record["basehead"] = basehead
            if isinstance(basehead, str) and "..." in basehead:
                base, head = basehead.split("...", 1)
                record["base"] = base
                record["head"] = head
            record["http_status"] = meta.get("http_status")
            record["request_start_time"] = meta.get("start_time")
            record["request_end_time"] = meta.get("end_time")
            record["duration_ms"] = meta.get("duration_ms")
            response_fields = meta.get("response_fields") if isinstance(meta.get("response_fields"), dict) else {}

            if meta.get("error") or not isinstance(comparison, dict):
                record["origin"] = "fresh_api_error"
                record["result_state"] = "UNVERIFIED"
                record["message"] = meta.get("error") or "Invalid comparison data returned by GitHub."
                record["raw_status"] = response_fields.get("status")
                record["ahead_by"] = response_fields.get("ahead_by")
                record["behind_by"] = response_fields.get("behind_by")
                record["total_commits"] = response_fields.get("total_commits")
                return record

            ahead_by = comparison.get("ahead_by")
            behind_by = comparison.get("behind_by")
            total_commits = comparison.get("total_commits")
            raw_status = comparison.get("status")
            record["raw_status"] = raw_status
            record["ahead_by"] = ahead_by
            record["behind_by"] = behind_by
            record["total_commits"] = total_commits

            if (
                isinstance(ahead_by, bool) or not isinstance(ahead_by, int) or ahead_by < 0
                or isinstance(behind_by, bool) or not isinstance(behind_by, int) or behind_by < 0
            ):
                record["origin"] = "fresh_api_invalid"
                record["result_state"] = "UNVERIFIED"
                record["message"] = "Invalid comparison counts returned by GitHub."
                return record

            if behind_by == 0 and ahead_by == 0:
                derived_status = "up-to-date"
            elif behind_by > 0 and ahead_by == 0:
                derived_status = "behind"
            elif ahead_by > 0 and behind_by == 0:
                derived_status = "ahead"
            else:
                derived_status = "diverged"

            record["origin"] = "fresh_api"
            record["result_state"] = "VERIFIED_FRESH"
            record["derived_status"] = derived_status
            record["message"] = "Fresh compare completed."
            return record
        except Exception as error:
            record["origin"] = "error"
            record["result_state"] = "UNVERIFIED"
            record["message"] = self._github_error_details(error)
            return record

    def _compare_fork(self, repo):
        """Validate fork metadata and compare its branch with its upstream."""
        if not isinstance(repo, dict):
            raise ValueError("Invalid repository data.")

        full_name = repo.get("full_name")
        fork_branch = repo.get("default_branch")
        parent = repo.get("parent")
        upstream_full_name = parent.get("full_name") if isinstance(parent, dict) else None
        upstream_branch = parent.get("default_branch") if isinstance(parent, dict) else None

        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Missing or invalid repository full_name.")
        full_name = full_name.strip()
        if full_name.count("/") != 1 or not all(full_name.split("/", 1)):
            raise ValueError("Invalid repository full_name.")
        if not isinstance(fork_branch, str) or not fork_branch.strip():
            raise ValueError("Missing or invalid default branch.")
        if (
            not isinstance(upstream_full_name, str)
            or not upstream_full_name.strip()
            or upstream_full_name.count("/") != 1
            or not all(upstream_full_name.strip().split("/", 1))
            or not isinstance(upstream_branch, str)
            or not upstream_branch.strip()
        ):
            raise ValueError("Missing upstream branch information.")

        comparison = self.github.compare_upstream(
            fork_full_name=full_name,
            upstream_full_name=upstream_full_name.strip(),
            upstream_branch=upstream_branch.strip(),
            fork_branch=fork_branch.strip(),
        )
        if not isinstance(comparison, dict):
            raise ValueError("Invalid comparison data returned by GitHub.")

        ahead_by = comparison.get("ahead_by")
        behind_by = comparison.get("behind_by")
        if (
            isinstance(ahead_by, bool)
            or not isinstance(ahead_by, int)
            or ahead_by < 0
            or isinstance(behind_by, bool)
            or not isinstance(behind_by, int)
            or behind_by < 0
        ):
            raise ValueError("Invalid comparison counts returned by GitHub.")

        return full_name, fork_branch.strip(), upstream_branch.strip(), ahead_by, behind_by

    @staticmethod
    def _github_error_details(error):
        response = getattr(error, "response", None)
        if response is None:
            return str(error)
        status = getattr(response, "status_code", None)
        detail = None
        try:
            payload = response.json()
            if isinstance(payload, dict):
                message = payload.get("message")
                doc = payload.get("documentation_url")
                errors = payload.get("errors")
                parts = []
                if isinstance(message, str) and message.strip():
                    parts.append(message.strip())
                if isinstance(errors, list) and errors:
                    parts.append(f"errors={errors}")
                if isinstance(doc, str) and doc.strip():
                    parts.append(f"docs={doc.strip()}")
                if parts:
                    detail = "; ".join(parts)
        except Exception:
            detail = None
        if detail:
            return f"HTTP {status}: {detail}" if status is not None else detail
        text = getattr(response, "text", "")
        if isinstance(text, str) and text.strip():
            snippet = text.strip().replace("\n", " ")[:300]
            return f"HTTP {status}: {snippet}" if status is not None else snippet
        return str(error)

    @staticmethod
    def _error_result(repo, error):
        full_name = (
            repo.get("full_name", "unknown")
            if isinstance(repo, dict)
            else "unknown"
        )
        return {
            "repository": full_name,
            "status": "error",
            "message": ForkSynchronizer._github_error_details(error),
        }

    @staticmethod
    def _ambiguous_result(repo, reason, error):
        full_name = (
            repo.get("full_name", "unknown")
            if isinstance(repo, dict)
            else "unknown"
        )
        details = ForkSynchronizer._github_error_details(error)
        return {
            "repository": full_name,
            "status": "ambiguous",
            "message": (
                f"Merge outcome is ambiguous: {reason}. {details} "
                "Preview again before retrying; no automatic retry was attempted."
            ),
        }

    def preview_fork(self, repo):
        """Read-only status check for one fork; no synchronization request is sent."""
        try:
            full_name, _, _, ahead_by, behind_by = self._compare_fork(repo)
            if behind_by == 0 and ahead_by == 0:
                return {
                    "repository": full_name,
                    "status": "up-to-date",
                    "message": "No changes.",
                    "behind_by": 0,
                    "ahead_by": 0,
                }
            if behind_by > 0 and ahead_by == 0:
                return {
                    "repository": full_name,
                    "status": "behind",
                    "message": f"{behind_by} upstream commit(s) available.",
                    "behind_by": behind_by,
                    "ahead_by": ahead_by,
                }
            if ahead_by > 0 and behind_by == 0:
                return {
                    "repository": full_name,
                    "status": "ahead",
                    "message": "Fork has local commits and is not safe to merge.",
                    "behind_by": behind_by,
                    "ahead_by": ahead_by,
                }
            return {
                "repository": full_name,
                "status": "diverged",
                "message": "Fork and upstream have diverged; no automatic sync.",
                "behind_by": behind_by,
                "ahead_by": ahead_by,
            }
        except (
            requests.exceptions.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            return self._error_result(repo, error)

    def preview_all(self, forks=None):
        """Discover and compare forks without changing any repository."""
        try:
            selected_forks = forks if forks is not None else self.get_forks()
        except (
            requests.exceptions.RequestException,
            ValueError,
            TypeError,
        ) as error:
            return [{
                "repository": "account",
                "status": "error",
                "message": str(error),
            }]

        return [self.preview_fork(repository) for repository in selected_forks]

    def sync_fork(self, repo):
        """Sync a fork only when its default branch is behind upstream and safe to update."""
        try:
            full_name, fork_branch, upstream_branch, ahead_by, behind_by = self._compare_fork(repo)
            if behind_by == 0 and ahead_by == 0:
                return {
                    "repository": full_name,
                    "status": "up-to-date",
                    "message": "No changes.",
                    "behind_by": 0,
                    "ahead_by": 0,
                }
            if ahead_by > 0 and behind_by == 0:
                return {
                    "repository": full_name,
                    "status": "ahead",
                    "message": "Fork has local commits and is not safe to merge.",
                    "behind_by": behind_by,
                    "ahead_by": ahead_by,
                }
            if behind_by > 0 and ahead_by > 0:
                return {
                    "repository": full_name,
                    "status": "diverged",
                    "message": "Fork and upstream have diverged; no automatic sync.",
                    "behind_by": behind_by,
                    "ahead_by": ahead_by,
                }
            if behind_by <= 0:
                return {
                    "repository": full_name,
                    "status": "up-to-date",
                    "message": "No synchronized refresh required.",
                    "behind_by": behind_by,
                    "ahead_by": ahead_by,
                }

            try:
                self.github.merge_upstream(full_name, fork_branch)
            except requests.exceptions.Timeout as error:
                return self._ambiguous_result(
                    repo, "the merge-upstream request timed out", error
                )
            except requests.exceptions.HTTPError as error:
                response = getattr(error, "response", None)
                status_code = getattr(response, "status_code", None)
                if isinstance(status_code, int) and status_code >= 500:
                    return self._ambiguous_result(
                        repo, f"GitHub returned HTTP {status_code}", error
                    )
                raise
            return {
                "repository": full_name,
                "status": "synced",
                "message": f"Synced {behind_by} upstream commits.",
                "behind_by": behind_by,
                "ahead_by": ahead_by,
            }
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            full_name = repo.get("full_name", "unknown") if isinstance(repo, dict) else "unknown"
            return {
                "repository": full_name,
                "status": "conflict" if status_code == 409 else "error",
                "message": self._github_error_details(error),
            }
        except (
            requests.exceptions.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ) as error:
            return self._error_result(repo, error)

    def sync_all(self, forks=None, dry_run=False):
        """Process each fork independently so one failure cannot stop others."""
        try:
            selected_forks = forks if forks is not None else self.get_forks()
        except (
            requests.exceptions.RequestException,
            ValueError,
            TypeError,
        ) as error:
            return [{
                "repository": "account",
                "status": "error",
                "message": str(error),
            }]

        if dry_run:
            return [
                {
                    "repository": repo.get("full_name", "unknown"),
                    "status": "dry-run",
                    "message": "Would synchronize fork with upstream.",
                }
                for repo in selected_forks
                if isinstance(repo, dict)
            ]

        results = []
        for repository in selected_forks:
            try:
                results.append(self.sync_fork(repository))
            except Exception as error:
                results.append(self._error_result(repository, error))
        return results
