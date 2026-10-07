"""installer/package.py: an app's .deb from a commit, off every live path.

Run with:  python3 -m unittest discover -s tests
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import package  # noqa: E402

STEMDECK = REPO / "stemdeck"


def tmpdir(case):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    return Path(tmp.name)


class DebianVersion(unittest.TestCase):
    def test_tag_plus_commits(self):
        self.assertEqual("03.0+63", package.debian_version("v03.0-63-g2656b74\n"))

    def test_a_fresh_tag_is_plus_zero(self):
        self.assertEqual("03.0+0", package.debian_version("v03.0-0-g8260a7e"))

    def test_no_tag_is_an_error_not_a_guess(self):
        with self.assertRaises(ValueError):
            package.debian_version("8260a7e")

    def test_version_of_a_revision_asks_git_for_that_revision(self):
        with mock.patch.object(package, "git", return_value="v03.0-7-gabc1234\n") as git:
            self.assertEqual("03.0+7", package.version_of(Path("/r"), "abc1234"))
        git.assert_called_once_with(Path("/r"), "describe", "--tags", "--long",
                                    "--match", "v*", "abc1234")

    @unittest.skipUnless((STEMDECK / ".git").exists(), "stemdeck submodule not checked out")
    def test_stemdecks_first_tag(self):
        self.assertEqual("03.0+0", package.version_of(STEMDECK, "v03.0"))


class RefuseDirty(unittest.TestCase):
    def test_by_hand_a_tracked_change_is_refused_and_named(self):
        with mock.patch.object(package, "git", return_value=" M Source/Recorder.h\n"):
            with self.assertRaises(package.BuildError) as raised:
                package.refuse_dirty(Path("/r"), None)
        self.assertIn("Source/Recorder.h", str(raised.exception))

    def test_by_hand_a_clean_tree_builds(self):
        with mock.patch.object(package, "git", return_value=""):
            package.refuse_dirty(Path("/r"), None)

    def test_a_named_revision_ignores_the_working_copy(self):
        with mock.patch.object(package, "git", side_effect=AssertionError("git asked")):
            package.refuse_dirty(Path("/r"), "abc1234")

    def test_untracked_files_do_not_count(self):
        with mock.patch.object(package, "git", return_value="") as git:
            package.refuse_dirty(Path("/r"), None)
        self.assertIn("--untracked-files=no", git.call_args.args)


class RefuseInside(unittest.TestCase):
    def test_nothing_is_written_into_the_checkout(self):
        repo = tmpdir(self) / "stemdeck"
        repo.mkdir()
        for inside in (repo, repo / "build-make", repo / "a" / "b"):
            with self.subTest(path=inside):
                with self.assertRaises(package.BuildError):
                    package.refuse_inside(repo, inside)

    def test_nothing_is_written_under_usr(self):
        with self.assertRaises(package.BuildError):
            package.refuse_inside(Path("/home/x/repo"), Path("/usr/lib/stemdeck"))

    def test_the_cache_and_the_debs_folder_are_fine(self):
        home = tmpdir(self)
        package.refuse_inside(home / "a3-system/stemdeck", home / ".cache/a3-build", home / "a3-debs")


CONTROL = ("Package: stemdeck\nVersion: 0\nArchitecture: amd64\n"
           "Depends: ${shlibs:Depends}, xdotool, onboard\nDescription: x\n y\n")


class Control(unittest.TestCase):
    def test_the_name(self):
        self.assertEqual("stemdeck", package.package_name(CONTROL))

    def test_no_name_is_an_error(self):
        with self.assertRaises(package.BuildError):
            package.package_name("Version: 0\n")

    def test_version_and_libraries_are_stamped_and_the_rest_kept(self):
        stamped = package.stamp_control(CONTROL, "03.0+7", "libc6 (>= 2.43), libjack-jackd2-0")
        self.assertIn("Version: 03.0+7\n", stamped)
        self.assertIn("Depends: libc6 (>= 2.43), libjack-jackd2-0, xdotool, onboard\n", stamped)
        self.assertNotIn("${shlibs:Depends}", stamped)
        self.assertTrue(stamped.endswith("Description: x\n y\n"))

    def test_no_libraries_is_an_error(self):
        with self.assertRaises(ValueError):
            package.stamp_control(CONTROL, "03.0+7", "")


class SyncTree(unittest.TestCase):
    """git archive stamps every file with the commit's time, older than the
    last build's objects: only files whose content changed may get a new
    mtime, or make would skip a changed source."""

    def setUp(self):
        root = tmpdir(self)
        self.fresh, self.kept = root / "fresh", root / "kept"

    def write(self, base, files):
        if base.exists():
            import shutil
            shutil.rmtree(base)
        for name, text in files.items():
            (base / name).parent.mkdir(parents=True, exist_ok=True)
            (base / name).write_text(text)

    def test_unchanged_keeps_its_time_changed_gets_a_new_one(self):
        self.write(self.fresh, {"a.cpp": "one", "b.cpp": "two"})
        package.sync_tree(self.fresh, self.kept)
        for name in ("a.cpp", "b.cpp"):
            os.utime(self.kept / name, (1_000_000, 1_000_000))
        self.write(self.fresh, {"a.cpp": "one", "b.cpp": "TWO"})
        package.sync_tree(self.fresh, self.kept)
        self.assertEqual(1_000_000, int((self.kept / "a.cpp").stat().st_mtime))
        self.assertGreater((self.kept / "b.cpp").stat().st_mtime, 1_000_000)
        self.assertEqual("TWO", (self.kept / "b.cpp").read_text())

    def test_new_files_come_and_dropped_files_go(self):
        self.write(self.fresh, {"old.cpp": "x", "dir/gone.h": "y"})
        package.sync_tree(self.fresh, self.kept)
        self.write(self.fresh, {"new.cpp": "z"})
        package.sync_tree(self.fresh, self.kept)
        self.assertEqual({"new.cpp"}, {str(p.relative_to(self.kept)) for p in self.kept.rglob("*")})

    def test_the_executable_bit_is_carried(self):
        self.write(self.fresh, {"tool": "#!/bin/sh\n"})
        (self.fresh / "tool").chmod(0o755)
        package.sync_tree(self.fresh, self.kept)
        self.assertEqual(0o755, (self.kept / "tool").stat().st_mode & 0o777)

    def test_symlinks_stay_symlinks(self):
        self.write(self.fresh, {"real": "x"})
        (self.fresh / "link").symlink_to("real")
        package.sync_tree(self.fresh, self.kept)
        self.assertEqual("real", os.readlink(self.kept / "link"))


class DebPath(unittest.TestCase):
    def test_debian_naming(self):
        self.assertEqual(Path("/d/stemdeck_03.0+7_amd64.deb"),
                         package.deb_path(Path("/d"), "stemdeck", "03.0+7"))


if __name__ == "__main__":
    unittest.main()
