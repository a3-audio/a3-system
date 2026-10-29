#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install every package of one line's apt archive into a clean root.

    python3 ci/install_test.py <archive-root> <suite>              (CI: root, in a container)
    python3 ci/install_test.py <archive-root> <suite> --simulate   (local: no root, nothing installed)

Prints "<N> packages resolve" and exits 0, or names what could not be installed.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from installer.roles.core import preseed_lines  # noqa: E402
from installer.settings import Settings  # noqa: E402

DEBIAN_KEYRING = Path("/usr/share/keyrings/debian-archive-keyring.gpg")
CI_SOURCES = Path("/etc/apt/sources.list.d/a3-ci.list")
CI_USER = "aaa"
UNMET = re.compile(r"Depends: .*|Unable to locate package .*|E: .*")


class InstallTestError(Exception):
    pass


def run_command(command, input=None):
    # Noninteractive so no postinst can wait for a terminal that is not there.
    env = {**os.environ, "DEBIAN_FRONTEND": "noninteractive"}
    return subprocess.run(command, input=input, capture_output=True, text=True, env=env)


def read_index(root, suite):
    """(arch, package names) of the one Packages file under dists/<suite>."""
    found = sorted(Path(root).glob(f"dists/{suite}/main/binary-*/Packages"))
    if len(found) != 1:
        raise InstallTestError(f"{root}/dists/{suite} has {len(found)} Packages files, wanted 1")
    arch = found[0].parent.name.removeprefix("binary-")
    names = re.findall(r"^Package: (.+)$", found[0].read_text(), re.MULTILINE)
    return arch, list(dict.fromkeys(names))


OUTPUT_TAIL_LINES = 40


def explain(command, done):
    """Why a command failed: apt's unmet-dependency lines first, then the end
    of the output, where a failing postinst says what it could not do."""
    lines = (done.stderr + done.stdout).splitlines()
    reasons = [line.strip() for line in lines if UNMET.search(line)]
    tail = [line.rstrip() for line in lines[-OUTPUT_TAIL_LINES:]]
    return "\n".join([f"{' '.join(command)} failed:", *reasons, *tail])


def checked(runner, command, input=None):
    done = runner(command, input=input)
    if done.returncode != 0:
        raise InstallTestError(explain(command, done))
    return done


def ensure_user(runner):
    # a3-core's postinst writes to this user's home.
    if runner(["id", CI_USER]).returncode != 0:
        checked(runner, ["useradd", "-m", CI_USER])


def core_preseed():
    # replace=[] answers a3-core's replace-config with "nothing": a clean root has no config to keep.
    settings = Settings(Path("/nonexistent/install.conf"))
    return preseed_lines(settings, [])


def archive_source_line(root, suite):
    return f"deb [trusted=yes] file:{root} {suite} main"


def install_in_clean_root(root, suite, runner, sources_file=CI_SOURCES):
    _, names = read_index(root, suite)
    sources_file.write_text(archive_source_line(root, suite) + "\n")
    ensure_user(runner)
    checked(runner, ["debconf-set-selections"], input=core_preseed())
    checked(runner, ["apt-get", "update"])
    checked(runner, ["apt-get", "install", "-y", *names])
    for name in names:
        checked(runner, ["dpkg", "-s", name])
    return len(names)


def private_apt_options(work, arch, keyring):
    options = {
        "Dir::State": work / "state",
        "Dir::Cache": work / "cache",
        "Dir::State::status": work / "status",
        "Dir::Etc::sourcelist": work / "sources.list",
        "Dir::Etc::sourceparts": work / "sources.list.d",
        "Dir::Etc::trustedparts": work / "trusted.gpg.d",
        "APT::Architecture": arch,
    }
    if keyring:
        options["Dir::Etc::trusted"] = keyring
    return [part for key, value in options.items() for part in ("-o", f"{key}={value}")]


def prepare_private_apt(work, root, suite, keyring):
    for folder in ("state/lists/partial", "cache/archives/partial",
                   "sources.list.d", "trusted.gpg.d"):
        (work / folder).mkdir(parents=True, exist_ok=True)
    (work / "status").write_text("")
    (work / "sources.list").write_text(
        f"deb http://deb.debian.org/debian {suite} main\n"
        f"{archive_source_line(root, suite)}\n")


def simulate_install(root, suite, runner, work, keyring=DEBIAN_KEYRING):
    arch, names = read_index(root, suite)
    work = Path(work)
    keyring = keyring if Path(keyring).exists() else None
    prepare_private_apt(work, root, suite, keyring)
    apt = ["apt-get", *private_apt_options(work, arch, keyring)]
    checked(runner, [*apt, "update"])
    checked(runner, [*apt, "-s", "install", *names])
    return len(names)


def command_line():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", type=Path)
    parser.add_argument("suite")
    parser.add_argument("--simulate", action="store_true")
    return parser


def main(argv=None):
    args = command_line().parse_args(argv)
    try:
        if args.simulate:
            with tempfile.TemporaryDirectory() as work:
                count = simulate_install(args.root.resolve(), args.suite, run_command, work)
        else:
            count = install_in_clean_root(args.root.resolve(), args.suite, run_command)
    except InstallTestError as error:
        print(f"install_test: {error}", file=sys.stderr)
        return 1
    print(f"{count} packages resolve" if args.simulate else f"{count} packages installed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
