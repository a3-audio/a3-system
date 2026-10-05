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
from installer.cli import install_roles, update_version, where_problems  # noqa: E402
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


class UpdateWithoutAVersion(unittest.TestCase):
    TAGS = ["v03.1", "v03.0"]

    def test_a_named_version_wins(self):
        self.assertEqual("v03.0", update_version("v03.0", "main", self.TAGS, "main"))

    def test_a_stored_branch_stays(self):
        self.assertEqual("main", update_version("", "main", self.TAGS, "v03.0"))

    def test_a_stored_tag_moves_to_the_newest(self):
        self.assertEqual("v03.1", update_version("", "v03.0", self.TAGS, "v03.0"))

    def test_nothing_stored_takes_the_newest_tag(self):
        self.assertEqual("v03.1", update_version("", "", self.TAGS, "main"))

    def test_without_tags_it_stays_where_it_is(self):
        self.assertEqual("main", update_version("", "", [], "main"))


class ABranchCatchesUp(unittest.TestCase):
    def commands(self, version, origin_has_it=True):
        log = Log()
        runner = Runner(dry_run=True, log=log)
        found = mock.Mock(return_value="abc\n") if origin_has_it else \
            mock.Mock(side_effect=Exception("unknown ref"))
        with mock.patch.object(runner, "output", found):
            release.catch_up(runner, REPO, version)
        return [c.split("  (in ")[0] for c in log.commands()], found

    def test_a_branch_fast_forwards_to_origin(self):
        commands, _ = self.commands("main")
        self.assertEqual(["git merge --ff-only --quiet origin/main"], commands)

    def test_a_tag_stays_and_asks_nothing(self):
        commands, found = self.commands("v03.0")
        self.assertEqual([], commands)
        found.assert_not_called()

    def test_a_branch_origin_lacks_stays(self):
        self.assertEqual([], self.commands("local-only", origin_has_it=False)[0])


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
    "libflac-dev", "libvorbis-dev", "libogg-dev", "libjack-jackd2-dev",
    # its unit waits for JACK with jack_wait (stemdeck a521412), on a
    # machine without the Core too
    "jack-example-tools",
    # its on-screen keyboard starts onboard
    "onboard")
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



# -- roles that leave -----------------------------------------------------------

import datetime  # noqa: E402

TODAY = datetime.date.today().isoformat()


class FailingRole(FakeRole):
    def install(self, ctx):
        raise RoleError("kaputt")


class LeavingRole(FakeRole):
    """A fake role that can leave: says what goes, logs its uninstall."""

    def __init__(self, name, needs_screen=False, fails=False):
        super().__init__(name, needs_screen=needs_screen)
        self.fails = fails

    def leaving_lines(self, ctx):
        return [f"  unit-of-{self.name}.service"]

    def uninstall(self, ctx):
        if self.fails:
            raise RoleError("geht nicht weg")
        ctx.runner.log(f"$ uninstall {self.name}")


class AnsweringPrompter(Prompter):
    """Someone at the machine, answering every yes/no with `answer`."""

    interactive = True

    def __init__(self, answer):
        self.answer = answer
        self.asked = []

    def yesno(self, question, default):
        self.asked.append((question, default))
        return self.answer


def nothing_found(_user_units):
    return []


def with_fakes(roles):
    by_name = {r.name: r for r in roles}
    return (mock.patch("installer.cli.BY_NAME", by_name),
            mock.patch("installer.leave.BY_NAME", by_name),
            mock.patch("installer.leave.ALL", tuple(roles)),
            mock.patch("installer.roles.BY_NAME", by_name),
            mock.patch("installer.roles.ALL", tuple(roles)))


def apply_fakes(roles, chosen, installed, prompter=None, allow=None, platform="debian"):
    """apply_roles on fake roles, dry run, with `installed` in the state."""
    from installer.cli import apply_roles
    with tempfile.TemporaryDirectory() as tmp:
        settings = {("uninstall", "allow"): allow} if allow else {}
        ctx, log = context(tmp, settings)
        ctx.platform = platform
        if prompter:
            ctx.prompter = prompter
        for name in installed:
            ctx.state.set("installed", name, "2026-10-01")
        patches = with_fakes(roles)
        for p in patches:
            p.start()
        try:
            left, installed_rows = apply_roles(ctx, chosen, discover=nothing_found)
            results = left + installed_rows
        finally:
            for p in patches:
                p.stop()
        recorded = {n: ctx.state.get("installed", n) for n in installed}
        return [c.removeprefix("sudo ") for c in log.commands()], results, list(log), recorded


