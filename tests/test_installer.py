"""The installer's decisions, without installing anything.

Commands go through a Runner in dry-run mode whose log is kept, so a test
reads what would have been run. Run with:

    python3 -m unittest discover -s tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import release  # noqa: E402
from installer.cli import install_roles, where_problems  # noqa: E402
from installer.prompt import Prompter, TextPrompter  # noqa: E402
from installer.roles import ALL, BY_NAME, needed_packages, needed_submodules  # noqa: E402
from installer.roles.base import Context, RoleError, State  # noqa: E402
from installer.roles.core import chosen_groups, preseed_lines  # noqa: E402
from installer.roles import motion, screen  # noqa: E402
from installer.roles.motion import (Motion, drop_in_text, panel_usb_ids,  # noqa: E402
                                    serial_candidates)
from installer.settings import Settings  # noqa: E402
from installer.system import Runner  # noqa: E402


class Log(list):
    def __call__(self, message):
        self.append(message)

    def commands(self):
        return [line[2:] for line in self if line.startswith("$ ")]


def context(tmp, settings=None):
    s = Settings(Path(tmp) / "install.conf")
    for (section, key), value in (settings or {}).items():
        s.set(section, key, value)
    log = Log()
    runner = Runner(dry_run=True, log=log)
    return Context(REPO, s, runner, Prompter(), "debian", home=tmp, user="aaa"), log


class SettingsKeepAnswers(unittest.TestCase):
    def test_a_saved_answer_is_read_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a3" / "install.conf"
            s = Settings(path)
            s.set_flag("roles", "stemdeck", True)
            s.set("core", "address", "192.168.8.11/24")
            s.save()
            again = Settings(path)
            self.assertEqual(["stemdeck"], again.roles())
            self.assertEqual("192.168.8.11/24", again.get("core", "address"))

    def test_the_defaults_replace_everything_and_flash_nothing_unasked(self):
        s = Settings("/nonexistent/install.conf")
        self.assertEqual("all", s.get("core", "replace"))
        self.assertEqual("ask", s.get("motion", "flash_firmware"))
        self.assertEqual([], s.roles())


class ReplaceSetting(unittest.TestCase):
    DIFFERING = ["reaper", "i3", "systemd"]

    def test_all_is_whatever_differs(self):
        self.assertEqual(self.DIFFERING, chosen_groups("all", self.DIFFERING))

    def test_none(self):
        self.assertEqual([], chosen_groups("none", self.DIFFERING))

    def test_a_list_keeps_only_what_differs(self):
        self.assertEqual(["i3"], chosen_groups("i3, qjackctl", self.DIFFERING))


class Preseeding(unittest.TestCase):
    def lines(self, **core):
        s = Settings("/nonexistent/install.conf")
        for key, value in core.items():
            s.set("core", key, value)
        return preseed_lines(s, ["reaper", "i3"]).splitlines()

    def test_every_answer_is_marked_seen(self):
        """The postinst takes a seen answer as the installer's (a3-core 8dcb2c7)."""
        lines = self.lines()
        answers = [l for l in lines if not l.endswith(" seen true")]
        for answer in answers:
            question = answer.split()[1]
            self.assertIn(f"a3-core {question} seen true", lines)

    def test_no_network_asks_for_no_addresses(self):
        joined = "\n".join(self.lines(configure_network="no"))
        self.assertIn("a3-core/configure-network boolean false", joined)
        self.assertNotIn("a3-core/address", joined)

    def test_a_network_hands_over_the_address(self):
        joined = "\n".join(self.lines(configure_network="yes", address="192.168.8.11/24"))
        self.assertIn("a3-core/address string 192.168.8.11/24", joined)

    def test_the_chosen_parts(self):
        self.assertIn("a3-core a3-core/replace-config multiselect reaper, i3", self.lines())


class Tags(unittest.TestCase):
    def test_newest_first_and_numbers_as_numbers(self):
        class Fake:
            def output(self, args, cwd=None):
                return "v03.0\nv03.10\nv03.9\nv.0.2\n"
        self.assertEqual(["v03.10", "v03.9", "v03.0"], release.tags(Fake(), REPO))


