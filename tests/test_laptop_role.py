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

    def wiring_ctx(self, settings=None):
        ctx, log = self.ctx(settings)
        laptop.TRUTH.write_text(json.dumps(shipped_truth()))
        engine = Path(ctx.home) / "shipped-engine.json"
        engine.write_text(json.dumps(shipped_engine()))
        for name, value in (("ENGINE_CONFIG", engine),
                            ("SHIPPED_RATE", Path(ctx.home) / "10-stemdeck-rate.conf")):
            patcher = mock.patch.object(base, name, value) if name == "SHIPPED_RATE" \
                else mock.patch.object(laptop, name, value)
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


# -- the local wiring (Task 14) -------------------------------------------------

USB = "alsa_output.usb-Focusrite_Scarlett_2i2-00.pro-output-0"


def shipped_truth():
    """The parts of the shipped truth the wiring reads; not the real file."""
    truth = truth_with_decks(4)
    truth["hosts"] = {"core": "192.168.8.10", "mixer": "192.168.8.11",
                      "local": "127.0.0.1", "any": "0.0.0.0"}
    truth["listeners"] = [{"name": "core.vu-relay", "host": "local", "port": 9003},
                          {"name": "core.osc", "host": "any", "port": 9000}]
    return truth


def shipped_engine():
    return {"engine": {"channels": 4, "decks": 2, "analogInputs": 12},
            "backend": {"type": "jack"},
            "io": {"jack": {"analog_1": ["system:capture_1"],
                            "main_sub": ["system:playback_1"],
                            "booth_sub": ["system:playback_17"],
                            "rec_L": ["beat-analyzer:bpm_1"],
                            "phones_L": ["system:playback_9"],
                            "deckA_1": ["StemDeck-A:bformat_1"]}},
            "spatial": {"order": 3}}


def conf_block(conf, name):
    """The text of `name = { ... }` in a loopback conf (no nested braces)."""
    start = conf.index(name + " = {")
    return conf[start:conf.index("}", start)]


