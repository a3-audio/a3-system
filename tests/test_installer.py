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
from installer.roles import core, motion, screen  # noqa: E402
from installer.roles.motion import Motion, panel_usb_ids, serial_candidates  # noqa: E402
from installer.settings import Settings  # noqa: E402
from installer.system import CommandFailed, Runner  # noqa: E402


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

    def test_the_network_answers_are_marked_as_the_installers(self):
        """seen alone is no sign: package 1.0.0 left it set, and the postinst
        took it for the installer's answer (a3-core#68). The postinst takes
        the network answers only with this marker, and clears it."""
        for answer in ("yes", "no"):
            self.assertIn("a3-core a3-core/preseeded boolean true",
                          self.lines(configure_network=answer), answer)


PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEXAMPLEexampleEXAMPLEexample0123456789ab you@laptop"


class AnSshKeyFromTheCommandLine(unittest.TestCase):
    """install --ssh-key FILE hands one public key to the a3-core package's
    question a3-core/ssh-key, which a noninteractive install never asks."""

    def key_file(self, text):
        tmp = tempfile.mkdtemp()
        path = Path(tmp) / "key.pub"
        path.write_text(text)
        return path

    def test_one_public_key_line_is_read(self):
        self.assertEqual(PUBLIC_KEY, core.read_ssh_key(self.key_file(PUBLIC_KEY + "\n")))

    def test_a_private_key_is_refused(self):
        private = ("-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAA\n"
                   "-----END OPENSSH PRIVATE KEY-----\n")
        with self.assertRaisesRegex(RoleError, "privat"):
            core.read_ssh_key(self.key_file(private))

    def test_several_keys_are_refused(self):
        with self.assertRaisesRegex(RoleError, "eine Zeile"):
            core.read_ssh_key(self.key_file(PUBLIC_KEY + "\n" + PUBLIC_KEY + "\n"))

    def test_options_in_front_of_the_key_are_refused(self):
        with self.assertRaises(RoleError):
            core.read_ssh_key(self.key_file('command="/bin/sh" ' + PUBLIC_KEY))

    def test_a_missing_file_is_said_plainly(self):
        with self.assertRaisesRegex(RoleError, "nicht lesen"):
            core.read_ssh_key(Path("/nonexistent/key.pub"))

    def test_the_key_is_preseeded_and_marked_seen(self):
        lines = preseed_lines(Settings("/nonexistent/install.conf"), None,
                              ssh_key=PUBLIC_KEY).splitlines()
        self.assertIn(f"a3-core a3-core/ssh-key string {PUBLIC_KEY}", lines)
        self.assertIn("a3-core a3-core/ssh-key seen true", lines)

    def test_without_the_option_the_question_is_left_alone(self):
        text = preseed_lines(Settings("/nonexistent/install.conf"), None)
        self.assertNotIn("ssh-key", text)

    def test_the_core_install_hands_the_key_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp)
            ctx.answers["ssh_key"] = PUBLIC_KEY
            with mock.patch.object(core, "build_package", return_value=Path(tmp) / "a3-core.deb"):
                BY_NAME["core"].install(ctx)
        self.assertIn(f"    | a3-core a3-core/ssh-key string {PUBLIC_KEY}", "\n".join(log))

    def test_a_bad_key_stops_the_installer_before_anything_runs(self):
        from installer import cli
        bad = self.key_file("not a key\n")
        with mock.patch.object(cli, "Runner") as runner, \
                mock.patch("sys.stderr", new_callable=lambda: __import__("io").StringIO()) as err:
            self.assertEqual(2, cli.main(["--dry-run", "--ssh-key", str(bad)]))
        runner.assert_not_called()
        self.assertIn("--ssh-key", err.getvalue())


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
    # without the Core, qjackctl-stemdeck.service runs QjackCtl with
    # StemDeck's patchbay (stemdeck .config/rncbc.org)
    "qjackctl")
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

    def test_core_installs_the_screen_and_the_analyzer_build_and_mixer_none(self):
        from installer.roles.base import SCREEN_PACKAGES
        from installer.roles.core import ANALYZER_BUILD_PACKAGES
        self.assertEqual(SCREEN_PACKAGES + ANALYZER_BUILD_PACKAGES, BY_NAME["core"].packages)
        self.assertEqual((), BY_NAME["mixer"].packages)

    def test_stemdeck_alone_gets_nothing_of_motion(self):
        packages = needed_packages(["stemdeck"])
        self.assertEqual(set(), set(STEMDECK_NEEDS) - set(packages))
        self.assertEqual(set(), {"libgsl-dev", "libgpiod-dev", "libserial-dev"} & set(packages))

    def test_core_alone_installs_the_screen_and_the_analyzer_build(self):
        from installer.roles.core import ANALYZER_BUILD_PACKAGES
        self.assertEqual(sorted(set(SCREEN_NEEDS) | set(ANALYZER_BUILD_PACKAGES)),
                         needed_packages(["core"]))

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
            return discover_roles(units, core_installed=lambda: core,
                                  stemdeck_installed=lambda: False,
                                  motion_installed=lambda: False)

    def test_every_combination(self):
        import itertools
        for core, stemdeck, motion in itertools.product((False, True), repeat=3):
            with self.subTest(core=core, stemdeck=stemdeck, motion=motion):
                expected = [n for n, there in (("core", core), ("stemdeck", stemdeck),
                                               ("motion", motion)) if there]
                self.assertEqual(expected, self.discover(core, stemdeck, motion))

    def test_stemdeck_is_found_by_its_package_too(self):
        from installer.leave import discover_roles
        with tempfile.TemporaryDirectory() as tmp:
            found = discover_roles(Path(tmp), core_installed=lambda: False,
                                   stemdeck_installed=lambda: True,
                                   motion_installed=lambda: False)
        self.assertEqual(["stemdeck"], found)

    def test_motion_is_found_by_its_package_too(self):
        from installer.leave import discover_roles
        with tempfile.TemporaryDirectory() as tmp:
            found = discover_roles(Path(tmp), core_installed=lambda: False,
                                   stemdeck_installed=lambda: False,
                                   motion_installed=lambda: True)
        self.assertEqual(["motion"], found)

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


