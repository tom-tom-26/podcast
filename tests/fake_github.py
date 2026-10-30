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
        self.jobs = []
        self.logs = {}  # job id -> log text
        self.issues = []
        self.pulls = {}  # number -> {"head": ref, "sha": sha, "files": [...], "messages": [...]}
        self.labels = {}  # issue or PR number -> labels added
        self.comments = {}  # issue or PR number -> comment bodies
        self.merged = {}  # PR number -> the head sha it was merged at
        self.dispatches = []  # (workflow file, inputs)

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

    def run_jobs(self, run_id):
        self.calls.append("run_jobs")
        return self.jobs

    def job_log(self, job_id):
        self.calls.append("job_log")
        if job_id not in self.logs:
            raise RuntimeError(f"GET job {job_id} log failed: HTTP Error 404: Not Found")
        return self.logs[job_id]

    def open_issue(self, title, body, labels, assignees):
        self.calls.append("open_issue")
        self.issues.append({"title": title, "body": body, "labels": labels, "assignees": assignees})
        return f"https://github.com/{self.repo}/issues/{len(self.issues)}"

    def pull_request(self, number):
        self.calls.append("pull_request")
        pull = self.pulls[number]
        return {
            "head": {"ref": pull["head"], "sha": pull["sha"]},
            "state": "closed" if number in self.merged else "open",
            "labels": [{"name": name} for name in self.labels.get(number, [])],
        }

    def remove_label(self, number, label):
        self.calls.append("remove_label")
        self.labels[number].remove(label)

    def pull_files(self, number):
        self.calls.append("pull_files")
        return self.pulls[number]["files"]

    def pull_commit_messages(self, number):
        self.calls.append("pull_commit_messages")
        return self.pulls[number]["messages"]

    def add_labels(self, number, labels):
        self.calls.append("add_labels")
        self.labels.setdefault(number, []).extend(labels)

    def comment(self, number, body):
        self.calls.append("comment")
        self.comments.setdefault(number, []).append(body)

    def squash_merge(self, number, sha):
        self.calls.append("squash_merge")
        assert sha == self.pulls[number]["sha"], "merged a head the decision never saw"
        self.merged[number] = sha

    def dispatch(self, workflow, inputs):
        self.calls.append("dispatch")
        self.dispatches.append((workflow, inputs))
