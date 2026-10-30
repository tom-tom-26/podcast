"""The Pipeline's one way to reach GitHub, so the entry points can be tested with a fake."""

import base64
import json
import mimetypes
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"


class GitHub:
    def __init__(self, repo: str, token: str, branch: str = "main"):
        self.repo = repo
        self.branch = branch
        self._token = token
        self._release_ids: dict[str, int] = {}

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

    def create_release(self, tag: str, title: str, notes: str) -> None:
        release = self._request(
            "POST",
            f"{API}/repos/{self.repo}/releases",
            {"tag_name": tag, "target_commitish": self.branch, "name": title, "body": notes},
        )
        self._release_ids[tag] = release["id"]

    def upload_asset(self, tag: str, file: Path) -> None:
        query = urllib.parse.urlencode({"name": file.name})
        url = f"{UPLOADS}/repos/{self.repo}/releases/{self._release_ids[tag]}/assets?{query}"
        content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        self._request("POST", url, file.read_bytes(), content_type)

    def asset_sizes(self, tag: str) -> dict[str, int]:
        """Each asset's byte size as GitHub reports it, by file name."""
        release = self._request("GET", f"{API}/repos/{self.repo}/releases/tags/{tag}")
        return {asset["name"]: asset["size"] for asset in release["assets"]}

    def _request(self, method, url, body=None, content_type="application/json"):
        if body is not None and content_type == "application/json":
            body = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(url, data=body, method=method)
        request.add_header("Authorization", f"Bearer {self._token}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if body is not None:
            request.add_header("Content-Type", content_type)
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:500]
            raise RuntimeError(f"GitHub {method} {url} failed: {error.code} {detail}") from None
