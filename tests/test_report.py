import argparse

from pipeline import report
from tests.fake_github import FakeGitHub

PUBLISH_LOG = """\
2026-11-02T18:00:01.0000000Z ##[group]Run pipeline lint "bundles/2026-11-02-tides"
2026-11-02T18:00:01.1000000Z pipeline lint "bundles/2026-11-02-tides"
2026-11-02T18:00:01.2000000Z ##[endgroup]
2026-11-02T18:00:05.0000000Z lint 2026-11-02-tides: 0 firm failures, 2 warnings
2026-11-02T18:00:06.0000000Z ##[group]Run pipeline render "bundles/2026-11-02-tides"
2026-11-02T18:00:06.1000000Z ##[endgroup]
2026-11-02T18:09:40.0000000Z render 2026-11-02-tides: chunk 41 of 212 failed: engine timed out
2026-11-02T18:09:40.1000000Z ##[error]Process completed with exit code 1.
2026-11-02T18:09:41.0000000Z Post job cleanup.
2026-11-02T18:09:41.5000000Z Cleaning up orphan processes
"""


def failed_publish_run(github, log=PUBLISH_LOG):
    github.jobs = [
        {
            "id": 101,
            "name": "publish",
            "conclusion": "failure",
            "steps": [
                {"name": "Find the Bundle", "conclusion": "success"},
                {"name": "Lint", "conclusion": "success"},
                {"name": "Render", "conclusion": "failure"},
                {"name": "Publish", "conclusion": "skipped"},
            ],
        },
        {"id": 102, "name": "report / report", "conclusion": None, "steps": []},
    ]
    github.logs = {101: log}


def test_a_failed_stage_opens_one_issue_with_the_stage_bundle_and_last_log_lines():
    github = FakeGitHub()
    failed_publish_run(github)

    assert run_report(github, "--bundle", "2026-11-02-tides") == 0

    [issue] = github.issues
    assert issue["labels"] == ["pipeline-failure"]
    assert issue["assignees"] == ["owner"]
    assert "publish-episode" in issue["title"]
    assert "publish / Render" in issue["title"]
    assert "**Stage:** publish / Render" in issue["body"]
    assert "**Bundle:** 2026-11-02-tides" in issue["body"]
    assert "chunk 41 of 212 failed: engine timed out" in issue["body"]
    assert "https://github.com/example/podcast/actions/runs/7" in issue["body"]


def test_the_log_lines_end_at_the_error_without_timestamps():
    github = FakeGitHub()
    failed_publish_run(github)

    run_report(github, "--bundle", "2026-11-02-tides")

    body = github.issues[0]["body"]
    assert "##[error]Process completed with exit code 1.\n```" in body
    assert "Cleaning up orphan processes" not in body
    assert "2026-11-02T18:09:40" not in body


def test_only_the_last_lines_before_the_error_are_kept():
    github = FakeGitHub()
    noise = "".join(f"2026-11-02T18:00:00.0000000Z line {n}\n" for n in range(100))
    failed_publish_run(github, log=noise + PUBLISH_LOG)

    run_report(github, "--bundle", "2026-11-02-tides")

    body = github.issues[0]["body"]
    assert "line 99" in body
    assert "line 50" not in body


def test_a_step_cut_off_by_its_timeout_is_named_as_the_stage():
    github = FakeGitHub()
    failed_publish_run(github)
    github.jobs[0]["steps"][2]["conclusion"] = "cancelled"

    run_report(github, "--bundle", "2026-11-02-tides")

    assert "**Stage:** publish / Render" in github.issues[0]["body"]


def test_a_log_that_cannot_be_fetched_still_opens_the_issue():
    github = FakeGitHub()
    failed_publish_run(github)
    github.logs = {}

    assert run_report(github, "--bundle", "2026-11-02-tides") == 0

    [issue] = github.issues
    assert "The job log could not be fetched" in issue["body"]
    assert "**Stage:** publish / Render" in issue["body"]


def test_a_failed_deploy_with_no_bundle_says_so():
    github = FakeGitHub()
    github.jobs = [
        {"id": 201, "name": "deploy", "conclusion": "success", "steps": []},
        {
            "id": 202,
            "name": "smoke-check",
            "conclusion": "failure",
            "steps": [{"name": "Check the live site", "conclusion": "failure"}],
        },
    ]
    github.logs = {202: "2026-11-02T18:30:00.0000000Z site check: 1 problems\n"}

    run_report(github, "--workflow", "deploy-site")

    [issue] = github.issues
    assert issue["title"] == "deploy-site failed at smoke-check / Check the live site"
    assert "**Bundle:** none" in issue["body"]
    assert "site check: 1 problems" in issue["body"]


def run_report(github, *argv):
    parser = argparse.ArgumentParser()
    report.add_arguments(parser)
    args = parser.parse_args(
        ["--run-id", "7", "--assignee", "owner", "--workflow", "publish-episode", *argv]
    )
    return report.main(args, github=github)