def uninstall_commands(name, chosen=(), installed=(), home_files=(), package_installed=True):
    """A role's uninstall in a dry run: the commands, without sudo, and the log."""
    with tempfile.TemporaryDirectory() as tmp:
        settings = {("roles", r): "yes" for r in chosen}
        ctx, log = context(tmp, settings)
        for role in installed:
            ctx.state.set("installed", role, "2026-10-01", dry_run=True)
        for rel in home_files:
            (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(tmp) / rel).touch()
        from installer.roles import motion as motion_module
        from installer.roles import stemdeck as stemdeck_module
        with mock.patch.object(stemdeck_module, "package_is_installed",
                               lambda _ctx: package_installed), \
                mock.patch.object(motion_module, "package_is_installed",
                                  lambda _ctx: package_installed), \
                mock.patch.object(core, "analyzer_is_installed",
                                  lambda _ctx: package_installed, create=True):
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
        """The analyzer's unit is its own package's; an a3-core pinned from
        before that package still ships it in ~/.config."""
        from installer.roles.core import ANALYZER_UNIT, CORE_UNITS
        if not CORE_UNITS_SHIPPED.is_dir():
            self.skipTest("a3-core is not checked out here")
        shipped = {p.name for p in CORE_UNITS_SHIPPED.glob("*.service")}
        self.assertEqual(shipped - {ANALYZER_UNIT}, set(CORE_UNITS))

    def test_the_analyzer_unit_stops_with_the_core(self):
        commands, _ = uninstall_commands("core")
        self.assertIn("systemctl --user disable --now beat-analyzer.service", commands)

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
        for unit in ("zita-n2j.service", "zita-j2n.service"):
            self.assertIn(f"systemctl --user disable --now {unit}", commands)
            self.assertIn(f"rm -f ~units/{unit}", commands)
        self.assertIn("systemctl --user disable --now stemdeck.service", commands)
        self.assertIn("systemctl --user daemon-reload", commands)

    def test_with_the_core_chosen_only_stemdeck(self):
        commands, _ = uninstall_commands("stemdeck", chosen=["core"])
        self.assertIn("systemctl --user disable --now stemdeck.service", commands)
        self.assertNotIn("rm -f ~units/stemdeck.service", commands)
        self.assertFalse(any("zita" in c for c in commands), commands)

    def test_a_core_still_installed_keeps_its_zita_files(self):
        """The zita files then are the Core's; the Core stops them when it leaves."""
        commands, _ = uninstall_commands("stemdeck", installed=["core"])
        self.assertFalse(any("zita" in c for c in commands), commands)

    def test_its_patchbay_unit_goes_too(self):
        """It is StemDeck's alone, by its own name: never the Core's qjackctl."""
        for chosen in ((), ("core",)):
            with self.subTest(chosen=chosen):
                commands, _ = uninstall_commands("stemdeck", chosen=chosen)
                self.assertIn("systemctl --user disable --now qjackctl-stemdeck.service",
                              commands)
                self.assertIn("rm -f ~units/qjackctl-stemdeck.service", commands)
                self.assertFalse(any(c.endswith(" qjackctl.service") or
                                     c.endswith("/qjackctl.service") for c in commands),
                                 commands)

    def test_build_and_library_stay(self):
        commands, _ = uninstall_commands("stemdeck")
        self.assertFalse(any("rm -rf" in c or "build-make" in c for c in commands), commands)


class MotionLeaves(unittest.TestCase):
    def test_its_unit_stops_and_the_package_goes(self):
        commands, _ = uninstall_commands("motion")
        self.assertIn("systemctl --user disable --now a3-motion.service", commands)
        self.assertIn("apt-mark unhold a3-motion-ui", commands)
        self.assertTrue(any("apt-get remove -y a3-motion-ui" in c for c in commands), commands)

    def test_the_installers_old_drop_in_goes_and_his_stay(self):
        commands, _ = uninstall_commands(
            "motion", home_files=(".config/systemd/user/a3-motion.service.d/a3-system.conf",
                                  ".config/systemd/user/a3-motion.service.d/display.conf"))
        self.assertIn("rm -f ~units/a3-motion.service.d/a3-system.conf", commands)
        self.assertFalse(any("display.conf" in c for c in commands), commands)

    def test_a_hand_unit_is_listed_a_symlink_is_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp, {})
            ctx.user_units.mkdir(parents=True)
            unit = ctx.user_units / "a3-motion.service"
            unit.write_text("[Service]\n")
            self.assertIn(unit, BY_NAME["motion"].leaving_files(ctx))
            unit.unlink()
            unit.symlink_to("/nonexistent/a3-motion.service")
            self.assertNotIn(unit, BY_NAME["motion"].leaving_files(ctx))

    def test_without_the_package_apt_is_not_called(self):
        commands, _ = uninstall_commands("motion", package_installed=False)
        self.assertFalse(any("apt-get" in c for c in commands), commands)

    def test_what_stays_is_named(self):
        from installer.leave import leaving_text
        with tempfile.TemporaryDirectory() as tmp:
            ctx, _ = context(tmp, {})
            text = leaving_text(ctx, ["motion"])
        for word in ("~/.local/share/a3-motion", "a3-motion-ui"):
            self.assertIn(word, text)


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


PIN = "0123456789abcdef0123456789abcdef01234567"


def stemdeck_seams(fragment="/usr/lib/systemd/user/stemdeck.service"):
    """The StemDeck role without JUCE, git or this machine's systemd."""
    from contextlib import ExitStack
    from installer.roles import apppackage, stemdeck
    stack = ExitStack()
    stack.enter_context(mock.patch.object(stemdeck, "ensure_juce", lambda _ctx: Path("/juce")))
    stack.enter_context(mock.patch.object(stemdeck, "pinned_commit", lambda _ctx: PIN))
    stack.enter_context(mock.patch.object(apppackage.debs, "version_of", lambda *_: "03.0+7"))
    stack.enter_context(mock.patch.object(apppackage, "fragment_path", lambda _ctx, _app: fragment))
    return stack


class FailingRunner(RecordingRunner):
    """RecordingRunner whose commands containing `fail_on` end with an error."""

    def __init__(self, fail_on, error=None, once=False, **kwargs):
        super().__init__(**kwargs)
        self.fail_on = fail_on
        self.error = error or (lambda: CommandFailed(f"{fail_on} ended with 100"))
        self.once = once

    def run(self, args, **kwargs):
        super().run(args, **kwargs)
        if self.fail_on and self.fail_on in " ".join(str(a) for a in args):
            if self.once:
                self.fail_on = None
            raise self.error()
        return 0