class LocalWiring(LaptopCase):
    def test_the_truth_points_core_and_mixer_home(self):
        shipped = shipped_truth()
        truth = laptop.laptop_truth(shipped)
        self.assertEqual("127.0.0.1", truth["hosts"]["core"])
        self.assertEqual("127.0.0.1", truth["hosts"]["mixer"])
        self.assertEqual(shipped["listeners"], truth["listeners"])
        self.assertEqual(shipped["addresses"], truth["addresses"])
        self.assertEqual("0.0.0.0", truth["hosts"]["any"])
        self.assertEqual("192.168.8.10", shipped["hosts"]["core"], "the shipped dict stays")

    def test_the_engine_counts_decks_from_the_truth_when_unset(self):
        config = laptop.laptop_engine_config(shipped_engine(), None, False)
        self.assertNotIn("decks", config["engine"])
        self.assertEqual(4, config["engine"]["channels"])
        self.assertEqual({"order": 3}, config["spatial"])
        self.assertEqual(3, laptop.laptop_engine_config(shipped_engine(), 3, False)["engine"]["decks"])

    def test_rec_is_the_laptops_main_and_feeds_the_analyzer(self):
        config = laptop.laptop_engine_config(shipped_engine(), None, False)
        self.assertEqual({"rec_L": ["a3-laptop-out:playback_FL", "beat-analyzer:bpm_1"],
                          "rec_R": ["a3-laptop-out:playback_FR"]}, config["io"]["jack"])
        with_phones = laptop.laptop_engine_config(shipped_engine(), None, True)
        self.assertEqual(["a3-laptop-out:playback_RL"], with_phones["io"]["jack"]["phones_L"])
        self.assertEqual(["a3-laptop-out:playback_RR"], with_phones["io"]["jack"]["phones_R"])
        self.assertEqual(4, len(with_phones["io"]["jack"]))

    def test_no_device_means_the_default_sink(self):
        conf = laptop.loopback_conf("", (1, 2), None)
        self.assertIn("libpipewire-module-loopback", conf)
        self.assertNotIn("target.object", conf)
        self.assertIn('node.name = "a3-laptop-out"', conf)
        self.assertIn('media.class = "Audio/Sink"', conf)
        self.assertIn("audio.position = [ FL FR ]", conf)
        self.assertNotIn("AUX", conf)

    def test_a_device_is_followed_and_may_fall_back(self):
        conf = laptop.loopback_conf(USB, (3, 4), (5, 6))
        capture, playback = conf.split("playback.props")
        self.assertIn("audio.position = [ FL FR RL RR ]", capture)
        self.assertIn(f'target.object = "{USB}"', playback)
        self.assertIn("audio.position = [ AUX2 AUX3 AUX4 AUX5 ]", playback)
        self.assertIn("node.dont-fallback = false", playback)
        self.assertIn("node.passive = false", playback)
        # It must find the card again when it comes back.
        self.assertNotIn("dont-reconnect", conf)

    def test_the_analyzer_sends_to_the_local_core(self):
        self.assertIn("OSC_HOST_core=127.0.0.1:9000\n", laptop.analyzer_env(shipped_truth()))

    def test_output_channels_are_two_numbers_from_one(self):
        self.assertEqual((1, 2), laptop.output_channels("1,2"))
        self.assertEqual((3, 4), laptop.output_channels(" 3 , 4 "))
        for value in ("0,1", "1", "a,b", "1,2,3", ""):
            with self.subTest(value):
                with self.assertRaises(RoleError):
                    laptop.output_channels(value)

    # -- written into the home

    def wire(self, ctx):
        laptop.Laptop()._wire(ctx, ["A", "B", "C", "D"])

    def test_the_wiring_writes_its_files_into_the_home(self):
        ctx, _ = self.wiring_ctx({("laptop", "output_device"): USB,
                                  ("laptop", "output_main"): "1,2"})
        self.wire(ctx)
        home = Path(ctx.home)
        truth = json.loads((home / ".config/a3/laptop/a3-osc.json").read_text())
        self.assertEqual("127.0.0.1", truth["hosts"]["core"])
        engine = json.loads((home / ".config/a3/engine/engine.json").read_text())
        self.assertNotIn("decks", engine["engine"])
        conf = (home / ".config/pipewire/pipewire.conf.d/60-a3-laptop-out.conf").read_text()
        self.assertIn(USB, conf)
        env = (home / ".config/beat-analyzer/conf.d/60-a3-laptop.env").read_text()
        self.assertIn("OSC_HOST_core=127.0.0.1:9000", env)
        rate = home / ".config/pipewire/pipewire.conf.d/10-stemdeck-rate.conf"
        self.assertEqual(base.SHIPPED_RATE, Path(rate.readlink()))
        self.assertFalse((home / ".config/a3/network.json").exists())
        for path in laptop.wiring_files(home):
            with self.subTest(path):
                self.assertTrue(path.is_symlink() or path.is_file())

    def test_bad_channels_are_refused_before_any_file(self):
        ctx, _ = self.wiring_ctx({("laptop", "output_device"): USB,
                                  ("laptop", "output_main"): "a,b"})
        with self.assertRaises(RoleError):
            self.wire(ctx)
        self.assertFalse((Path(ctx.home) / ".config/a3/laptop").exists())

    def test_a_hand_edited_engine_json_stays(self):
        ctx, log = self.wiring_ctx()
        self.wire(ctx)
        engine = Path(ctx.home) / ".config/a3/engine/engine.json"
        engine.write_text('{"by": "hand"}')
        self.wire(ctx)
        self.assertEqual('{"by": "hand"}', engine.read_text())
        self.assertIn("engine.json was changed by hand: the laptop's output links are left "
                      "as they are", list(log))

    def test_an_engine_json_the_installer_did_not_write_stays(self):
        ctx, log = self.wiring_ctx()
        engine = Path(ctx.home) / ".config/a3/engine/engine.json"
        engine.parent.mkdir(parents=True)
        engine.write_text('{"by": "hand"}')
        self.wire(ctx)
        self.assertEqual('{"by": "hand"}', engine.read_text())

    def test_an_unchanged_engine_json_is_rewritten_on_reinstall(self):
        ctx, log = self.wiring_ctx()
        self.wire(ctx)
        engine = Path(ctx.home) / ".config/a3/engine/engine.json"
        ctx.settings.set("laptop", "decks", "2")
        self.wire(ctx)
        self.assertEqual(2, json.loads(engine.read_text())["engine"]["decks"])
        self.assertEqual([], [line for line in log if "changed by hand" in line])

    def test_the_sink_s_jack_name_is_the_one_the_engine_links(self):
        # pipewire-jack names a client after node.description, not node.name.
        conf = laptop.loopback_conf(USB, (1, 2), None)
        capture, playback = conf_block(conf, "capture.props"), conf_block(conf, "playback.props")
        self.assertIn(f'node.description = "{laptop.OWN_LOOPBACK}"', capture)
        self.assertNotIn(f'node.description = "{laptop.OWN_LOOPBACK}"', playback)
        self.assertIn("node.description", playback)
        self.assertNotIn("node.description", conf[:conf.index("capture.props")])
        links = laptop.laptop_engine_config(shipped_engine(), None, True)["io"]["jack"]
        clients = {peer.split(":")[0] for peers in links.values() for peer in peers}
        self.assertEqual({laptop.OWN_LOOPBACK, "beat-analyzer"}, clients)

    def test_phones_without_a_device_are_ignored_with_one_line(self):
        ctx, log = self.wiring_ctx({("laptop", "output_phones"): "3,4"})
        self.wire(ctx)
        home = Path(ctx.home)
        conf = (home / laptop.LOOPBACK_CONF).read_text()
        self.assertIn("audio.position = [ FL FR ]", conf)
        engine = json.loads((home / laptop.ENGINE_JSON).read_text())
        self.assertNotIn("phones_L", engine["io"]["jack"])
        self.assertEqual(["phones need an output device; ignored"],
                         [line for line in log if "phones" in line and "ignored" in line])

    def test_a_stored_device_without_main_channels_plays_on_1_2(self):
        ctx, _ = self.wiring_ctx({("laptop", "output_device"): USB,
                                  ("laptop", "output_main"): ""})
        self.wire(ctx)
        conf = (Path(ctx.home) / laptop.LOOPBACK_CONF).read_text()
        self.assertIn("audio.position = [ AUX0 AUX1 ]", conf)

    def test_a_truth_without_the_core_s_listener_is_a_role_error(self):
        truth = shipped_truth()
        truth["listeners"] = [entry for entry in truth["listeners"] if entry["name"] != "core.osc"]
        with self.assertRaises(RoleError) as caught:
            laptop.analyzer_env(truth)
        self.assertIn("core.osc", str(caught.exception))

    def test_an_engine_json_not_written_by_the_installer_says_so(self):
        ctx, log = self.wiring_ctx()
        engine = Path(ctx.home) / laptop.ENGINE_JSON
        engine.parent.mkdir(parents=True)
        engine.write_text('{"by": "hand"}')
        self.wire(ctx)
        self.assertIn("engine.json exists and was not written by this installer: the laptop's "
                      "output links are left as they are", list(log))
        self.assertEqual([], [line for line in log if "changed by hand" in line])


