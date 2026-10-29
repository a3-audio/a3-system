# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""ci/matrix.py: the workflow's build matrix comes from ci/lines.json.

Run with:  python3 -m unittest discover -s tests
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "ci" / "matrix.py"
LINES = json.loads((REPO / "ci" / "lines.json").read_text())


def run_matrix(*args):
    return subprocess.run([sys.executable, "-I", str(MATRIX), *args],
                          capture_output=True, text=True, check=True).stdout


class Matrix(unittest.TestCase):
    def test_each_line_is_one_include_entry_with_its_runner_and_image(self):
        matrix = json.loads(run_matrix())
        expected = [{"suite": suite, "arch": line["arch"], "runner": line["runner"],
                     "image": line["image"]} for suite, line in LINES.items()]
        self.assertEqual(matrix, {"include": expected})

    def test_the_matrix_is_one_line_for_github_output(self):
        self.assertEqual(len(run_matrix().strip().splitlines()), 1)

    def test_suites_lists_suite_and_arch_one_per_line(self):
        rows = [row.split() for row in run_matrix("--suites").splitlines()]
        self.assertEqual(rows, [[suite, line["arch"]] for suite, line in LINES.items()])


if __name__ == "__main__":
    unittest.main()
