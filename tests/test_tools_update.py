"""tools/a3-update: what it would run on a rig machine, without running it.

    python3 -m unittest discover -s tests
"""

import tempfile
import unittest
from pathlib import Path

from tools_fake import Answers, FakeRunner, Output, load_tool

update = load_tool("a3-update")

LIST_NAME = "192.168.8.5_apt_dists_a3_main_binary-amd64_Packages"

POLICY_OUTDATED = """stemdeck:
  Installed: 03.0+7
  Candidate: 03.0+9
  Version table:
     03.0+9 500
        500 http://192.168.8.5/apt a3/main amd64 Packages
 *** 03.0+7 100
        100 /var/lib/dpkg/status
"""

POLICY_CURRENT = """stemdeck:
  Installed: 03.0+9
  Candidate: 03.0+9
  Version table:
 *** 03.0+9 500
        500 http://192.168.8.5/apt a3/main amd64 Packages
        100 /var/lib/dpkg/status
"""

POLICY_ABSENT = """stemdeck:
  Installed: (none)
  Candidate: 03.0+9
  Version table:
     03.0+9 500
        500 http://192.168.8.5/apt a3/main amd64 Packages
"""


def lists_with(tmp, *packages):
    text = "".join(f"Package: {p}\nVersion: 1\nArchitecture: amd64\n\n" for p in packages)
    (Path(tmp) / LIST_NAME).write_text(text)
    (Path(tmp) / "deb.debian.org_debian_dists_forky_main_binary-amd64_Packages").write_text(
        "Package: bash\nVersion: 5\n\n")
    return tmp


def replies(policy=POLICY_OUTDATED, unit="loaded"):
    return [
        (["apt-cache", "policy"], 0, policy, ""),
        (["systemctl", "--user", "show"], 0, unit + "\n", ""),
    ]


def run_update(argv, runner, answers, lists):
    out = Output()
    code = update.main(argv, runner=runner, ask=answers, out=out, lists_dir=lists)
    return code, out


class PolicyParsing(unittest.TestCase):
    def test_installed_and_candidate_are_read(self):
        self.assertEqual(("03.0+7", "03.0+9"), update.parse_policy(POLICY_OUTDATED))

    def test_none_means_not_installed(self):
        self.assertEqual((None, "03.0+9"), update.parse_policy(POLICY_ABSENT))

    def test_an_unknown_package_has_neither(self):
        self.assertEqual((None, None), update.parse_policy(""))


class PackagesFromTheA3Source(unittest.TestCase):
    def test_only_the_a3_list_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            lists_with(tmp, "stemdeck", "a3-motion")
            self.assertEqual(["a3-motion", "stemdeck"], update.offered_packages(Path(tmp)))

    def test_no_list_means_no_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual([], update.offered_packages(Path(tmp)))


class Plan(unittest.TestCase):
    def test_versions_are_shown(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            code, out = run_update([], runner, Answers("n"), lists_with(tmp, "stemdeck"))
            self.assertIn("stemdeck 03.0+7 → 03.0+9", out.text())
            self.assertEqual(0, code)

    def test_up_to_date_asks_nothing_and_installs_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies(POLICY_CURRENT))
            code, out = run_update([], runner, Answers(), lists_with(tmp, "stemdeck"))
            self.assertIn("stemdeck 03.0+9 up to date", out.text())
            self.assertEqual([["sudo", "apt", "update"]], runner.ran())
            self.assertEqual(0, code)

    def test_not_installed_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies(POLICY_ABSENT))
            _, out = run_update([], runner, Answers(), lists_with(tmp, "stemdeck"))
            self.assertIn("stemdeck not installed — skipped, install it first", out.text())
            self.assertEqual([["sudo", "apt", "update"]], runner.ran())

    def test_named_packages_replace_the_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update(["a3-motion"], runner, Answers("n"), lists_with(tmp, "stemdeck"))
            asked = [a for a in runner.everything() if a[:2] == ["apt-cache", "policy"]]
            self.assertEqual([["apt-cache", "policy", "a3-motion"]], asked)


