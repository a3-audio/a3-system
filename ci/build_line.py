#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build one package line's .debs from the umbrella's submodule pins.

    python3 ci/build_line.py <suite> [--repo .] [--out DIR] [--cache DIR] [--juce DIR] [--jobs N]
    python3 ci/build_line.py <suite> --build-depends

The first form prints one .deb path per line and exits 1 at the first package
that fails, naming it. The second prints the apt packages a build host needs.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GITLINK_MODE = "160000"

# Which installer role's build packages build which path.
ROLE_OF_PATH = {
    "a3-core": "core",
    "stemdeck": "stemdeck",
    "a3-mixer": "desk",
    "a3-motion/ui": "motion",
    "beat-analyzer": "core",
}
CI_TOOLS = ("git", "python3", "dpkg-dev", "build-essential", "ccache",
            "ca-certificates", "curl", "gnupg")


class BuildLineError(Exception):
    pass


def run(command):
    """Run a command, returning its stdout; its stderr stays on ours as progress."""
    done = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    if done.returncode != 0:
        raise BuildLineError(f"{' '.join(map(str, command))} exited {done.returncode}")
    return done.stdout


def load_lines():
    return json.loads((HERE / "lines.json").read_text())


def gitlink_at(containing, rev, relative, run):
    """The sha the tree of `rev` pins at `relative`, or None if it is no gitlink there."""
    listing = run(["git", "-C", str(containing), "ls-tree", rev, relative]).strip()
    if not listing:
        return None
    meta, _, _ = listing.partition("\t")
    mode, _, sha = meta.split()
    return sha if mode == GITLINK_MODE else None


def pinned_commit(repo, path, run):
    """Walk `path` through the nested submodules; each boundary is one gitlink."""
    containing, rev, parts = Path(repo), "HEAD", path.split("/")
    while parts:
        for length in range(1, len(parts) + 1):
            relative = "/".join(parts[:length])
            sha = gitlink_at(containing, rev, relative, run)
            if sha:
                containing, rev, parts = containing / relative, sha, parts[length:]
                break
        else:
            raise BuildLineError(f"{path} is nowhere a submodule pin in {repo}")
    return rev


def package_command(repo, path, rev, out, cache, juce, jobs):
    return ["python3", "-I", str(repo / "installer" / "package.py"), str(repo / path),
            "--rev", rev, "--out", str(out), "--cache", str(cache),
            "--juce", str(juce), "--jobs", str(jobs)]


def build_commands(line, repo, out, cache, juce, jobs, run=run):
    return [package_command(repo, build["path"], pinned_commit(repo, build["path"], run),
                            out, cache, juce, jobs)
            for build in line["builds"]]


def check_architecture(deb, arch, run):
    found = run(["dpkg-deb", "--field", deb, "Architecture"]).strip()
    if found not in (arch, "all"):
        raise BuildLineError(f"{deb} is {found}, this line wants {arch}")


def build_line(line, commands, run):
    debs = []
    for build, command in zip(line["builds"], commands):
        try:
            deb = run(command).strip().splitlines()[-1]
            check_architecture(deb, line["arch"], run)
        except (BuildLineError, IndexError) as error:
            raise BuildLineError(f"{build['path']} failed: {error or 'no .deb printed'}")
        debs.append(deb)
    return debs


def role_build_packages(role):
    # Today a role lists runtime and build packages together.
    return role.packages


def build_depends(line):
    sys.path.insert(0, str(HERE.parent))  # run as a script, the repo root is not on the path
    from installer import roles
    needed = set(CI_TOOLS)
    for build in line["builds"]:
        needed.update(role_build_packages(roles.BY_NAME[ROLE_OF_PATH[build["path"]]]))
    return sorted(needed)


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Build a package line from the umbrella's pins.")
    parser.add_argument("suite")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("debs"))
    parser.add_argument("--cache", type=Path, default=Path.home() / ".cache/a3-ci")
    parser.add_argument("--juce", type=Path, default=Path.home() / "local/juce")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--build-depends", action="store_true",
                        help="print the apt packages a build host needs instead of building")
    return parser.parse_args(argv)


def main(argv=None, run=run):
    args = parse_arguments(argv)
    lines = load_lines()
    if args.suite not in lines:
        print(f"build_line: unknown suite {args.suite!r}; known: {', '.join(sorted(lines))}",
              file=sys.stderr)
        return 1
    line = lines[args.suite]
    if args.build_depends:
        print("\n".join(build_depends(line)))
        return 0
    repo = args.repo.resolve()
    try:
        commands = build_commands(line, repo, args.out.resolve(), args.cache,
                                  args.juce, args.jobs, run=run)
        debs = build_line(line, commands, run)
    except BuildLineError as error:
        print(f"build_line: {error}", file=sys.stderr)
        return 1
    print("\n".join(debs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
