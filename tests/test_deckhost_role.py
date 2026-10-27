# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The role deck-host: a StemDeck deck on a machine without the Core (a3nuc2
runs deck B beside Motion). The stemdeck package, one deck instance with the
AES67 link map, the panel handed over by workspace, and a PTP client."""

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
from installer.roles import ALL, BY_NAME, needed_submodules  # noqa: E402
from installer.roles.base import RoleError  # noqa: E402
from installer.settings import ROLES  # noqa: E402

STOCK_PTP4L = """\
# linuxptp's stock file
[global]
#
# Default Data Set
#
twoStepFlag\t\t1
clientOnly\t\t0
socket_priority\t\t0
priority1\t\t128
priority2\t\t128
step_threshold\t\t0.0
first_step_threshold\t0.00002
"""


class InputRunner(RecordingRunner):
    """RecordingRunner that also keeps what each command was handed on stdin,
    by the command's last word (the target of `install -D ... /dev/stdin X`)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = {}

    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        words = [str(a) for a in args]
        if input is not None:
            self.inputs[words[-1]] = input
        self.log("$ " + ("sudo " if root else "") + " ".join(words))
        return 0


def deckhost_seams(stock):
    from installer.roles import apppackage, deckhost, stemdeck
    stack = ExitStack()
    stack.enter_context(mock.patch.object(stemdeck, "ensure_juce", lambda _ctx: Path("/juce")))
    stack.enter_context(mock.patch.object(stemdeck, "pinned_commit", lambda _ctx: PIN))
    stack.enter_context(mock.patch.object(apppackage.debs, "version_of", lambda *_: "03.0+7"))
    stack.enter_context(mock.patch.object(deckhost, "STOCK_PTP4L", stock))
    return stack


class DeckHostCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.stock = self.tmp / "stock-ptp4l.conf"
        self.stock.write_text(STOCK_PTP4L)

    def ctx(self, settings=None, dry_run=False):
        values = {("roles", "deck-host"): "yes", ("deck-host", "audio_port"): "enp2s0"}
        values.update(settings or {})
        home = self.tmp / "home"
        home.mkdir(exist_ok=True)
        ctx, log = context(home, values)
        ctx.runner = InputRunner(log=log)
        ctx.runner.dry_run = dry_run
        return ctx, log

    def install(self, ctx):
        from installer.roles import deckhost
        with deckhost_seams(self.stock):
            deckhost.DeckHost().install(ctx)

    def drop_in(self, ctx, letter="B"):
        return ctx.user_units / f"stemdeck@{letter}.service.d" / "deck-host.conf"

    def i3_config(self, ctx, text):
        path = ctx.home / ".config" / "i3" / "config"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path


class TheRoleIsOffered(unittest.TestCase):
    def test_it_installs_after_stemdeck_and_before_motion(self):
        names = [role.name for role in ALL]
        self.assertEqual(names.index("deck-host"), names.index("stemdeck") + 1)
        self.assertEqual(names.index("motion"), names.index("deck-host") + 1)
        self.assertIn("deck-host", ROLES)

    def test_it_builds_from_stemdeck_only(self):
        self.assertEqual(needed_submodules(["deck-host"]), ["stemdeck"])
        self.assertTrue(BY_NAME["deck-host"].needs_screen)
        self.assertIn("linuxptp", BY_NAME["deck-host"].packages)


class TheDeckInstance(DeckHostCase):
    def test_writes_the_drop_in_with_link_map_latency_and_panel(self):
        ctx, _ = self.ctx()
        self.install(ctx)
        text = self.drop_in(ctx).read_text()
        for line in ("Environment=STEMDECK_LINK_MAP=/usr/share/stemdeck/links-aes67.json",
                     "Environment=STEMDECK_PATH_LATENCY_MS=0",
                     "Environment=STEMDECK_PANEL_WORKSPACE=2:STEMDECK",
                     "Wants=a3-aes67-deck@%i.service",
                     "After=a3-aes67-deck@%i.service"):
            self.assertIn(line, text.splitlines())
        self.assertLess(text.index("[Unit]"), text.index("Wants="))
        self.assertLess(text.index("[Service]"), text.index("Environment="))

    def test_enables_the_deck_instance_by_symlink(self):
        ctx, log = self.ctx()
        self.install(ctx)
        link = ctx.user_units / "default.target.wants" / "stemdeck@B.service"
        self.assertTrue(link.is_symlink())
        self.assertEqual(Path("/usr/lib/systemd/user/stemdeck@.service"), Path(link.readlink()))
        self.assertIn("systemctl --user restart stemdeck@B.service", log.commands())

    def test_it_installs_the_stemdeck_package_the_stemdeck_way(self):
        ctx, log = self.ctx()
        self.install(ctx)
        commands = log.commands()
        build = next(c for c in commands if "installer/package.py" in c)
        self.assertIn(f"--rev {PIN}", build)
        self.assertTrue(any("apt-get install" in c and "stemdeck_03.0+7" in c for c in commands))
        self.assertIn("sudo apt-mark hold stemdeck", commands)
        # The two-deck unit is not this role's: it would fight the instance.
        self.assertFalse(any("stemdeck.service" in c and "stemdeck@" not in c
                             for c in commands if c.startswith("systemctl")), commands)

    def test_letter_and_latency_from_settings(self):
        ctx, log = self.ctx({("deck-host", "letter"): "C",
                             ("deck-host", "path_latency_ms"): "18"})
        self.install(ctx)
        text = self.drop_in(ctx, "C").read_text()
        self.assertIn("Environment=STEMDECK_PATH_LATENCY_MS=18", text.splitlines())
        self.assertTrue((ctx.user_units / "default.target.wants" / "stemdeck@C.service")
                        .is_symlink())
        self.assertFalse(self.drop_in(ctx, "B").exists())

    def test_the_defaults_are_deck_b_without_latency(self):
        from installer.settings import Settings
        s = Settings(self.tmp / "none.conf")
        self.assertEqual("B", s.get("deck-host", "letter"))
        self.assertEqual("0", s.get("deck-host", "path_latency_ms"))

    def test_a_letter_outside_a_to_d_is_refused(self):
        ctx, _ = self.ctx({("deck-host", "letter"): "E"})
        with self.assertRaises(RoleError):
            self.install(ctx)

    def test_a_latency_that_is_no_whole_number_is_refused(self):
        ctx, _ = self.ctx({("deck-host", "path_latency_ms"): "-3"})
        with self.assertRaises(RoleError):
            self.install(ctx)