class OnlyWhatTheRolesNeed(unittest.TestCase):
    """A machine gets the submodules its roles build from, not the docs'
    234 MB of history on a Motion panel's Pi."""

    def submodule_commands(self, roles, version=None):
        log = Log()
        runner = Runner(dry_run=True, log=log)
        if version:
            release.check_out(runner, REPO, version)
        release.update_submodules(runner, REPO, needed_submodules(roles))
        commands = [c.split("  (in ")[0] for c in log.commands()]
        return [c for c in commands if "submodule" in c or "checkout" in c]

    def test_each_role_names_what_it_builds_from(self):
        self.assertEqual(["a3-core", "beat-analyzer"], needed_submodules(["core"]))
        self.assertEqual(["stemdeck"], needed_submodules(["stemdeck"]))
        self.assertEqual(["a3-motion"], needed_submodules(["motion"]))

    def test_in_install_order_and_once(self):
        self.assertEqual(["a3-core", "beat-analyzer", "stemdeck", "a3-motion"],
                         needed_submodules(["motion", "stemdeck", "core", "core"]))

    def test_only_those_are_initialised(self):
        commands = self.submodule_commands(["stemdeck", "motion"])
        update = [c for c in commands if "update" in c]
        self.assertEqual(1, len(update))
        self.assertTrue(update[0].endswith("--init --recursive -- stemdeck a3-motion"),
                        update[0])
        self.assertNotIn("a3-doc", " ".join(commands))

    def test_a_checkout_initialises_nothing_by_itself(self):
        commands = self.submodule_commands([], version="v03.0")
        self.assertEqual(["git checkout --quiet v03.0"], commands)

    def test_every_named_submodule_is_one(self):
        gitmodules = (REPO / ".gitmodules").read_text()
        for role in ALL:
            for path in role.submodules:
                self.assertIn(f"path = {path}\n", gitmodules, (role.name, path))


class OneJuceForEveryProduct(unittest.TestCase):
    """StemDeck and Motion UI build against one JUCE, the pinned one, and a
    prefix holds only that one: with two, CMake takes either."""

    def ensure(self, installed=(), latest="9.0.3"):
        from installer.roles import base
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp)
            for version in installed:
                (base.juce_prefix(ctx) / "lib" / "cmake" / f"JUCE-{version}").mkdir(parents=True)
            with mock.patch.object(base, "latest_juce", lambda _ctx: latest):
                base.ensure_juce(ctx)
            commands = [c.split("  (in ")[0] for c in log.commands()]
            return commands, list(log), str(base.juce_prefix(ctx))

    def test_the_pin_is_the_newest_release(self):
        from installer.roles.base import JUCE_VERSION
        self.assertEqual("9.0.3", JUCE_VERSION)

    def test_the_pinned_one_installed_builds_nothing(self):
        commands, _, _ = self.ensure(installed=["9.0.3"])
        self.assertEqual([], commands)

    def test_none_installed_is_cloned_at_the_pin(self):
        commands, _, prefix = self.ensure()
        self.assertTrue(any("--depth 1 --branch 9.0.3" in c for c in commands), commands)
        self.assertNotIn(f"rm -rf {prefix}", commands)

    def test_another_version_is_replaced_not_joined(self):
        commands, _, prefix = self.ensure(installed=["8.0.12"])
        self.assertIn(f"rm -rf {prefix}", commands)
        clone = next(i for i, c in enumerate(commands) if "git clone" in c)
        self.assertLess(commands.index(f"rm -rf {prefix}"), clone)

    def test_a_newer_release_is_named_but_not_taken(self):
        commands, lines, _ = self.ensure(installed=["9.0.3"], latest="9.1.0")
        self.assertEqual([], commands)
        self.assertTrue(any("9.1.0" in line for line in lines), lines)

    def test_no_network_is_no_hint_and_no_error(self):
        commands, lines, _ = self.ensure(installed=["9.0.3"], latest=None)
        self.assertEqual([], commands)