class MovingRunner(RecordingRunner):
    """RecordingRunner that also does what `mv -n a b` would, so a check that
    reads the files afterwards sees them where the role put them."""

    def run(self, args, **kwargs):
        super().run(args, **kwargs)
        words = [str(a) for a in args]
        if words[:2] == ["mv", "-n"] and not Path(words[3]).exists():
            Path(words[2]).rename(words[3])
        return 0


class MovingFailingRunner(FailingRunner):
    """FailingRunner that also moves files as `mv -n` would."""

    def run(self, args, **kwargs):
        words = [str(a) for a in args]
        if words[:2] == ["mv", "-n"] and not Path(words[3]).exists():
            Path(words[2]).rename(words[3])
        return super().run(args, **kwargs)


class DropInsThatShadowThePackage(unittest.TestCase):
    def ctx(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, _ = context(tmp, {})
        (ctx.user_units / "a3-motion.service.d").mkdir(parents=True)
        return ctx

    def drop_in(self, ctx, name, text):
        path = ctx.user_units / "a3-motion.service.d" / name
        path.write_text(text)
        return path

    def test_lines_that_set_what_is_started_or_where(self):
        from installer.roles.apppackage import shadowing_lines
        text = ("[Service]\n# ExecStart=commented\nEnvironment=DISPLAY=:0\n"
                "WorkingDirectory=/x\nExecStart=\nExecStart=/y\nExecStartPost=/z\n")
        self.assertEqual(["WorkingDirectory=/x", "ExecStart=", "ExecStart=/y"],
                         shadowing_lines(text))

    def test_only_those_drop_ins_shadow(self):
        from installer.roles.apppackage import AppPackage, shadowing_drop_ins
        ctx = self.ctx()
        self.drop_in(ctx, "display.conf", "[Service]\nEnvironment=DISPLAY=:0\n")
        self.drop_in(ctx, "restart.conf", "[Service]\nRestart=on-failure\nRestartSec=5\n")
        branch = self.drop_in(ctx, "zz-branch-test.conf",
                              "[Service]\nWorkingDirectory=/w\nExecStart=\nExecStart=/b\n")
        self.drop_in(ctx, "old.conf.before-package", "[Service]\nExecStart=/old\n")
        self.assertEqual([branch], shadowing_drop_ins(ctx, AppPackage("a3-motion-ui", "a3-motion.service")))

    def test_an_add_only_drop_in_of_stemdeck_is_not_shadowing(self):
        from installer.roles.apppackage import shadowing_lines
        self.assertEqual([], shadowing_lines(
            "[Unit]\nAfter=a3-jack.service\nBindsTo=a3-jack.service\n"))


class StemDeckComesAsAPackage(unittest.TestCase):
    def install(self, roles=("core",), hand_unit=None, aside=False, fragment=None,
                fail_on=None, symlink=False, twice=False, keep=None, error=None, once=False,
                drop_ins=None, moving=False):
        from installer.roles import stemdeck
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {("stemdeck", "library"): str(Path(tmp) / "stems"),
                                 **{("roles", r): "yes" for r in roles}})
        if fail_on:
            runner = MovingFailingRunner if moving else FailingRunner
            ctx.runner = runner(fail_on, error=error, once=once, log=log)
        else:
            ctx.runner = (MovingRunner if moving else RecordingRunner)(log=log)
        ctx.user_units.mkdir(parents=True)
        for name, text in (drop_ins or {}).items():
            folder = ctx.user_units / "stemdeck.service.d"
            folder.mkdir(exist_ok=True)
            (folder / name).write_text(text)
        if symlink:
            (ctx.user_units / "stemdeck.service").symlink_to("/nonexistent/stemdeck.service")
        if hand_unit is not None:
            (ctx.user_units / "stemdeck.service").write_text(hand_unit)
        if aside:
            (ctx.user_units / "stemdeck.service.before-package").write_text("older")
        seams = stemdeck_seams(fragment) if fragment else stemdeck_seams()
        with seams:
            try:
                stemdeck.StemDeck().install(ctx)
            finally:
                if keep is not None:
                    keep.append((log.commands(), ctx))
            if twice:
                hand = ctx.user_units / "stemdeck.service"
                if hand.exists():  # the recording runner moved nothing; do it as mv would
                    hand.rename(hand.with_name("stemdeck.service.before-package"))
                log.clear()
                stemdeck.StemDeck().install(ctx)
        return log.commands(), ctx

    def test_it_builds_the_pinned_commit_off_the_checkout(self):
        commands, ctx = self.install()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertIn(f"--rev {PIN}", build)
        self.assertIn(f"--out {ctx.home / 'a3-debs'}", build)
        self.assertIn(f"--cache {ctx.home / '.cache/a3-build'}", build)
        self.assertIn("--jobs 2", build)
        self.assertIn("--juce /juce", build)
        self.assertFalse(any(c.startswith("cmake") or "build-make" in c for c in commands), commands)

    def test_the_build_goes_through_the_cli(self):
        commands, _ = self.install()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertTrue(build.startswith("python3 "), build)

    def test_the_cli_lowers_the_priority_before_it_builds(self):
        from installer import package
        order = []
        with mock.patch.object(package, "lower_priority", lambda: order.append("nice")), \
                mock.patch.object(package, "build",
                                  lambda *a, **k: order.append("build") or Path("/x.deb")):
            package.main(["/some/repo", "--rev", PIN])
        self.assertEqual(["nice", "build"], order)

    def test_install_then_hold_then_restart(self):
        commands, ctx = self.install()
        deb = ctx.home / "a3-debs" / "stemdeck_03.0+7_amd64.deb"
        install = next(i for i, c in enumerate(commands) if "apt-get install" in c)
        self.assertIn(str(deb), commands[install])
        hold = commands.index("apt-mark hold stemdeck")
        restart = commands.index("systemctl --user restart stemdeck.service")
        build = next(i for i, c in enumerate(commands) if "installer/package.py" in c)
        self.assertLess(build, install)
        self.assertLess(install, hold)
        self.assertLess(hold, restart)

    def test_the_unit_is_no_longer_copied_into_the_home(self):
        commands, _ = self.install()
        self.assertFalse(any(c.startswith("install -D") and c.endswith("/stemdeck.service")
                             for c in commands), commands)

    def test_a_hand_unit_is_disabled_and_set_aside_before_the_package(self):
        commands, ctx = self.install(hand_unit="[Service]\nExecStart=/old\n")
        disable = commands.index("systemctl --user disable stemdeck.service")
        move = commands.index(f"mv -n {ctx.user_units / 'stemdeck.service'} "
                              f"{ctx.user_units / 'stemdeck.service.before-package'}")
        install = next(i for i, c in enumerate(commands) if "apt-get install" in c)
        self.assertLess(disable, move)
        self.assertLess(move, install)
        self.assertFalse(any(c.startswith("rm") and "stemdeck.service" in c for c in commands))

    CORE_CONF = "[Unit]\nAfter=a3-jack.service\nBindsTo=a3-jack.service\n"
    BRANCH_CONF = "[Service]\nWorkingDirectory=/w\nExecStart=\nExecStart=/b\n"
    DROP_INS = {"a3-core.conf": CORE_CONF, "zz-branch-test.conf": BRANCH_CONF}

    def folder(self, ctx):
        return ctx.user_units / "stemdeck.service.d"

    def test_the_drop_in_folder_stays_where_it_is(self):
        """stemdeck.service.d/a3-core.conf supplies After=/BindsTo=a3-jack to
        the packaged unit; only the drop-in that sets ExecStart goes."""
        commands, ctx = self.install(hand_unit="[Service]\n", drop_ins=self.DROP_INS,
                                     moving=True)
        folder = self.folder(ctx)
        self.assertEqual(self.CORE_CONF, (folder / "a3-core.conf").read_text())
        self.assertFalse((folder / "zz-branch-test.conf").exists())
        self.assertEqual(self.BRANCH_CONF, (folder / "zz-branch-test.conf.before-package").read_text())
        self.assertFalse(any("a3-core.conf" in c for c in commands), commands)
        self.assertFalse(any(c.startswith("rmdir") for c in commands), commands)

    def test_a_shadowing_drop_in_is_set_aside_before_apt(self):
        commands, ctx = self.install(drop_ins=self.DROP_INS, moving=True)
        branch = self.folder(ctx) / "zz-branch-test.conf"
        aside = self.folder(ctx) / "zz-branch-test.conf.before-package"
        self.assertLess(commands.index(f"mv -n {branch} {aside}"),
                        next(i for i, c in enumerate(commands) if "apt-get install" in c))
        self.assertIn("apt-mark hold stemdeck", commands)

    def test_a_failed_apt_install_puts_the_drop_in_back(self):
        _, ctx = self.install_failing_apt(error=None)
        self.assert_drop_ins_back(ctx)

    def test_ctrl_c_during_apt_puts_the_drop_in_back(self):
        _, ctx = self.install_failing_apt(error=KeyboardInterrupt, raises=KeyboardInterrupt)
        self.assert_drop_ins_back(ctx)

    def install_failing_apt(self, error, raises=CommandFailed):
        keep = []
        with self.assertRaises(raises):
            self.install(drop_ins=self.DROP_INS, moving=True, fail_on="apt-get install",
                         error=error, keep=keep)
        return keep[0]

    def assert_drop_ins_back(self, ctx):
        folder = self.folder(ctx)
        self.assertEqual(self.CORE_CONF, (folder / "a3-core.conf").read_text())
        self.assertEqual(self.BRANCH_CONF, (folder / "zz-branch-test.conf").read_text())
        self.assertFalse((folder / "zz-branch-test.conf.before-package").exists())

    def test_a_shadowing_drop_in_that_is_still_there_after_install_is_an_error(self):
        with self.assertRaises(RoleError) as raised:
            self.install(drop_ins=self.DROP_INS)  # the recording runner moves nothing
        self.assertIn("zz-branch-test.conf", str(raised.exception))
        self.assertNotIn("a3-core.conf", str(raised.exception))

    def test_no_hand_unit_nothing_set_aside(self):
        commands, _ = self.install()
        self.assertFalse(any(c.startswith("mv ") for c in commands), commands)
        self.assertNotIn("systemctl --user disable stemdeck.service", commands)

    def test_two_hand_units_stop_it_before_anything_is_built(self):
        with self.assertRaises(RoleError):
            self.install(hand_unit="x", aside=True)

    def test_a_failed_build_leaves_the_hand_unit_alone(self):
        keep = []
        with self.assertRaises(CommandFailed):
            self.install(hand_unit="x", fail_on="installer/package.py", keep=keep)
        commands, _ = keep[0]
        self.assertFalse(any(c.startswith("mv ") for c in commands), commands)
        self.assertNotIn("systemctl --user disable stemdeck.service", commands)

    def test_a_failed_apt_install_puts_the_hand_unit_back(self):
        keep = []
        with self.assertRaises(CommandFailed):
            self.install(hand_unit="x", fail_on="apt-get install", keep=keep)
        commands, ctx = keep[0]
        hand, aside = ctx.user_units / "stemdeck.service", ctx.user_units / "stemdeck.service.before-package"
        away = commands.index(f"mv -n {hand} {aside}")
        back = commands.index(f"mv -n {aside} {hand}")
        self.assertLess(away, back)
        self.assertLess(back, commands.index("systemctl --user enable stemdeck.service"))
        self.assertNotIn("apt-mark hold stemdeck", commands)

    def test_ctrl_c_during_apt_puts_the_hand_unit_back(self):
        """A Ctrl-C at the sudo prompt is no CommandFailed: without the put-back
        the machine is left with the hand unit renamed, disabled, and no package."""
        keep = []
        with self.assertRaises(KeyboardInterrupt):
            self.install(hand_unit="x", fail_on="apt-get install", error=KeyboardInterrupt,
                         keep=keep)
        commands, ctx = keep[0]
        hand, aside = ctx.user_units / "stemdeck.service", ctx.user_units / "stemdeck.service.before-package"
        back = commands.index(f"mv -n {aside} {hand}")
        self.assertLess(back, commands.index("systemctl --user enable stemdeck.service"))
        self.assertNotIn("apt-mark hold stemdeck", commands)

    def test_ctrl_c_at_the_disable_enables_the_hand_unit_again(self):
        keep = []
        with self.assertRaises(KeyboardInterrupt):
            self.install(hand_unit="x", fail_on="systemctl --user disable", error=KeyboardInterrupt,
                         keep=keep)
        commands, _ = keep[0]
        self.assertIn("systemctl --user enable stemdeck.service", commands)
        self.assertFalse(any(c.startswith("mv ") for c in commands), commands)
        self.assertFalse(any("apt-get install" in c for c in commands), commands)

    def test_a_failed_set_aside_enables_the_hand_unit_again(self):
        keep = []
        with self.assertRaises(CommandFailed):
            self.install(hand_unit="x", fail_on="mv -n", once=True, keep=keep)
        commands, _ = keep[0]
        self.assertEqual(1, sum(c.startswith("mv ") for c in commands), commands)
        self.assertLess(commands.index("systemctl --user disable stemdeck.service"),
                        commands.index("systemctl --user enable stemdeck.service"))
        self.assertFalse(any("apt-get install" in c for c in commands), commands)

    def test_a_symlink_shadowing_the_package_is_refused_before_anything_is_built(self):
        keep = []
        with self.assertRaises(RoleError) as raised:
            self.install(symlink=True, keep=keep)
        self.assertIn("stemdeck.service", str(raised.exception))
        self.assertEqual([], [c for c in keep[0][0] if "package.py" in c or "apt" in c])

    def test_a_second_run_changes_nothing_but_apt_hold_and_restart(self):
        commands, _ = self.install(hand_unit="x", twice=True)
        self.assertFalse(any(c.startswith("mv ") or " disable " in c for c in commands), commands)
        self.assertTrue(any("apt-get install" in c for c in commands))
        self.assertIn("apt-mark hold stemdeck", commands)
        self.assertIn("systemctl --user restart stemdeck.service", commands)

    def test_a_unit_still_shadowing_the_package_is_an_error(self):
        with self.assertRaises(RoleError) as raised:
            self.install(fragment="/home/aaa/.config/systemd/user/stemdeck.service")
        self.assertIn("shadows", str(raised.exception))


