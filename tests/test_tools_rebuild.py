"""tools/a3-rebuild: queueing a build by hand, the way the gitolite hook does.

    python3 -m unittest discover -s tests
"""

import unittest

from tools_fake import FakeRunner, Output, load_tool

rebuild = load_tool("a3-rebuild")

SHA = "0123456789abcdef0123456789abcdef01234567"
MAIN = "89abcdef0123456789abcdef0123456789abcdef"


def run_rebuild(argv, runner):
    out = Output()
    code = rebuild.main(argv, runner=runner, out=out)
    return code, out.text()


def queued_with(runner):
    writes = [a for a in runner.ran() if a[:3] == ["sudo", "-u", "git"]]
    return writes


class Names(unittest.TestCase):
    def test_valid_repo_names(self):
        for name in ("stemdeck", "a3-motion-ui", "a3.core", "x+y", "0day"):
            self.assertTrue(rebuild.valid_repo(name), name)

    def test_invalid_repo_names(self):
        for name in ("", "-x", ".git", "Stemdeck", "a/b", "../etc", "a b", "a;rm"):
            self.assertFalse(rebuild.valid_repo(name), name)

    def test_commit_must_be_forty_hex(self):
        self.assertTrue(rebuild.valid_commit(SHA))
        for bad in ("", SHA[:39], SHA + "0", "g" * 40, "main"):
            self.assertFalse(rebuild.valid_commit(bad), bad)


class Refused(unittest.TestCase):
    def test_a_bad_repo_queues_nothing(self):
        runner = FakeRunner()
        code, text = run_rebuild(["../etc", SHA], runner)
        self.assertNotEqual(0, code)
        self.assertEqual([], runner.everything())
        self.assertIn("not a repository name", text)

    def test_a_bad_commit_queues_nothing(self):
        runner = FakeRunner()
        code, text = run_rebuild(["stemdeck", "main"], runner)
        self.assertNotEqual(0, code)
        self.assertEqual([], runner.everything())
        self.assertIn("40 hex", text)

    def test_an_unknown_repo_queues_nothing(self):
        runner = FakeRunner([(["git", "ls-remote"], 128, "", "FATAL: R any nope aaa DENIED\n")])
        code, _ = run_rebuild(["nope"], runner)
        self.assertNotEqual(0, code)
        self.assertEqual([], queued_with(runner))

    def test_a_repo_without_main_queues_nothing(self):
        runner = FakeRunner([(["git", "ls-remote"], 0, "", "")])
        code, text = run_rebuild(["stemdeck"], runner)
        self.assertNotEqual(0, code)
        self.assertEqual([], queued_with(runner))
        self.assertIn("no main", text)


class Queued(unittest.TestCase):
    def test_default_commit_is_main_from_gitolite(self):
        runner = FakeRunner([(["git", "ls-remote"], 0, f"{MAIN}\trefs/heads/main\n", "")])
        code, _ = run_rebuild(["stemdeck"], runner)
        self.assertEqual(0, code)
        self.assertIn(["git", "ls-remote", "git@localhost:stemdeck", "refs/heads/main"],
                      runner.everything())
        [write] = queued_with(runner)
        self.assertEqual([MAIN, "stemdeck"], write[-2:])

    def test_written_to_tmp_then_moved_as_git(self):
        runner = FakeRunner()
        code, text = run_rebuild(["stemdeck", SHA.upper()], runner)
        self.assertEqual(0, code)
        [write] = queued_with(runner)
        self.assertEqual(["sudo", "-u", "git", "sh", "-c"], write[:5])
        script = write[5]
        self.assertIn("/var/spool/a3-build/tmp/", script)
        self.assertIn("mv -f", script)
        self.assertIn("/var/spool/a3-build/queue/", script)
        self.assertEqual([SHA, "stemdeck"], write[-2:])
        self.assertIn("a3-build-status", text)
        self.assertIn("sudo journalctl -u a3-build -f", text)

    def test_a_failed_write_fails(self):
        runner = FakeRunner([(["sudo"], 1, "", "")])
        code, _ = run_rebuild(["stemdeck", SHA], runner)
        self.assertNotEqual(0, code)


if __name__ == "__main__":
    unittest.main()