class TheProductsNameThePinnedJuce(unittest.TestCase):
    """Where a product's docs name a JUCE release, at the commit this
    repository records, it is JUCE_VERSION: one JUCE for every product."""

    DOCS = {
        "stemdeck": ("stemdeck", "README.md"),
        "a3-motion-ui README": ("a3-motion/ui", "README.md"),
        "a3-motion-ui ARCHITECTURE": ("a3-motion/ui", "ARCHITECTURE.md"),
    }

    @staticmethod
    def pinned_text(path, name):
        """`name` at the commit recorded for `path`, through nested gitlinks."""
        import subprocess

        def git(cwd, *args):
            return subprocess.run(["git", *args], cwd=cwd, check=True,
                                  capture_output=True, text=True).stdout.strip()
        here, commit = REPO, git(REPO, "rev-parse", "HEAD")
        for part in Path(path).parts:
            commit = git(here, "rev-parse", f"{commit}:{part}")
            here = here / part
        return git(here, "show", f"{commit}:{name}")

    def test_one_version(self):
        import re
        import subprocess
        from installer.roles.base import JUCE_VERSION
        for label, (path, name) in self.DOCS.items():
            with self.subTest(label):
                try:
                    text = self.pinned_text(path, name)
                except subprocess.CalledProcessError:
                    self.skipTest(f"{path} is not checked out here")
                named = set(re.findall(r"JUCE\W{0,2}(\d+\.\d+\.\d+)", text))
                self.assertLessEqual(named, {JUCE_VERSION}, label)


class NewestJuceTag(unittest.TestCase):
    def test_releases_only_numbers_as_numbers(self):
        from installer.roles.base import newest_release
        listing = ("abc\trefs/tags/8.0.12\n"
                   "def\trefs/tags/9.0.10\n"
                   "ghi\trefs/tags/9.0.3\n"
                   "jkl\trefs/tags/9.0.3^{}\n"
                   "mno\trefs/tags/juce-9-preview\n")
        self.assertEqual("9.0.10", newest_release(listing))


class TextQuestions(unittest.TestCase):
    def prompter(self, *answers):
        replies = iter(answers)
        return TextPrompter(read=lambda _: next(replies), write=lambda _: None)

    def test_enter_keeps_the_default(self):
        self.assertTrue(self.prompter("").yesno("?", True))
        self.assertEqual("eno1", self.prompter("").text("?", "eno1"))

    def test_checklist_by_numbers_and_dash_for_none(self):
        options = [("a", "A"), ("b", "B"), ("c", "C")]
        self.assertEqual(["a", "c"], self.prompter("3 1").checklist("?", options, []))
        self.assertEqual([], self.prompter("-").checklist("?", options, ["a"]))
        self.assertEqual(["b"], self.prompter("").checklist("?", options, ["b"]))


class WhereItRuns(unittest.TestCase):
    def test_the_units_paths_are_required(self):
        self.assertEqual([], where_problems(Path("/home/aaa/a3-system"), "aaa"))
        self.assertEqual(2, len(where_problems(Path("/home/ra/a3-system"), "ra")))


class Roles(unittest.TestCase):
    def test_core_comes_first(self):
        self.assertEqual("core", ALL[0].name)

    def test_the_mixer_says_it_is_not_supported_yet(self):
        self.assertFalse(BY_NAME["mixer"].supported("debian"))

    def test_nothing_is_supported_off_debian_yet(self):
        for role in ALL:
            for other in ("windows", "macos", "raspios"):
                self.assertFalse(role.supported(other), (role.name, other))


# What each product needs to build on Debian, moved here from a3-core's
# test_package_build_dependencies: the roles install it themselves, so a
# machine without the Core builds too (a3nuc2, 2026-10-05).
JUCE_NEEDS = (
    "libasound2-dev", "libx11-dev", "libxcomposite-dev", "libxcursor-dev",
    "libxext-dev", "libxinerama-dev", "libxrandr-dev", "libxrender-dev",
    "libfreetype-dev", "libfontconfig1-dev", "libglu1-mesa-dev",
    # JUCE 9's OpenGL module includes EGL/egl.h
    "libegl-dev",
    # JUCE 9's juce_gui_basics includes X11/extensions/XInput2.h
    "libxi-dev",
    "cmake", "pkg-config", "git", "build-essential",
    # rebuilds after an update are mostly cache hits
    "ccache",
)
STEMDECK_NEEDS = JUCE_NEEDS + (
    "libflac-dev", "libvorbis-dev", "libogg-dev", "libjack-jackd2-dev")
# Motion UI and its V3 hardware interface
MOTION_NEEDS = JUCE_NEEDS + ("libgsl-dev", "libgpiod-dev", "libserial-dev")
# X started by startx from the tty1 login, i3 on it, xrandr/xset for the screen
SCREEN_NEEDS = ("xinit", "i3", "x11-xserver-utils")