UI_PIN = "fedcba9876543210fedcba9876543210fedcba98"


def motion_seams(fragment="/usr/lib/systemd/user/a3-motion.service", packaged=True):
    from contextlib import ExitStack
    from installer.roles import apppackage, motion
    stack = ExitStack()
    stack.enter_context(mock.patch.object(motion, "ensure_juce", lambda _ctx: Path("/juce")))
    stack.enter_context(mock.patch.object(motion, "pinned_commit", lambda _ctx: UI_PIN))
    stack.enter_context(mock.patch.object(motion, "has_packaging", lambda *_: packaged))
    stack.enter_context(mock.patch.object(motion.debs, "version_of", lambda *_: "03.0+570"))
    stack.enter_context(mock.patch.object(apppackage, "fragment_path", lambda _ctx, _app: fragment))
    stack.enter_context(mock.patch.object(motion.Motion, "_dialout", lambda self, ctx: None))
    stack.enter_context(mock.patch.object(motion.Motion, "_firmware", lambda self, ctx: None))
    return stack


class MotionPinnedCommit(unittest.TestCase):
    def test_umbrella_pins_a3_motion_and_that_pins_ui(self):
        from installer.roles import motion
        calls = []
        answers = iter(["motionsha\n", "uisha\n"])

        class Fake:
            def output(self, args, cwd=None):
                calls.append([str(a) for a in args])
                return next(answers)

        ctx = mock.Mock(runner=Fake(), repo=Path("/repo"))
        self.assertEqual("uisha", motion.pinned_commit(ctx))
        self.assertEqual([["git", "-C", "/repo", "rev-parse", "HEAD:a3-motion"],
                          ["git", "-C", "/repo/a3-motion", "rev-parse", "motionsha:ui"]], calls)


