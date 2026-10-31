"""The virtual desk as an installer role (spec virtual-desk Q6): the package
a3-desk from the pinned a3-mixer, no unit -- an app a person opens."""

import shutil
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_installer import PIN, RecordingRunner, context  # noqa: E402
from installer.roles import BY_NAME, needed_submodules  # noqa: E402


def desk_seams(packaged=True, asked=None):
    from installer.roles import apppackage, desk
    stack = ExitStack()

    def has_packaging(_ctx, _source, _commit, recipe="packaging"):
        if asked is not None:
            asked.append(recipe)
        return packaged

    stack.enter_context(mock.patch.object(desk, "has_packaging", has_packaging))
    stack.enter_context(mock.patch.object(desk, "ensure_juce", lambda _ctx: Path("/juce")))
    stack.enter_context(mock.patch.object(desk, "pinned_commit", lambda _ctx: PIN))
    stack.enter_context(mock.patch.object(apppackage.debs, "version_of", lambda *_: "03.0+9"))
    # The desk's own steps; the updater every role brings is test_updater_role's.
    stack.enter_context(mock.patch.object(desk, "install_updater", lambda _ctx: None))
    return stack


class TheDeskIsARole(unittest.TestCase):
    def test_it_is_offered_and_builds_from_a3_mixer(self):
        self.assertIn("desk", BY_NAME)
        self.assertEqual(needed_submodules(["desk"], from_source=True), ["a3-mixer"])
        self.assertTrue(BY_NAME["desk"].needs_screen)

    def test_the_hardware_desks_role_stays_as_it_was(self):
        self.assertEqual(BY_NAME["mixer"].platforms, ())

    def test_a_saved_choice_brings_it_back(self):
        from installer.settings import Settings
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        s = Settings(Path(tmp) / "install.conf")
        s.set_flag("roles", "desk", True)
        self.assertIn("desk", s.roles())


class TheDeskComesAsAPackage(unittest.TestCase):
    def install(self, packaged=True, asked=None):
        from installer.roles import desk
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = context(tmp, {("roles", "desk"): "yes"})
        ctx.runner = RecordingRunner(log=log)
        ctx.user_units.mkdir(parents=True)
        with desk_seams(packaged, asked):
            desk.Desk().install(ctx)
        return log.commands(), ctx

    def test_a_pin_older_than_the_desk_is_refused_before_any_build(self):
        """The umbrella's a3-mixer pin may predate packaging/: say so, rather
        than let installer/package.py fail with a raw git error."""
        from installer.roles.base import RoleError
        with self.assertRaises(RoleError) as caught:
            self.install(packaged=False)
        self.assertIn("a3-mixer", str(caught.exception))
        self.assertIn("raise it first", str(caught.exception))

    def test_it_builds_the_pinned_commit_through_the_cli(self):
        commands, ctx = self.install()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertIn(f"--rev {PIN}", build)
        self.assertIn(str(ctx.repo / "a3-mixer"), build)
        self.assertTrue(build.startswith("python3 "), build)

    def test_the_recipe_is_the_desks_folder_ui_packaging(self):
        """a3-mixer's top level reads like a3-motion's since 2026-10-31: the
        desk is ui/, its recipe ui/packaging/."""
        asked = []
        commands, _ = self.install(asked=asked)
        self.assertEqual(asked, ["ui/packaging"])
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertIn("--recipe ui/packaging", build)

    def test_it_installs_then_holds(self):
        commands, ctx = self.install()
        deb = ctx.home / "a3-debs" / "a3-desk_03.0+9_amd64.deb"
        at = next(i for i, c in enumerate(commands) if "apt-get install" in c)
        self.assertIn(str(deb), commands[at])
        self.assertIn("apt-mark hold a3-desk", commands[at + 1])

    def test_it_starts_and_disables_no_service(self):
        commands, _ = self.install()
        self.assertFalse(any("systemctl" in c for c in commands), commands)

    def test_leaving_removes_only_the_package(self):
        from installer.roles import desk
        self.assertEqual(desk.Desk().leaving_packages(None), ["a3-desk"])
        self.assertEqual(desk.Desk().leaving_units(None), [])


if __name__ == "__main__":
    unittest.main()
