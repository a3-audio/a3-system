#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""One apt archive for both package lines (forky/amd64, trixie/arm64).

    python3 ci/archive.py index <root> <suite> <arch> <deb>...
    python3 ci/archive.py sign <release> [--gpg-home DIR]
    python3 ci/archive.py key-matches <committed.asc> [--gpg-home DIR]

All suites share <root>/pool; each suite has its own dists/<suite>/ with its own
Packages, listing only the debs of its architecture (plus arch "all").
"""

import argparse
import gzip
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path


class ArchiveError(Exception):
    pass


def run(command, **kwargs):
    done = subprocess.run(command, capture_output=True, text=True, **kwargs)
    if done.returncode != 0:
        raise ArchiveError(f"{' '.join(map(str, command))} failed: {done.stderr.strip()}")
    return done.stdout


def deb_field(deb, field):
    return run(["dpkg-deb", "-f", str(deb), field]).strip()


def pool_directory(root, package):
    # Debian's rule: lib* packages are filed under their first four letters.
    prefix = package[:4] if package.startswith("lib") else package[:1]
    return root / "pool" / "main" / prefix / package


def check_architecture(deb, arch):
    found = deb_field(deb, "Architecture")
    if found not in (arch, "all"):
        raise ArchiveError(f"{deb.name} is {found}, this suite wants {arch}")


def copy_into_pool(root, debs, arch):
    for deb in debs:
        deb = Path(deb)
        check_architecture(deb, arch)
        folder = pool_directory(root, deb_field(deb, "Package"))
        folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(deb, folder / deb.name)


def scan_packages(root, arch):
    # Run from root so Filename is pool/main/...; --arch keeps the other
    # line's debs, which share the pool, out of this suite's index.
    return run(["dpkg-scanpackages", "--multiversion", "--arch", arch, "pool"],
               cwd=root).encode()


def write_packages(root, suite, arch):
    folder = root / "dists" / suite / "main" / f"binary-{arch}"
    folder.mkdir(parents=True, exist_ok=True)
    packages = scan_packages(root, arch)
    (folder / "Packages").write_bytes(packages)
    (folder / "Packages.gz").write_bytes(gzip.compress(packages, mtime=0))
    return {f"main/binary-{arch}/Packages": packages,
            f"main/binary-{arch}/Packages.gz": (folder / "Packages.gz").read_bytes()}


def release_text(suite, arch_list, files, date):
    lines = ["Origin: a3-audio", "Label: a3-system", f"Suite: {suite}",
             f"Codename: {suite}", f"Date: {date}",
             f"Architectures: {' '.join(arch_list)}", "Components: main",
             "SHA256:"]
    for path, content in sorted(files.items()):
        lines.append(f" {hashlib.sha256(content).hexdigest()} {len(content)} {path}")
    return "\n".join(lines) + "\n"


def index_suite(root, suite, arch, debs):
    root = Path(root)
    copy_into_pool(root, debs, arch)
    files = write_packages(root, suite, arch)
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    release = root / "dists" / suite / "Release"
    release.write_text(release_text(suite, [arch], files, date))
    return release


def gpg_command(gpg_home, *args):
    home = ["--homedir", str(gpg_home)] if gpg_home else []
    return ["gpg", "--batch", "--yes", *home, *args]


def sign(release, gpg_home=None):
    release = Path(release)
    run(gpg_command(gpg_home, "--armor", "--detach-sign",
                    "--output", str(release.parent / "Release.gpg"), str(release)))
    run(gpg_command(gpg_home, "--clearsign",
                    "--output", str(release.parent / "InRelease"), str(release)))


def primary_fingerprints(colon_listing):
    # The fpr line after each pub/sec record is the primary key's; subkeys follow.
    found, expecting = [], False
    for line in colon_listing.splitlines():
        record = line.split(":")[0]
        if record in ("pub", "sec"):
            expecting = True
        elif record == "fpr" and expecting:
            found.append(line.split(":")[9])
            expecting = False
    return found


def fingerprints(gpg_home, secret):
    listing = "--list-secret-keys" if secret else "--list-keys"
    return primary_fingerprints(
        run(gpg_command(gpg_home, "--with-colons", "--fingerprint", listing)))


def fingerprints_of_file(key_file):
    return primary_fingerprints(
        run(["gpg", "--batch", "--with-colons", "--fingerprint",
             "--import-options", "show-only", "--import", str(key_file)]))


def key_matches(gpg_home, committed):
    secret = set(fingerprints(gpg_home, secret=True))
    return bool(secret & set(fingerprints_of_file(committed)))


def command_line():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index")
    index.add_argument("root", type=Path)
    index.add_argument("suite")
    index.add_argument("arch")
    index.add_argument("debs", nargs="+", type=Path)
    for name, positional in (("sign", "release"), ("key-matches", "committed")):
        sub = commands.add_parser(name)
        sub.add_argument(positional, type=Path)
        sub.add_argument("--gpg-home", type=Path)
    return parser


def main(argv=None):
    args = command_line().parse_args(argv)
    try:
        if args.command == "index":
            print(index_suite(args.root, args.suite, args.arch, args.debs))
        elif args.command == "sign":
            sign(args.release, args.gpg_home)
        else:
            return report_key_match(args)
    except ArchiveError as error:
        print(f"archive: {error}", file=sys.stderr)
        return 1
    return 0


def report_key_match(args):
    if key_matches(args.gpg_home, args.committed):
        return 0
    print(f"signing key {', '.join(fingerprints(args.gpg_home, secret=True))} "
          f"does not match committed key "
          f"{', '.join(fingerprints_of_file(args.committed))}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