class ThePanel(DeckHostCase):
    def panel(self, ctx):
        return ctx.user_units / "a3-motion.service.d" / "panel-follows.conf"

    def test_motion_drop_in_only_with_the_motion_role(self):
        ctx, _ = self.ctx({("roles", "motion"): "yes"})
        self.install(ctx)
        self.assertIn("Environment=A3_MOTION_PANEL_WORKSPACE=1:MOTION",
                      self.panel(ctx).read_text().splitlines())

        alone, _ = self.ctx({("roles", "motion"): "no"})
        shutil.rmtree(alone.home / ".config")
        self.install(alone)
        self.assertFalse(self.panel(alone).exists())


class TheRefusals(DeckHostCase):
    def test_refuses_beside_the_core_role(self):
        ctx, log = self.ctx({("roles", "core"): "yes"})
        with self.assertRaises(RoleError) as caught:
            self.install(ctx)
        self.assertIn("deck A is local there", str(caught.exception))
        self.assertEqual([], log.commands())

    def test_refuses_beside_the_two_deck_stemdeck_role(self):
        ctx, log = self.ctx({("roles", "stemdeck"): "yes"})
        with self.assertRaises(RoleError):
            self.install(ctx)
        self.assertEqual([], log.commands())


class TheI3Rule(DeckHostCase):
    def test_a_config_without_a_stemdeck_rule_gets_the_block(self):
        ctx, _ = self.ctx()
        path = self.i3_config(ctx, "set $mod Mod4\n")
        self.install(ctx)
        text = path.read_text()
        self.assertTrue(text.startswith("set $mod Mod4\n"))
        self.assertIn('assign [class="StemDeck"] number "2:STEMDECK"', text.splitlines())

    def test_the_block_is_written_once(self):
        ctx, _ = self.ctx()
        path = self.i3_config(ctx, "set $mod Mod4\n")
        self.install(ctx)
        once = path.read_text()
        self.install(ctx)
        self.assertEqual(once, path.read_text())

    def test_a_config_with_its_own_stemdeck_rule_stays(self):
        ctx, _ = self.ctx()
        text = 'set $ws2 "2:STEMDECK"\nassign [class="StemDeck"] number $ws2\n'
        path = self.i3_config(ctx, text)
        self.install(ctx)
        self.assertEqual(text, path.read_text())

    def test_no_config_is_not_created(self):
        """i3 then runs /etc/i3/config; a file with one rule would replace it."""
        ctx, _ = self.ctx()
        self.install(ctx)
        self.assertFalse((ctx.home / ".config" / "i3" / "config").exists())