class TheSharedHomeHelpers(unittest.TestCase):
    def test_deck_host_and_screen_use_base_s_writer_and_rate(self):
        from installer.roles import screen
        self.assertIs(base.write_home_file, deckhost.write_home_file)
        self.assertIs(base.write_home_file, screen.write_home_file)
        self.assertIs(base.link_server_rate, deckhost.link_server_rate)
        self.assertEqual(Path("/usr/share/stemdeck/10-stemdeck-rate.conf"), base.SHIPPED_RATE)


REAL_UNITS = (
    Path("/home/aaa/a3-system/wt/a3-core/feat/core-app-package/packaging/a3-engine.service"),
    Path("/home/aaa/a3-system/wt/a3-core/feat/core-app-package/packaging/a3-core.service"),
    Path("/home/aaa/a3-system/wt/a3-core/feat/core-app-package/packaging/a3-core-window.service"),
    Path("/home/aaa/a3-system/a3-motion/ui/platform_config/a3-motion.service"),
    Path("/home/aaa/a3-system/wt/stemdeck/feat/deck-window-flag/.config/systemd/user/stemdeck@.service"),
    Path("/home/aaa/a3-system/wt/stemdeck/feat/deck-window-flag/.config/systemd/user/stemdeck.service"),
)
LETTERS = ["A", "B", "C", "D"]


