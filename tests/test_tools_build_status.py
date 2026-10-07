"""tools/a3-build-status: what it shows, and how it degrades without rights.

    python3 -m unittest discover -s tests
"""

import os
import tempfile
import unittest
from pathlib import Path

from tools_fake import FakeRunner, Output, load_tool

status = load_tool("a3-build-status")

SHA = "0123456789abcdef0123456789abcdef01234567"

SHOW_RUNNING = """ActiveState=activating
SubState=start
StateChangeTimestamp=Wed 2026-10-07 21:40:02 CEST
"""

SHOW_DONE = """ActiveState=inactive
SubState=dead
StateChangeTimestamp=Wed 2026-10-07 23:33:39 CEST
Result=success
ExecMainExitTimestamp=Wed 2026-10-07 23:33:39 CEST
"""

PACKAGES = """Package: stemdeck
Version: 03.0+7
Architecture: amd64

Package: a3-motion
Version: 03.0+2
Architecture: amd64
"""

JOURNAL_DENIED_STDERR = (
    "Hint: You are currently not seeing messages from other users and the system.\n"
    "      Users in groups 'adm', 'systemd-journal' can see all messages.\n")


def report(runner, queue, packages="/nonexistent/Packages"):
    out = Output()
    code = status.main([], runner=runner, out=out, queue_dir=Path(queue),
                       packages_file=Path(packages))
    return code, out.text()


class Queue(unittest.TestCase):
    def test_each_entry_shows_repo_and_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "stemdeck").write_text(SHA + "\n")
            _, text = report(FakeRunner(), tmp)
            self.assertIn(f"stemdeck {SHA}", text)

    def test_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, text = report(FakeRunner(), tmp)
            self.assertIn("queue: empty", text)

    @unittest.skipIf(os.geteuid() == 0, "root reads everything")
    def test_unreadable_is_said_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue"
            queue.mkdir(mode=0o000)
            try:
                code, text = report(FakeRunner(), queue)
            finally:
                queue.chmod(0o700)
            self.assertIn("queue: not readable", text)
            self.assertEqual(0, code)


class Service(unittest.TestCase):
    def test_state_and_since(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["systemctl", "show", "a3-build.service"], 0, SHOW_RUNNING, "")])
            _, text = report(runner, tmp)
            self.assertIn("a3-build.service: activating (start) since Wed 2026-10-07 21:40:02 CEST",
                          text)

    def test_inactive_shows_the_last_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["systemctl", "show", "a3-build.service"], 0, SHOW_DONE, "")])
            _, text = report(runner, tmp)
            self.assertIn("a3-build.service: inactive (dead) since Wed 2026-10-07 23:33:39 CEST"
                          " — last run: success, 23:33:39", text)

    def test_running_shows_no_last_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["systemctl", "show", "a3-build.service"], 0,
                                  SHOW_RUNNING + "Result=success\n", "")])
            _, text = report(runner, tmp)
            self.assertNotIn("last run", text)

    def test_result_is_asked_for(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner()
            report(runner, tmp)
            [args] = [a for a in runner.everything() if a[:3] == ["systemctl", "show", "a3-build.service"]]
            self.assertIn("Result", args)
            self.assertIn("ExecMainExitTimestamp", args)


class Published(unittest.TestCase):
    def test_reprepro_list_is_shown(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["reprepro"], 0, "a3|main|amd64: stemdeck 03.0+7\n", "")])
            _, text = report(runner, tmp)
            self.assertIn("stemdeck 03.0+7", text)

    def test_falls_back_to_the_published_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            packages = Path(tmp) / "Packages"
            packages.write_text(PACKAGES)
            runner = FakeRunner([(["reprepro"], 254, "", "Error opening database\n")])
            _, text = report(runner, tmp, packages)
            self.assertIn("stemdeck 03.0+7", text)
            self.assertIn("a3-motion 03.0+2", text)

    def test_neither_is_said(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["reprepro"], 127, "", "")])
            code, text = report(runner, tmp)
            self.assertIn("published: unknown", text)
            self.assertEqual(0, code)