class InstalledRolesAreRecorded(unittest.TestCase):
    def install(self, roles, dry_run=False):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            ctx.runner.dry_run = dry_run
            ctx.platform = "other"
            by_name = {r.name: r for r in roles}
            with mock.patch("installer.cli.BY_NAME", by_name), \
                    mock.patch("installer.roles.BY_NAME", by_name), \
                    mock.patch("installer.roles.ALL", tuple(roles)):
                install_roles(ctx, [r.name for r in roles])
            path = ctx.state.path
            return State(path) if path.exists() else None

    def test_after_a_successful_install_with_the_date(self):
        state = self.install([FakeRole("a"), FakeRole("b")])
        self.assertEqual(TODAY, state.get("installed", "a"))
        self.assertEqual(TODAY, state.get("installed", "b"))

    def test_not_after_a_failed_one_nor_the_ones_after_it(self):
        state = self.install([FakeRole("a"), FailingRole("b"), FakeRole("c")])
        self.assertEqual(TODAY, state.get("installed", "a"))
        self.assertEqual("", state.get("installed", "b"))
        self.assertEqual("", state.get("installed", "c"))

    def test_a_dry_run_writes_nothing(self):
        self.assertIsNone(self.install([FakeRole("a")], dry_run=True))


class RolesFoundOnAMachineSetUpBefore(unittest.TestCase):
    """No [installed] section: the roles are taken from what is there."""

    def discover(self, core, stemdeck, motion):
        from installer.leave import discover_roles
        with tempfile.TemporaryDirectory() as tmp:
            units = Path(tmp)
            if stemdeck:
                (units / "stemdeck.service").touch()
            if motion:
                (units / "a3-motion.service").touch()
            return discover_roles(units, core_installed=lambda: core)

    def test_every_combination(self):
        import itertools
        for core, stemdeck, motion in itertools.product((False, True), repeat=3):
            with self.subTest(core=core, stemdeck=stemdeck, motion=motion):
                expected = [n for n, there in (("core", core), ("stemdeck", stemdeck),
                                               ("motion", motion)) if there]
                self.assertEqual(expected, self.discover(core, stemdeck, motion))

    def test_the_package_counts_when_dpkg_says_installed(self):
        from installer.leave import package_installed
        self.assertTrue(package_installed("a3-core", lambda _: "install ok installed"))
        self.assertTrue(package_installed("a3-core", lambda _: "hold ok installed"))
        self.assertFalse(package_installed("a3-core", lambda _: "deinstall ok config-files"))
        self.assertFalse(package_installed("a3-core", lambda _: None))

    def test_a_recorded_section_wins_even_when_empty(self):
        from installer.leave import installed_now
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            found = lambda _units: ["core", "stemdeck"]  # noqa: E731
            self.assertEqual((["core", "stemdeck"], True), installed_now(ctx, found))
            ctx.state.set("installed", "motion", "2026-10-01")
            self.assertEqual((["motion"], False), installed_now(ctx, found))
            ctx.state.remove("installed", "motion")
            self.assertEqual(([], False), installed_now(ctx, found))

    def test_found_roles_are_recorded_after_the_dialog(self):
        from installer.cli import apply_roles
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            roles = [LeavingRole("core"), LeavingRole("stemdeck")]
            patches = with_fakes(roles)
            for p in patches:
                p.start()
            try:
                apply_roles(ctx, ["stemdeck"], discover=lambda _u: ["core", "stemdeck"])
            finally:
                for p in patches:
                    p.stop()
            # Not allowed to leave (no [uninstall] allow), so both stay recorded.
            self.assertEqual(TODAY, ctx.state.get("installed", "core"))
            self.assertEqual(TODAY, ctx.state.get("installed", "stemdeck"))


