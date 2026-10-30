"""Open a Failure issue for a failed workflow run: the stage, the Bundle, the last log lines."""

import argparse
import os
import re
import sys

from pipeline._lib.github import GitHub

LABEL = "pipeline-failure"
# A job or step cut off by its timeout concludes as cancelled, not failed.
FAILED = ("failure", "cancelled")
LOG_LINES = 30
TIMESTAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ")
ANSI = re.compile(r"\x1b\[[\d;]*m")


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
    failed = [job for job in github.run_jobs(args.run_id) if job["conclusion"] in FAILED]
    if not failed:
        print(f"report: run {args.run_id} has no failed job; no issue opened", file=sys.stderr)
        return 0
    job = failed[0]
    steps = [step for step in job["steps"] if step["conclusion"] in FAILED]
    stage = f"{job['name']} / {steps[0]['name']}" if steps else job["name"]
    try:
        log_tail = _log_tail(github.job_log(job["id"]))
    except RuntimeError as error:
        log_tail = f"The job log could not be fetched: {error}"

    bundle = args.bundle or "none"
    run_url = f"https://github.com/{github.repo}/actions/runs/{args.run_id}"
    title = f"{args.workflow} failed at {stage}"
    if args.bundle:
        title += f" for {args.bundle}"
    body = (
        f"**Stage:** {stage}\n**Bundle:** {bundle}\n**Run:** {run_url}\n\n"
        f"**Last log lines:**\n\n```text\n{log_tail}\n```\n"
    )
    url = github.open_issue(title, body, [LABEL], [args.assignee])
    print(f"report: run {args.run_id} failed at {stage}; opened {url}", file=sys.stderr)
    return 0


def _log_tail(log: str) -> str:
    """The lines up to the job's last error, without timestamps, so the post-job cleanup
    that follows a failure doesn't push the cause out of view. Each step's echo of its own
    script and env is cut to its first line, which is enough to say which step it was."""
    lines = []
    in_group = False
    for line in log.splitlines():
        line = ANSI.sub("", TIMESTAMP.sub("", line))
        if line.startswith("##[group]"):
            lines.append(line.removeprefix("##[group]"))
            in_group = True
        elif line == "##[endgroup]":
            in_group = False
        elif not in_group:
            lines.append(line)
    errors = [i for i, line in enumerate(lines) if line.startswith("##[error]")]
    if errors:
        lines = lines[: errors[-1] + 1]
    return "\n".join(lines[-LOG_LINES:])
