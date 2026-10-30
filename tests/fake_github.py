from pathlib import Path

REPO = Path(__file__).parent.parent


class FakeGitHub:
    """Stands in for the Pipeline's GitHub client: an in-memory repo and its Releases."""

    def __init__(self, upload_loses_bytes=0):
        self.files = {"episodes.yaml": (REPO / "episodes.yaml").read_text(encoding="utf-8")}
        self.releases = {}
        self.commits = []
        self.calls = []
        self.upload_loses_bytes = upload_loses_bytes

    def read_file(self, path):
        self.calls.append("read_file")
        return self.files[path], f"sha-{len(self.commits)}"

    def commit_file(self, path, text, sha, message):
        self.calls.append("commit_file")
        assert sha == f"sha-{len(self.commits)}", "committed over a newer version of the file"
        self.files[path] = text
        self.commits.append((path, message))

    def create_release(self, tag, title, notes):
        self.calls.append("create_release")
        assert tag not in self.releases, f"Release {tag} already exists"
        self.releases[tag] = {"title": title, "notes": notes, "assets": {}}

    def upload_asset(self, tag, file):
        self.calls.append("upload_asset")
        size = file.stat().st_size - self.upload_loses_bytes
        self.releases[tag]["assets"][file.name] = size

    def asset_sizes(self, tag):
        self.calls.append("asset_sizes")
        return dict(self.releases[tag]["assets"])