class RolesNameTheirPackages(unittest.TestCase):
    """A role installs what it builds against; nothing comes by way of
    another role's package."""

    def test_the_two_that_stopped_a3nuc2_are_in_the_juce_list(self):
        from installer.roles.base import JUCE_PACKAGES
        self.assertIn("libxi-dev", JUCE_PACKAGES)
        self.assertIn("libegl-dev", JUCE_PACKAGES)

    def test_stemdeck_covers_its_build(self):
        self.assertEqual(set(), set(STEMDECK_NEEDS) - set(BY_NAME["stemdeck"].packages))

    def test_motion_covers_its_build(self):
        self.assertEqual(set(), set(MOTION_NEEDS) - set(BY_NAME["motion"].packages))

    def test_core_installs_only_the_screen_and_mixer_none(self):
        from installer.roles.base import SCREEN_PACKAGES
        self.assertEqual(SCREEN_PACKAGES, BY_NAME["core"].packages)
        self.assertEqual((), BY_NAME["mixer"].packages)

    def test_stemdeck_alone_gets_nothing_of_motion(self):
        packages = needed_packages(["stemdeck"])
        self.assertEqual(set(), set(STEMDECK_NEEDS) - set(packages))
        self.assertEqual(set(), {"libgsl-dev", "libgpiod-dev", "libserial-dev"} & set(packages))

    def test_core_alone_installs_only_the_screen(self):
        self.assertEqual(sorted(SCREEN_NEEDS), needed_packages(["core"]))

    def test_sorted_and_once(self):
        packages = needed_packages(["stemdeck", "motion"])
        self.assertEqual(sorted(set(packages)), packages)
        self.assertEqual(set(STEMDECK_NEEDS) | set(MOTION_NEEDS) | set(SCREEN_NEEDS),
                         set(packages))

    def test_every_screen_role_brings_the_screen(self):
        for name in ("core", "stemdeck", "motion"):
            with self.subTest(name):
                self.assertTrue(BY_NAME[name].needs_screen)
                self.assertEqual(set(), set(SCREEN_NEEDS) - set(BY_NAME[name].packages))

    def test_the_mixer_has_no_screen(self):
        self.assertFalse(BY_NAME["mixer"].needs_screen)


class FakeRole:
    def __init__(self, name, packages=(), needs_screen=False):
        self.name, self.label, self.packages = name, name, packages
        self.needs_screen = needs_screen

    def install(self, ctx):
        ctx.runner.log(f"$ install {self.name}")


def install_fakes(roles, platform="debian"):
    """install_roles on fake roles, dry run: the commands without sudo, and the results."""
    with tempfile.TemporaryDirectory() as tmp:
        ctx, log = context(tmp)
        ctx.platform = platform
        by_name = {r.name: r for r in roles}
        with mock.patch("installer.cli.BY_NAME", by_name), \
                mock.patch("installer.roles.BY_NAME", by_name), \
                mock.patch("installer.roles.ALL", tuple(roles)):
            results = install_roles(ctx, [r.name for r in roles])
        return [c.removeprefix("sudo ") for c in log.commands()], results


class PackagesBeforeTheRoles(unittest.TestCase):
    install = staticmethod(install_fakes)

    def test_one_apt_call_first(self):
        commands, results = self.install([FakeRole("a", ("y", "x")), FakeRole("b", ("x",))])
        self.assertEqual(["env DEBIAN_FRONTEND=noninteractive apt-get install -y x y",
                          "install a", "install b"], commands)
        self.assertEqual([("a", "ok"), ("b", "ok")], results)

    def test_no_packages_no_apt(self):
        commands, _ = self.install([FakeRole("core")])
        self.assertEqual(["install core"], commands)

    def test_apt_only_on_debian(self):
        commands, _ = self.install([FakeRole("a", ("x",))], platform="other")
        self.assertEqual(["install a"], commands)


class TheScreenStepRunsOnceBetweenPackagesAndRoles(unittest.TestCase):
    install = staticmethod(install_fakes)

    def test_after_the_packages_and_before_the_first_role(self):
        commands, results = self.install([FakeRole("a", ("x",), needs_screen=True),
                                          FakeRole("b", needs_screen=True)])
        apt = commands.index("env DEBIAN_FRONTEND=noninteractive apt-get install -y x")
        disable = commands.index("systemctl disable lightdm")
        self.assertEqual(0, apt)
        self.assertLess(disable, commands.index("install a"))
        self.assertEqual(1, commands.count("systemctl disable lightdm"))
        self.assertEqual([("autologin", "ok"), ("a", "ok"), ("b", "ok")], results)

    def test_skipped_when_no_chosen_role_needs_a_screen(self):
        commands, results = self.install([FakeRole("mixer")])
        self.assertEqual(["install mixer"], commands)
        self.assertEqual([("mixer", "ok")], results)


