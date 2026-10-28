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

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
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


def refuse_option_like(rev):
    """A revision starting with "-" would be read by git as an option."""
    if rev.startswith("-"):
        raise BuildError(f"{rev!r} is not a revision")


def version_of(repo, rev):
    try:
        return debian_version(git(repo, "describe", "--tags", "--long", "--match", "v*", rev))
    except subprocess.CalledProcessError as error:
        raise BuildError(f"{rev} has no v* tag in its history to number the package from"
                         f" ({error.stderr.strip() if error.stderr else error})") from error
    except ValueError as error:
        raise BuildError(str(error)) from error


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


PACKAGE_NAME = re.compile(r"^[a-z0-9][a-z0-9+.-]+$")


def package_name(control_text):
    """The name from the commit's control; it becomes a folder in the build
    cache, so only a Debian package name is taken, never a path."""
    for line in control_text.splitlines():
        if line.startswith("Package:"):
            name = line.split(":", 1)[1].strip()
            if not PACKAGE_NAME.match(name):
                raise BuildError(f"packaging/DEBIAN/control names {name!r}, not a Debian package name")
            return name
    raise BuildError("packaging/DEBIAN/control names no Package")


def stamp_control(text, version, shlibs):
    if not shlibs:
        raise ValueError("no shared-library dependencies to stamp")
    if SHLIBS_TOKEN not in text:
        raise BuildError(f"packaging control has no {SHLIBS_TOKEN}: the libraries would be missing")
    lines = []
    for line in text.splitlines(keepends=True):
        if line.startswith("Version:"):
            line = f"Version: {version}\n"
        elif line.startswith("Depends:"):
            line = line.replace(SHLIBS_TOKEN, shlibs)
        lines.append(line)
    stamped = "".join(lines)
    if SHLIBS_TOKEN in stamped:
        raise BuildError(f"{SHLIBS_TOKEN} is left outside the Depends: line (folded?): "
                         "it would ship unexpanded")
    return stamped


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


GITLINK_MODE = "160000"


def submodule_pins(repo, commit):
    """(path, sha) of every gitlink in the commit's tree."""
    listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", commit],
                             check=True, capture_output=True, text=True).stdout
    pins = []
    for entry in filter(None, listing.split("\0")):
        meta, path = entry.split("\t", 1)
        mode, _kind, sha = meta.split()
        if mode == GITLINK_MODE:
            pins.append((path, sha))
    return pins


def is_initialised(checkout):
    """A folder without its own .git would make git fall back to the
    enclosing repository, so it is not a checkout of the submodule."""
    return (Path(checkout) / ".git").exists()


def has_commit(checkout, sha):
    return subprocess.run(["git", "-C", str(checkout), "cat-file", "-e", f"{sha}^{{commit}}"],
                          capture_output=True).returncode == 0


def is_bare(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "--is-bare-repository"],
                          check=True, capture_output=True, text=True).stdout.strip() == "true"


def _url_for_path(gitmodules_text, path):
    listing = subprocess.run(["git", "config", "--file", "/dev/stdin", "--null", "--get-regexp",
                              r"^submodule\..*\.(path|url)$"],
                             input=gitmodules_text, capture_output=True, text=True).stdout
    paths, urls = {}, {}
    for item in filter(None, listing.split("\0")):
        key, value = item.split("\n", 1)
        section, kind = key[len("submodule."):].rsplit(".", 1)
        (paths if kind == "path" else urls)[section] = value
    for section, value in paths.items():
        if value == path:
            return urls.get(section)
    return None


def sibling_repo(repo, commit, path):
    """The bare repo next to `repo` that holds the submodule at `path`: named
    by the last element of its URL in the commit's .gitmodules, minus `.git`."""
    shown = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:.gitmodules"],
                           capture_output=True, text=True)
    url = _url_for_path(shown.stdout, path) if shown.returncode == 0 else None
    if url is None:
        raise BuildError(f"{repo}: no .gitmodules entry for submodule {path} at {commit[:10]}")
    name = url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
    return Path(repo).resolve().parent / f"{name}.git"


def archive_submodule_from_forge(repo, commit, path, sha, dest):
    """A sibling that is absent leaves the submodule out with a note (the
    build may bring its own copy); one that lacks the pin is an error."""
    sibling = sibling_repo(repo, commit, path)
    if not sibling.is_dir():
        print(f"note: submodule {path} has no forge repo {sibling.name}, left out of the archive",
              file=sys.stderr)
        return
    if not has_commit(sibling, sha):
        raise BuildError(f"submodule {path}: the forge repo {sibling} lacks {sha[:10]}")
    archive(sibling, sha, dest)


def archive(repo, commit, dest):
    """The committed tree of `commit`, modes kept, into `dest`; every
    initialised submodule at its pinned commit, from its local checkout; an
    uninitialised one is skipped with a note. A bare `repo` has no checkouts:
    its submodules come from sibling bare repos; a sibling without the pinned
    commit is an error, an absent one a note. Never fetches."""
    refuse_option_like(commit)
    data = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", commit],
                          check=True, capture_output=True).stdout
    Path(dest).mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest, filter="tar")
    bare = is_bare(repo)
    for path, sha in submodule_pins(repo, commit):
        if bare:
            archive_submodule_from_forge(repo, commit, path, sha, Path(dest) / path)
            continue
        checkout = Path(repo) / path
        if not is_initialised(checkout):
            print(f"note: submodule {path} is not initialised, left out of the archive",
                  file=sys.stderr)
            continue
        if not has_commit(checkout, sha):
            raise BuildError(f"submodule {path} lacks {sha[:10]}: fetch it into {checkout}")
        archive(checkout, sha, Path(dest) / path)


