"""ci/install_test.py: install every package of a line's archive into a clean root.

Run with:  python3 -m unittest discover -s tests
"""

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from ci import install_test  # noqa: E402

PACKAGES = (
    "Package: a3-core\nVersion: 1.0\nArchitecture: amd64\n\n"
    "Package: stemdeck\nVersion: 2.0\nArchitecture: amd64\n\n"
    "Package: a3-desk\nVersion: 3.0\nArchitecture: all\n")
NAMES = ["a3-core", "stemdeck", "a3-desk"]


def make_archive(case, suite="forky", arch="amd64"):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    folder = Path(tmp.name) / "dists" / suite / "main" / f"binary-{arch}"
    folder.mkdir(parents=True)
    (folder / "Packages").write_text(PACKAGES)
    return Path(tmp.name)


class FakeRunner:
    """Records every command; `fail` maps a command's first words to output."""

    def __init__(self, fail=None, unknown_user=True):
        self.calls = []
        self.inputs = {}
        self.fail = fail or {}
        self.unknown_user = unknown_user

    def __call__(self, command, input=None):
        self.calls.append(list(command))
        if input is not None:
            self.inputs[command[0]] = input
        for words, output in self.fail.items():
            if command[:len(words)] == list(words):
                return SimpleNamespace(returncode=100, stdout="", stderr=output)
        if command[:2] == ["id", "aaa"] and self.unknown_user:
            return SimpleNamespace(returncode=1, stdout="", stderr="no such user")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def starting(self, *words):
        return [c for c in self.calls if c[:len(words)] == list(words)]


class CleanRootInstall(unittest.TestCase):
    def install(self, runner=None):
        root = make_archive(self)
        runner = runner or FakeRunner()
        sources = Path(tempfile.mkdtemp()) / "a3-ci.list"
        self.addCleanup(lambda: sources.exists() and sources.unlink())
        count = install_test.install_in_clean_root(root, "forky", runner, sources)
        return root, runner, sources, count

    def test_every_package_of_the_index_is_installed_in_one_call(self):
        _, runner, _, count = self.install()
        installs = runner.starting("apt-get", "install")
        self.assertEqual(len(installs), 1)
        self.assertEqual(installs[0][-3:], NAMES)
        self.assertIn("-y", installs[0])
        self.assertEqual(count, 3)

    def test_each_package_is_checked_installed_afterwards(self):
        _, runner, _, _ = self.install()
        self.assertEqual([c[-1] for c in runner.starting("dpkg", "-s")], NAMES)

    def test_the_archive_is_a_trusted_source_and_apt_is_updated_first(self):
        root, runner, sources, _ = self.install()
        self.assertEqual(sources.read_text(),
                         f"deb [trusted=yes] file:{root} forky main\n")
        order = [c[:2] for c in runner.calls]
        self.assertLess(order.index(["apt-get", "update"]),
                        order.index(["apt-get", "install"]))

    def test_the_user_aaa_is_created_before_anything_installs(self):
        _, runner, _, _ = self.install()
        self.assertEqual(runner.starting("useradd"), [["useradd", "-m", "aaa"]])
        self.assertLess(runner.calls.index(["useradd", "-m", "aaa"]),
                        runner.calls.index(runner.starting("apt-get", "install")[0]))

    def test_an_existing_user_aaa_is_left_alone(self):
        _, runner, _, _ = self.install(FakeRunner(unknown_user=False))
        self.assertEqual(runner.starting("useradd"), [])

    def test_a3_cores_questions_are_preseeded_to_touch_nothing(self):
        _, runner, _, _ = self.install()
        seeded = runner.inputs["debconf-set-selections"]
        self.assertIn("a3-core a3-core/configure-network boolean false", seeded)
        self.assertIn("a3-core a3-core/replace-config multiselect \n", seeded)
        self.assertLess(runner.calls.index(["debconf-set-selections"]),
                        runner.calls.index(runner.starting("apt-get", "install")[0]))

    def test_a_failing_postinst_output_reaches_the_error(self):
        runner = FakeRunner(fail={("apt-get", "install"): (
            "The following packages have unmet dependencies:\n"
            " a3-core : Depends: libfoo1 but it is not installable\n"
            "Setting up a3-core (1.0) ...\n"
            "a3-core postinst: cannot write /home/aaa/.config: Permission denied\n"
            "dpkg: error processing package a3-core (--configure):\n")})
        with self.assertRaises(install_test.InstallTestError) as caught:
            self.install(runner)
        self.assertIn("cannot write /home/aaa/.config", str(caught.exception))

    def test_a_missing_dependency_is_named_in_the_error(self):
        runner = FakeRunner(fail={("apt-get", "install"): (
            "The following packages have unmet dependencies:\n"
            " a3-core : Depends: libfoo1 but it is not installable\n")})
        with self.assertRaises(install_test.InstallTestError) as caught:
            self.install(runner)
        self.assertIn("libfoo1", str(caught.exception))