AUTOLOGIN_TARGET = "/etc/systemd/system/getty@tty1.service.d/a3-autologin.conf"


class AutologinWithoutADisplayManager(unittest.TestCase):
    def test_the_drop_in_text(self):
        self.assertEqual("[Service]\n"
                         "ExecStart=\n"
                         "ExecStart=-/sbin/agetty --autologin aaa --noclear %I $TERM\n",
                         screen.autologin_drop_in("aaa"))

    def test_a_missing_bash_profile_keeps_reading_profile(self):
        """bash reads ~/.bash_profile instead of ~/.profile, not as well."""
        text = screen.with_autologin_block(None)
        self.assertIn(". ~/.profile", text)
        self.assertLess(text.index(". ~/.profile"), text.index(screen.BLOCK_BEGIN))
        self.assertIn(screen.autologin_block(), text)

    def test_the_block_starts_x_only_on_tty1_without_a_display(self):
        block = screen.autologin_block()
        self.assertTrue(block.startswith(screen.BLOCK_BEGIN + "\n"), block)
        self.assertTrue(block.endswith(screen.BLOCK_END + "\n"), block)
        self.assertIn('[ -z "$DISPLAY" ]', block)
        self.assertIn('"$(tty)" = /dev/tty1', block)
        self.assertIn("exec startx", block)

    def test_a_present_block_is_replaced_and_nothing_else(self):
        before = "export A=1\n"
        after = "alias ll='ls -l'\n"
        old = f"{screen.BLOCK_BEGIN}\nexec something-old\n{screen.BLOCK_END}\n"
        text = screen.with_autologin_block(before + old + after)
        self.assertEqual(before + screen.autologin_block() + after, text)

    def test_a_foreign_file_gets_the_block_appended(self):
        foreign = "# mine\nexport PATH=$HOME/bin:$PATH"
        text = screen.with_autologin_block(foreign)
        self.assertTrue(text.startswith(foreign + "\n"), text)
        self.assertTrue(text.endswith(screen.autologin_block()), text)
        self.assertNotIn(". ~/.profile", text)

    def test_twice_is_once(self):
        for start in (None, "export A=1\n"):
            once = screen.with_autologin_block(start)
            self.assertEqual(once, screen.with_autologin_block(once))
            self.assertEqual(1, once.count(screen.BLOCK_BEGIN))

    def files_context(self, tmp, dry_run=False):
        log = Log()
        runner = Runner(dry_run=dry_run, log=log)
        s = Settings(Path(tmp) / "install.conf")
        return Context(REPO, s, runner, Prompter(), "debian", home=tmp, user="aaa"), log

    def test_bash_profile_written_into_the_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = self.files_context(tmp)
            (Path(tmp) / ".bash_profile").write_text("export A=1\n")
            screen.ensure_bash_profile(ctx)
            text = (Path(tmp) / ".bash_profile").read_text()
            self.assertTrue(text.startswith("export A=1\n"))
            self.assertIn(screen.autologin_block(), text)

    def test_xinitrc_written_when_missing_and_rewritten_when_ours(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = self.files_context(tmp)
            xinitrc = Path(tmp) / ".xinitrc"
            screen.ensure_xinitrc(ctx)
            self.assertEqual(screen.XINITRC_TEXT, xinitrc.read_text())
            self.assertIn("exec i3\n", xinitrc.read_text())
            xinitrc.write_text(screen.XINITRC_MARKER + "\nexec twm\n")
            screen.ensure_xinitrc(ctx)
            self.assertEqual(screen.XINITRC_TEXT, xinitrc.read_text())

    def test_xinitrc_hands_the_display_to_the_user_manager_before_i3(self):
        """a3-reaper and qjackctl set no DISPLAY; under lightdm Xsession.d
        imported it into systemd --user, with startx only this does."""
        text = screen.XINITRC_TEXT
        imported = text.index("systemctl --user import-environment DISPLAY XAUTHORITY")
        self.assertLess(imported, text.index("exec /etc/X11/Xsession i3"))
        self.assertLess(imported, text.index("exec i3"))

    def test_a_foreign_xinitrc_is_kept_and_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = self.files_context(tmp)
            xinitrc = Path(tmp) / ".xinitrc"
            xinitrc.write_text("exec openbox\n")
            screen.ensure_xinitrc(ctx)
            self.assertEqual("exec openbox\n", xinitrc.read_text())
            self.assertTrue(any(".xinitrc" in line and "gelassen" in line for line in log),
                            list(log))

    def set_up(self, tmp):
        ctx, log = self.files_context(tmp, dry_run=True)
        with mock.patch("installer.system.os.geteuid", lambda: 1000), \
                mock.patch.object(screen.shutil, "which", lambda name: "/usr/bin/" + name):
            screen.set_up_screen(ctx)
        return log

    def test_a_dry_run_records_the_root_commands_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = self.set_up(tmp)
            commands = log.commands()
            self.assertIn(f"sudo install -D -m 644 /dev/stdin {AUTOLOGIN_TARGET}", commands)
            self.assertIn("sudo systemctl disable lightdm", commands)
            self.assertIn("sudo systemctl daemon-reload", commands)
            joined = "\n".join(log)
            self.assertIn("| ExecStart=-/sbin/agetty --autologin aaa --noclear %I $TERM",
                          joined)
            self.assertFalse((Path(tmp) / ".bash_profile").exists())
            self.assertFalse((Path(tmp) / ".xinitrc").exists())

    def test_lightdm_is_disabled_not_purged_and_the_log_says_when(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = self.set_up(tmp)
            self.assertFalse(any("purge" in c or "remove" in c for c in log.commands()))
            joined = "\n".join(log)
            self.assertIn("sudo apt purge lightdm", joined)
            self.assertIn("Neustart", joined)

    def test_the_drop_in_is_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            commands = self.set_up(tmp).commands()
            verify = [c for c in commands if c.startswith("systemd-analyze verify")]
            self.assertEqual(["systemd-analyze verify getty@tty1.service"], verify)
            self.assertLess(commands.index(f"sudo install -D -m 644 /dev/stdin "
                                           f"{AUTOLOGIN_TARGET}"),
                            commands.index(verify[0]))

    def test_problems_name_a_missing_block_and_missing_programs(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".bash_profile").write_text("export A=1\n")
            problems = screen.screen_problems(home, lambda name: None)
            joined = "\n".join(problems)
            self.assertIn(".bash_profile", joined)
            for program in ("startx", "i3", "Xorg"):
                self.assertIn(program, joined)

    def test_no_problems_when_all_is_there(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".bash_profile").write_text(screen.with_autologin_block(None))
            self.assertEqual([], screen.screen_problems(home, lambda name: "/usr/bin/" + name))


class MotionOnAnyMachine(unittest.TestCase):
    def test_the_drop_in_has_what_a3nuc2_was_missing(self):
        text = drop_in_text(Path("/home/aaa/a3-system/a3-motion/ui"))
        self.assertIn("Environment=DISPLAY=:0", text)
        self.assertIn("WorkingDirectory=/home/aaa/a3-system/a3-motion/ui\n", text)
        # Reset before set: a second ExecStart on a simple unit is an error.
        self.assertIn("ExecStart=\nExecStart=/home/aaa/a3-system/a3-motion/ui/build/", text)
        self.assertIn("ExecStartPre=\nExecStartPre=/home/aaa/a3-system/a3-motion/ui/"
                      "platform_config/a3-wait-for-the-screen", text)

    def firmware(self, mode, flashed_tree="", force=False):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp, {("motion", "flash_firmware"): mode,
                                     ("motion", "serial_port"): "/dev/ttyACM0"})
            tree = ctx.runner.output(["git", "rev-parse", "HEAD:firmware"],
                                     cwd=REPO / "a3-motion").strip()
            if flashed_tree == "current":
                ctx.state.set("motion", "firmware_tree", tree)
            if force:
                ctx.answers["flash_firmware"] = True
            Motion()._firmware(ctx)
            return [c for c in log.commands() if "upload" in c]

    def test_unchanged_firmware_is_not_flashed(self):
        self.assertEqual([], self.firmware("yes", flashed_tree="current"))

    def test_changed_firmware_is_flashed_when_allowed(self):
        flashed = self.firmware("yes")
        self.assertEqual(1, len(flashed))
        self.assertIn("--upload-port /dev/ttyACM0", flashed[0])

    def test_changed_firmware_is_left_when_switched_off(self):
        self.assertEqual([], self.firmware("no"))

    def test_ask_without_anyone_to_ask_does_not_flash(self):
        self.assertEqual([], self.firmware("ask"))

    def test_forced_flashes_even_unchanged(self):
        self.assertEqual(1, len(self.firmware("no", flashed_tree="current", force=True)))


def fake_serial_devices(root, devices):
    """/dev/serial/by-id and /sys/class/tty as udev and the kernel lay them out.

    devices: by-id name -> (tty, vendor, product, driver); driver "acm" puts
    the tty directly under the USB interface, "usb-serial" one level deeper.
    """
    by_id, dev, sys_tty = root / "by-id", root / "dev", root / "sys/class/tty"
    for d in (by_id, dev, sys_tty):
        d.mkdir(parents=True)
    for name, (tty, vendor, product, driver) in devices.items():
        (dev / tty).touch()
        (by_id / name).symlink_to(dev / tty)
        usb = root / "sys/devices" / name / "3-1"
        interface = usb / "3-1:1.0"
        device = interface / tty if driver == "usb-serial" else interface
        device.mkdir(parents=True)
        (usb / "idVendor").write_text(vendor + "\n")
        (usb / "idProduct").write_text(product + "\n")
        (sys_tty / tty).mkdir()
        (sys_tty / tty / "device").symlink_to(device)
    return by_id, sys_tty


PANEL_BRIDGE = ("1a86", "55d3")


class ThePanelIsFoundByItsUsbId(unittest.TestCase):
    """The tty number differs between machines; the USB ID does not."""

    def test_the_ids_come_from_the_board_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp) / "board.json"
            board.write_text(json.dumps({"build": {"hwids": [["0x1A86", "0x55D3"]]}}))
            self.assertEqual({PANEL_BRIDGE}, panel_usb_ids(board))

    def test_only_the_panel_whatever_its_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            by_id, sys_tty = fake_serial_devices(Path(tmp), {
                "usb-Raspberry_Pi_Pico-if00": ("ttyACM0", "2e8a", "000a", "acm"),
                "usb-1a86_USB_Single_Serial_5B7A-if00": ("ttyACM1", "1a86", "55d3", "acm"),
            })
            self.assertEqual([str(by_id / "usb-1a86_USB_Single_Serial_5B7A-if00")],
                             serial_candidates({PANEL_BRIDGE}, by_id, sys_tty))

    def test_a_usb_serial_tty_is_found_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            by_id, sys_tty = fake_serial_devices(Path(tmp), {
                "usb-wch-if00": ("ttyUSB0", "1a86", "55d3", "usb-serial"),
            })
            self.assertEqual(1, len(serial_candidates({PANEL_BRIDGE}, by_id, sys_tty)))

    def test_no_by_id_directory_is_no_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual([], serial_candidates({PANEL_BRIDGE}, Path(tmp) / "none",
                                                   Path(tmp)))

    def test_auto_flashes_the_one_panel(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp, {("motion", "serial_port"): "auto"})
            by_id, sys_tty = fake_serial_devices(Path(tmp) / "devs", {
                "usb-other-if00": ("ttyACM0", "2e8a", "000a", "acm"),
                "usb-panel-if00": ("ttyACM1", "1a86", "55d3", "acm"),
            })
            with mock.patch.object(motion, "BY_ID", by_id), \
                    mock.patch.object(motion, "SYS_TTY", sys_tty), \
                    mock.patch.object(motion, "panel_usb_ids", lambda _: {PANEL_BRIDGE}):
                Motion().flash(ctx, "tree")
            uploads = [c for c in log.commands() if "upload" in c]
            self.assertEqual(1, len(uploads))
            self.assertIn("--upload-port " + str(by_id / "usb-panel-if00"), uploads[0])


class MissingUnitsAreSaidPlainly(unittest.TestCase):
    def test_a_component_without_its_unit_is_a_role_error(self):
        from installer.roles.base import install_user_unit
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            with self.assertRaises(RoleError) as caught:
                install_user_unit(ctx, REPO / "stemdeck" / "no-such.service")
            self.assertIn("Pin", str(caught.exception))


class StateIsKept(unittest.TestCase):
    def test_written_and_read_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state"
            State(path).set("motion", "firmware_tree", "abc")
            self.assertEqual("abc", State(path).get("motion", "firmware_tree"))

    def test_a_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state"
            State(path).set("motion", "firmware_tree", "abc", dry_run=True)
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
