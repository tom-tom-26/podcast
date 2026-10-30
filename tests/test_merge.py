import argparse
import shutil
from pathlib import Path

import pytest
import yaml

from pipeline import merge
from pipeline.merge import decide
from tests.fake_github import FakeGitHub

REPO = Path(__file__).parent.parent

TIDES = "bundles/2026-11-02-tides"


def new_bundle(path=TIDES):
    return [("added", f"{path}/{file}") for file in ("script.md", "meta.yaml", "show_notes.md")]


def test_a_new_bundle_merges_and_dispatches_publish_episode():
    decision = decide(new_bundle(), "Add the tides Bundle", published=set())

    assert decision.refusals == []
    assert decision.lint == ["2026-11-02-tides"]
    assert decision.publish == ["2026-11-02-tides"]
    assert decision.deploy is False


def test_a_change_to_pipeline_code_needs_the_owner():
    decision = decide(
        new_bundle() + [("modified", "pipeline/render.py")], "Add tides", published=set()
    )

    assert decision.refusals == ["pipeline/render.py is not on the auto-merge allow-list"]
    assert decision.publish == []


@pytest.mark.parametrize(
    "path",
    [
        "learnings/general.md",
        "learnings/fields/sleep.md",
        "pinned.txt",
        "config/listener_profile.md",
        "config/backlog.md",
        "config/lexicon.yaml",
        "config/deslop_rules.yaml",
    ],
)
def test_data_the_skill_writes_merges_without_the_owner(path):
    decision = decide([("modified", path)], "Log feedback on Episode 7", published=set())

    assert decision.refusals == []


@pytest.mark.parametrize(
    "path", [f"{TIDES}/tides.m4a", f"{TIDES}/notes/extra.md", "bundles/tides/script.md"]
)
def test_a_file_that_is_not_part_of_a_bundle_needs_the_owner(path):
    decision = decide(new_bundle() + [("added", path)], "Add tides", published=set())

    assert decision.refusals == [f"{path} is not on the auto-merge allow-list"]


def test_deleting_a_file_needs_the_owner():
    decision = decide([("removed", f"{TIDES}/show_notes.md")], "Tidy up", published=set())

    assert decision.refusals == [f"{TIDES}/show_notes.md is deleted, which only the owner does"]


INSTRUCTED = (
    'Shorten the typical Standard Episode to 22 minutes\n\nOwner-instructed: "make them shorter"\n'
)


@pytest.mark.parametrize("path", ["config/template.yaml", "config/voices.yaml"])
def test_tunables_and_the_voice_roster_merge_on_an_owner_instructed_commit(path):
    decision = decide([("modified", path)], INSTRUCTED, published=set())

    assert decision.refusals == []


@pytest.mark.parametrize(
    "message",
    [
        "Shorten the typical Standard Episode to 22 minutes",
        # Marked, but with nothing of the owner's quoted.
        'Shorten Standard Episodes\n\nOwner-instructed: ""\n',
        "Shorten Standard Episodes\n\nOwner-instructed: make them shorter\n",
        # The marker inside the body text is not a trailer line.
        'The owner never wrote Owner-instructed: "make them shorter" here\n',
    ],
)
def test_tunables_need_the_owner_without_a_quoted_instruction(message):
    decision = decide([("modified", "config/template.yaml")], message, published=set())

    assert decision.refusals == [
        "config/template.yaml changes only on a commit marked Owner-instructed that quotes "
        "the owner"
    ]


def test_an_instruction_quoted_on_an_iphone_counts():
    message = "Slow bm_lewis down\n\nOwner-instructed: “slower please”\n"

    decision = decide([("modified", "config/voices.yaml")], message, published=set())

    assert decision.refusals == []


def test_a_pin_list_change_dispatches_deploy_site():
    decision = decide([("modified", "pinned.txt")], "Bring back Episode 3", published=set())

    assert decision.publish == []
    assert decision.deploy is True


