# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The role laptop: a whole A³ rig on one machine (Core and engine, the
StemDeck decks, the desk, Motion UI, the beat-analyzer), from packages only,
for any user anywhere. This file covers its settings, refusals and packages."""

import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_installer import Log, RecordingRunner  # noqa: E402
from installer import archive, cli  # noqa: E402
from installer.prompt import Prompter  # noqa: E402
from installer.roles import ALL, BY_NAME, base, deckhost, needed_packages, needs_screen  # noqa: E402
from installer.roles import laptop  # noqa: E402
from installer.roles.base import Context, RoleError  # noqa: E402
from installer.settings import DEFAULTS, ROLES, Settings  # noqa: E402
from installer.system import CommandFailed, Runner  # noqa: E402

A3_ROOT = str(archive.A3_ROOT)
FIVE_APPS = "a3-core-app stemdeck a3-desk a3-motion-ui beat-analyzer"


def truth_with_decks(highest):
    """The part of the shipped truth the deck count is read from."""
    return {"addresses": {"stemdeck.deck-hello": {"pattern": "/stemdeck/{deck}/hello",
                                                  "deck": [1, highest]}}}


def pw_node(node_id, media_class, name, description=None, nick=None):
    props = {"media.class": media_class, "node.name": name}
    if description:
        props["node.description"] = description
    if nick:
        props["node.nick"] = nick
    return {"id": node_id, "type": "PipeWire:Interface:Node", "info": {"props": props}}


PW_DUMP = [
    {"id": 0, "type": "PipeWire:Interface:Core", "info": {"props": {}}},
    pw_node(40, "Audio/Sink", "alsa_output.pci-0000_00_1f.3.analog-stereo",
            description="Built-in Audio Analog Stereo"),
    pw_node(41, "Audio/Source", "alsa_input.pci-0000_00_1f.3.analog-stereo",
            description="Built-in Audio Microphone"),
    pw_node(42, "Audio/Sink", "alsa_output.usb-Focusrite_Scarlett_2i2-00.pro-output-0",
            nick="Scarlett 2i2"),
    pw_node(43, "Audio/Sink", laptop.OWN_LOOPBACK, description="A3 laptop out"),
    {"id": 44, "type": "PipeWire:Interface:Node", "info": None},
]


class PwDumpRunner(RecordingRunner):
    """Runs nothing; `pw-dump` answers with `dump` (None: it is missing)."""

    def __init__(self, dump, **kwargs):
        super().__init__(**kwargs)
        self.dump = dump

    def output(self, args, cwd=None):
        if [str(a) for a in args][:1] != ["pw-dump"]:
            raise AssertionError(f"unexpected output() call: {args}")
        if self.dump is None:
            raise FileNotFoundError("pw-dump")
        return json.dumps(self.dump)


class RootRecordingRunner(PwDumpRunner):
    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        self.log("$ " + ("root: " if root else "") + " ".join(str(a) for a in args))
        return 0


class ScriptedPrompter(Prompter):
    interactive = True

    def __init__(self, choice="", texts=()):
        self.choice = choice
        self.texts = list(texts)
        self.questions = []
        self.offered = None

    def choose(self, question, options, default):
        self.questions.append(question)
        self.offered = options
        return self.choice

    def text(self, question, default):
        self.questions.append(question)
        return self.texts.pop(0) if self.texts else default


class LaptopCase(unittest.TestCase):
    def ctx(self, settings=None, prompter=None, dump=PW_DUMP, from_source=False,
            highest_deck=4):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        s = Settings(Path(tmp) / "install.conf")
        s.set("roles", "laptop", "yes")
        for (section, key), value in (settings or {}).items():
            s.set(section, key, value)
        log = Log()
        ctx = Context(REPO, s, RootRecordingRunner(dump, log=log), prompter or Prompter(),
                      "debian", home=tmp, user="somebody", from_source=from_source)
        ctx.user_units.mkdir(parents=True)
        truth = Path(tmp) / "a3-osc.json"
        truth.write_text(json.dumps(truth_with_decks(highest_deck)))
        patcher = mock.patch.object(laptop, "TRUTH", truth)
        patcher.start()
        self.addCleanup(patcher.stop)
        return ctx, log


class TheDecks(unittest.TestCase):
    def test_letters_follow_the_engine_scheme(self):
        self.assertEqual(["A"], laptop.deck_letters(1))
        self.assertEqual(["A", "B", "C", "D"], laptop.deck_letters(4))
        self.assertEqual(["Y", "Z", "AA"], laptop.deck_letters(27)[-3:])
        self.assertEqual("AB", laptop.deck_letters(28)[-1])
        self.assertEqual(28, len(laptop.deck_letters(28)))

    def test_the_truths_range_is_the_deck_hello_s_highest_deck(self):
        self.assertEqual(4, laptop.truth_deck_count(truth_with_decks(4)))
        self.assertEqual(6, laptop.truth_deck_count(truth_with_decks(6)))

    def test_empty_decks_take_the_truths_range(self):
        s = Settings("/nonexistent/install.conf")
        self.assertEqual("", s.get("laptop", "decks"))
        self.assertEqual(4, laptop.deck_count(s, truth_with_decks(4)))

    def test_a_number_within_the_range_is_taken(self):
        s = Settings("/nonexistent/install.conf")
        s.set("laptop", "decks", "2")
        self.assertEqual(2, laptop.deck_count(s, truth_with_decks(4)))

    def test_more_decks_than_the_truth_knows_are_refused_with_the_number(self):
        s = Settings("/nonexistent/install.conf")
        s.set("laptop", "decks", "6")
        with self.assertRaises(RoleError) as caught:
            laptop.deck_count(s, truth_with_decks(4))
        self.assertIn("6", str(caught.exception))
        self.assertIn("4", str(caught.exception))

    def test_no_number_or_none_at_all_is_refused(self):
        for value in ("zwei", "0", "-1", "2.5", "\u00b2", "\u0663"):
            with self.subTest(value):
                s = Settings("/nonexistent/install.conf")
                s.set("laptop", "decks", value)
                with self.assertRaises(RoleError):
                    laptop.deck_count(s, truth_with_decks(4))


class TheRole(unittest.TestCase):
    def test_it_is_registered_last_with_its_settings(self):
        self.assertIsInstance(ALL[-1], laptop.Laptop)
        self.assertIs(BY_NAME["laptop"], ALL[-1])
        self.assertEqual("laptop", ROLES[-1])
        self.assertEqual({"decks": "", "output_device": "", "output_main": "1,2",
                          "output_phones": ""}, DEFAULTS["laptop"])

    def test_its_attributes(self):
        role = laptop.Laptop()
        self.assertEqual("Laptop rig (Core, decks, desk, Motion UI on one machine)", role.label)
        self.assertEqual(("debian",), role.platforms)
        self.assertTrue(role.runs_without_checkout)
        self.assertTrue(role.any_user_anywhere)
        self.assertEqual(("a3-core-app", "stemdeck", "a3-desk", "a3-motion-ui",
                          "beat-analyzer"), laptop.APPS)
        self.assertEqual(["pipewire-bin", "xdotool"], needed_packages(["laptop"], False))

    def test_it_needs_no_screen_autologin(self):
        self.assertFalse(laptop.Laptop().needs_screen)
        self.assertFalse(needs_screen(["laptop"]))

    def test_the_rig_roles_keep_the_user_and_place_check(self):
        for role in ALL:
            if role.name != "laptop":
                with self.subTest(role.name):
                    self.assertFalse(role.any_user_anywhere)
                    self.assertFalse(role.runs_without_checkout)


class TheUserAndPlaceCheck(unittest.TestCase):
    ELSEWHERE = Path("/home/ra/src/a3-system")

    def test_the_laptop_role_runs_as_any_user_anywhere(self):
        self.assertEqual([], cli.place_problems(self.ELSEWHERE, "ra", ["laptop"]))

    def test_a_rig_role_keeps_the_check(self):
        self.assertEqual(2, len(cli.place_problems(self.ELSEWHERE, "ra", ["core"])))
        self.assertEqual(2, len(cli.place_problems(self.ELSEWHERE, "ra", ["laptop", "desk"])))

    def test_no_roles_yet_keeps_the_check(self):
        self.assertEqual(2, len(cli.place_problems(self.ELSEWHERE, "ra", [])))

    def test_the_rig_s_own_place_passes_for_any_role(self):
        self.assertEqual([], cli.place_problems(Path("/home/aaa/a3-system"), "aaa", ["core"]))


class TheRefusals(LaptopCase):
    def test_laptop_excludes_every_other_role(self):
        for other in ("core", "stemdeck", "deck-host", "motion", "desk", "mixer"):
            with self.subTest(other):
                why = cli.refused_together([other, "laptop"])
                self.assertIn(other, why)
                self.assertIn("laptop", why)

    def test_the_rig_roles_go_together_as_before(self):
        self.assertIsNone(cli.refused_together(["core", "stemdeck", "motion", "desk"]))
        self.assertIsNone(cli.refused_together(["laptop"]))

    def test_from_source_is_refused_before_any_change(self):
        ctx, log = self.ctx(from_source=True)
        with self.assertRaises(RoleError) as caught:
            laptop.Laptop().install(ctx)
        self.assertIn("packages", str(caught.exception))
        self.assertEqual([], log.commands())

    def test_a_deck_count_that_is_no_number_is_refused_before_any_change(self):
        ctx, log = self.ctx({("laptop", "decks"): "vier"})
        with self.assertRaises(RoleError):
            laptop.Laptop().install(ctx)
        self.assertEqual([], log.commands())


class TheInstall(LaptopCase):
    def install(self, ctx):
        with mock.patch.object(laptop.Laptop, "_wire") as wire, \
                mock.patch.object(laptop.Laptop, "_units") as units:
            laptop.Laptop().install(ctx)
        return wire, units

    def test_it_installs_the_five_apps_and_not_the_rig_deployment(self):
        ctx, log = self.ctx()
        self.install(ctx)
        commands = log.commands()
        installs = [c for c in commands if c.startswith(f"root: {A3_ROOT} install")]
        self.assertEqual([f"root: {A3_ROOT} install {FIVE_APPS}"], installs)
        installed = [name for c in installs for name in c.split()[3:]]
        self.assertNotIn("a3-core", installed)
        self.assertFalse(any("apt-get" in c or "package.py" in c for c in commands), commands)

    def test_the_user_joins_audio_after_the_apps(self):
        ctx, log = self.ctx()
        self.install(ctx)
        commands = log.commands()
        self.assertEqual(f"root: {A3_ROOT} join-audio", commands[-1])
        self.assertLess(commands.index(f"root: {A3_ROOT} install {FIVE_APPS}"),
                        commands.index(f"root: {A3_ROOT} join-audio"))

    def test_wiring_and_units_get_the_deck_letters_from_the_installed_truth(self):
        ctx, _ = self.ctx({("laptop", "decks"): "3"}, highest_deck=6)
        wire, units = self.install(ctx)
        wire.assert_called_once_with(ctx, ["A", "B", "C"])
        units.assert_called_once_with(ctx, ["A", "B", "C"])

    def test_more_decks_than_the_installed_truth_knows_are_refused_before_joining(self):
        ctx, log = self.ctx({("laptop", "decks"): "5"}, highest_deck=4)
        with self.assertRaises(RoleError) as caught:
            self.install(ctx)
        self.assertIn("5", str(caught.exception))
        self.assertNotIn(f"root: {A3_ROOT} join-audio", log.commands())

    def test_a_missing_truth_after_the_install_is_a_role_error(self):
        ctx, _ = self.ctx()
        laptop.TRUTH.unlink()
        with self.assertRaises(RoleError) as caught:
            self.install(ctx)
        self.assertIn(str(laptop.TRUTH), str(caught.exception))


class TheOutputDevice(LaptopCase):
    def test_the_sinks_are_the_choices_after_the_default(self):
        self.assertEqual(
            [("", "default (the internal card)"),
             ("alsa_output.pci-0000_00_1f.3.analog-stereo", "Built-in Audio Analog Stereo"),
             ("alsa_output.usb-Focusrite_Scarlett_2i2-00.pro-output-0", "Scarlett 2i2")],
            laptop.output_device_choices(PW_DUMP))

    def test_a_sink_without_description_or_nick_shows_its_name(self):
        dump = [pw_node(7, "Audio/Sink", "plain_sink")]
        self.assertEqual(("plain_sink", "plain_sink"), laptop.output_device_choices(dump)[1])

    def test_interactive_asks_for_the_device_and_its_main_channels(self):
        usb = "alsa_output.usb-Focusrite_Scarlett_2i2-00.pro-output-0"
        ask = ScriptedPrompter(choice=usb, texts=["3,4"])
        ctx, _ = self.ctx(prompter=ask)
        laptop.Laptop().configure(ctx)
        self.assertEqual(3, len(ask.offered))
        self.assertEqual(usb, ctx.settings.get("laptop", "output_device"))
        self.assertEqual("3,4", ctx.settings.get("laptop", "output_main"))

    def test_the_default_card_asks_no_channels(self):
        ask = ScriptedPrompter(choice="")
        ctx, _ = self.ctx(prompter=ask)
        laptop.Laptop().configure(ctx)
        self.assertEqual(1, len(ask.questions))
        self.assertEqual("", ctx.settings.get("laptop", "output_device"))

    def test_without_pw_dump_only_the_default_is_offered_with_one_line(self):
        ask = ScriptedPrompter(choice="")
        ctx, log = self.ctx(prompter=ask, dump=None)
        laptop.Laptop().configure(ctx)
        self.assertEqual([("", "default (the internal card)")], ask.offered)
        self.assertEqual(1, len([line for line in log if "pw-dump" in line]))

    def test_without_questions_the_stored_device_stays(self):
        ctx, log = self.ctx({("laptop", "output_device"): "some_sink",
                             ("laptop", "output_main"): "5,6"}, dump=None)
        laptop.Laptop().configure(ctx)
        self.assertEqual("some_sink", ctx.settings.get("laptop", "output_device"))
        self.assertEqual("5,6", ctx.settings.get("laptop", "output_main"))
        self.assertEqual([], [line for line in log if "pw-dump" in line])


class TheTwoDeckDropIn(unittest.TestCase):
    def test_it_lives_in_base_and_deck_host_uses_it(self):
        self.assertIs(base.two_deck_off_drop_in, deckhost.two_deck_off_drop_in)
        text = base.two_deck_off_drop_in("# mark\n")
        self.assertTrue(text.startswith("# mark\n"))
        self.assertIn("ExecCondition=/bin/false", text)

    def test_the_mark_is_required(self):
        with self.assertRaises(TypeError):
            base.two_deck_off_drop_in()


class FailingInstallRunner(RootRecordingRunner):
    """a3-root install fails; everything else is only logged."""

    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        super().run(args, cwd=cwd, env=env, root=root, check=check, input=input)
        if [str(a) for a in args][:2] == [A3_ROOT, "install"]:
            raise CommandFailed("a3-root install failed")
        return 0


class TheHandUnits(LaptopCase):
    def hand_unit(self, ctx):
        hand = ctx.user_units / "stemdeck.service"
        hand.write_text("[Service]\nExecStart=/opt/stemdeck\n")
        return hand

    def test_a_hand_unit_of_one_of_the_five_is_set_aside_before_the_one_install(self):
        ctx, log = self.ctx()
        hand = self.hand_unit(ctx)
        with mock.patch.object(laptop.Laptop, "_wire"), mock.patch.object(laptop.Laptop, "_units"):
            laptop.Laptop().install(ctx)
        commands = log.commands()
        aside = f"mv -n {hand} {hand}.before-package"
        self.assertIn(aside, commands)
        self.assertLess(commands.index(aside),
                        commands.index(f"root: {A3_ROOT} install {FIVE_APPS}"))

    def test_it_is_put_back_when_the_install_fails(self):
        ctx, log = self.ctx()
        ctx.runner = FailingInstallRunner(PW_DUMP, log=log)
        hand = self.hand_unit(ctx)
        with self.assertRaises(CommandFailed):
            laptop.Laptop().install(ctx)
        commands = log.commands()
        back = f"mv -n {hand}.before-package {hand}"
        self.assertIn(back, commands)
        self.assertGreater(commands.index(back),
                           commands.index(f"root: {A3_ROOT} install {FIVE_APPS}"))
        self.assertIn("systemctl --user enable stemdeck.service", commands)


class AnsweringPrompter(Prompter):
    interactive = True

    def __init__(self, roles):
        self.roles = roles

    def checklist(self, question, options, chosen):
        return list(self.roles)

    def yesno(self, question, default):
        return False   # "Install like this?" no: the run stops before any install


class Main(unittest.TestCase):
    """cli.main with a runner that records every command and runs none."""

    def main(self, argv, roles=(), prompter=None, user="aaa", place_ok=True):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home)
        conf = home / "install.conf"
        conf.write_text("[roles]\n" + "".join(f"{r} = yes\n" for r in roles)
                        + "[system]\narchive = public\n")
        ran = []

        class Untouchable(Runner):
            def run(self, args, **_kwargs):
                ran.append([str(a) for a in args])
                return 0

            def output(self, args, cwd=None):
                ran.append([str(a) for a in args])
                return ""

        with ExitStack() as stack:
            for patch in (mock.patch.object(cli, "Runner", Untouchable),
                          mock.patch.object(cli, "DEFAULT_PATH", conf),
                          mock.patch.object(cli, "make_prompter",
                                            lambda interactive: prompter or Prompter()),
                          mock.patch.object(cli.getpass, "getuser", lambda: user),
                          mock.patch.object(Path, "home", lambda: home)):
                stack.enter_context(patch)
            if place_ok:
                stack.enter_context(mock.patch.object(cli, "where_problems", lambda *_: []))
            stderr = io.StringIO()
            stack.enter_context(redirect_stderr(stderr))
            stack.enter_context(redirect_stdout(io.StringIO()))
            code = cli.main(argv)
        return code, stderr.getvalue(), ran

    def test_laptop_beside_another_role_is_refused_before_any_command(self):
        code, said, ran = self.main(["--update"], roles=("core", "laptop"))
        self.assertEqual(2, code)
        self.assertIn("core", said)
        self.assertIn("laptop", said)
        self.assertEqual([], ran)

    def test_a_wrong_user_s_first_run_touches_no_git(self):
        code, said, ran = self.main([], prompter=AnsweringPrompter(["core"]), user="root",
                                    place_ok=False)
        self.assertEqual(2, code)
        self.assertIn("cannot run like this", said)
        self.assertEqual([], [c for c in ran if c[:1] == ["git"]])

    def test_the_laptop_role_skips_the_version_checkout(self):
        def must_not_run(*_args, **_kwargs):
            raise AssertionError("the version step ran for a role without a checkout")
        with mock.patch.object(cli, "choose_version", must_not_run), \
                mock.patch.object(cli.release, "check_out", must_not_run), \
                mock.patch.object(cli.release, "catch_up", must_not_run):
            code, said, ran = self.main([], prompter=AnsweringPrompter(["laptop"]),
                                        user="somebody", place_ok=False)
        self.assertEqual(1, code, said)   # cancelled at "Install like this?"
        self.assertEqual([], [c for c in ran if c[:1] == ["git"]])


if __name__ == "__main__":
    unittest.main()