class Deselected(unittest.TestCase):
    def test_installed_minus_chosen_in_install_order(self):
        from installer.leave import deselected
        self.assertEqual(["core", "motion"],
                         deselected(["core", "stemdeck", "motion"], ["stemdeck"]))

    def test_chosen_but_not_installed_is_nothing_to_leave(self):
        from installer.leave import deselected
        self.assertEqual([], deselected(["stemdeck"], ["stemdeck", "motion"]))


CORE_UNITS_SHIPPED = REPO / ("a3-core/platform-config/debian-x86_64/a3-core/home/aaa/"
                             ".local/share/a3-core/config/systemd/user")


def uninstall_commands(name, chosen=(), installed=(), home_files=()):
    """A role's uninstall in a dry run: the commands, without sudo, and the log."""
    with tempfile.TemporaryDirectory() as tmp:
        settings = {("roles", r): "yes" for r in chosen}
        ctx, log = context(tmp, settings)
        for role in installed:
            ctx.state.set("installed", role, "2026-10-01", dry_run=True)
        for rel in home_files:
            (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(tmp) / rel).touch()
        BY_NAME[name].uninstall(ctx)
        units = str(ctx.user_units)
        commands = [c.removeprefix("sudo ").replace(units, "~units").replace(tmp, "~")
                    for c in log.commands()]
        return commands, list(log)


class CoreLeaves(unittest.TestCase):
    def test_its_units_stop_and_are_disabled(self):
        from installer.roles.core import CORE_UNITS
        commands, _ = uninstall_commands("core")
        for unit in CORE_UNITS:
            self.assertIn(f"systemctl --user disable --now {unit}", commands)

    def test_the_units_are_the_ones_the_package_ships(self):
        from installer.roles.core import CORE_UNITS
        if not CORE_UNITS_SHIPPED.is_dir():
            self.skipTest("a3-core is not checked out here")
        shipped = {p.name for p in CORE_UNITS_SHIPPED.glob("*.service")}
        self.assertEqual(shipped, set(CORE_UNITS))

    def test_unheld_and_removed_never_purged(self):
        commands, _ = uninstall_commands("core")
        remove = "env DEBIAN_FRONTEND=noninteractive apt-get remove -y a3-core"
        self.assertIn(remove, commands)
        self.assertLess(commands.index("apt-mark unhold a3-core"), commands.index(remove))
        last_disable = max(i for i, c in enumerate(commands) if "disable --now" in c)
        self.assertLess(last_disable, commands.index(remove))
        self.assertFalse(any("purge" in c for c in commands), commands)

    def test_the_ssh_keys_the_package_ships_are_kept(self):
        """dpkg removes ~/.ssh/authorized_keys with the package; without it a
        machine run over ssh is locked out."""
        commands, _ = uninstall_commands("core", home_files=[".ssh/authorized_keys"])
        remove = next(i for i, c in enumerate(commands) if "apt-get remove" in c)
        keep = next(i for i, c in enumerate(commands) if c.startswith("cp -p ~/.ssh/authorized_keys"))
        back = next(i for i, c in enumerate(commands) if c.startswith("mv ") and "authorized_keys" in c)
        self.assertLess(keep, remove)
        self.assertLess(remove, back)

    def test_no_keys_no_copy(self):
        commands, _ = uninstall_commands("core")
        self.assertFalse(any("authorized_keys" in c for c in commands), commands)


class StemDeckLeaves(unittest.TestCase):
    def test_without_a_core_its_zita_units_go_too(self):
        commands, _ = uninstall_commands("stemdeck")
        for unit in ("stemdeck.service", "zita-n2j.service", "zita-j2n.service"):
            self.assertIn(f"systemctl --user disable --now {unit}", commands)
            self.assertIn(f"rm -f ~units/{unit}", commands)
        self.assertEqual("systemctl --user daemon-reload", commands[-1])

    def test_with_the_core_chosen_only_stemdeck(self):
        commands, _ = uninstall_commands("stemdeck", chosen=["core"])
        self.assertIn("systemctl --user disable --now stemdeck.service", commands)
        self.assertIn("rm -f ~units/stemdeck.service", commands)
        self.assertFalse(any("zita" in c for c in commands), commands)

    def test_a_core_still_installed_keeps_its_zita_files(self):
        """The zita files then are the Core's; the Core stops them when it leaves."""
        commands, _ = uninstall_commands("stemdeck", installed=["core"])
        self.assertFalse(any("zita" in c for c in commands), commands)

    def test_build_and_library_stay(self):
        commands, _ = uninstall_commands("stemdeck")
        self.assertFalse(any("rm -rf" in c or "build-make" in c for c in commands), commands)


