from pathlib import Path

REPO = Path(__file__).parent.parent


class FakeGitHub:
    """Stands in for the Pipeline's GitHub client: an in-memory repo and its Releases."""

    repo = "example/podcast"

    def __init__(self, upload_loses_bytes=0):
        self.files = {"episodes.yaml": (REPO / "episodes.yaml").read_text(encoding="utf-8")}
        self.releases = {}
        self.commits = []
        self.calls = []
        self.audio = {}  # (tag, file name) -> bytes, for Releases a test puts in place
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
        self.releases[tag] = {"title": title, "notes": notes, "draft": True, "assets": {}}
        return tag

    def upload_asset(self, release_id, file):
        self.calls.append("upload_asset")
        size = file.stat().st_size - self.upload_loses_bytes
        self.releases[release_id]["assets"][file.name] = size

    def asset_sizes(self, release_id):
        self.calls.append("asset_sizes")
        return dict(self.releases[release_id]["assets"])

    def publish_release(self, release_id):
        self.calls.append("publish_release")
        self.releases[release_id]["draft"] = False

    def add_published_release(self, tag, audio, published_at):
        """A Release as publish leaves it, with its audio, for site to fetch from."""
        assets = {audio.name: audio.stat().st_size}
        self.releases[tag] = {"draft": False, "assets": assets, "published_at": published_at}
        self.audio[tag, audio.name] = audio.read_bytes()

    def published_at(self, tag):
        self.calls.append("published_at")
        return self.releases[tag]["published_at"]

    def download_url(self, tag, name):
        return f"https://github.com/{self.repo}/releases/download/{tag}/{name}"

    def download_asset(self, tag, name, dest):
        self.calls.append("download_asset")
        if (tag, name) not in self.audio:
            raise RuntimeError(f"GET {self.download_url(tag, name)} failed: 404 Not Found")
        dest.write_bytes(self.audio[tag, name])
