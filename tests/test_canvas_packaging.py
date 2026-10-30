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
                          "usr/share/a3/canvas.json",
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

    def test_the_recipe_has_every_maintainer_script_the_builder_wants(self):
        from installer import package
        for name in package.DEBIAN_FILES:
            self.assertTrue((RECIPE / "DEBIAN" / name).is_file(), name)

    def test_the_shipped_support_target_is_the_maintainers_paypal(self):
        import json
        self.assertEqual({"kofi": "", "paypal": "https://www.paypal.com/paypalme/RaphaelEismann", "bitcoin": ""},
                         json.loads((RECIPE / "canvas.json").read_text()))

    def cmake_arguments(self, environment):
        """`stage build` with a stand-in cmake that writes down what it was asked."""
        bin_dir = tmpdir(self)
        record = bin_dir / "calls"
        fake = bin_dir / "cmake"
        fake.write_text(f'#!/bin/sh\necho "$@" >> "{record}"\n')
        fake.chmod(0o755)
        env = {"PATH": f"{bin_dir}:/usr/bin:/bin", **environment}
        subprocess.run([str(RECIPE / "stage"), "build", str(ROOT), str(tmpdir(self)), "/juce", "1"],
                       check=True, capture_output=True, env=env)
        return record.read_text().splitlines()[0].split()

    def test_the_package_version_reaches_cmake(self):
        self.assertIn("-DA3CANVAS_VERSION=03.0+12", self.cmake_arguments({"A3_PACKAGE_VERSION": "03.0+12"}))

    def test_without_a_package_version_cmake_falls_back_to_its_own(self):
        self.assertIn("-DA3CANVAS_VERSION=", self.cmake_arguments({}))

    def test_an_unknown_step_is_a_usage_error(self):
        result = subprocess.run([str(RECIPE / "stage"), "pack"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn("usage", result.stderr)


if __name__ == "__main__":
    unittest.main()
