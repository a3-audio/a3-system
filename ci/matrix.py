#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The workflow's view of ci/lines.json.

    python3 ci/matrix.py            prints {"include": [{suite, arch, runner, image}, ...]} on one line
    python3 ci/matrix.py --suites   prints "<suite> <arch>" one per line
"""

import argparse
import json
import sys
from pathlib import Path

LINES = Path(__file__).resolve().parent / "lines.json"


def load_lines():
    return json.loads(LINES.read_text())


def matrix(lines):
    return {"include": [{"suite": suite, "arch": line["arch"], "runner": line["runner"],
                         "image": line["image"]} for suite, line in lines.items()]}


def suites(lines):
    return [f"{suite} {line['arch']}" for suite, line in lines.items()]


def main(argv=None):
    parser = argparse.ArgumentParser(description="The workflow's view of ci/lines.json.")
    parser.add_argument("--suites", action="store_true", help="print '<suite> <arch>' per line")
    args = parser.parse_args(argv)
    lines = load_lines()
    if args.suites:
        print("\n".join(suites(lines)))
    else:
        # One line: it goes into $GITHUB_OUTPUT as matrix=<json>.
        print(json.dumps(matrix(lines), separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