class MotionComesAsAPackage(unittest.TestCase):
    def install(self, drop_ins=None, hand_unit=None, packaged=True, fail_on=None, error=None,
                keep=None):
        from installer.roles import motion
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {})
        ctx.runner = (FailingRunner(fail_on, error=error, log=log) if fail_on
                      else MovingRunner(log=log))
        (ctx.user_units / "a3-motion.service.d").mkdir(parents=True)
        for name, text in (drop_ins or {}).items():
            (ctx.user_units / "a3-motion.service.d" / name).write_text(text)
        if hand_unit is not None:
            (ctx.user_units / "a3-motion.service").write_text(hand_unit)
        with motion_seams(packaged=packaged):
            try:
                motion.Motion().install(ctx)
            finally:
                if keep is not None:
                    keep.append((log.commands(), ctx))
        return log.commands(), ctx

    def test_it_builds_the_pinned_ui_commit_off_the_checkout(self):
        commands, ctx = self.install()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertTrue(build.startswith("python3 "), build)
        self.assertIn(str(ctx.repo / "a3-motion/ui"), build)
        self.assertIn(f"--rev {UI_PIN}", build)
        self.assertIn("--jobs 2", build)
        self.assertFalse(any("build.sh" in c for c in commands), commands)

    def test_install_then_hold_then_restart(self):
        commands, ctx = self.install()
        deb = ctx.home / "a3-debs" / "a3-motion-ui_03.0+570_amd64.deb"
        install = next(i for i, c in enumerate(commands) if "apt-get install" in c)
        self.assertIn(str(deb), commands[install])
        self.assertLess(install, commands.index("apt-mark hold a3-motion-ui"))
        self.assertLess(commands.index("apt-mark hold a3-motion-ui"),
                        commands.index("systemctl --user restart a3-motion.service"))

    def test_no_unit_and_no_drop_in_is_written_into_the_home(self):
        _, ctx = self.install()
        self.assertFalse((ctx.user_units / "a3-motion.service").exists())
        self.assertFalse((ctx.user_units / "a3-motion.service.d/a3-system.conf").exists())

    def test_a_drop_in_that_starts_the_checkout_is_set_aside_and_the_rest_stay(self):
        commands, ctx = self.install(drop_ins={
            "display.conf": "[Service]\nEnvironment=DISPLAY=:0\n",
            "zz-branch-test.conf": "[Service]\nWorkingDirectory=/w\nExecStart=\nExecStart=/b\n",
            "a3-system.conf": "[Service]\nEnvironment=DISPLAY=:0\nExecStart=\nExecStart=/c\n"})
        d = ctx.user_units / "a3-motion.service.d"
        self.assertTrue((d / "display.conf").is_file())
        self.assertTrue((d / "zz-branch-test.conf.before-package").is_file())
        self.assertTrue((d / "a3-system.conf.before-package").is_file())
        self.assertFalse((d / "display.conf.before-package").exists())

    def test_a_hand_unit_is_disabled_and_set_aside(self):
        commands, ctx = self.install(hand_unit="[Service]\nExecStart=/usr/bin/a3-motion\n")
        self.assertIn("systemctl --user disable a3-motion.service", commands)
        self.assertTrue((ctx.user_units / "a3-motion.service.before-package").is_file())

    def test_a_pin_without_packaging_is_refused_before_anything_is_built(self):
        from installer.roles.base import RoleError
        with self.assertRaises(RoleError):
            self.install(packaged=False)

    def test_an_interrupted_apt_puts_everything_back(self):
        keep = []
        with self.assertRaises(KeyboardInterrupt):
            self.install(hand_unit="[Service]\nExecStart=/old\n",
                         drop_ins={"zz-branch-test.conf": "[Service]\nExecStart=\nExecStart=/b\n"},
                         fail_on="apt-get install", error=KeyboardInterrupt, keep=keep)
        commands, ctx = keep[0]
        apt = next(i for i, c in enumerate(commands) if "apt-get install" in c)
        after = commands[apt + 1:]
        d = ctx.user_units / "a3-motion.service.d"
        self.assertIn(f"mv -n {d / 'zz-branch-test.conf.before-package'} {d / 'zz-branch-test.conf'}", after)
        self.assertIn(f"mv -n {ctx.user_units / 'a3-motion.service.before-package'} "
                      f"{ctx.user_units / 'a3-motion.service'}", after)
        self.assertIn("systemctl --user enable a3-motion.service", after)

    def test_a_shadowing_drop_in_left_over_is_refused(self):
        from installer.roles import apppackage, motion
        from installer.roles.base import RoleError
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {})
        ctx.runner = RecordingRunner(log=log)   # does not move: the drop-in stays
        (ctx.user_units / "a3-motion.service.d").mkdir(parents=True)
        (ctx.user_units / "a3-motion.service.d/zz.conf").write_text("[Service]\nExecStart=/b\n")
        with motion_seams(), self.assertRaises(RoleError):
            motion.Motion().install(ctx)

    def test_a3nuc1_as_it_is_sets_aside_the_hand_unit_and_the_branch_drop_in_only(self):
        commands, ctx = self.install(
            hand_unit="[Service]\nExecStart=/home/aaa/a3-system/a3-motion/ui/build/x\n",
            drop_ins={
                "display.conf": "[Service]\nEnvironment=DISPLAY=:0\n",
                "restart.conf": "[Service]\nRestart=on-failure\nRestartSec=5\n",
                "zz-branch-test.conf": ("[Service]\nWorkingDirectory=/w\n"
                                        "ExecStart=\nExecStart=/w/a3-motion-ui\n")})
        d = ctx.user_units / "a3-motion.service.d"
        self.assertTrue((ctx.user_units / "a3-motion.service.before-package").is_file())
        self.assertFalse((ctx.user_units / "a3-motion.service").exists())
        self.assertTrue((d / "zz-branch-test.conf.before-package").is_file())
        self.assertFalse((d / "zz-branch-test.conf").exists())
        for stays in ("display.conf", "restart.conf"):
            self.assertTrue((d / stays).is_file(), stays)
            self.assertFalse((d / (stays + ".before-package")).exists(), stays)
        self.assertEqual(2, len([c for c in commands if c.startswith("mv -n")]), commands)


