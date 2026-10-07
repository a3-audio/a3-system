"""installer/package.py: an app's .deb from a commit, off every live path.

Run with:  python3 -m unittest discover -s tests
"""

import io
import os
import shutil
import subprocess
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

    def test_no_tag_in_the_history_is_a_build_error(self):
        failure = subprocess.CalledProcessError(128, ["git", "describe"])
        with mock.patch.object(package, "git", side_effect=failure):
            with self.assertRaises(package.BuildError) as raised:
                package.version_of(Path("/r"), "abc1234")
        self.assertIn("tag", str(raised.exception))

    def test_an_untagged_description_is_a_build_error(self):
        with mock.patch.object(package, "git", return_value="8260a7e\n"):
            with self.assertRaises(package.BuildError):
                package.version_of(Path("/r"), "abc1234")

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

    def test_a_name_that_is_a_path_is_refused(self):
        """The name becomes a folder under the build cache: `../..` would put
        the build -- and its rm -rf of src.fresh -- outside it."""
        for name in ("../..", "a/b", "Stemdeck", "x", ".hidden", "-x"):
            with self.subTest(name=name), self.assertRaises(package.BuildError):
                package.package_name(f"Package: {name}\nVersion: 0\n")

    def test_a_debian_name_with_plus_dot_and_dash_is_taken(self):
        self.assertEqual("lib-a3.x+y", package.package_name("Package: lib-a3.x+y\n"))

    def test_version_and_libraries_are_stamped_and_the_rest_kept(self):
        stamped = package.stamp_control(CONTROL, "03.0+7", "libc6 (>= 2.43), libjack-jackd2-0")
        self.assertIn("Version: 03.0+7\n", stamped)
        self.assertIn("Depends: libc6 (>= 2.43), libjack-jackd2-0, xdotool, onboard\n", stamped)
        self.assertNotIn("${shlibs:Depends}", stamped)
        self.assertTrue(stamped.endswith("Description: x\n y\n"))

    def test_a_control_without_the_token_is_an_error(self):
        with self.assertRaises(package.BuildError):
            package.stamp_control(CONTROL.replace("${shlibs:Depends}, ", ""), "03.0+7", "libc6")

    def test_a_token_on_a_folded_line_is_an_error_not_shipped(self):
        folded = CONTROL.replace("Depends: ${shlibs:Depends}, xdotool",
                                 "Depends: xdotool,\n ${shlibs:Depends}")
        with self.assertRaises(package.BuildError):
            package.stamp_control(folded, "03.0+7", "libc6")

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


HAVE_DPKG = shutil.which("dpkg-deb") and shutil.which("dpkg-shlibdeps")


class Archive(unittest.TestCase):
    @unittest.skipUnless((STEMDECK / ".git").exists(), "stemdeck submodule not checked out")
    def test_the_committed_tree_with_its_modes(self):
        dest = tmpdir(self) / "src"
        package.archive(STEMDECK, "v03.0", dest)
        self.assertTrue((dest / "CMakeLists.txt").is_file())
        self.assertTrue(os.access(dest / "tools/rig-keep-the-screen.sh", os.X_OK))
        self.assertFalse((dest / "build-make").exists())

    def test_a_revision_that_looks_like_an_option_is_refused(self):
        with mock.patch.object(package.subprocess, "run", side_effect=AssertionError("git ran")):
            with self.assertRaises(package.BuildError):
                package.archive(Path("/r"), "--output=/tmp/x", tmpdir(self) / "src")


class RevisionCheck(unittest.TestCase):
    def test_a_dash_first_revision_is_refused_before_git_is_asked(self):
        with mock.patch.object(package, "git", side_effect=AssertionError("git asked")):
            for rev in ("-x", "--upload-pack=sh"):
                with self.subTest(rev=rev):
                    with self.assertRaises(package.BuildError):
                        package.build(Path("/r"), rev=rev, out=Path("/o"), cache=Path("/c"))


class Libraries(unittest.TestCase):
    def test_only_elf_files_count(self):
        root = tmpdir(self)
        (root / "usr/bin").mkdir(parents=True)
        shutil.copy("/usr/bin/true", root / "usr/bin/app")
        (root / "usr/bin/script").write_text("#!/bin/sh\n")
        self.assertEqual([root / "usr/bin/app"], package.elf_files(root))

    @unittest.skipUnless(HAVE_DPKG, "dpkg-dev missing")
    def test_a_binary_needs_libc(self):
        stage = tmpdir(self)
        (stage / "usr/bin").mkdir(parents=True)
        shutil.copy("/usr/bin/true", stage / "usr/bin/app")
        self.assertIn("libc6", package.shlibs_depends(stage))

    def test_a_tree_without_a_binary_is_an_error(self):
        with self.assertRaises(package.BuildError):
            package.shlibs_depends(tmpdir(self))


class Pack(unittest.TestCase):
    def stage(self):
        stage = Path(tempfile.mkdtemp(dir=tmpdir(self)))  # 0700, like the builder's
        (stage / "DEBIAN").mkdir()
        (stage / "DEBIAN/control").write_text(
            "Package: a3-pack-test\nVersion: 1\nArchitecture: amd64\n"
            "Maintainer: test\nDescription: test\n")
        (stage / "usr/bin").mkdir(parents=True)
        shutil.copy("/usr/bin/true", stage / "usr/bin/a3-pack-test")
        return stage

    @unittest.skipUnless(HAVE_DPKG, "dpkg-dev missing")
    def test_the_root_is_world_readable_and_owned_by_root(self):
        final = tmpdir(self) / "debs" / "a3-pack-test_1_amd64.deb"
        package.pack(self.stage(), final)
        listing = subprocess.run(["dpkg-deb", "-c", final], check=True,
                                 capture_output=True, text=True).stdout.splitlines()
        self.assertTrue(listing[0].startswith("drwxr-xr-x root/root"), listing[0])

    @unittest.skipUnless(HAVE_DPKG, "dpkg-dev missing")
    def test_no_half_written_package_is_left(self):
        final = tmpdir(self) / "debs" / "a3-pack-test_1_amd64.deb"
        package.pack(self.stage(), final)
        self.assertEqual([final.name], [p.name for p in final.parent.iterdir()])