class MotionLeaves(unittest.TestCase):
    def test_unit_and_drop_in_go(self):
        commands, _ = uninstall_commands("motion")
        self.assertEqual([
            "systemctl --user disable --now a3-motion.service",
            "rm -f ~units/a3-motion.service",
            "rm -f ~units/a3-motion.service.d/a3-system.conf",
            "rmdir --ignore-fail-on-non-empty ~units/a3-motion.service.d",
            "systemctl --user daemon-reload",
        ], commands)

    def test_the_drop_in_is_the_one_install_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            ctx.runner.dry_run = False
            from installer.roles.base import write_drop_in
            written = write_drop_in(ctx, "a3-motion.service", "a3-system.conf", "x")
            self.assertIn(written, BY_NAME["motion"].leaving_files(ctx))


class TheDialogBeforeAnythingLeaves(unittest.TestCase):
    def test_it_lists_units_package_and_what_stays(self):
        from installer.leave import leaving_text
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp)
            text = leaving_text(ctx, ["core", "motion"])
        for expected in ("a3-main.service", "a3-jack.service", "a3-reaper.service",
                         "a3-core", "a3-motion.service", "a3-system.conf", "Bleibt"):
            self.assertIn(expected, text)
        self.assertIn("Pakete", text)

    def test_asked_with_no_as_default(self):
        prompter = AnsweringPrompter(False)
        apply_fakes([LeavingRole("a"), LeavingRole("b")], ["b"], ["a", "b"], prompter)
        self.assertEqual(1, len(prompter.asked))
        question, default = prompter.asked[0]
        self.assertFalse(default)
        self.assertIn("unit-of-a.service", question)

    def test_no_changes_nothing_and_the_install_goes_on(self):
        commands, results, log, recorded = apply_fakes(
            [LeavingRole("a"), LeavingRole("b")], ["b"], ["a", "b"], AnsweringPrompter(False))
        self.assertNotIn("uninstall a", commands)
        self.assertIn("install b", commands)
        self.assertEqual("2026-10-01", recorded["a"])
        self.assertTrue(any("trotzdem" in line for line in log), log)

    def test_yes_removes_and_forgets_the_role(self):
        commands, results, _, recorded = apply_fakes(
            [LeavingRole("a"), LeavingRole("b")], ["b"], ["a", "b"], AnsweringPrompter(True))
        self.assertIn("uninstall a", commands)
        self.assertEqual("", recorded["a"])
        self.assertIn(("a", "entfernt"), results)

    def test_a_failed_uninstall_keeps_the_record(self):
        _, results, _, recorded = apply_fakes(
            [LeavingRole("a", fails=True), LeavingRole("b")], ["b"], ["a", "b"],
            AnsweringPrompter(True))
        self.assertEqual("2026-10-01", recorded["a"])
        self.assertTrue(any(n == "a" and r.startswith("FEHLER") for n, r in results), results)

    def test_nothing_to_leave_asks_nothing(self):
        prompter = AnsweringPrompter(True)
        apply_fakes([LeavingRole("a")], ["a"], ["a"], prompter)
        self.assertEqual([], prompter.asked)