class StemDeckLeavesThroughApt(unittest.TestCase):
    def test_unhold_then_remove_never_purge(self):
        commands, _ = uninstall_commands("stemdeck", chosen=["core"])
        unhold = commands.index("apt-mark unhold stemdeck")
        remove = next(i for i, c in enumerate(commands) if "apt-get remove" in c and "stemdeck" in c)
        self.assertLess(unhold, remove)
        self.assertFalse(any("purge" in c for c in commands), commands)

    def test_an_old_style_install_loses_its_unit_file_and_needs_no_apt(self):
        commands, _ = uninstall_commands(
            "stemdeck", home_files=[".config/systemd/user/stemdeck.service"],
            package_installed=False)
        self.assertIn("rm -f ~units/stemdeck.service", commands)
        self.assertFalse(any("apt" in c for c in commands), commands)

    def test_a_missing_unit_file_is_not_removed(self):
        commands, _ = uninstall_commands("stemdeck", package_installed=True)
        self.assertNotIn("rm -f ~units/stemdeck.service", commands)

    def test_its_data_stays(self):
        commands, _ = uninstall_commands("stemdeck")
        self.assertFalse(any(".local/share/stemdeck" in c for c in commands), commands)

    def test_it_names_its_package(self):
        from installer.roles.stemdeck import StemDeck
        self.assertEqual(["stemdeck"], StemDeck().leaving_packages(None))


class StemDeckInstallsItsLibrary(unittest.TestCase):
    def install(self, dry_run, settings_file=STEMDECK_SETTINGS, roles=("core",)):
        from installer.roles import stemdeck
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        library = Path(tmp) / "data" / "stems"
        ctx, log = context(tmp, {("stemdeck", "library"): str(library),
                                 **{("roles", r): "yes" for r in roles}})
        ctx.user_units.mkdir(parents=True, exist_ok=True)
        if not dry_run:
            ctx.runner = RecordingRunner(log=log)
        path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
        if settings_file is not None:
            path.parent.mkdir(parents=True)
            path.write_text(settings_file)
        with stemdeck_seams():
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

    def test_a_dry_run_says_it_skipped_the_shadow_check(self):
        log, _, _ = self.install(dry_run=True)
        self.assertTrue(any("shadow" in line and "skipped" in line for line in log))

    def test_a_dry_run_writes_nothing_and_says_what_it_would(self):
        log, path, library = self.install(dry_run=True)
        self.assertFalse(library.exists())
        self.assertEqual(STEMDECK_SETTINGS, path.read_text())
        self.assertTrue(any(str(library) in line and "stemFolder" in line for line in log))
        self.assertIn("systemctl --user stop stemdeck.service", log.commands())