class DebianScripts(unittest.TestCase):
    SCRIPTS = {"control": 0o644, "postinst": 0o755, "prerm": 0o755, "postrm": 0o755}

    def source(self):
        src = tmpdir(self) / "src"
        (src / package.DEBIAN_DIR).mkdir(parents=True)
        for name, mode in self.SCRIPTS.items():
            path = src / package.DEBIAN_DIR / name
            path.write_text("x\n")
            path.chmod(0o664 if name == "control" else mode)
        return src

    def test_control_and_the_three_maintainer_scripts_arrive_with_their_modes(self):
        stage = tmpdir(self) / "stage"
        stage.mkdir()
        package.install_debian(self.source(), stage)
        for name, mode in self.SCRIPTS.items():
            with self.subTest(name=name):
                self.assertEqual(mode, (stage / "DEBIAN" / name).stat().st_mode & 0o777)
        self.assertEqual(0o755, (stage / "DEBIAN").stat().st_mode & 0o777)

    def test_a_missing_script_is_an_error(self):
        src = self.source()
        (src / package.DEBIAN_DIR / "prerm").unlink()
        stage = tmpdir(self) / "stage"
        stage.mkdir()
        with self.assertRaises(package.BuildError):
            package.install_debian(src, stage)

    @unittest.skipUnless((Path.home() / "a3-system/wt/stemdeck/feat/deb-package/packaging/DEBIAN").is_dir(),
                         "stemdeck packaging worktree missing")
    def test_stemdecks_own_four_files_are_all_there(self):
        stage = tmpdir(self) / "stage"
        stage.mkdir()
        package.install_debian(Path.home() / "a3-system/wt/stemdeck/feat/deb-package", stage)
        self.assertEqual(sorted(self.SCRIPTS), sorted(p.name for p in (stage / "DEBIAN").iterdir()))


class Build(unittest.TestCase):
    def test_a_build_into_the_checkout_is_refused_before_anything_is_written(self):
        root = tmpdir(self)
        repo = root / "stemdeck"
        repo.mkdir()
        with mock.patch.object(package, "git", side_effect=AssertionError("git asked")):
            with self.assertRaises(package.BuildError):
                package.build(repo, out=repo / "debs", cache=root / "cache")
        self.assertEqual(["stemdeck"], [p.name for p in root.iterdir()])

    def test_a_cache_inside_the_checkout_is_refused_before_anything_is_written(self):
        root = tmpdir(self)
        repo = root / "stemdeck"
        repo.mkdir()
        with mock.patch.object(package, "git", side_effect=AssertionError("git asked")), \
             mock.patch.object(package, "sync_tree", side_effect=AssertionError("synced")):
            with self.assertRaises(package.BuildError):
                package.build(repo, out=root / "debs", cache=repo / "build-make")
        self.assertEqual([], list(repo.iterdir()))

    def test_every_path_it_writes_to_is_checked(self):
        root = tmpdir(self)
        repo = root / "stemdeck"
        repo.mkdir()
        seen = []
        real = package.refuse_inside

        def spy(checkout, *paths):
            seen.extend(Path(p) for p in paths)
            real(checkout, *paths)

        control = "Package: stemdeck\n"
        answers = {"rev-parse": "c0ffee\n", "show": control}
        with mock.patch.object(package, "refuse_inside", spy), \
             mock.patch.object(package, "git", lambda repo_, *a: answers[a[0]]), \
             mock.patch.object(package, "version_of", return_value="03.0+1"), \
             mock.patch.object(package, "archive", side_effect=package.BuildError("stop")):
            with self.assertRaises(package.BuildError):
                package.build(repo, rev="abc", out=root / "debs", cache=root / "cache")
        work = root / "cache/stemdeck"
        for path in (root / "debs", root / "cache", work, work / "src", work / "build"):
            self.assertIn(path, seen)


class Main(unittest.TestCase):
    def test_it_lowers_its_priority_and_prints_the_package(self):
        with mock.patch.object(package, "build", return_value=Path("/d/x_1_amd64.deb")) as build, \
             mock.patch.object(package.os, "setpriority") as setpriority, \
             mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            self.assertEqual(0, package.main(["/r", "--rev", "abc", "--jobs", "2"]))
        setpriority.assert_called_once_with(os.PRIO_PROCESS, 0, package.NICENESS)
        self.assertEqual("/d/x_1_amd64.deb", out.getvalue().splitlines()[-1])
        self.assertEqual("abc", build.call_args.kwargs["rev"])

    def test_a_refusal_is_exit_1_with_the_reason(self):
        with mock.patch.object(package, "build", side_effect=package.BuildError("dirty")), \
             mock.patch.object(package.os, "setpriority"), \
             mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            self.assertEqual(1, package.main(["/r"]))
        self.assertIn("package: dirty", err.getvalue())


if __name__ == "__main__":
    unittest.main()
