# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Packages mode, the default: the apps come by name from the apt archive
through installer/a3-root; --from-source builds them from the pins as before."""

import io
import shutil
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stderr
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_installer import (PIN, FakeRole, Log, MovingFailingRunner,  # noqa: E402
                            RecordingRunner, context as from_source_context)
from installer import archive, cli  # noqa: E402
from installer.prompt import Prompter  # noqa: E402
from installer.roles import apppackage, core, desk, motion, needed_submodules, stemdeck  # noqa: E402
from installer.roles.base import Context, State  # noqa: E402
from installer.settings import Settings  # noqa: E402
from installer.system import CommandFailed, Runner  # noqa: E402

A3_ROOT = str(archive.A3_ROOT)


class RootRecordingRunner(RecordingRunner):
    """Runs nothing; logs each command, a root one as `root: <command>`."""

    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        self.log("$ " + ("root: " if root else "") + " ".join(str(a) for a in args))
        return 0


def packages_context(tmp, roles=()):
    settings = Settings(Path(tmp) / "install.conf")
    settings.set("stemdeck", "library", str(Path(tmp) / "stems"))
    for name in roles:
        settings.set("roles", name, "yes")
    log = Log()
    ctx = Context(REPO, settings, RootRecordingRunner(log=log), Prompter(), "debian",
                  home=tmp, user="aaa")
    ctx.user_units.mkdir(parents=True)
    return ctx, log


def no_build_seams():
    """A packages-mode install that reached for JUCE, a pin or a recipe fails."""
    def must_not_run(*_args, **_kwargs):
        raise AssertionError("a packages-mode install looked at the source")
    stack = ExitStack()
    for module in (core, stemdeck, desk, motion):
        stack.enter_context(mock.patch.object(module, "ensure_juce", must_not_run))
    for module in (core, desk, motion):
        stack.enter_context(mock.patch.object(module, "has_packaging", must_not_run))
    for module in (stemdeck, desk, motion):
        stack.enter_context(mock.patch.object(module, "pinned_commit", must_not_run))
    stack.enter_context(mock.patch.object(core, "analyzer_commit", must_not_run))
    stack.enter_context(mock.patch.object(core, "core_commit", must_not_run))
    stack.enter_context(mock.patch.object(core, "leftover_engine_installed", lambda _ctx: False))
    stack.enter_context(mock.patch.object(apppackage, "fragment_path",
                                          lambda _ctx, app: app.packaged_unit))
    stack.enter_context(mock.patch.object(motion.Motion, "_dialout", lambda self, ctx: None))
    stack.enter_context(mock.patch.object(motion.Motion, "_firmware", lambda self, ctx: None))
    return stack


ROLES = {"core": core.Core, "stemdeck": stemdeck.StemDeck, "desk": desk.Desk,
         "motion": motion.Motion}


class PackagesMode(unittest.TestCase):
    def install(self, name, roles=("core", "stemdeck")):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = packages_context(tmp, roles)
        with no_build_seams():
            ROLES[name]().install(ctx)
        return log.commands()

    def test_it_is_the_default(self):
        self.assertFalse(cli.parse([]).from_source)
        self.assertTrue(cli.parse(["--from-source"]).from_source)
        ctx = Context(REPO, Settings("/nonexistent/install.conf"), Runner(dry_run=True),
                      Prompter(), "debian", home="/nonexistent", user="aaa")
        self.assertFalse(ctx.from_source)

    def test_packages_mode_builds_nothing(self):
        for name in ROLES:
            with self.subTest(name):
                commands = self.install(name)
                self.assertFalse(any("installer/package.py" in c for c in commands), commands)

    def test_packages_mode_installs_by_name_through_a3_root(self):
        for name, packages in (("stemdeck", ["stemdeck"]), ("desk", ["a3-desk"]),
                               ("motion", ["a3-motion-ui"]),
                               ("core", ["a3-core-app a3-core", "beat-analyzer"])):
            with self.subTest(name):
                commands = self.install(name)
                installs = [c for c in commands if c.startswith(f"root: {A3_ROOT} install")]
                self.assertEqual([f"root: {A3_ROOT} install {p}"
                                  for p in packages + ["a3-update"]], installs)
                self.assertFalse(any("apt-get" in c or "apt-mark hold" in c for c in commands),
                                 commands)

    def test_the_core_preseed_still_runs_before_its_install(self):
        commands = self.install("core")
        preseed = commands.index("root: debconf-set-selections")
        installed = commands.index(f"root: {A3_ROOT} install a3-core-app a3-core")
        self.assertLess(preseed, installed)
        # The marker is cleared after, as from source (a3-system#76).
        self.assertEqual(2, commands.count("root: debconf-set-selections"))
        self.assertGreater(len(commands) - commands[::-1].index("root: debconf-set-selections"),
                           installed)


class FromSource(unittest.TestCase):
    def test_from_source_is_todays_command_list(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = from_source_context(tmp, {("stemdeck", "library"): tmp + "/stems",
                                             ("roles", "core"): "yes",
                                             ("roles", "stemdeck"): "yes"})
        ctx.runner = RecordingRunner(log=log)
        ctx.user_units.mkdir(parents=True)
        with mock.patch.object(stemdeck, "ensure_juce", lambda _ctx: Path("/juce")), \
                mock.patch.object(stemdeck, "pinned_commit", lambda _ctx: PIN), \
                mock.patch.object(apppackage.debs, "version_of", lambda *_: "03.0+7"), \
                mock.patch.object(apppackage.debs, "host_architecture", lambda: "amd64"), \
                mock.patch.object(apppackage, "fragment_path",
                                  lambda _ctx, app: app.packaged_unit):
            stemdeck.StemDeck().install(ctx)
        commands = [c.replace(tmp, "~").replace(str(REPO), "REPO") for c in log.commands()]
        self.assertEqual([
            "python3 REPO/installer/package.py REPO/stemdeck --rev "
            "0123456789abcdef0123456789abcdef01234567 --out ~/a3-debs "
            "--cache ~/.cache/a3-build --jobs 2 --juce /juce",
            "env DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-downgrades "
            "--allow-change-held-packages ~/a3-debs/stemdeck_03.0+7_amd64.deb",
            "apt-mark hold stemdeck",
            "systemctl --user stop stemdeck.service",
            "systemctl --user daemon-reload",
            "systemctl --user enable stemdeck.service",
            "systemctl --user restart stemdeck.service",
        ], commands)


class PackagesModeLeaves(unittest.TestCase):
    def test_leaving_removes_through_a3_root(self):
        for name, role, package in (("stemdeck", stemdeck.StemDeck, "stemdeck"),
                                    ("desk", desk.Desk, "a3-desk"),
                                    ("motion", motion.Motion, "a3-motion-ui")):
            with self.subTest(name):
                tmp = tempfile.mkdtemp()
                self.addCleanup(shutil.rmtree, tmp)
                ctx, log = packages_context(tmp)
                with mock.patch.object(sys.modules[role.__module__], "package_is_installed",
                                       lambda _ctx: True):
                    role().uninstall(ctx)
                commands = log.commands()
                self.assertIn(f"root: {A3_ROOT} remove {package}", commands)
                self.assertFalse(any("apt-get" in c or "apt-mark" in c for c in commands),
                                 commands)

    def test_the_core_leaves_through_a3_root_and_keeps_the_keys(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = packages_context(tmp)
        (Path(tmp) / ".ssh").mkdir()
        (Path(tmp) / ".ssh" / "authorized_keys").write_text("ssh-ed25519 AAAA x\n")
        with mock.patch.object(core, "analyzer_is_installed", lambda _ctx: True):
            core.Core().uninstall(ctx)
        commands = log.commands()
        removed = commands.index(f"root: {A3_ROOT} remove a3-core a3-core-app")
        self.assertIn(f"root: {A3_ROOT} remove beat-analyzer", commands)
        self.assertTrue(commands[removed - 1].startswith("cp -p "), commands)
        self.assertTrue(commands[removed + 1].startswith("mv -f "), commands)
        self.assertFalse(any("apt-get" in c or "apt-mark" in c for c in commands), commands)


class OnlyTheSubmodulesARoleReads(unittest.TestCase):
    def test_packages_mode_checks_out_only_configuration(self):
        # core: the truth, the shipped config and the postinst functions in a3-core;
        # stemdeck: its patchbay unit; motion: the panel firmware; desk and
        # deck-host read nothing from a submodule.
        self.assertEqual(["a3-core"], needed_submodules(["core"], from_source=False))
        self.assertEqual(["stemdeck"], needed_submodules(["stemdeck"], from_source=False))
        self.assertEqual(["a3-motion"], needed_submodules(["motion"], from_source=False))
        self.assertEqual([], needed_submodules(["desk"], from_source=False))
        self.assertEqual([], needed_submodules(["deck-host"], from_source=False))

    def test_from_source_checks_out_what_builds(self):
        self.assertEqual(["a3-core", "beat-analyzer"],
                         needed_submodules(["core"], from_source=True))
        self.assertEqual(["a3-mixer"], needed_submodules(["desk"], from_source=True))


FORKY = "PRETTY_NAME=\"Debian forky\"\nID=debian\nVERSION_CODENAME=forky\n"


class TheArchiveSource(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        (self.tmp / "os-release").write_text(FORKY)
        self.sources = self.tmp / "a3-audio.sources"
        self.keyring = self.tmp / "a3-audio.gpg"
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(mock.patch.object(cli, "OS_RELEASE", self.tmp / "os-release"))
        self.stack.enter_context(mock.patch.object(archive, "SOURCES", self.sources))
        self.stack.enter_context(mock.patch.object(archive, "KEYRING", self.keyring))

    def install_roles(self, archive_setting="public", from_source=False, platform="debian"):
        ctx, log = packages_context(self.tmp / "home")
        ctx.settings.set("system", "archive", archive_setting)
        ctx.from_source = from_source
        ctx.platform = platform
        roles = (FakeRole("a"), FakeRole("b"))
        by_name = {r.name: r for r in roles}
        with mock.patch("installer.cli.BY_NAME", by_name), \
                mock.patch("installer.roles.BY_NAME", by_name), \
                mock.patch("installer.roles.ALL", roles):
            cli.install_roles(ctx, ["a", "b"])
        return log

    def test_the_source_is_written_once(self):
        commands = self.install_roles().commands()
        self.assertEqual([f"root: {A3_ROOT} source forky"],
                         [c for c in commands if " source " in c])
        self.assertLess(commands.index(f"root: {A3_ROOT} source forky"),
                        commands.index("install a"))

    def test_a_matching_source_and_key_are_left_alone(self):
        self.sources.write_text(archive.sources_text("forky"))
        self.keyring.write_bytes(b"key")
        self.assertFalse(any(" source " in c for c in self.install_roles().commands()))

    def test_a_differing_source_is_written(self):
        self.sources.write_text(archive.sources_text("trixie"))
        self.keyring.write_bytes(b"key")
        self.assertIn(f"root: {A3_ROOT} source forky", self.install_roles().commands())

    def test_a_missing_key_is_written(self):
        self.sources.write_text(archive.sources_text("forky"))
        self.assertIn(f"root: {A3_ROOT} source forky", self.install_roles().commands())

    def test_lan_writes_nothing_and_says_so(self):
        log = self.install_roles("lan")
        self.assertFalse(any(" source " in c for c in log.commands()))
        self.assertTrue(any("http://192.168.8.5/apt a3 main" in line for line in log), log)

    def test_from_source_needs_no_archive(self):
        self.assertFalse(any(" source " in c
                             for c in self.install_roles(from_source=True).commands()))

    def test_only_apt_platforms_get_a_source(self):
        self.assertFalse(any(" source " in c
                             for c in self.install_roles(platform="macos").commands()))


class AnUnsupportedCodenameIsRefusedBeforeAnyChange(unittest.TestCase):
    UBUNTU = {"ID": "ubuntu", "VERSION_CODENAME": "noble"}

    def refusal(self, archive_name="public", platform="debian", argv=("--update",)):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        settings = Settings(tmp / "install.conf")
        settings.set("system", "archive", archive_name)
        return cli.refusal(cli.parse(list(argv)), settings, State(tmp / "install.state"),
                           platform=platform, release_info=self.UBUNTU)

    def test_public_archive_on_ubuntu_is_refused(self):
        self.assertIn("VERSION_CODENAME=noble", self.refusal())

    def test_lan_from_source_and_other_platforms_are_not_asked(self):
        self.assertIsNone(self.refusal("lan"))
        self.assertIsNone(self.refusal(argv=("--update", "--from-source")))
        self.assertIsNone(self.refusal(platform="macos"))

    def test_main_runs_nothing_on_ubuntu(self):
        with mock.patch.object(cli, "os_release", lambda _path: self.UBUNTU), \
                mock.patch.object(cli, "platform_name", lambda: "debian"):
            code, said, ran = RefusedBeforeAnyChange.main(self, ["--update"])
        self.assertEqual((2, []), (code, ran))
        self.assertIn("VERSION_CODENAME=noble", said)


class RefusedBeforeAnyChange(unittest.TestCase):
    def main(self, argv, settings_text="", home=None):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        home = home or tmp
        config = tmp / "install.conf"
        config.write_text(settings_text)
        ran = []

        class Untouchable(Runner):
            def run(self, args, **_kwargs):
                ran.append(args)
                return 0

            def output(self, args, cwd=None):
                ran.append(args)
                return ""

        stderr = io.StringIO()
        with mock.patch.object(cli, "Runner", Untouchable), redirect_stderr(stderr), \
                mock.patch.object(Path, "home", lambda: home):
            code = cli.main([*argv, "--config", str(config)])
        return code, stderr.getvalue(), ran

    def test_update_with_a_version_in_packages_mode_points_to_from_source(self):
        code, said, ran = self.main(["--update", "v03.0"])
        self.assertEqual(2, code)
        self.assertIn("newest", said)
        self.assertIn("--from-source", said)
        self.assertEqual([], ran)

    def test_an_unknown_archive_is_refused_naming_both(self):
        code, said, ran = self.main(["--update"], "[system]\narchive = forge\n")
        self.assertEqual(2, code)
        self.assertIn("public", said)
        self.assertIn("lan", said)
        self.assertEqual([], ran)


UNSET = ("`[system] archive` is not set: set it to public (the GitHub archive) or lan "
         "(the forge on 192.168.8.5), or run with --from-source to build as before.")


class AnInstalledMachineChoosesItsArchive(unittest.TestCase):
    """A machine installed before (the rig, on its LAN archive) is not moved to
    the public archive unasked: a source written there breaks its apt until
    removed by hand when the archive is not published yet (P25)."""

    def refusal(self, conf="", installed=True, argv=("--update",)):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        (tmp / "install.conf").write_text(conf)
        state = State(tmp / "install.state")
        if installed:
            state.set("installed", "stemdeck", "2026-10-01")
        return cli.refusal(cli.parse(list(argv)), Settings(tmp / "install.conf"), state)

    def test_an_installed_machine_without_the_key_is_refused(self):
        self.assertEqual(UNSET, self.refusal())

    def test_a_set_key_is_taken(self):
        self.assertIsNone(self.refusal("[system]\narchive = lan\n"))
        self.assertIsNone(self.refusal("[system]\narchive = public\n"))

    def test_a_fresh_machine_takes_public(self):
        self.assertIsNone(self.refusal(installed=False))

    def test_from_source_needs_no_archive(self):
        self.assertIsNone(self.refusal(argv=("--update", "--from-source")))

    def test_a_from_source_run_does_not_save_the_default_archive(self):
        """--from-source passes the check and saves; the next packages-mode run
        must still be refused, not take the saved default."""
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        conf = tmp / "install.conf"
        conf.write_text("[roles]\nstemdeck = yes\n")
        state = State(tmp / "install.state")
        state.set("installed", "stemdeck", "2026-10-01")
        first = Settings(conf)
        self.assertIsNone(cli.refusal(cli.parse(["--update", "--from-source"]), first, state))
        first.save()
        self.assertEqual(UNSET, cli.refusal(cli.parse(["--update"]), Settings(conf), state))

    def test_an_archive_in_the_file_or_set_in_the_run_is_saved(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        kept, chosen = tmp / "kept.conf", tmp / "chosen.conf"
        kept.write_text("[system]\narchive = lan\n")
        Settings(kept).save()
        self.assertEqual("lan", Settings(kept).get("system", "archive"))
        self.assertTrue(Settings(kept).in_file("system", "archive"))
        settings = Settings(chosen)
        settings.set("system", "archive", "public")
        settings.save()
        self.assertTrue(Settings(chosen).in_file("system", "archive"))

    def test_the_run_stops_before_any_command(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        State(tmp / ".config" / "a3" / "install.state").set("installed", "desk", "2026-10-01")
        code, said, ran = RefusedBeforeAnyChange.main(self, ["--update"], home=tmp)
        self.assertEqual(2, code)
        self.assertIn(UNSET, said)
        self.assertEqual([], ran)


class AFreshMachineKeepsItsArchiveForTheNextRun(unittest.TestCase):
    """The first packages-mode run records the archive it used; without it
    the second run of that very machine was refused (installed, key unset)."""

    def run_main(self, home, argv):
        conf = home / ".config" / "a3" / "install.conf"
        stderr = io.StringIO()
        with mock.patch.object(Path, "home", lambda: home), \
                mock.patch.object(cli, "DEFAULT_PATH", conf), \
                mock.patch.object(cli, "Runner", RootRecordingRunner), \
                mock.patch.object(cli, "where_problems", lambda *_: []), \
                mock.patch.object(cli, "ensure_archive", lambda *_: None), \
                mock.patch.object(cli.release, "fetch", lambda *_: None), \
                mock.patch.object(cli.release, "tags", lambda *_: ["v03.1"]), \
                mock.patch.object(cli.release, "current", lambda *_: "v03.1"), \
                mock.patch.object(cli.release, "catch_up", lambda *_: None), \
                mock.patch.object(cli.release, "update_submodules", lambda *_: None), \
                redirect_stderr(stderr):
            code = cli.main(argv)
        return code, stderr.getvalue(), conf

    def test_the_second_run_is_not_refused(self):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home)
        code, said, conf = self.run_main(home, ["--update"])
        self.assertEqual((0, ""), (code, said))
        self.assertTrue(Settings(conf).in_file("system", "archive"))
        State(home / cli.STATE_FILE).set("installed", "desk", "2026-10-29")
        code, said, _ = self.run_main(home, ["--update"])
        self.assertEqual((0, ""), (code, said))

    def test_an_installed_machine_without_the_key_is_still_refused(self):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home)
        State(home / cli.STATE_FILE).set("installed", "desk", "2026-10-29")
        code, said, conf = self.run_main(home, ["--update"])
        self.assertEqual(2, code)
        self.assertIn("is not set", said)
        self.assertFalse(conf.exists())

    def test_from_source_records_nothing(self):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home)
        _, _, conf = self.run_main(home, ["--update", "--from-source"])
        self.assertFalse(Settings(conf).in_file("system", "archive"))


class AnOlderVersionIsNamed(unittest.TestCase):
    def choose(self, stored, from_source=False):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = packages_context(tmp)
        ctx.from_source = from_source
        ctx.settings.set("system", "version", stored)
        with mock.patch.object(cli.release, "fetch", lambda *_: None), \
                mock.patch.object(cli.release, "tags", lambda *_: ["v03.1", "v03.0"]), \
                mock.patch.object(cli.release, "current", lambda *_: "v03.1"):
            version = cli.choose_version(ctx, cli.parse([]))
        return version, [line for line in log if "--from-source" in line]

    def test_a_version_other_than_the_newest_is_said(self):
        version, said = self.choose("v03.0")
        self.assertEqual("v03.0", version)
        self.assertEqual(["Packages come from the archive's newest whatever version is "
                          "checked out; use --from-source to build this version."], said)

    def test_the_newest_is_not(self):
        self.assertEqual([], self.choose("v03.1")[1])

    def test_from_source_builds_the_version(self):
        self.assertEqual([], self.choose("v03.0", from_source=True)[1])


class APackagesInstallThatFailsPutsTheHandUnitBack(unittest.TestCase):
    def test_a_failing_a3_root_install_puts_the_hand_unit_back(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        ctx, log = packages_context(tmp)
        ctx.runner = MovingFailingRunner(f"{A3_ROOT} install", log=log)
        hand = ctx.user_units / "stemdeck.service"
        hand.write_text("[Service]\nExecStart=/hand\n")
        with no_build_seams(), self.assertRaises(CommandFailed):
            stemdeck.install_package(ctx)
        commands = log.commands()
        aside = f"{hand}.before-package"
        self.assertIn(f"mv -n {hand} {aside}", commands)
        self.assertIn(f"mv -n {aside} {hand}", commands)
        self.assertEqual("systemctl --user enable stemdeck.service", commands[-1])
        self.assertLess(commands.index(f"{A3_ROOT} install stemdeck"),
                        commands.index(f"mv -n {aside} {hand}"))


if __name__ == "__main__":
    unittest.main()