def test_a_new_bundle_with_a_pin_list_change_only_publishes():
    # publish-episode dispatches deploy-site itself once the Episode is out.
    changes = new_bundle() + [("modified", "pinned.txt")]

    decision = decide(changes, "Add tides", published=set())

    assert decision.publish == ["2026-11-02-tides"]
    assert decision.deploy is False


def test_an_edit_to_a_published_bundle_is_linted_but_publishes_nothing():
    decision = decide(
        [("modified", f"{TIDES}/ledger.md")], "Fix a ledger tier", published={"2026-11-02-tides"}
    )

    assert decision.lint == ["2026-11-02-tides"]
    assert decision.publish == []
    assert decision.deploy is False


def test_learnings_alone_dispatch_nothing():
    decision = decide([("added", "learnings/general.md")], "Learn", published=set())

    assert decision == decide([], "", published=set())
    assert decision.publish == [] and decision.deploy is False


def test_a_refused_change_dispatches_nothing():
    changes = [("modified", "pinned.txt"), ("modified", ".github/workflows/ci.yml")]

    decision = decide(changes, "Pin and tweak", published=set())

    assert decision.refusals
    assert decision.deploy is False


@pytest.fixture
def branch(tmp_path, smoke_bundle):
    """A checkout of a claude/ branch that adds the tides Bundle."""
    root = tmp_path / "branch"
    shutil.copytree(REPO / "config", root / "config")
    shutil.copy(REPO / "episodes.yaml", root / "episodes.yaml")
    shutil.copytree(smoke_bundle, root / TIDES)
    return root


def tides_pr(github, files=None, messages=("Add the tides Bundle",), head="claude/tides"):
    files = files or [
        {"status": "added", "filename": f"{TIDES}/{file}"}
        for file in ("script.md", "meta.yaml", "show_notes.md", "ledger.md", "lint_report.yaml")
    ]
    github.pulls[12] = {"head": head, "sha": "abc123", "files": files, "messages": list(messages)}


def run_merge(github, branch, sha="abc123"):
    return merge.main(argparse.Namespace(pr=12, sha=sha, repo=branch), github=github)


def test_a_push_after_the_checkout_leaves_the_decision_to_the_newer_run(branch):
    github = FakeGitHub()
    tides_pr(github)

    assert run_merge(github, branch, sha="older0") == 0

    assert github.merged == {} and github.labels == {} and github.dispatches == []


def test_a_safe_pr_is_squash_merged_and_its_bundle_published(branch):
    github = FakeGitHub()
    tides_pr(github)

    assert run_merge(github, branch) == 0

    assert github.merged == {12: "abc123"}
    assert github.dispatches == [
        ("publish-episode.yml", {"bundle": "2026-11-02-tides", "dry_run": "false"})
    ]
    assert github.labels == {} and github.comments == {}


def test_a_disallowed_path_leaves_the_pr_open_for_the_owner_with_the_reason(branch):
    github = FakeGitHub()
    files = [{"status": "modified", "filename": "pipeline/lint.py"}]
    tides_pr(github, files)

    assert run_merge(github, branch) == 0

    assert github.merged == {}
    assert github.dispatches == []
    assert github.labels == {12: ["needs-owner"]}
    [comment] = github.comments[12]
    assert "pipeline/lint.py is not on the auto-merge allow-list" in comment


def test_a_firm_lint_failure_leaves_the_pr_open_for_the_owner(branch):
    script = branch / TIDES / "script.md"
    script.write_text(
        script.read_text(encoding="utf-8") + "\nWithout further ado, the tides.\n",
        encoding="utf-8",
    )
    github = FakeGitHub()
    tides_pr(github)

    assert run_merge(github, branch) == 0

    assert github.merged == {}
    assert github.labels == {12: ["needs-owner"]}
    assert "2026-11-02-tides fails a firm lint rule" in github.comments[12][0]


