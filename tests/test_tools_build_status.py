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


class Journal(unittest.TestCase):
    def test_last_lines_are_asked_for(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["journalctl"], 0, "a3-build: published x.deb\n", "")])
            _, text = report(runner, tmp)
            self.assertIn("a3-build: published x.deb", text)
            self.assertIn(["journalctl", "-u", "a3-build", "-n", "15", "--no-pager"],
                          runner.everything())

    def test_unreadable_gives_the_one_line_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = FakeRunner([(["journalctl"], 0, "-- No entries --\n", JOURNAL_DENIED_STDERR)])
            code, text = report(runner, tmp)
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