class StemDeckWiresItselfWithoutTheCore(unittest.TestCase):
    """Without the Core nothing connects StemDeck to zita-j2n (a3nuc2,
    2026-10-06): a QjackCtl with StemDeck's patchbay does. With the Core its
    own patchbay does, and a second QjackCtl must not run there."""

    PATCHBAY_UNIT = "qjackctl-stemdeck.service"

    def install(self, roles, installed_before=False):
        from installer.roles import stemdeck
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {("stemdeck", "library"): str(Path(tmp) / "stems"),
                                 **{("roles", r): "yes" for r in roles}})
        ctx.runner = RecordingRunner(log=log)
        ctx.user_units.mkdir(parents=True, exist_ok=True)
        if installed_before:
            (ctx.user_units / self.PATCHBAY_UNIT).touch()
        with stemdeck_seams():
            stemdeck.StemDeck().install(ctx)
        return log.commands(), ctx

    def test_without_the_core_its_patchbay_unit_is_installed_and_enabled(self):
        commands, ctx = self.install(roles=())
        source = REPO / "stemdeck" / ".config/systemd/user" / self.PATCHBAY_UNIT
        self.assertIn(f"install -D -m 644 {source} {ctx.user_units / self.PATCHBAY_UNIT}",
                      commands)
        self.assertIn(f"systemctl --user enable {self.PATCHBAY_UNIT}", commands)
        self.assertIn(f"systemctl --user restart {self.PATCHBAY_UNIT}", commands)

    def test_the_patchbay_is_not_copied(self):
        commands, _ = self.install(roles=())
        self.assertFalse(any("rncbc.org" in c for c in commands), commands)

    def test_with_the_core_nothing_of_it(self):
        commands, _ = self.install(roles=("core",))
        self.assertFalse(any("qjackctl" in c for c in commands), commands)

    def test_a_machine_becoming_a_core_loses_it(self):
        """Installed earlier without the Core: the Core's qjackctl.service
        would run beside it, two QjackCtls on one JACK."""
        commands, ctx = self.install(roles=("core",), installed_before=True)
        self.assertIn(f"systemctl --user disable --now {self.PATCHBAY_UNIT}", commands)
        self.assertIn(f"rm -f {ctx.user_units / self.PATCHBAY_UNIT}", commands)
        self.assertFalse(any(c.startswith(("systemctl --user enable",
                                           "systemctl --user restart"))
                             and "qjackctl" in c for c in commands), commands)


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
        ctx.user_units.mkdir(parents=True, exist_ok=True)
        path = Path(tmp) / ".config" / "StemDeck" / "StemDeck.settings"
        if settings_file is not None:
            path.parent.mkdir(parents=True)
            path.write_text(settings_file)
        role = stemdeck.StemDeck()
        role.configure(ctx)
        with stemdeck_seams():
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
    def test_onboard_comes_with_the_package_not_the_role(self):
        """StemDeck's on-screen keyboard starts onboard; since the role installs
        the stemdeck package, apt gets it from the package's Depends."""
        self.assertNotIn("onboard", BY_NAME["stemdeck"].packages)


IP_OUTPUT = """1: lo    inet 127.0.0.1/8 scope host lo\\       valid_lft forever preferred_lft forever
3: br0    inet 192.168.8.10/24 brd 192.168.8.255 scope global br0\\       valid_lft forever
4: wlan0    inet 10.0.0.5/24 brd 10.0.0.255 scope global dynamic wlan0\\       valid_lft 3000sec
"""


class OneCoreInTheLan(unittest.TestCase):
    """Two Cores in one LAN would both announce /core/here, and the desk
    could end up on the wrong one: the Core role installs only on the
    machine that owns the truth's core address (2026-10-05)."""

    TRUTH = "192.168.8.10"

    def test_the_truth_names_the_core(self):
        self.assertEqual(self.TRUTH, core.truth_core_address(REPO))

    def test_the_addresses_of_this_machine_from_ip(self):
        self.assertEqual(["127.0.0.1", "192.168.8.10", "10.0.0.5"],
                         core.addresses_in(IP_OUTPUT))

    def test_owning_the_address_allows_it(self):
        self.assertIsNone(core.core_refusal(self.TRUTH, ["127.0.0.1", self.TRUTH], None))

    def test_its_own_network_answers_setting_the_address_allow_it(self):
        self.assertIsNone(core.core_refusal(self.TRUTH, ["192.168.43.58"], self.TRUTH))

    def test_neither_refuses_naming_the_address_and_the_second_core(self):
        message = core.core_refusal(self.TRUTH, ["192.168.8.20"], "192.168.8.20")
        self.assertIn(self.TRUTH, message)
        self.assertIn("zweiter Core", message)

    def test_a_truth_without_a_core_refuses(self):
        self.assertIsNotNone(core.core_refusal(None, ["192.168.8.10"], None))

    def test_the_answered_address_counts_only_when_the_network_is_configured(self):
        s = Settings("/nonexistent/install.conf")
        s.set("core", "address", "192.168.8.10/24")
        s.set_flag("core", "configure_network", False)
        self.assertIsNone(core.answered_address(s))
        s.set_flag("core", "configure_network", True)
        self.assertEqual("192.168.8.10", core.answered_address(s))

    def check(self, own, settings=None):
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp, settings)
            return core.check_core(ctx, lookup=lambda runner: own), list(log)

    def test_the_check_on_the_rig_allows(self):
        refusal, _ = self.check(["192.168.8.10"])
        self.assertIsNone(refusal)

    def test_the_check_on_a_second_machine_refuses(self):
        refusal, _ = self.check(["192.168.8.20"])
        self.assertIn(self.TRUTH, refusal)

    def test_the_check_with_its_own_network_answer_allows(self):
        refusal, _ = self.check([], {("core", "configure_network"): "yes",
                                     ("core", "address"): "192.168.8.10/24"})
        self.assertIsNone(refusal)

    def test_a_dry_run_prints_the_check(self):
        _, log = self.check(["192.168.8.20"])
        said = "\n".join(log)
        self.assertIn(self.TRUTH, said)
        self.assertIn("192.168.8.20", said)

    def test_refused_the_others_install_and_an_installed_core_stays(self):
        roles = [LeavingRole("core"), FakeRole("stemdeck"), FakeRole("motion")]
        from installer.cli import apply_roles
        with tempfile.TemporaryDirectory() as tmp:
            ctx, log = context(tmp)
            ctx.state.set("installed", "core", "2026-10-01")
            patches = with_fakes(roles)
            for p in patches:
                p.start()
            try:
                left, rows = apply_roles(ctx, ["core", "stemdeck", "motion"],
                                         discover=nothing_found,
                                         refused={"core": "nein"})
            finally:
                for p in patches:
                    p.stop()
        commands = log.commands()
        self.assertEqual([], left)
        self.assertIn("install stemdeck", commands)
        self.assertIn("install motion", commands)
        self.assertNotIn("install core", commands)
        self.assertNotIn("uninstall core", commands)
        self.assertEqual(("core", "ABGELEHNT: nein"), rows[0])
        self.assertIn(("stemdeck", "ok"), rows)

    def test_the_summary_says_it(self):
        from installer.cli import summary_text
        text = summary_text("v03.0", ["core", "stemdeck"], {"core": "Grund"})
        self.assertIn("Grund", text)
        self.assertNotIn("A³ Core", text.split("Rollen:")[1].splitlines()[0])