class WithoutQuestionsOnlyTheFileLetsARoleLeave(unittest.TestCase):
    """--config FILE and --update: no one to ask, so [uninstall] allow decides."""

    def test_without_allow_nothing_leaves_but_it_is_listed(self):
        commands, results, log, recorded = apply_fakes(
            [LeavingRole("a"), LeavingRole("b")], ["b"], ["a", "b"])
        self.assertNotIn("uninstall a", commands)
        self.assertIn("install b", commands)
        self.assertEqual("2026-10-01", recorded["a"])
        joined = "\n".join(log)
        self.assertIn("unit-of-a.service", joined)
        self.assertIn("allow = yes", joined)

    def test_with_allow_it_leaves(self):
        commands, _, _, recorded = apply_fakes(
            [LeavingRole("a"), LeavingRole("b")], ["b"], ["a", "b"], allow="yes")
        self.assertIn("uninstall a", commands)
        self.assertEqual("", recorded["a"])

    def test_the_setting_defaults_to_no(self):
        self.assertFalse(Settings("/nonexistent/install.conf").flag("uninstall", "allow"))


class RolesLeaveBeforeAnythingInstalls(unittest.TestCase):
    def test_before_the_packages_the_screen_and_the_first_install(self):
        roles = [LeavingRole("a"), FakeRole("b", ("x",), needs_screen=True)]
        commands, _, _, _ = apply_fakes(roles, ["b"], ["a"], allow="yes")
        leave = commands.index("uninstall a")
        self.assertLess(leave, commands.index(
            "env DEBIAN_FRONTEND=noninteractive apt-get install -y x"))
        self.assertLess(leave, commands.index("systemctl disable lightdm"))
        self.assertLess(leave, commands.index("install b"))

    def test_in_reverse_install_order(self):
        """The Core last: StemDeck's leaving asks whether a Core is still there."""
        roles = [LeavingRole("a"), LeavingRole("b"), LeavingRole("c")]
        commands, _, _, _ = apply_fakes(roles, ["c"], ["a", "b", "c"], allow="yes")
        self.assertLess(commands.index("uninstall b"), commands.index("uninstall a"))


class TheAutologinStaysWhenTheLastScreenRoleLeaves(unittest.TestCase):
    def test_named_with_how_to_remove_it(self):
        roles = [LeavingRole("a", needs_screen=True), LeavingRole("b")]
        commands, _, log, _ = apply_fakes(roles, ["b"], ["a"], allow="yes")
        joined = "\n".join(log)
        self.assertIn(AUTOLOGIN_TARGET, joined)
        self.assertFalse(any(AUTOLOGIN_TARGET in c for c in commands), commands)

    def test_not_named_while_a_screen_role_stays(self):
        roles = [LeavingRole("a", needs_screen=True), LeavingRole("b", needs_screen=True)]
        _, _, log, _ = apply_fakes(roles, ["b"], ["a"], allow="yes")
        self.assertFalse(any("tty1" in line and "bleibt" in line for line in log), log)



class ALongQuestionScrolls(unittest.TestCase):
    """The leaving dialog lists every unit; a 12-line box would cut it off."""

    def asked(self, question):
        from installer.prompt import WhiptailPrompter
        prompter = WhiptailPrompter()
        calls = []
        prompter._run = lambda args: calls.append(args) or (1, "")
        prompter.yesno(question, False)
        return calls[0]

    def test_a_long_question_gets_a_tall_scrolling_box(self):
        args = self.asked("\n".join(f"line {n}" for n in range(40)))
        self.assertIn("--scrolltext", args)
        self.assertEqual("24", args[args.index("--yesno") + 2])

    def test_a_short_one_keeps_its_box(self):
        args = self.asked("So installieren?")
        self.assertEqual("12", args[args.index("--yesno") + 2])


# The real file's shape (~/.config/StemDeck/StemDeck.settings, 2026-10-05):
# a JUCE PropertiesFile, one VALUE per key; some carry XML, as a child
# element or escaped in val.
STEMDECK_SETTINGS = """<?xml version="1.0" encoding="UTF-8"?>

<PROPERTIES>
  <VALUE name="stemFolder" val="/home/aaa/stems"/>
  <VALUE name="windowState" val="fs -366 32 1500 960 frame 0 0 0 0"/>
  <VALUE name="syncSource" val="pio"/>
  <VALUE name="escaped" val="&lt;?xml version=&quot;1.0&quot;?&gt;&lt;A b=&quot;c &amp;amp; d&quot;/&gt;"/>
  <VALUE name="audioDeviceState">
    <DEVICESETUP deviceType="ALSA" audioOutputDeviceName="" audioInputDeviceName=""/>
  </VALUE>
</PROPERTIES>
"""