class ThePtpClient(DeckHostCase):
    CONF = "/etc/linuxptp/a3-ptp4l.conf"
    DROP_IN = "/etc/systemd/system/ptp4l@.service.d/a3.conf"

    def test_the_client_config_is_the_stock_one_with_three_keys_changed(self):
        from installer.roles.deckhost import client_ptp4l_config, ptp4l_keys
        ours, stock = ptp4l_keys(client_ptp4l_config(STOCK_PTP4L)), ptp4l_keys(STOCK_PTP4L)
        self.assertEqual({"clientOnly": "1", "priority1": "128", "step_threshold": "0.001"},
                         {k: ours[k] for k in ("clientOnly", "priority1", "step_threshold")})
        self.assertEqual(set(stock), set(ours))
        for key in set(stock) - {"clientOnly", "priority1", "step_threshold"}:
            self.assertEqual(stock[key], ours[key], key)
        self.assertIn("[global]", client_ptp4l_config(STOCK_PTP4L).splitlines())

    def test_a_stock_file_without_a_key_is_refused(self):
        from installer.roles.deckhost import client_ptp4l_config
        with self.assertRaises(RoleError):
            client_ptp4l_config(STOCK_PTP4L.replace("step_threshold\t\t0.0\n", ""))

    def test_it_writes_both_files_as_root_and_enables_ptp4l_on_the_audio_port(self):
        ctx, log = self.ctx()
        self.install(ctx)
        commands = log.commands()
        self.assertIn(f"sudo install -D -m 644 /dev/stdin {self.CONF}", commands)
        self.assertIn(f"sudo install -D -m 644 /dev/stdin {self.DROP_IN}", commands)
        self.assertIn("sudo systemctl enable ptp4l@enp2s0.service", commands)
        self.assertFalse(any("ptp4l" in c and "start" in c for c in commands), commands)
        self.assertIn("clientOnly\t\t1", ctx.runner.inputs[self.CONF])
        self.assertEqual(["ExecStart=",
                          "ExecStart=/usr/sbin/ptp4l -f /etc/linuxptp/a3-ptp4l.conf -i %I"],
                         [l for l in ctx.runner.inputs[self.DROP_IN].splitlines()
                          if l.startswith("ExecStart")])

    def test_the_stock_file_is_never_written(self):
        ctx, log = self.ctx()
        self.install(ctx)
        self.assertFalse(any("/etc/linuxptp/ptp4l.conf" in c for c in log.commands()))
        self.assertEqual(STOCK_PTP4L, self.stock.read_text())

    def test_without_an_audio_port_there_is_no_ptp(self):
        ctx, log = self.ctx({("deck-host", "audio_port"): ""})
        self.install(ctx)
        self.assertFalse(any("ptp4l" in c for c in log.commands()), log.commands())


class DryRun(DeckHostCase):
    def test_dry_run_writes_nothing(self):
        ctx, _ = self.ctx({("roles", "motion"): "yes"}, dry_run=True)
        i3 = self.i3_config(ctx, "set $mod Mod4\n")
        before = sorted(p for p in ctx.home.rglob("*"))
        self.install(ctx)
        self.assertEqual(before, sorted(p for p in ctx.home.rglob("*")))
        self.assertEqual("set $mod Mod4\n", i3.read_text())


class Leaving(DeckHostCase):
    def test_leaving_removes_only_its_files(self):
        from installer.roles import deckhost
        ctx, _ = self.ctx({("roles", "motion"): "yes"})
        i3 = self.i3_config(ctx, "set $mod Mod4\n")
        self.install(ctx)
        hand = ctx.user_units / "stemdeck@B.service.d" / "by-hand.conf"
        hand.write_text("[Service]\nNice=0\n")
        motion_own = ctx.user_units / "a3-motion.service.d" / "display.conf"
        motion_own.write_text("[Service]\n")

        ctx.runner = InputRunner(log=ctx.runner.log)
        ctx.runner.log.clear()
        role = deckhost.DeckHost()
        role.uninstall(ctx)
        commands = ctx.runner.log.commands()

        removed = [c.split()[-1] for c in commands if " rm -f " in f" {c}"]
        self.assertEqual(sorted([
            str(self.drop_in(ctx)),
            str(ctx.user_units / "default.target.wants" / "stemdeck@B.service"),
            str(ctx.user_units / "a3-motion.service.d" / "panel-follows.conf"),
            "/etc/linuxptp/a3-ptp4l.conf",
            "/etc/systemd/system/ptp4l@.service.d/a3.conf"]), sorted(removed))
        self.assertIn("sudo rm -f /etc/linuxptp/a3-ptp4l.conf", commands)
        self.assertIn("systemctl --user disable --now stemdeck@B.service", commands)
        self.assertIn("sudo systemctl disable ptp4l@enp2s0.service", commands)
        self.assertFalse(any("apt-get" in c for c in commands), commands)
        self.assertEqual("set $mod Mod4\n", i3.read_text())
        self.assertTrue(hand.exists() and motion_own.exists())

    def test_leaving_keeps_a_stemdeck_rule_it_did_not_write(self):
        from installer.roles import deckhost
        ctx, _ = self.ctx()
        text = 'assign [class="StemDeck"] number $ws2\n'
        i3 = self.i3_config(ctx, text)
        deckhost.DeckHost().uninstall(ctx)
        self.assertEqual(text, i3.read_text())

    def test_the_dialog_names_the_package_as_staying(self):
        from installer.roles import deckhost
        ctx, _ = self.ctx()
        lines = "\n".join(deckhost.DeckHost().leaving_lines(ctx))
        self.assertIn("deck-host.conf", lines)
        self.assertIn("/etc/linuxptp/a3-ptp4l.conf", lines)
        self.assertIn("stemdeck package", lines)


if __name__ == "__main__":
    unittest.main()