class Answering(unittest.TestCase):
    def test_enter_means_no(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update([], runner, Answers(""), lists_with(tmp, "stemdeck"))
            self.assertEqual([["sudo", "apt", "update"]], runner.ran())

    def test_end_of_input_means_no(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update([], runner, Answers(EOFError()), lists_with(tmp, "stemdeck"))
            self.assertEqual([["sudo", "apt", "update"]], runner.ran())

    def test_yes_installs_and_keeps_the_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update([], runner, Answers("y", "n"), lists_with(tmp, "stemdeck"))
            self.assertEqual([
                ["sudo", "apt", "update"],
                ["sudo", "apt-get", "install", "--allow-change-held-packages", "stemdeck"],
                ["sudo", "apt-mark", "hold", "stemdeck"],
            ], runner.ran())

    def test_restart_defaults_to_no_and_says_when_it_takes_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            answers = Answers("y", "")
            _, out = run_update([], runner, answers, lists_with(tmp, "stemdeck"))
            self.assertIn("restart stemdeck.service now? [y/N] ", answers.questions)
            self.assertNotIn(["systemctl", "--user", "restart", "stemdeck.service"], runner.ran())
            self.assertIn("runs after the next restart", out.text())

    def test_restart_on_yes(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update([], runner, Answers("y", "y"), lists_with(tmp, "stemdeck"))
            self.assertEqual(["systemctl", "--user", "restart", "stemdeck.service"],
                             runner.ran()[-1])

    def test_no_restart_question_without_a_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies(unit="not-found"))
            answers = Answers("y")
            run_update([], runner, answers, lists_with(tmp, "stemdeck"))
            self.assertEqual(["update these? [y/N] "], answers.questions)

    def test_yes_flag_skips_the_update_question_not_the_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            answers = Answers("n")
            run_update(["--yes"], runner, answers, lists_with(tmp, "stemdeck"))
            self.assertEqual(["restart stemdeck.service now? [y/N] "], answers.questions)
            self.assertIn(["sudo", "apt-mark", "hold", "stemdeck"], runner.ran())

    def test_a_failed_install_holds_nothing_and_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["sudo", "apt-get"], 100, "", "")] + replies())
            code, _ = run_update(["--yes"], runner, Answers(), lists_with(tmp, "stemdeck"))
            self.assertNotEqual(0, code)
            self.assertNotIn(["sudo", "apt-mark", "hold", "stemdeck"], runner.ran())

    def test_a_failed_apt_update_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["sudo", "apt", "update"], 1, "", "")] + replies())
            code, _ = run_update(["--yes"], runner, Answers(), lists_with(tmp, "stemdeck"))
            self.assertNotEqual(0, code)
            self.assertEqual([["sudo", "apt", "update"]], runner.ran())


class DryRun(unittest.TestCase):
    def test_dry_run_changes_nothing_and_asks_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            code, out = run_update(["--dry-run"], runner, Answers(), lists_with(tmp, "stemdeck"))
            self.assertEqual([], runner.ran())
            self.assertIn("stemdeck 03.0+7 → 03.0+9", out.text())
            self.assertIn("apt-get install --allow-change-held-packages stemdeck", out.text())
            self.assertEqual(0, code)


class NeverTheWholeSystem(unittest.TestCase):
    def test_no_autoremove_and_no_upgrade_ever(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner(replies())
            run_update(["--yes"], runner, Answers("y"), lists_with(tmp, "stemdeck"))
            for args in runner.everything():
                self.assertNotIn("autoremove", args)
                self.assertNotIn("upgrade", args)
                self.assertNotIn("dist-upgrade", args)
                self.assertNotIn("full-upgrade", args)


if __name__ == "__main__":
    unittest.main()