def stemdeck_values(text):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(text)
    return root.tag, {v.get("name"): (v.get("val"), [ET.tostring(c) for c in v])
                      for v in root.findall("VALUE")}


class NotAsked(Prompter):
    """--update and --config: nobody there, and nothing may be asked."""

    def text(self, question, default):
        raise AssertionError(f"asked: {question}")


class TextAnswers(Prompter):
    interactive = True

    def __init__(self, answer):
        self.answer = answer
        self.asked = []

    def text(self, question, default):
        self.asked.append((question, default))
        return self.answer or default


class StemDeckAsksForItsLibrary(unittest.TestCase):
    def configure(self, prompter, stored=None, settings_file=None):
        from installer.roles.stemdeck import StemDeck
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp, {("stemdeck", "library"): stored} if stored else {})
            ctx.prompter = prompter
            if settings_file is not None:
                path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
                path.parent.mkdir(parents=True)
                path.write_text(settings_file)
            StemDeck().configure(ctx)
            return ctx.settings.get("stemdeck", "library"), tmp

    def test_the_default_is_the_folder_stemdeck_uses_now(self):
        prompter = TextAnswers("")
        stored, _ = self.configure(prompter, settings_file=STEMDECK_SETTINGS)
        self.assertEqual("/home/aaa/stems", prompter.asked[0][1])
        self.assertEqual("/home/aaa/stems", stored)

    def test_without_a_settings_file_the_default_is_stems_in_home(self):
        prompter = TextAnswers("")
        stored, tmp = self.configure(prompter)
        self.assertEqual(str(Path(tmp) / "stems"), prompter.asked[0][1])
        self.assertEqual(str(Path(tmp) / "stems"), stored)

    def test_the_question_names_the_stem_library(self):
        prompter = TextAnswers("")
        self.configure(prompter)
        self.assertIn("Stem-Bibliothek", prompter.asked[0][0])

    def test_the_answer_is_kept_in_the_installer_settings(self):
        stored, _ = self.configure(TextAnswers("/data/stems"),
                                   settings_file=STEMDECK_SETTINGS)
        self.assertEqual("/data/stems", stored)

    def test_a_home_relative_answer_is_made_absolute(self):
        """StemDeck takes an absolute path only (MainComponent.cpp)."""
        stored, tmp = self.configure(TextAnswers("~/musik/stems"))
        self.assertEqual(str(Path(tmp) / "musik" / "stems"), stored)

    def test_stemdecks_own_choice_comes_before_the_stored_answer(self):
        """The DJ may have changed it in StemDeck since the last install."""
        prompter = TextAnswers("")
        self.configure(prompter, stored="/data/stems", settings_file=STEMDECK_SETTINGS)
        self.assertEqual("/home/aaa/stems", prompter.asked[0][1])

    def test_the_stored_answer_when_stemdeck_names_none(self):
        prompter = TextAnswers("")
        self.configure(prompter, stored="/data/stems")
        self.assertEqual("/data/stems", prompter.asked[0][1])

    def test_a_relative_stem_folder_in_stemdeck_is_no_choice(self):
        prompter = TextAnswers("")
        self.configure(prompter, stored="/data/stems", settings_file=STEMDECK_SETTINGS
                       .replace('val="/home/aaa/stems"', 'val="stems"'))
        self.assertEqual("/data/stems", prompter.asked[0][1])

    def test_update_and_config_keep_what_stemdeck_uses(self):
        stored, _ = self.configure(NotAsked(), stored="/data/stems",
                                   settings_file=STEMDECK_SETTINGS)
        self.assertEqual("/home/aaa/stems", stored)

    def test_update_and_config_take_the_stored_answer_when_stemdeck_has_none(self):
        stored, _ = self.configure(NotAsked(), stored="/data/stems")
        self.assertEqual("/data/stems", stored)

    def test_nothing_stored_and_nobody_to_ask_takes_the_default(self):
        stored, _ = self.configure(NotAsked(), settings_file=STEMDECK_SETTINGS)
        self.assertEqual("/home/aaa/stems", stored)


