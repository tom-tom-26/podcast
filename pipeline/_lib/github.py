"""The Pipeline's one way to reach GitHub, so the entry points can be tested with a fake."""

import base64
import json
import mimetypes
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from pipeline._lib.network import retry

API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
IDEMPOTENT = {"GET", "PATCH"}


class GitHub:
    def __init__(self, repo: str, token: str, branch: str = "main"):
        self.repo = repo
        self.branch = branch
        self._token = token

    @classmethod
    def from_env(cls) -> "GitHub":
        missing = [name for name in ("GITHUB_REPOSITORY", "GITHUB_TOKEN") if name not in os.environ]
        if missing:
            raise RuntimeError(f"GitHub client needs {' and '.join(missing)} set")
        return cls(os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_TOKEN"])

    def read_file(self, path: str) -> tuple[str, str]:
        """The file's text on the branch and the blob sha a commit over it must name."""
        query = urllib.parse.urlencode({"ref": self.branch})
        found = self._request("GET", f"{API}/repos/{self.repo}/contents/{path}?{query}")
        return base64.b64decode(found["content"]).decode("utf-8"), found["sha"]

    def commit_file(self, path: str, text: str, sha: str, message: str) -> None:
        # GitHub refuses the commit if the file has moved on from sha, so a stale write fails.
        self._request(
            "PUT",
            f"{API}/repos/{self.repo}/contents/{path}",
            {
                "message": message,
                "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
                "sha": sha,
                "branch": self.branch,
            },
        )

    def create_release(self, tag: str, title: str, notes: str) -> int:
        """A draft Release, so nothing is public until its upload checks out."""
        release = self._request(
            "POST",
            f"{API}/repos/{self.repo}/releases",
            {
                "tag_name": tag,
                "target_commitish": self.branch,
                "name": title,
                "body": notes,
                "draft": True,
            },
        )
        return release["id"]

    def upload_asset(self, release_id: int, file: Path) -> None:
        query = urllib.parse.urlencode({"name": file.name})
        url = f"{UPLOADS}/repos/{self.repo}/releases/{release_id}/assets?{query}"
        content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        self._request("POST", url, file.read_bytes(), content_type)

    def asset_sizes(self, release_id: int) -> dict[str, int]:
        # By id, because the by-tag lookup does not see drafts.
        release = self._request("GET", f"{API}/repos/{self.repo}/releases/{release_id}")
        return {asset["name"]: asset["size"] for asset in release["assets"]}

    def publish_release(self, release_id: int) -> None:
        self._request("PATCH", f"{API}/repos/{self.repo}/releases/{release_id}", {"draft": False})

    def published_at(self, tag: str) -> str:
        release = self._request("GET", f"{API}/repos/{self.repo}/releases/tags/{tag}")
        return release["published_at"]

    def download_url(self, tag: str, name: str) -> str:
        """The stable public URL of a Release asset, which redirects to a short-lived one."""
        return f"https://github.com/{self.repo}/releases/download/{tag}/{name}"

    def download_asset(self, tag: str, name: str, dest: Path) -> None:
        # No token: the public URL needs none, and it must not follow the redirect to storage.
        url = self.download_url(tag, name)

        def download():
            with urllib.request.urlopen(url, timeout=300) as response, dest.open("wb") as out:
                shutil.copyfileobj(response, out)

        try:
            retry(download, f"GET {url}")
        except OSError as error:
            raise RuntimeError(f"GET {url} failed: {error}") from None

    def run_jobs(self, run_id: str) -> list[dict]:
        query = urllib.parse.urlencode({"per_page": 100})
        url = f"{API}/repos/{self.repo}/actions/runs/{run_id}/jobs?{query}"
        return self._request("GET", url)["jobs"]

    def job_log(self, job_id: int) -> str:
        # GitHub answers with a redirect to storage that must not get the token.
        url = f"{API}/repos/{self.repo}/actions/jobs/{job_id}/logs"

        def find_log():
            request = urllib.request.Request(url)
            request.add_header("Authorization", f"Bearer {self._token}")
            try:
                _NO_REDIRECT.open(request, timeout=60)
            except urllib.error.HTTPError as error:
                if error.code == 302 and error.headers.get("Location"):
                    return error.headers["Location"]
                raise
            raise RuntimeError(f"GitHub GET {url} gave no redirect to the log")

        def read_log(location):
            with urllib.request.urlopen(location, timeout=60) as response:
                return response.read().decode("utf-8", "replace")

        try:
            location = retry(find_log, f"GET {url}")
            return retry(lambda: read_log(location), f"GET job {job_id} log")
        except OSError as error:
            raise RuntimeError(f"GET job {job_id} log failed: {error}") from None

    def open_issue(self, title: str, body: str, labels: list[str], assignees: list[str]) -> str:
        issue = self._request(
            "POST",
            f"{API}/repos/{self.repo}/issues",
            {"title": title, "body": body, "labels": labels, "assignees": assignees},
        )
        return issue["html_url"]

    def pull_request(self, number: int) -> dict:
        return self._request("GET", f"{API}/repos/{self.repo}/pulls/{number}")

    def pull_files(self, number: int) -> list[dict]:
        """Every changed file, as GitHub lists it (status, filename, previous_filename)."""
        files, page = [], 1
        while True:
            query = urllib.parse.urlencode({"per_page": 100, "page": page})
            batch = self._request("GET", f"{API}/repos/{self.repo}/pulls/{number}/files?{query}")
            files += batch
            if len(batch) < 100:
                return files
            page += 1

    def pull_commit_messages(self, number: int) -> list[str]:
        # GitHub lists at most 250 commits here, far more than a Skill branch carries.
        query = urllib.parse.urlencode({"per_page": 100})
        url = f"{API}/repos/{self.repo}/pulls/{number}/commits?{query}"
        return [commit["commit"]["message"] for commit in self._request("GET", url)]

    def add_labels(self, number: int, labels: list[str]) -> None:
        url = f"{API}/repos/{self.repo}/issues/{number}/labels"
        self._request("POST", url, {"labels": labels})

    def comment(self, number: int, body: str) -> None:
        self._request("POST", f"{API}/repos/{self.repo}/issues/{number}/comments", {"body": body})

    def squash_merge(self, number: int, sha: str) -> None:
        # GitHub refuses the merge if the head has moved on from sha.
        url = f"{API}/repos/{self.repo}/pulls/{number}/merge"
        self._request("PUT", url, {"merge_method": "squash", "sha": sha})

    def dispatch(self, workflow: str, inputs: dict[str, str]) -> None:
        url = f"{API}/repos/{self.repo}/actions/workflows/{workflow}/dispatches"
        self._request("POST", url, {"ref": self.branch, "inputs": inputs})

    def _request(self, method, url, body=None, content_type="application/json"):
        if body is not None and content_type == "application/json":
            body = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(url, data=body, method=method)
        request.add_header("Authorization", f"Bearer {self._token}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if body is not None:
            request.add_header("Content-Type", content_type)

        def send():
            with urllib.request.urlopen(request, timeout=300) as response:
                # A workflow dispatch answers 204 with no body.
                data = response.read()
                return json.loads(data) if data else None

        try:
            # A POST or a sha-guarded PUT may have landed before its answer was lost, so only
            # requests that can safely run twice are retried.
            return retry(send, f"GitHub {method} {url}") if method in IDEMPOTENT else send()
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:500]
            raise RuntimeError(f"GitHub {method} {url} failed: {error.code} {detail}") from None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


_NO_REDIRECT = urllib.request.build_opener(_NoRedirect)
