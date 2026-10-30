# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The a3-canvas package's recipe (canvas/packaging): what `stage files` lays
out, and what the control file says. No build: a stand-in binary is staged."""

import configparser
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPE = ROOT / "canvas" / "packaging"


def tmpdir(case):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    return Path(tmp.name)


class CanvasPackaging(unittest.TestCase):
    def staged(self):
        build = tmpdir(self) / "build"
        binary = build / "A3Canvas_artefacts" / "Release" / "a3-canvas"
        binary.parent.mkdir(parents=True)
        binary.write_text("#!/bin/sh\n")
        stage = tmpdir(self) / "stage"
        subprocess.run([str(RECIPE / "stage"), "files", str(ROOT), str(build), str(stage)],
                       check=True, capture_output=True)
        return stage

    def test_the_package_is_the_app_and_its_menu_entry(self):
        stage = self.staged()
        files = sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file())
        self.assertEqual(["usr/bin/a3-canvas",
                          "usr/share/applications/a3-canvas.desktop",
                          "usr/share/doc/a3-canvas/copyright"], files)
        self.assertTrue((stage / "usr/bin/a3-canvas").stat().st_mode & 0o111)

    def test_the_menu_entry_starts_the_app(self):
        entry = configparser.ConfigParser(interpolation=None)
        entry.optionxform = str
        entry.read(RECIPE / "a3-canvas.desktop")
        section = entry["Desktop Entry"]
        self.assertEqual("Application", section["Type"])
        self.assertEqual("a3-canvas", section["Exec"])
        self.assertEqual("A³ Canvas", section["Name"])

    def test_the_control_names_the_package_and_its_tokens(self):
        control = (RECIPE / "DEBIAN" / "control").read_text()
        self.assertIn("Package: a3-canvas\n", control)
        self.assertIn("${shlibs:Depends}", control)
        # Not before the maintainer's yes (plan, open question 1): the installer job comes later.
        self.assertNotIn("pkexec", control)
        self.assertNotIn("polkitd", control)

    def test_an_unknown_step_is_a_usage_error(self):
        result = subprocess.run([str(RECIPE / "stage"), "pack"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn("usage", result.stderr)


if __name__ == "__main__":
    unittest.main()
