"""Which state of the system a machine runs: a tag of this repository.

A version is a tag, set in every repository at once (README: "A version is a
tag, and it is the same tag everywhere"), and this repository records which
commit of each submodule belongs to it. Checking out the tag here and then
the submodules brings the whole coherent set; nothing is taken from a
submodule's own newest commit.
"""

import re

TAG = re.compile(r"^v\d")


def _version_key(tag):
    """v03.10 after v03.9: numbers compare as numbers."""
    return [int(part) if part.isdigit() else part
            for part in re.split(r"(\d+)", tag)]


def tags(runner, repo):
    """The release tags, newest first."""
    listed = runner.output(["git", "tag", "--list", "v*"], cwd=repo).split()
    return sorted((t for t in listed if TAG.match(t)), key=_version_key, reverse=True)


def current(runner, repo):
    """The tag checked out, or the branch, or the commit."""
    for args in (["git", "describe", "--tags", "--exact-match", "--match", "v*"],
                 ["git", "symbolic-ref", "--short", "-q", "HEAD"],
                 ["git", "rev-parse", "--short", "HEAD"]):
        try:
            found = runner.output(args, cwd=repo).strip()
        except Exception:
            continue
        if found:
            return found
    return ""


def fetch(runner, repo):
    runner.run(["git", "fetch", "--tags", "origin"], cwd=repo)


def check_out(runner, repo, version):
    """This repository at `version` and every submodule at the commit it
    records there. A local change in a submodule stops the checkout rather
    than being overwritten: it is somebody's work."""
    runner.run(["git", "checkout", "--quiet", version], cwd=repo)
    runner.run(["git", "submodule", "sync", "--recursive"], cwd=repo)
    runner.run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo)


def submodule_commit(runner, repo, path):
    """The commit checked out at `path` inside the repository."""
    return runner.output(["git", "rev-parse", "HEAD"], cwd=repo / path).strip()
