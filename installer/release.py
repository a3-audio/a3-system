"""Which state of the system a machine runs: a tag of this repository.

A version is a tag, set in every repository at once (README: "A version is a
tag, and it is the same tag everywhere"), and this repository records which
commit of each submodule belongs to it. Checking out the tag here and then
the submodules the machine's roles need brings their part of the coherent
set; nothing is taken from a submodule's own newest commit.
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
    """This repository at `version`. Its submodules follow in
    update_submodules(), and only those the machine's roles need."""
    runner.run(["git", "checkout", "--quiet", version], cwd=repo)


def upstream(runner, repo, version):
    """origin/<version> when `version` is a branch origin has, else None:
    a tag never moves."""
    if TAG.match(version):
        return None
    ref = f"origin/{version}"
    try:
        runner.output(["git", "rev-parse", "--verify", "--quiet",
                       f"refs/remotes/{ref}"], cwd=repo)
    except Exception:
        return None
    return ref


def catch_up(runner, repo, version):
    """A branch checked out here brought to origin's newest commit, after
    fetch(). Fast-forward only: a local commit stops the update rather than
    being overwritten, as in update_submodules()."""
    ref = upstream(runner, repo, version)
    if ref:
        runner.run(["git", "merge", "--ff-only", "--quiet", ref], cwd=repo)


def update_submodules(runner, repo, paths):
    """These submodules at the commit this repository records. Run on every
    install, not only on a version change: a role added later needs its
    submodule too. A local change in a submodule stops the update rather than
    being overwritten: it is somebody's work."""
    if not paths:
        return
    runner.run(["git", "submodule", "sync", "--recursive", "--", *paths], cwd=repo)
    runner.run(["git", "submodule", "update", "--init", "--recursive", "--", *paths],
               cwd=repo)


def submodule_commit(runner, repo, path):
    """The commit checked out at `path` inside the repository."""
    return runner.output(["git", "rev-parse", "HEAD"], cwd=repo / path).strip()