class SimulatedInstall(unittest.TestCase):
    def keyring(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        keyring = Path(folder.name) / "debian.gpg"
        keyring.write_bytes(b"")
        return keyring

    def simulate(self, runner=None, keyring=None):
        keyring = keyring or self.keyring()
        root = make_archive(self)
        runner = runner or FakeRunner()
        work = Path(tempfile.mkdtemp())
        count = install_test.simulate_install(root, "forky", runner, work, keyring)
        return root, runner, work, count

    def test_simulate_never_needs_root_and_starts_from_an_empty_dpkg_status(self):
        _, runner, work, count = self.simulate()
        self.assertEqual(count, 3)
        self.assertEqual((work / "status").read_text(), "")
        for forbidden in ("useradd", "debconf-set-selections", "dpkg"):
            self.assertEqual(runner.starting(forbidden), [])
        install = runner.starting("apt-get")[-1]
        self.assertIn("-s", install)
        self.assertEqual(install[-3:], NAMES)
        for call in runner.starting("apt-get"):
            self.assertIn(f"Dir::State::status={work / 'status'}", call)
            self.assertIn(f"Dir::State={work / 'state'}", call)
            self.assertIn(f"Dir::Cache={work / 'cache'}", call)
            self.assertIn("APT::Architecture=amd64", call)

    def test_the_private_sources_are_debian_plus_the_local_archive(self):
        root, _, work, _ = self.simulate()
        sources = (work / "sources.list").read_text().splitlines()
        self.assertEqual(sources, [
            "deb http://deb.debian.org/debian forky main",
            f"deb [trusted=yes] file:{root} forky main"])
        self.assertTrue((work / "sources.list.d").is_dir())

    def test_debians_keyring_is_the_only_trust_when_present(self):
        keyring = self.keyring()
        _, runner, _, _ = self.simulate(keyring=keyring)
        self.assertIn(f"Dir::Etc::trusted={keyring}", runner.starting("apt-get")[0])

    def test_without_debians_keyring_apt_gets_no_trusted_file(self):
        _, runner, _, _ = self.simulate(keyring=Path("/nonexistent/key.gpg"))
        self.assertFalse([a for a in runner.starting("apt-get")[0]
                          if a.startswith("Dir::Etc::trusted=")])

    def test_updates_before_it_simulates(self):
        _, runner, _, _ = self.simulate()
        self.assertEqual([c[-1] for c in runner.starting("apt-get")][0], "update")

    def test_an_unmet_dependency_names_the_package(self):
        runner = FakeRunner(fail={("apt-get",): "x : Depends: libbar2 but it is not installable"})
        with self.assertRaises(install_test.InstallTestError) as caught:
            self.simulate(runner)
        self.assertIn("libbar2", str(caught.exception))


class ReadingTheIndex(unittest.TestCase):
    def test_names_and_the_architecture_come_from_the_suites_packages_file(self):
        root = make_archive(self, "trixie", "arm64")
        self.assertEqual(install_test.read_index(root, "trixie"), ("arm64", NAMES))

    def test_a_suite_without_an_index_is_an_error(self):
        root = make_archive(self)
        with self.assertRaises(install_test.InstallTestError):
            install_test.read_index(root, "nosuch")


if __name__ == "__main__":
    unittest.main()