def service_lines(text):
    """The lines after [Service], without comments."""
    lines = text.splitlines()
    return [line for line in lines[lines.index("[Service]") + 1:]
            if line and not line.startswith("#")]


class UnitsCase(LaptopCase):
    def units(self, ctx, letters=LETTERS):
        laptop.Laptop()._units(ctx, letters)

    def drop_in(self, ctx, unit):
        return (ctx.user_units / f"{unit}.d" / "laptop.conf").read_text()


class Units(UnitsCase):
    def test_every_drop_in_resets_the_environment_first(self):
        ctx, _ = self.ctx()
        self.units(ctx)
        self.assertEqual(("a3-engine.service", "a3-core.service", "a3-core-window.service",
                          "a3-motion.service", "stemdeck@.service"), laptop.UNITS_WITH_TRUTH)
        for unit in laptop.UNITS_WITH_TRUTH:
            with self.subTest(unit):
                text = self.drop_in(ctx, unit)
                self.assertTrue(text.startswith(laptop.WRITTEN_BY))
                lines = service_lines(text)
                self.assertEqual("Environment=", lines[0])
                self.assertIn("Environment=A3_OSC_TRUTH=%h/.config/a3/laptop/a3-osc.json", lines)
                self.assertIn("Environment=A3_SCREEN_TRIES=1", lines)
                self.assertIn("CPUAffinity=", lines)

    def test_no_drop_in_names_the_display(self):
        # The session's imported DISPLAY/XAUTHORITY win (Review Focus 2).
        ctx, _ = self.ctx()
        self.units(ctx)
        for path in ctx.user_units.glob("*.d/laptop.conf"):
            with self.subTest(path.parent.name):
                self.assertNotIn("DISPLAY", path.read_text())
                self.assertNotIn("XAUTHORITY", path.read_text())

    def test_the_engine_keeps_its_preload(self):
        ctx, _ = self.ctx()
        self.units(ctx)
        self.assertIn("Environment=LD_PRELOAD=/usr/lib/a3-core/libjack-rt-priority.so",
                      service_lines(self.drop_in(ctx, "a3-engine.service")))
        for unit in laptop.UNITS_WITH_TRUTH[1:]:
            with self.subTest(unit):
                self.assertNotIn("LD_PRELOAD", self.drop_in(ctx, unit))

    def test_decks_run_windowed(self):
        ctx, _ = self.ctx()
        self.units(ctx)
        self.assertIn("Environment=STEMDECK_WINDOW=",
                      service_lines(self.drop_in(ctx, "stemdeck@.service")))

    def test_the_two_deck_player_stays_off_with_the_laptop_s_mark(self):
        ctx, log = self.ctx()
        self.units(ctx)
        self.assertEqual(base.two_deck_off_drop_in(laptop.WRITTEN_BY),
                         self.drop_in(ctx, "stemdeck.service"))
        self.assertNotIn(deckhost.WRITTEN_BY, self.drop_in(ctx, "stemdeck.service"))
        self.assertIn("systemctl --user stop stemdeck.service", log.commands())

    def test_nothing_is_enabled_at_boot(self):
        ctx, log = self.ctx()
        self.units(ctx)
        self.assertEqual([], [c for c in log.commands() if "enable" in c.split()])
        self.assertEqual([], list(ctx.user_units.glob("*.wants")))
        self.assertEqual([], [c for c in log.commands()
                              if c.split()[:3] in (["systemctl", "--user", "start"],
                                                   ["systemctl", "--user", "restart"])])

    def test_the_user_manager_reloads_after_the_drop_ins(self):
        ctx, log = self.ctx()
        self.units(ctx)
        self.assertIn("systemctl --user daemon-reload", log.commands())

    def test_the_installed_letters_are_recorded(self):
        ctx, _ = self.ctx()
        self.units(ctx, ["A", "B", "C"])
        self.assertEqual("A,B,C", ctx.state.get("laptop", "letters"))

    def test_fewer_decks_stop_the_extra_instances(self):
        ctx, log = self.ctx()
        self.units(ctx, LETTERS)
        self.units(ctx, ["A", "B"])
        stops = [c for c in log.commands() if c.startswith("systemctl --user stop stemdeck@")]
        self.assertEqual(["systemctl --user stop stemdeck@C.service",
                          "systemctl --user stop stemdeck@D.service"], stops)
        self.assertEqual("A,B", ctx.state.get("laptop", "letters"))

    def test_the_install_writes_the_units_for_the_counted_decks(self):
        ctx, _ = self.ctx({("laptop", "decks"): "2"})
        with mock.patch.object(laptop.Laptop, "_wire"):
            laptop.Laptop().install(ctx)
        self.assertEqual("A,B", ctx.state.get("laptop", "letters"))

    def test_systemd_reads_the_drop_ins(self):
        if shutil.which("systemd-analyze") is None:
            self.skipTest("systemd-analyze is not installed")
        real = [path for path in REAL_UNITS if path.is_file()]
        if len(real) < len(REAL_UNITS):
            self.skipTest("the unit files of a3-core, Motion UI and StemDeck are not checked out "
                          "here: " + ", ".join(str(p) for p in REAL_UNITS if not p.is_file()))
        ctx, _ = self.ctx()
        self.units(ctx)
        tree = Path(ctx.home) / "unit-tree"
        shutil.copytree(ctx.user_units, tree)
        for path in real:
            shutil.copy(path, tree / path.name)
        # Without the default path (no trailing colon) this machine's own units
        # stay out; the targets every service is ordered after are stubs.
        for target in ("basic.target", "default.target", "graphical.target"):
            (tree / target).write_text("[Unit]\nDescription=stub\n")
        units = ["a3-engine.service", "a3-core.service", "a3-core-window.service",
                 "a3-motion.service", "stemdeck@A.service", "stemdeck.service"]
        self.assertEqual([], syntax_problems(tree, units))
        # The negative control: a bad key in a drop-in is reported, so the
        # drop-ins are read and the filter does not hide everything.
        bad = tree / "a3-engine.service.d" / "laptop.conf"
        bad.write_text(bad.read_text() + "NoSuchKey=1\n")
        self.assertTrue(any(str(bad) in line for line in syntax_problems(tree, units)))