def test_a_bundle_already_in_the_registry_on_main_is_not_published_again(branch):
    github = FakeGitHub()
    github.files["episodes.yaml"] = yaml.safe_dump(
        {
            "episodes": [
                {"number": "2", "episode_id": "ep-002-tides", "bundle_id": "2026-11-02-tides"}
            ]
        }
    )
    tides_pr(github, [{"status": "modified", "filename": f"{TIDES}/ledger.md"}])

    assert run_merge(github, branch) == 0

    assert github.merged == {12: "abc123"}
    assert github.dispatches == []


def test_a_pin_list_change_redeploys_the_site(branch):
    github = FakeGitHub()
    tides_pr(github, [{"status": "modified", "filename": "pinned.txt"}])

    assert run_merge(github, branch) == 0

    assert github.dispatches == [("deploy-site.yml", {})]


def test_a_renamed_bundle_file_counts_as_deleting_the_old_path(branch):
    github = FakeGitHub()
    renamed = {
        "status": "renamed",
        "filename": f"{TIDES}/show_notes.md",
        "previous_filename": f"{TIDES}/notes.md",
    }
    tides_pr(github, [renamed])

    run_merge(github, branch)

    assert f"{TIDES}/notes.md is deleted" in github.comments[12][0]


def test_an_owner_instructed_trailer_in_any_commit_of_the_branch_counts(branch):
    github = FakeGitHub()
    tides_pr(
        github,
        [{"status": "modified", "filename": "config/voices.yaml"}],
        messages=["Log feedback on Episode 7", 'Slow bm_lewis\n\nOwner-instructed: "slower"'],
    )

    run_merge(github, branch)

    assert github.merged == {12: "abc123"}


def test_a_branch_outside_claude_is_left_alone(branch):
    github = FakeGitHub()
    tides_pr(github, head="feature/tides")

    assert run_merge(github, branch) == 1

    assert github.merged == {} and github.labels == {}


def phrase_list_pr(github, branch, block):
    """A PR whose phrase list keeps only these firm phrases, against main's full list."""
    rules = REPO / "config" / "deslop_rules.yaml"
    github.files["config/deslop_rules.yaml"] = rules.read_text(encoding="utf-8")
    phrases = yaml.safe_load(rules.read_text(encoding="utf-8"))
    phrases["block"] = block
    (branch / "config" / "deslop_rules.yaml").write_text(yaml.safe_dump(phrases), encoding="utf-8")
    tides_pr(github, [{"status": "modified", "filename": "config/deslop_rules.yaml"}])
    return phrases


def test_a_phrase_list_that_drops_a_firm_phrase_needs_the_owner(branch):
    # Otherwise a branch could lift the very rule its own Bundle fails.
    github = FakeGitHub()
    main_block = yaml.safe_load(
        (REPO / "config" / "deslop_rules.yaml").read_text(encoding="utf-8")
    )["block"]
    phrase_list_pr(github, branch, [p for p in main_block if p != "without further ado"])

    run_merge(github, branch)

    assert github.merged == {}
    assert (
        "config/deslop_rules.yaml drops 'without further ado'; feedback only adds phrases"
        in github.comments[12][0]
    )


def test_a_phrase_list_that_only_adds_merges(branch):
    github = FakeGitHub()
    main_block = yaml.safe_load(
        (REPO / "config" / "deslop_rules.yaml").read_text(encoding="utf-8")
    )["block"]
    phrase_list_pr(github, branch, main_block + ["at the end of the day"])

    run_merge(github, branch)

    assert github.merged == {12: "abc123"}


def test_a_pr_that_now_passes_loses_its_needs_owner_label(branch):
    github = FakeGitHub()
    tides_pr(github)
    github.labels[12] = ["needs-owner"]

    run_merge(github, branch)

    assert github.merged == {12: "abc123"}
    assert github.labels[12] == []


def test_a_run_queued_behind_the_merge_does_nothing(branch):
    github = FakeGitHub()
    tides_pr(github)
    run_merge(github, branch)
    github.dispatches.clear()

    assert run_merge(github, branch) == 0

    assert github.dispatches == [] and github.comments == {}
