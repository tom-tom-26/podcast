"""Open a Failure issue for a failed workflow run: the stage, the Bundle, the last log lines."""

import argparse
import os
import re
import sys

from pipeline._lib.github import GitHub

LABEL = "pipeline-failure"
LOG_LINES = 30
TIMESTAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ")


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--run-id", default=os.environ.get("GITHUB_RUN_ID"), help="the failed run (GITHUB_RUN_ID)"
    )
    parser.add_argument(
        "--workflow",
        default=os.environ.get("GITHUB_WORKFLOW", "a workflow"),
        help="the failed workflow's name, for the issue title (GITHUB_WORKFLOW)",
    )
    parser.add_argument("--bundle", default="", help="the Bundle the run was for, if any")
    parser.add_argument("--assignee", required=True, help="who the issue is assigned to")


def main(args: argparse.Namespace, github=None) -> int:
    if not args.run_id:
        print("report: no run id; pass --run-id or set GITHUB_RUN_ID", file=sys.stderr)
        return 1
    github = github or GitHub.from_env()
    failed = [job for job in github.run_jobs(args.run_id) if job["conclusion"] == "failure"]
    if failed:
        job = failed[0]
        steps = [s for s in job["steps"] if s["conclusion"] in ("failure", "cancelled")]
        stage = f"{job['name']} / {steps[0]['name']}" if steps else job["name"]
        try:
            lines = _last_lines(github.job_log(job["id"]))
        except RuntimeError as error:
            lines = f"The job log could not be fetched: {error}"
    else:
        stage = "unknown: no job in the run concluded with a failure"
        lines = "No failed job to take log lines from."

    bundle = args.bundle or "none"
    run_url = f"https://github.com/{github.repo}/actions/runs/{args.run_id}"
    title = f"{args.workflow} failed at {stage}"
    if args.bundle:
        title += f" for {args.bundle}"
    body = (
        f"**Stage:** {stage}\n**Bundle:** {bundle}\n**Run:** {run_url}\n\n"
        f"**Last log lines:**\n\n```text\n{lines}\n```\n"
    )
    url = github.open_issue(title, body, [LABEL], [args.assignee])
    print(f"report: run {args.run_id} failed at {stage}; opened {url}", file=sys.stderr)
    return 0


def _last_lines(log: str) -> str:
    """The lines up to the job's last error, without timestamps, so the post-job cleanup
    that follows a failure doesn't push the cause out of view."""
    lines = [TIMESTAMP.sub("", line) for line in log.splitlines()]
    lines = [line for line in lines if line != "##[endgroup]"]
    errors = [i for i, line in enumerate(lines) if line.startswith("##[error]")]
    if errors:
        lines = lines[: errors[-1] + 1]
    return "\n".join(lines[-LOG_LINES:])
