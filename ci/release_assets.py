#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The built .debs of every line as GitHub release assets, plus SHA256SUMS.

    python3 ci/release_assets.py <downloaded> <out>

<downloaded> is download-artifact's layout: one debs-<suite>/ folder per line.
Each .deb keeps its Debian file name (package, version, arch). A name that two
lines both build -- an arch "all" package -- gets its suite before the arch,
a3-mixer_<version>_forky_all.deb, because a release holds one asset per name
and the two are built against different Debians.
"""

import argparse
import hashlib
import shutil
import sys
from collections import Counter
from pathlib import Path

LINE_PREFIX = "debs-"


class AssetError(Exception):
    pass


def with_suite(name, suite):
    stem, separator, arch = name.rpartition("_")
    if not separator or not name.endswith(".deb"):
        raise AssetError(f"{name} is not <package>_<version>_<arch>.deb")
    return f"{stem}_{suite}_{arch}"


def asset_names(debs):
    """{path: asset name} for (suite, path) pairs."""
    counts = Counter(path.name for _, path in debs)
    return {path: with_suite(path.name, suite) if counts[path.name] > 1 else path.name
            for suite, path in debs}


def downloaded_debs(root):
    debs = []
    for folder in sorted(root.iterdir()):
        if not folder.name.startswith(LINE_PREFIX):
            raise AssetError(f"{folder} is no {LINE_PREFIX}<suite> folder")
        suite = folder.name[len(LINE_PREFIX):]
        debs += [(suite, deb) for deb in sorted(folder.glob("*.deb"))]
    if not debs:
        raise AssetError(f"no .deb under {root}")
    return debs


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_assets(debs, out):
    out.mkdir(parents=True, exist_ok=True)
    names = asset_names(debs)
    for path, name in names.items():
        shutil.copyfile(path, out / name)
    sums = [f"{sha256(out / name)}  {name}" for name in sorted(names.values())]
    (out / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    return sorted(names.values())


def main(argv=None):
    parser = argparse.ArgumentParser(description="The built .debs as release assets.")
    parser.add_argument("downloaded", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args(argv)
    try:
        names = write_assets(downloaded_debs(args.downloaded), args.out)
    except AssetError as error:
        print(f"release_assets: {error}", file=sys.stderr)
        return 1
    print("\n".join(names + ["SHA256SUMS"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