ANALYZER_PIN = "fedcba9876543210fedcba9876543210fedcba98"


def core_seams(fragment="/usr/lib/systemd/user/beat-analyzer.service", packaged=True):
    """The Core role without dpkg-deb, git or this machine's systemd."""
    from contextlib import ExitStack
    from installer.roles import apppackage
    stack = ExitStack()
    stack.enter_context(mock.patch.object(core, "build_package",
                                          lambda _ctx, work: work / "a3-core_03.0+400_amd64.deb"))
    stack.enter_context(mock.patch.object(core, "analyzer_commit", lambda _ctx: ANALYZER_PIN))
    stack.enter_context(mock.patch.object(core, "has_packaging", lambda *_: packaged))
    stack.enter_context(mock.patch.object(apppackage.debs, "version_of", lambda *_: "03.0+52"))
    stack.enter_context(mock.patch.object(apppackage, "fragment_path",
                                          lambda _ctx, _app: fragment))
    return stack


class TheAnalyzerComesWithTheCoreAsAPackage(unittest.TestCase):
    """a3-core no longer builds the beat-analyzer in its checkout (a3-core
    feat/analyzer-from-package); the Core role builds and installs the
    beat-analyzer package from the pinned commit instead."""

    def install(self, drop_ins=None, hand_unit=None, packaged=True, fragment=None):
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp)
        ctx, log = context(tmp, {("roles", "core"): "yes"})
        ctx.runner = MovingRunner(log=log)
        folder = ctx.user_units / "beat-analyzer.service.d"
        folder.mkdir(parents=True)
        for name, text in (drop_ins or {}).items():
            (folder / name).write_text(text)
        if hand_unit is not None:
            (ctx.user_units / "beat-analyzer.service").write_text(hand_unit)
        seams = core_seams(fragment) if fragment else core_seams(packaged=packaged)
        with seams:
            core.Core().install(ctx)
        return log.commands(), ctx

    def test_the_pinned_analyzer_commit_is_built_off_the_checkout(self):
        commands, ctx = self.install()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertIn(str(ctx.repo / "beat-analyzer"), build)
        self.assertIn(f"--rev {ANALYZER_PIN}", build)

    def test_after_a3_core_installed_then_held(self):
        commands, ctx = self.install()
        deb = ctx.home / "a3-debs" / "beat-analyzer_03.0+52_amd64.deb"
        core_apt = next(i for i, c in enumerate(commands)
                        if "apt-get install" in c and "a3-core_" in c)
        analyzer_apt = next(i for i, c in enumerate(commands)
                            if "apt-get install" in c and str(deb) in c)
        self.assertLess(core_apt, analyzer_apt)
        self.assertLess(analyzer_apt, commands.index("apt-mark hold beat-analyzer"))

    def test_not_enabled_a3_main_starts_it_and_a_running_one_moves_over(self):
        commands, _ = self.install()
        self.assertFalse(any(c.startswith("systemctl --user enable") and "beat-analyzer" in c
                             for c in commands), commands)
        self.assertIn("systemctl --user try-restart beat-analyzer.service", commands)

    def test_a3_cores_own_drop_in_stays(self):
        """a3-core.conf adds ExecStartPre=/bin/sleep 3 to the package's unit;
        it adds, it does not replace what is started."""
        text = ("[Unit]\nPartOf=a3-main.service\n[Service]\n"
                "ExecStartPre=/bin/sleep 3\nCPUAffinity=1 2 3\n")
        commands, ctx = self.install(drop_ins={"a3-core.conf": text})
        folder = ctx.user_units / "beat-analyzer.service.d"
        self.assertTrue((folder / "a3-core.conf").is_file())
        self.assertFalse((folder / "a3-core.conf.before-package").exists())

    def test_a_drop_in_that_starts_the_checkout_is_set_aside(self):
        commands, ctx = self.install(drop_ins={
            "zz-branch-test.conf": "[Service]\nExecStart=\nExecStart=/w/beat-analyzer\n"})
        folder = ctx.user_units / "beat-analyzer.service.d"
        self.assertTrue((folder / "zz-branch-test.conf.before-package").is_file())

    def test_the_old_checkout_unit_is_set_aside(self):
        commands, ctx = self.install(
            hand_unit="[Service]\nExecStart=/home/aaa/a3-system/beat-analyzer/build/beat-analyzer\n")
        self.assertTrue((ctx.user_units / "beat-analyzer.service.before-package").is_file())

    def test_a_pin_without_packaging_is_refused_before_anything_is_built(self):
        with self.assertRaises(RoleError):
            self.install(packaged=False)

    def test_a_unit_that_still_shadows_the_package_is_refused(self):
        with self.assertRaises(RoleError):
            self.install(fragment="/home/aaa/.config/systemd/user/beat-analyzer.service")

    def test_the_core_brings_what_the_analyzer_builds_with(self):
        for needed in ("cmake", "g++", "pkg-config", "curl",
                       "libjack-jackd2-dev", "libsamplerate0-dev"):
            self.assertIn(needed, BY_NAME["core"].packages)


class TheAnalyzerLeavesWithTheCore(unittest.TestCase):
    def test_unheld_and_removed_after_its_unit_stopped(self):
        commands, _ = uninstall_commands("core")
        remove = "env DEBIAN_FRONTEND=noninteractive apt-get remove -y beat-analyzer"
        self.assertIn(remove, commands)
        self.assertLess(commands.index("apt-mark unhold beat-analyzer"), commands.index(remove))
        self.assertLess(commands.index("systemctl --user disable --now beat-analyzer.service"),
                        commands.index(remove))

    def test_an_install_from_before_the_package_needs_no_apt_for_it(self):
        commands, _ = uninstall_commands("core", package_installed=False)
        self.assertFalse(any("beat-analyzer" in c and "apt" in c for c in commands), commands)


if __name__ == "__main__":
    unittest.main()