class TheLibraryGoesIntoStemDecksSettings(unittest.TestCase):
    def rewrite(self, text, folder="/data/stems"):
        from installer.roles.stemdeck import with_stem_folder
        return with_stem_folder(text, folder)

    def test_only_the_stem_folder_changes(self):
        tag, before = stemdeck_values(STEMDECK_SETTINGS)
        after_tag, after = stemdeck_values(self.rewrite(STEMDECK_SETTINGS))
        self.assertEqual(("PROPERTIES", "PROPERTIES"), (tag, after_tag))
        self.assertEqual("/data/stems", after.pop("stemFolder")[0])
        before.pop("stemFolder")
        self.assertEqual(before, after)

    def test_the_xml_values_survive(self):
        _, after = stemdeck_values(self.rewrite(STEMDECK_SETTINGS))
        self.assertEqual('<?xml version="1.0"?><A b="c &amp; d"/>', after["escaped"][0])
        self.assertIn(b'deviceType="ALSA"', after["audioDeviceState"][1][0])

    def test_a_missing_file_gets_just_the_stem_folder(self):
        tag, values = stemdeck_values(self.rewrite(None))
        self.assertEqual("PROPERTIES", tag)
        self.assertEqual({"stemFolder": ("/data/stems", [])}, values)

    def test_a_missing_entry_is_added(self):
        text = STEMDECK_SETTINGS.replace(
            '  <VALUE name="stemFolder" val="/home/aaa/stems"/>\n', "")
        _, values = stemdeck_values(self.rewrite(text))
        self.assertEqual("/data/stems", values["stemFolder"][0])
        self.assertEqual("pio", values["syncSource"][0])

    def test_it_starts_with_an_xml_declaration(self):
        self.assertTrue(self.rewrite(None).startswith('<?xml version="1.0" encoding="UTF-8"?>'))

    def test_an_unreadable_file_is_left_alone(self):
        with self.assertRaises(RoleError):
            self.rewrite("<PROPERTIES><VALUE")


class RecordingRunner(Runner):
    """Not a dry run, but runs nothing: the files are written, the
    commands only logged (no systemctl against this machine's StemDeck)."""

    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        self.log("$ " + " ".join(str(a) for a in args))
        return 0


class StemDeckInstallsItsLibrary(unittest.TestCase):
    def install(self, dry_run, settings_file=STEMDECK_SETTINGS, roles=("core",)):
        from installer.roles import stemdeck
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        library = Path(tmp) / "data" / "stems"
        ctx, log = context(tmp, {("stemdeck", "library"): str(library),
                                 **{("roles", r): "yes" for r in roles}})
        if not dry_run:
            ctx.runner = RecordingRunner(log=log)
        path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
        if settings_file is not None:
            path.parent.mkdir(parents=True)
            path.write_text(settings_file)
        with mock.patch.object(stemdeck, "ensure_juce", lambda _ctx: Path("/juce")):
            stemdeck.StemDeck().install(ctx)
        return log, path, library

    def test_stop_then_write_then_start(self):
        log, _, library = self.install(dry_run=False)
        lines = [line for line in log
                 if "stemdeck.service" in line or "stemFolder" in line]
        stop = lines.index("$ systemctl --user stop stemdeck.service")
        write = next(i for i, line in enumerate(lines) if "stemFolder" in line)
        restart = lines.index("$ systemctl --user restart stemdeck.service")
        self.assertLess(stop, write)
        self.assertLess(write, restart)

    def test_the_folder_is_made_and_named_in_stemdecks_settings(self):
        _, path, library = self.install(dry_run=False)
        self.assertTrue(library.is_dir())
        _, values = stemdeck_values(path.read_text())
        self.assertEqual(str(library), values["stemFolder"][0])
        self.assertEqual("pio", values["syncSource"][0])

    def test_a_missing_settings_file_is_made(self):
        _, path, library = self.install(dry_run=False, settings_file=None)
        _, values = stemdeck_values(path.read_text())
        self.assertEqual({"stemFolder": (str(library), [])}, values)

    def test_a_dry_run_writes_nothing_and_says_what_it_would(self):
        log, path, library = self.install(dry_run=True)
        self.assertFalse(library.exists())
        self.assertEqual(STEMDECK_SETTINGS, path.read_text())
        self.assertTrue(any(str(library) in line and "stemFolder" in line for line in log))
        self.assertIn("systemctl --user stop stemdeck.service", log.commands())