def syntax_problems(tree, units):
    """systemd-analyze's lines, without those on missing executables: the
    apps are not installed where the tests run."""
    import os
    import subprocess
    done = subprocess.run(["systemd-analyze", "--user", "verify", *units],
                          capture_output=True, text=True,
                          env={**os.environ, "SYSTEMD_UNIT_PATH": str(tree)})
    lines = (done.stdout + done.stderr).splitlines()
    return [line for line in lines if line.strip() and "is not executable" not in line]


class Leaving(UnitsCase):
    def installed(self):
        ctx, log = self.wiring_ctx()
        laptop.Laptop()._wire(ctx, LETTERS)
        self.units(ctx)
        return ctx, log

    def test_leaving_removes_what_it_wrote_and_keeps_engine_json(self):
        ctx, log = self.installed()
        role = laptop.Laptop()
        home = Path(ctx.home)
        drop_ins = [ctx.user_units / f"{unit}.d" / "laptop.conf"
                    for unit in laptop.UNITS_WITH_TRUTH + ("stemdeck.service",)]
        self.assertEqual(sorted(drop_ins + laptop.wiring_files(home)),
                         sorted(role.leaving_files(ctx)))
        self.assertNotIn(home / laptop.ENGINE_JSON, role.leaving_files(ctx))
        self.assertTrue(any("engine.json" in item for item in role.stays))
        self.assertEqual(["a3-engine.service", "a3-core.service", "a3-core-window.service",
                          "a3-motion.service", "stemdeck@A.service", "stemdeck@B.service",
                          "stemdeck@C.service", "stemdeck@D.service"], role.leaving_units(ctx))
        self.assertEqual(list(laptop.APPS), role.leaving_packages(ctx))
        del log[:]
        role.uninstall(ctx)
        commands = log.commands()
        self.assertIn("systemctl --user disable --now stemdeck@D.service", commands)
        self.assertIn("systemctl --user disable --now a3-engine.service", commands)
        for path in drop_ins + laptop.wiring_files(home):
            with self.subTest(path):
                self.assertIn(f"rm -f {path}", commands)
        self.assertNotIn(f"rm -f {home / laptop.ENGINE_JSON}", commands)
        self.assertIn("systemctl --user daemon-reload", commands)
        self.assertEqual(f"root: {A3_ROOT} remove {FIVE_APPS}", commands[-1])
        self.assertEqual("", ctx.state.get("laptop", "letters"))

    def test_a_hand_drop_in_of_the_laptop_s_name_stays(self):
        ctx, _ = self.installed()
        hand = ctx.user_units / "a3-motion.service.d" / "laptop.conf"
        hand.write_text("[Service]\nEnvironment=MINE=1\n")
        role = laptop.Laptop()
        self.assertNotIn(hand, role.leaving_files(ctx))
        self.assertEqual([hand], role.leaving_kept(ctx))

    def test_deck_host_s_two_deck_drop_in_is_not_the_laptop_s(self):
        ctx, _ = self.ctx()
        theirs = ctx.user_units / "stemdeck.service.d" / deckhost.DROP_IN
        theirs.parent.mkdir(parents=True)
        theirs.write_text(base.two_deck_off_drop_in(deckhost.WRITTEN_BY))
        self.assertNotIn(theirs, laptop.Laptop().leaving_files(ctx))
        self.assertNotIn(theirs, laptop.Laptop().leaving_kept(ctx))
        ours = ctx.user_units / "stemdeck.service.d" / "laptop.conf"
        ours.write_text(base.two_deck_off_drop_in(laptop.WRITTEN_BY))
        self.assertFalse(deckhost._written_by_us(ours))


class FromSourceAtTheStart(Main):
    def test_laptop_with_from_source_is_refused_before_any_command(self):
        code, said, ran = self.main(["--from-source", "--update"], roles=("laptop",))
        self.assertEqual(2, code)
        self.assertIn("--from-source", said)
        self.assertEqual([], ran)

    def test_the_refusal_names_only_packages_only_roles(self):
        self.assertIsNone(cli.refused_from_source(["core", "desk"], True))
        self.assertIsNone(cli.refused_from_source(["laptop"], False))
        self.assertIn("laptop", cli.refused_from_source(["laptop"], True))


if __name__ == "__main__":
    unittest.main()