def elf_files(root):
    found = []
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as handle:
                if handle.read(4) == b"\x7fELF":
                    found.append(path)
    return found


# dpkg-shlibdeps searches -l before the ld.so cache. A machine with PipeWire's
# ld.so.conf.d/pipewire-jack-*.conf (the Core, a deck host) resolves libjack.so.0
# to PipeWire's copy, which has no shlibs, and the build fails; this directory
# holds the packaged one. -l rather than LD_LIBRARY_PATH: it touches only this
# one command and leaves a caller's own LD_LIBRARY_PATH as it is.
MULTIARCH_LIB = "/usr/lib/x86_64-linux-gnu"


def shlibs_depends(stage):
    """The Depends dpkg-shlibdeps finds for the package's binaries. It wants a
    debian/control to read; a stub in a scratch folder is enough with -O."""
    binaries = elf_files(Path(stage) / "usr")
    if not binaries:
        raise BuildError(f"no ELF binary under {stage}/usr")
    with tempfile.TemporaryDirectory() as scratch:
        (Path(scratch) / "debian").mkdir()
        (Path(scratch) / "debian/control").write_text(
            "Source: a3-shlibs\n\nPackage: a3-shlibs\nArchitecture: any\n")
        out = subprocess.run(["dpkg-shlibdeps", "-O", f"-l{MULTIARCH_LIB}", *[f"-e{b}" for b in binaries]],
                             cwd=scratch, check=True, capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("shlibs:Depends="):
            return line.split("=", 1)[1].strip()
    raise BuildError("dpkg-shlibdeps named no libraries")


DEBIAN_FILES = {"control": 0o644, "postinst": 0o755, "prerm": 0o755, "postrm": 0o755}


def install_debian(src, stage):
    """packaging/DEBIAN into the stage, modes kept: the app's `packaging/stage`
    lays out the payload only, never DEBIAN/."""
    source = Path(src) / DEBIAN_DIR
    missing = [name for name in DEBIAN_FILES if not (source / name).is_file()]
    if missing:
        raise BuildError(f"{DEBIAN_DIR} lacks {', '.join(missing)}")
    target = Path(stage) / "DEBIAN"
    shutil.copytree(source, target)
    target.chmod(0o755)
    for name, mode in DEBIAN_FILES.items():
        (target / name).chmod(mode)


def pack(stage, final):
    """dpkg-deb into a temporary name beside `final`, then renamed: a package
    of that name is always whole."""
    Path(stage).chmod(0o755)
    final = Path(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    part = final.with_name(f".{final.name}.part")
    subprocess.run(["dpkg-deb", "--build", "--root-owner-group", str(stage), str(part)],
                   check=True, stdout=sys.stderr)
    os.replace(part, final)
    return final


def _log(message):
    print(message, file=sys.stderr)


def build(repo, rev=None, out=Path.home() / "a3-debs", cache=Path.home() / ".cache/a3-build",
          jobs=DEFAULT_JOBS, juce=Path.home() / "local/juce", test=False, log=_log):
    repo = Path(repo).resolve()
    if rev is not None:
        refuse_option_like(rev)
    refuse_inside(repo, out, cache)
    refuse_dirty(repo, rev)
    commit = git(repo, "rev-parse", "--verify", f"{rev or 'HEAD'}^{{commit}}").strip()
    version = version_of(repo, commit)
    name = package_name(git(repo, "show", f"{commit}:{DEBIAN_DIR}/control"))
    work = Path(cache) / name
    src, build_dir, fresh = work / "src", work / "build", work / "src.fresh"
    refuse_inside(repo, work, src, build_dir, fresh)
    log(f"package: {name} {version} from {repo} at {commit[:10]}")
    _remove(fresh)
    archive(repo, commit, fresh)
    sync_tree(fresh, src)
    _remove(fresh)
    stage_script = str(src / STAGE_SCRIPT)
    subprocess.run([stage_script, "build", str(src), str(build_dir), str(juce), str(jobs),
                    *(["--test"] if test else [])], check=True, stdout=sys.stderr)
    stage = Path(tempfile.mkdtemp(prefix="stage-", dir=work))
    try:
        refuse_inside(repo, stage)
        subprocess.run([stage_script, "files", str(src), str(build_dir), str(stage)],
                       check=True, stdout=sys.stderr)
        install_debian(src, stage)
        control = stage / "DEBIAN" / "control"
        control.write_text(stamp_control(control.read_text(), version, shlibs_depends(stage)))
        final = pack(stage, deb_path(out, name, version))
    finally:
        _remove(stage)
    log(f"package: {final}")
    return final


def lower_priority():
    os.setpriority(os.PRIO_PROCESS, 0, NICENESS)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build an app's .deb from a commit.")
    parser.add_argument("repo", type=Path)
    parser.add_argument("--rev", help="commit, tag or branch (default: HEAD, which must be clean)")
    parser.add_argument("--out", type=Path, default=Path.home() / "a3-debs")
    parser.add_argument("--cache", type=Path, default=Path.home() / ".cache/a3-build")
    parser.add_argument("--jobs", type=int, default=DEFAULT_JOBS)
    parser.add_argument("--juce", type=Path, default=Path.home() / "local/juce")
    parser.add_argument("--test", action="store_true", help="run the app's tests before packing")
    args = parser.parse_args(argv)
    os.umask(0o022)
    lower_priority()
    try:
        deb = build(args.repo, rev=args.rev, out=args.out, cache=args.cache,
                    jobs=args.jobs, juce=args.juce, test=args.test)
    except (BuildError, ValueError, subprocess.CalledProcessError) as error:
        print(f"package: {error}", file=sys.stderr)
        return 1
    print(deb)
    return 0


if __name__ == "__main__":
    sys.exit(main())
