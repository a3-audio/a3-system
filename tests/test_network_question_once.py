"""The Core's network questions are asked on the first install, or on request.

Maintainer, 2026-10-31: "the installer asks about the network every time --
that should only happen initially, or with an argument." A plain interactive
`install` asked whether to set up the network (and, on yes, six more
questions) on every run. Now a stored answer in install.conf stands, and
`install --network` asks again.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import cli  # noqa: E402
from installer.prompt import Prompter  # noqa: E402
from installer.roles import core  # noqa: E402
from installer.roles.base import Context  # noqa: E402
from installer.settings import Settings  # noqa: E402
from installer.system import Runner  # noqa: E402


class Recording(Prompter):
    interactive = True

    def __init__(self):
        self.asked = []

    def yesno(self, question, default):
        self.asked.append(question)
        return default

    def text(self, question, default):
        self.asked.append(question)
        return default


def configure(stored, ask_network=False):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "install.conf"
        if stored:
            path.write_text("[core]\n" + "".join(f"{k} = {v}\n" for k, v in stored.items()))
        prompter = Recording()
        ctx = Context(REPO, Settings(path), Runner(dry_run=True, log=lambda _m: None),
                      prompter, "debian", home=tmp, user="aaa")
        ctx.ask_network = ask_network
        with mock.patch.object(core, "differing_groups", lambda *_: []):
            core.Core().configure(ctx)
        return prompter.asked, ctx.settings


def network_questions(asked):
    return [q for q in asked if "network" in q.lower() or "Gateway" in q or "DNS" in q]


class FirstInstall(unittest.TestCase):
    def test_nothing_stored_asks(self):
        asked, _ = configure({})
        self.assertTrue(network_questions(asked), asked)


class LaterInstalls(unittest.TestCase):
    def test_a_stored_no_is_not_asked_again(self):
        asked, settings = configure({"configure_network": "no"})
        self.assertEqual([], network_questions(asked), asked)
        self.assertFalse(settings.flag("core", "configure_network"))

    def test_a_stored_yes_keeps_its_answers_unasked(self):
        asked, settings = configure({"configure_network": "yes", "address": "10.0.0.5/24"})
        self.assertEqual([], network_questions(asked), asked)
        self.assertTrue(settings.flag("core", "configure_network"))
        self.assertEqual("10.0.0.5/24", settings.get("core", "address"))

    def test_the_other_questions_are_still_asked(self):
        asked, _ = configure({"configure_network": "no"})
        self.assertTrue(any("monitor" in q for q in asked), asked)

    def test_the_network_flag_asks_again(self):
        asked, _ = configure({"configure_network": "no"}, ask_network=True)
        self.assertTrue(network_questions(asked), asked)


class TheFlag(unittest.TestCase):
    def test_it_is_parsed(self):
        self.assertTrue(cli.parse(["--network"]).network)
        self.assertFalse(cli.parse([]).network)


if __name__ == "__main__":
    unittest.main()