class AnUnreadableSettingsFileIsNotADarkScreen(unittest.TestCase):
    def test_stemdeck_is_started_again_and_the_file_left(self):
        from installer.roles import stemdeck
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp, {("stemdeck", "library"): str(Path(tmp) / "stems")})
            ctx.runner = RecordingRunner(log=log)
            path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
            path.parent.mkdir(parents=True)
            path.write_text("<PROPERTIES><VALUE")
            with self.assertRaises(RoleError):
                stemdeck.StemDeck()._hand_over_library(ctx)
            self.assertEqual(["systemctl --user stop stemdeck.service",
                              "systemctl --user start stemdeck.service"], log.commands())
            self.assertEqual("<PROPERTIES><VALUE", path.read_text())


class WithoutQuestionsStemDecksChoiceStays(unittest.TestCase):
    """--update and --config write stemFolder only where StemDeck has none."""

    def run_role(self, settings_file, stored=None):
        from installer.roles import stemdeck
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {("stemdeck", "library"): stored} if stored else {})
        ctx.runner = RecordingRunner(log=log)
        ctx.prompter = NotAsked()
        path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
        if settings_file is not None:
            path.parent.mkdir(parents=True)
            path.write_text(settings_file)
        role = stemdeck.StemDeck()
        role.configure(ctx)
        with mock.patch.object(stemdeck, "ensure_juce", lambda _ctx: Path("/juce")):
            role.install(ctx)
        return log, path, Path(tmp), ctx

    def test_an_existing_stem_folder_is_neither_written_nor_stopped_for(self):
        log, path, _, ctx = self.run_role(STEMDECK_SETTINGS, stored="/data/stems")
        self.assertNotIn("systemctl --user stop stemdeck.service", log.commands())
        self.assertEqual(STEMDECK_SETTINGS, path.read_text())
        self.assertTrue(any("StemDeck nutzt bereits /home/aaa/stems" in line
                            for line in log))
        self.assertEqual("/home/aaa/stems", ctx.settings.get("stemdeck", "library"))

    def test_a_different_library_in_the_file_is_said_not_applied(self):
        log, *_ = self.run_role(STEMDECK_SETTINGS, stored="/data/stems")
        self.assertTrue(any("/data/stems" in line and "nicht übernommen" in line
                            for line in log))

    def test_without_a_settings_file_it_writes(self):
        log, path, home, _ = self.run_role(None, stored=None)
        self.assertIn("systemctl --user stop stemdeck.service", log.commands())
        _, values = stemdeck_values(path.read_text())
        self.assertEqual(str(home / "stems"), values["stemFolder"][0])
        self.assertTrue((home / "stems").is_dir())

    def test_without_a_stem_folder_entry_it_writes_the_stored_one(self):
        text = STEMDECK_SETTINGS.replace(
            '  <VALUE name="stemFolder" val="/home/aaa/stems"/>\n', "")
        log, path, home, _ = self.run_role(text, stored=None)
        _, values = stemdeck_values(path.read_text())
        self.assertEqual(str(home / "stems"), values["stemFolder"][0])
        self.assertEqual("pio", values["syncSource"][0])

    def test_a_relative_stem_folder_is_replaced(self):
        library = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, library)
        log, path, _, _ = self.run_role(
            STEMDECK_SETTINGS.replace('val="/home/aaa/stems"', 'val="stems"'),
            stored=library)
        self.assertIn("systemctl --user stop stemdeck.service", log.commands())
        self.assertEqual(library, stemdeck_values(path.read_text())[1]["stemFolder"][0])


class StemDeckBringsTheKeyboard(unittest.TestCase):
    def test_onboard_is_among_its_packages(self):
        """StemDeck's on-screen keyboard starts onboard."""
        self.assertIn("onboard", BY_NAME["stemdeck"].packages)


if __name__ == "__main__":
    unittest.main()
