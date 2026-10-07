#!/usr/bin/env python3
"""An app's Debian package, built from a commit of its repository, off every
live path.

    python3 installer/package.py <repo> [--rev REV] [--out DIR] [--cache DIR]
                                        [--jobs N] [--juce DIR] [--test]

1. `git archive` of the commit, synced into <cache>/<package>/src -- only files
   whose content changed are rewritten (see sync_tree).
2. The app's own recipe, packaging/stage in that tree, builds in
   <cache>/<package>/build and lays the package out in a fresh stage folder.
3. DEBIAN/ from packaging/DEBIAN, the version stamped (newest v* tag + commits,
   as a3-core's tools/package_version.py), the libraries from dpkg-shlibdeps.
4. dpkg-deb into <out>/<package>_<version>_amd64.deb, written under a temporary
   name and renamed, so a half-written package is never there.

Nothing is written into the repository, its build folders, or /usr: the
service never runs what a build is writing. Without --rev the working copy's
HEAD is built, and refused while tracked files differ -- the package would not
hold those edits. The process runs at nice 19: on a rig a build is load.

Used by `install` (with --rev = the pinned commit), by hand, and by a build
runner: stdlib only, no import from the rest of the installer. The last line
on stdout is the .deb's path; progress goes to stderr.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

DESCRIBE = re.compile(r"^v(\d[0-9A-Za-z.]*)-(\d+)-g[0-9a-f]+$")
DEFAULT_JOBS = 2
NICENESS = 19
STAGE_SCRIPT = Path("packaging/stage")
DEBIAN_DIR = Path("packaging/DEBIAN")
SHLIBS_TOKEN = "${shlibs:Depends}"
NEVER_WRITTEN = Path("/usr")


class BuildError(Exception):
    """The package cannot be built as asked; the message says why."""


def debian_version(describe):
    """03.0+63 from `git describe --tags --long` output like v03.0-63-g2656b74."""
    match = DESCRIBE.match(describe.strip())
    if not match:
        raise ValueError(f"not a tagged description: {describe.strip()!r}")
    tag, commits = match.groups()
    return f"{tag}+{commits}"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def version_of(repo, rev):
    return debian_version(git(repo, "describe", "--tags", "--long", "--match", "v*", rev))


def tracked_changes(repo):
    return [line for line in git(repo, "status", "--porcelain", "--untracked-files=no").splitlines()
            if line.strip()]


def refuse_dirty(repo, rev):
    """By hand (no --rev) the tree must be clean: the package is built from
    the commit, and edits that are only in the working copy would be missing."""
    if rev is not None:
        return
    changed = tracked_changes(repo)
    if changed:
        raise BuildError(f"{repo} has uncommitted changes the package would not contain "
                         f"(commit them, or name a commit with --rev):\n" + "\n".join(changed))


def _within(path, folder):
    return path == folder or folder in path.parents


def refuse_inside(repo, *paths):
    repo = Path(repo).resolve()
    for path in paths:
        resolved = Path(path).resolve()
        if _within(resolved, repo):
            raise BuildError(f"{path} is inside {repo}: a package build writes nowhere in the checkout")
        if _within(resolved, NEVER_WRITTEN):
            raise BuildError(f"{path} is under {NEVER_WRITTEN}: only apt puts files there")


def package_name(control_text):
    for line in control_text.splitlines():
        if line.startswith("Package:"):
            return line.split(":", 1)[1].strip()
    raise BuildError("packaging/DEBIAN/control names no Package")


def stamp_control(text, version, shlibs):
    if not shlibs:
        raise ValueError("no shared-library dependencies to stamp")
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("Version:"):
            line = f"Version: {version}\n"
        elif line.startswith("Depends:"):
            line = line.replace(SHLIBS_TOKEN, shlibs)
        lines.append(line)
    return "".join(lines)


def _remove(path):
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def _sync_entry(source, target):
    if source.is_symlink():
        link = os.readlink(source)
        if target.is_symlink() and os.readlink(target) == link:
            return
        _remove(target)
        target.symlink_to(link)
        return
    if target.is_symlink() or target.is_dir():
        _remove(target)
    if not target.exists() or target.read_bytes() != source.read_bytes():
        shutil.copyfile(source, target)
    mode = source.stat().st_mode & 0o7777
    if target.stat().st_mode & 0o7777 != mode:
        target.chmod(mode)


def sync_tree(fresh, kept):
    """Make `kept` hold exactly what `fresh` holds, rewriting only files whose
    content differs. git archive stamps every file with the commit's time,
    older than the last build's objects: extracted straight over the old tree,
    a changed source would look older than its object and make would skip it."""
    fresh, kept = Path(fresh), Path(kept)
    kept.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for folder, dirs, files in os.walk(fresh):
        here = Path(folder)
        for name in dirs + files:
            source = here / name
            relative = source.relative_to(fresh)
            wanted.add(relative)
            target = kept / relative
            if source.is_dir() and not source.is_symlink():
                if target.is_symlink() or (target.exists() and not target.is_dir()):
                    _remove(target)
                target.mkdir(exist_ok=True)
            else:
                _sync_entry(source, target)
    for folder, dirs, files in os.walk(kept, topdown=False):
        here = Path(folder)
        for name in files + dirs:
            path = here / name
            if path.relative_to(kept) not in wanted:
                _remove(path)


def deb_path(out, package, version):
    return Path(out) / f"{package}_{version}_amd64.deb"