def build_journal(builds):
    """A journal of `builds` runs, each drowned in compiler output."""
    lines = []
    for n in range(builds):
        lines.append(f"Oct 07 23:{n:02d}:00 a3coreV01 systemd[1]: Starting a3-build.service - Build queued A3 packages...")
        lines.append(f"Oct 07 23:{n:02d}:01 a3coreV01 drain[9]: a3-build: stemdeck at {SHA}")
        lines += [f"Oct 07 23:{n:02d}:02 a3coreV01 drain[9]: juce_core.cpp:{i}: warning: unused" for i in range(40)]
        lines.append(f"Oct 07 23:{n:02d}:30 a3coreV01 drain[9]: a3-build: published stemdeck_03.0+{n}_amd64.deb")
        lines.append(f"Oct 07 23:{n:02d}:31 a3coreV01 systemd[1]: a3-build.service: Deactivated successfully.")
        lines.append(f"Oct 07 23:{n:02d}:31 a3coreV01 systemd[1]: Finished a3-build.service - Build queued A3 packages.")
    return "\n".join(lines) + "\n"


class Journal(unittest.TestCase):
    def journal(self, text, err=""):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["journalctl"], 0, text, err)])
            code, out = report(runner, tmp)
        return code, out, runner

    def test_compiler_output_is_left_out(self):
        _, text, _ = self.journal(build_journal(1))
        self.assertIn(f"a3-build: stemdeck at {SHA}", text)
        self.assertIn("a3-build: published stemdeck_03.0+0_amd64.deb", text)
        self.assertNotIn("warning", text)

    def test_only_the_last_ten_build_lines(self):
        _, text, _ = self.journal(build_journal(8))
        shown = [line for line in text.splitlines() if "a3-build: " in line and "drain" in line]
        self.assertEqual(10, len(shown))
        self.assertIn("published stemdeck_03.0+7_amd64.deb", shown[-1])
        self.assertNotIn("03.0+2_amd64", text)

    def test_the_last_systemd_result_is_shown(self):
        _, text, _ = self.journal(build_journal(2))
        result = [line for line in text.splitlines() if "systemd[1]" in line]
        self.assertEqual(1, len(result))
        self.assertIn("23:01:31", result[0])
        self.assertIn("Finished a3-build.service", result[0])

    def test_a_failed_run_is_the_result(self):
        text = build_journal(1) + (
            "Oct 07 23:50:00 a3coreV01 systemd[1]: a3-build.service: Failed with result 'exit-code'.\n"
            "Oct 07 23:50:00 a3coreV01 systemd[1]: Failed to start a3-build.service - Build.\n")
        _, out, _ = self.journal(text)
        self.assertIn("Failed to start a3-build.service", out)
        self.assertNotIn("Finished a3-build.service", out)

    def test_enough_of_the_journal_is_read(self):
        _, _, runner = self.journal("")
        [args] = [a for a in runner.everything() if a[0] == "journalctl"]
        self.assertEqual(["journalctl", "-u", "a3-build", "--no-pager"], args[:4])
        self.assertGreaterEqual(int(args[args.index("-n") + 1]), 1000)

    def test_unreadable_gives_the_one_line_hint(self):
        code, text, _ = self.journal("-- No entries --\n", JOURNAL_DENIED_STDERR)
        self.assertIn("sudo adduser $USER adm, then log in again", text)
        self.assertNotIn("No entries", text)
        self.assertEqual(0, code)


class OnlyLooks(unittest.TestCase):
    def test_runs_nothing_that_changes_anything(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner()
            report(runner, tmp)
            self.assertEqual([], runner.ran())
            for args in runner.everything():
                self.assertNotEqual("sudo", args[0])


if __name__ == "__main__":
    unittest.main()
