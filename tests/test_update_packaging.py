# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The a3-update package's recipe (update/packaging): what `stage files` lays
out, its modes, the control and the unit. No dpkg-deb: the stage is checked."""

import configparser
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from installer import package  # noqa: E402

RECIPE = ROOT / "update" / "packaging"
UNIT = ROOT / "update" / "a3-update.service"


def tmpdir(case):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    return Path(tmp.name)


def mode(path):
    return stat.S_IMODE(path.stat().st_mode)


class UpdatePackaging(unittest.TestCase):
    def staged(self):
        stage = tmpdir(self) / "stage"
        subprocess.run([str(RECIPE / "stage"), "files", str(ROOT), str(tmpdir(self)), str(stage)],
                       check=True, capture_output=True)
        return stage

    def test_the_package_is_the_helper_the_service_and_its_unit(self):
        stage = self.staged()
        files = sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file())
        self.assertEqual(["usr/lib/a3-update/a3-root",
                          "usr/lib/a3-update/a3-update",
                          "usr/lib/systemd/user/a3-update.service",
                          "usr/share/doc/a3-update/copyright"], files)

    def test_a3_root_is_the_installers_byte_for_byte(self):
        """One source file: the sudoers line names this copy."""
        shipped = self.staged() / "usr/lib/a3-update/a3-root"
        self.assertEqual((ROOT / "installer" / "a3-root").read_bytes(), shipped.read_bytes())

    def test_modes(self):
        stage = self.staged()
        self.assertEqual(0o755, mode(stage / "usr/lib/a3-update/a3-root"))
        self.assertEqual(0o755, mode(stage / "usr/lib/a3-update/a3-update"))
        self.assertEqual(0o644, mode(stage / "usr/lib/systemd/user/a3-update.service"))
        self.assertEqual(0o644, mode(stage / "usr/share/doc/a3-update/copyright"))
        for folder in (p for p in stage.rglob("*") if p.is_dir()):
            self.assertEqual(0o755, mode(folder), folder)

    def test_the_control(self):
        control = (RECIPE / "DEBIAN" / "control").read_text()
        self.assertIn("Package: a3-update\n", control)
        self.assertIn("Architecture: all\n", control)
        self.assertIn("Depends: python3, gpgv\n", control)
        self.assertNotIn("${shlibs:Depends}", control)
        self.assertEqual("a3-update", package.package_name(control))

    def test_the_recipe_has_every_maintainer_script_the_builder_wants(self):
        for name in package.DEBIAN_FILES:
            self.assertTrue((RECIPE / "DEBIAN" / name).is_file(), name)

    def test_the_unit_starts_the_service_for_the_session(self):
        unit = configparser.ConfigParser(interpolation=None, strict=False)
        unit.optionxform = str
        unit.read(UNIT)
        self.assertEqual("/usr/lib/a3-update/a3-update", unit["Service"]["ExecStart"])
        self.assertEqual("default.target", unit["Install"]["WantedBy"])
        self.assertIn(unit["Service"]["Restart"], ("always", "on-failure"))

    def test_the_package_enables_the_unit_for_every_user_and_disables_it_on_removal(self):
        postinst = (RECIPE / "DEBIAN" / "postinst").read_text()
        prerm = (RECIPE / "DEBIAN" / "prerm").read_text()
        self.assertIn("systemctl --global enable a3-update.service", postinst)
        self.assertIn("systemctl --global disable a3-update.service", prerm)
        self.assertNotIn("/etc/sudoers", postinst, "the sudoers line is the maintainer's to write")

    def test_build_compiles_nothing(self):
        build = tmpdir(self) / "build"
        subprocess.run([str(RECIPE / "stage"), "build", str(ROOT), str(build), "/juce", "2"],
                       check=True, capture_output=True)
        self.assertFalse(build.exists() and any(build.iterdir()))

    def test_an_unknown_step_is_a_usage_error(self):
        result = subprocess.run([str(RECIPE / "stage"), "pack"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertIn("usage", result.stderr)


if __name__ == "__main__":
    unittest.main()
