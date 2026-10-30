"""Auto-merge a Skill's claude/ branch PR when it is safe, and dispatch what the change needs."""

import argparse
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from pipeline import lint
from pipeline._lib.bundle import BUNDLE_FILES, BUNDLE_ID, load_meta
from pipeline._lib.github import GitHub
from pipeline._lib.registry import REGISTRY, load_registry
from pipeline._lib.window import PIN_LIST

LABEL = "needs-owner"

PHRASE_LIST = "config/deslop_rules.yaml"
# Data the Skill writes in a run, each cheap to undo (spec, Workflows > auto-merge).
ALWAYS_ALLOWED = {
    PIN_LIST,
    "config/listener_profile.md",
    "config/backlog.md",
    "config/lexicon.yaml",
    PHRASE_LIST,
}
# Defaults every later Episode follows, so only the owner's own instruction may change them.
OWNER_INSTRUCTED = {"config/template.yaml", "config/voices.yaml"}
# The iPhone keyboard types curly quotes.
INSTRUCTION = re.compile(r'^owner-instructed: *["“](.*\S.*)["”] *$', re.I | re.M)
BUNDLE_PATH = re.compile(
    rf"bundles/({BUNDLE_ID.pattern})/({'|'.join(map(re.escape, BUNDLE_FILES))})"
)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pr", type=int, required=True, help="the claude/ branch PR")
    parser.add_argument("--sha", required=True, help="the head commit checked out in --repo")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="a checkout of the PR's head, whose Bundles lint reads",
    )


def main(args: argparse.Namespace, github=None) -> int:
    started = time.perf_counter()
    github = github or GitHub.from_env()
    pull = github.pull_request(args.pr)
    head = pull["head"]["ref"]
    if not head.startswith("claude/"):
        print(f"merge: PR #{args.pr} is from {head}, not a claude/ branch", file=sys.stderr)
        return 1
    # Runs for one PR queue, so this one may wake to find an earlier run merged it.
    if pull["state"] != "open":
        print(f"merge: PR #{args.pr} is {pull['state']}; nothing to do", file=sys.stderr)
        return 0
    # The changed-file list is the head's as it is now, so it must be the commit lint reads.
    if pull["head"]["sha"] != args.sha:
        print(
            f"merge: PR #{args.pr} has moved on from {args.sha}; the run for its new head "
            f"decides, {time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 0

    changes = []
    for file in github.pull_files(args.pr):
        if file["status"] == "renamed":
            changes += [("removed", file["previous_filename"]), ("added", file["filename"])]
        else:
            changes.append((file["status"], file["filename"]))
    message = "\n\n".join(github.pull_commit_messages(args.pr))
    # The registry on main, since only a publish writes it and the branch may be behind.
    published = {e["bundle_id"] for e in load_registry(github.read_file(REGISTRY)[0])}
    decision = decide(changes, message, published)
    # Lint reads the branch's phrase list, so a branch that dropped a firm phrase could pass
    # the very rule its Bundle fails. Feedback mode only ever adds phrases.
    if any(path == PHRASE_LIST for _, path in changes):
        before = yaml.safe_load(github.read_file(PHRASE_LIST)[0])
        after = yaml.safe_load((args.repo / PHRASE_LIST).read_text(encoding="utf-8"))
        for key in ("block", "warn", "show_notes"):
            for phrase in before.get(key) or []:
                if phrase not in (after.get(key) or []):
                    decision.refusals.append(
                        f"{PHRASE_LIST} drops {phrase!r}; feedback only adds phrases"
                    )

    for bundle_id in decision.lint:
        checked = argparse.Namespace(
            bundle=args.repo / "bundles" / bundle_id, repo=args.repo, pron_check=False
        )
        if lint.main(checked) != 0:
            decision.refusals.append(f"{bundle_id} fails a firm lint rule")

    if decision.refusals:
        github.add_labels(args.pr, [LABEL])
        github.comment(
            args.pr,
            "Auto-merge left this for the owner:\n\n"
            + "".join(f"- {reason}\n" for reason in decision.refusals),
        )
        print(
            f"merge: PR #{args.pr} left open for the owner, {len(decision.refusals)} reasons, "
            f"in {time.perf_counter() - started:.1f} s",
            file=sys.stderr,
        )
        return 0

    # Left by an earlier push that needed the owner; this head no longer does.
    if any(label["name"] == LABEL for label in pull["labels"]):
        github.remove_label(args.pr, LABEL)
    # Pinned to the head that was decided on, so a push since then can't slip in unchecked.
    github.squash_merge(args.pr, args.sha)
    # A merge made with GITHUB_TOKEN triggers no workflow, so each is dispatched by hand.
    groups = _publish_groups(decision.publish, args.repo)
    for group in groups:
        github.dispatch("publish-episode.yml", {"bundle": group, "dry_run": "false"})
    if decision.deploy:
        github.dispatch("deploy-site.yml", {})
    dispatched = [f"publish-episode for {group}" for group in groups]
    dispatched += ["deploy-site"] if decision.deploy else []
    print(
        f"merge: PR #{args.pr} merged, {len(changes)} paths, dispatched "
        f"{', '.join(dispatched) or 'nothing'}, in {time.perf_counter() - started:.1f} s",
        file=sys.stderr,
    )
    return 0


def _publish_groups(bundle_ids: list[str], repo: Path) -> list[str]:
    """One publish-episode input per Episode: a Bundle id, or the Bundle ids of every Part of
    a topic in Part order, since Parts publish together or not at all."""
    groups: dict[str, list[tuple[int, str]]] = {}
    for bundle_id in bundle_ids:
        part = load_meta(repo / "bundles" / bundle_id).get("part")
        key = f"part {part['series_slug']}" if part else bundle_id
        groups.setdefault(key, []).append((part["n"] if part else 1, bundle_id))
    return [" ".join(bundle_id for _, bundle_id in sorted(group)) for group in groups.values()]


@dataclass
class Decision:
    refusals: list[str] = field(default_factory=list)
    lint: list[str] = field(default_factory=list)
    publish: list[str] = field(default_factory=list)
    deploy: bool = False


def decide(changes: list[tuple[str, str]], message: str, published: set[str]) -> Decision:
    """What auto-merge does with a PR, from its changed paths as (status, path) pairs, its
    commit messages and the Bundle ids already in the Episode registry."""
    decision = Decision()
    bundles = set()
    for status, path in changes:
        # A deleted Bundle file would break the next deploy, and Learnings are append-only.
        if status == "removed":
            decision.refusals.append(f"{path} is deleted, which only the owner does")
        elif found := BUNDLE_PATH.fullmatch(path):
            bundles.add(found[1])
        elif path in OWNER_INSTRUCTED:
            if not INSTRUCTION.search(message):
                decision.refusals.append(
                    f"{path} changes only on a commit marked Owner-instructed that quotes the owner"
                )
        elif path not in ALWAYS_ALLOWED and not path.startswith("learnings/"):
            decision.refusals.append(f"{path} is not on the auto-merge allow-list")
    decision.lint = sorted(bundles)
    if not decision.refusals:
        decision.publish = [b for b in decision.lint if b not in published]
        # A publish dispatches deploy-site itself once the Episode is out.
        decision.deploy = not decision.publish and any(p == PIN_LIST for _, p in changes)
    return decision
