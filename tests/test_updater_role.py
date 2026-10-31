# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""a3-update comes with every role: once per run, from the archive by name or
built from the umbrella's own recipe; the sudoers line is printed, never written."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_packages_mode import ROLES, A3_ROOT, no_build_seams, packages_context  # noqa: E402
from installer.roles import updater  # noqa: E402

SUDOERS_LINE = "aaa ALL=(root) NOPASSWD: /usr/lib/a3-update/a3-root install-release *"


class TheUpdater(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.ctx, self.log = packages_context(self.tmp)

    def test_from_the_archive_by_name_then_started(self):
        updater.install_updater(self.ctx)
        commands = self.log.commands()
        self.assertEqual([f"root: {A3_ROOT} install a3-update",
                          "systemctl --user daemon-reload",
                          "systemctl --user restart a3-update.service"], commands)

    def test_once_per_run(self):
        updater.install_updater(self.ctx)
        updater.install_updater(self.ctx)
        self.assertEqual(1, self.log.commands().count(f"root: {A3_ROOT} install a3-update"))

    def test_the_sudoers_line_is_printed_with_its_check_and_never_written(self):
        updater.install_updater(self.ctx)
        text = "\n".join(self.log)
        self.assertIn(SUDOERS_LINE, text)
        self.assertIn("sudo visudo -cf /tmp/a3-update", text)
        self.assertIn("sudo install -m 0440 -o root -g root /tmp/a3-update "
                      "/etc/sudoers.d/a3-update", text)
        self.assertFalse(any("sudoers" in c for c in self.log.commands()))

    def test_the_line_names_the_installers_user(self):
        self.ctx.user = "dj"
        updater.install_updater(self.ctx)
        self.assertIn("dj ALL=(root) NOPASSWD: /usr/lib/a3-update/a3-root install-release *",
                      "\n".join(self.log))

    def test_from_source_it_is_built_from_the_umbrellas_own_recipe(self):
        self.ctx.from_source = True
        with mock.patch.object(updater, "umbrella_commit", return_value="c0ffee"), \
                mock.patch.object(updater.apppackage, "has_packaging", return_value=True), \
                mock.patch.object(updater.apppackage.debs, "version_of", return_value="03.2+1"), \
                mock.patch.object(updater.apppackage.debs, "host_architecture",
                                  side_effect=AssertionError("an all package has no host arch")):
            updater.install_updater(self.ctx)
        commands = self.log.commands()
        build = [c for c in commands if "installer/package.py" in c][0]
        self.assertIn(f"package.py {REPO} --rev c0ffee", build)
        self.assertTrue(build.endswith("--recipe update/packaging --without-submodules"), build)
        deb = self.tmp / "a3-debs" / "a3-update_03.2+1_all.deb"
        self.assertTrue(any(c.startswith("root: env DEBIAN_FRONTEND=noninteractive apt-get install")
                            and c.endswith(str(deb)) for c in commands), commands)
        self.assertIn("root: apt-mark hold a3-update", commands)

    def test_from_source_a_version_without_the_recipe_leaves_it_out(self):
        self.ctx.from_source = True
        with mock.patch.object(updater, "umbrella_commit", return_value="c0ffee"), \
                mock.patch.object(updater.apppackage, "has_packaging", return_value=False):
            updater.install_updater(self.ctx)
        self.assertEqual([], self.log.commands())
        self.assertTrue(any("a3-update" in line for line in self.log))


class EveryRoleBringsIt(unittest.TestCase):
    def test_each_role_installs_the_updater(self):
        for name, role in ROLES.items():
            with self.subTest(name):
                tmp = tempfile.mkdtemp()
                self.addCleanup(shutil.rmtree, tmp)
                ctx, log = packages_context(tmp, ("core", "stemdeck"))
                with no_build_seams():
                    role().install(ctx)
                self.assertIn(f"root: {A3_ROOT} install a3-update", log.commands())


if __name__ == "__main__":
    unittest.main()
