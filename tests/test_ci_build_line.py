"""ci/build_line.py: build one package line's .debs from the umbrella's pins.

Run with:  python3 -m unittest discover -s tests
"""

import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from ci import build_line  # noqa: E402

UMBRELLA = Path("/umbrella")
SHA = {
    "a3-core": "c" * 40, "stemdeck": "d" * 40, "a3-mixer": "e" * 40,
    "a3-motion": "a" * 40, "beat-analyzer": "b" * 40, "ui-in-motion": "f" * 40,
}
BUILD_DEPENDS = "libasound2-dev\nlibx11-dev\npython3\ndpkg-dev\n"


class FakeGit:
    """Answers git ls-tree / git show for an umbrella with one nested submodule."""

    def __init__(self):
        self.calls = []

    def __call__(self, command):
        self.calls.append(list(command))
        if command[0] != "git":
            raise AssertionError(f"unexpected command {command}")
        folder, *git_args = command[2:] if command[1] == "-C" else (None, *command[1:])
        if git_args[0] == "show":
            return BUILD_DEPENDS
        assert git_args[0] == "ls-tree", git_args
        rev, path = git_args[1], git_args[2]
        if folder == str(UMBRELLA) and path in ("a3-core", "stemdeck", "a3-mixer",
                                                 "a3-motion", "beat-analyzer"):
            return f"160000 commit {SHA[path]}\t{path}\n"
        if folder == str(UMBRELLA) and path == "a3-motion/ui":
            return ""  # the umbrella's tree stops at a3-motion
        if folder == str(UMBRELLA / "a3-motion") and rev == SHA["a3-motion"] and path == "ui":
            return f"160000 commit {SHA['ui-in-motion']}\tui\n"
        return ""


def line(arch="amd64", paths=("a3-core", "stemdeck")):
    return {"arch": arch, "builds": [{"path": p, "recipes": ["packaging"]} for p in paths]}


def commands(line_, git=None):
    return build_line.build_commands(line_, UMBRELLA, Path("/out"), Path("/cache"),
                                     Path("/juce"), 2, run=git or FakeGit())


class Commands(unittest.TestCase):
    def test_each_submodule_is_built_at_the_umbrellas_pin(self):
        built = commands(line(paths=("a3-core", "stemdeck", "a3-mixer")))
        self.assertEqual(built[0], [
            "python3", "-I", "/umbrella/installer/package.py", "/umbrella/a3-core",
            "--rev", SHA["a3-core"], "--out", "/out", "--cache", "/cache",
            "--juce", "/juce", "--jobs", "2", "--recipe", "packaging"])
        self.assertEqual([c[5] for c in built], [SHA["a3-core"], SHA["stemdeck"], SHA["a3-mixer"]])

    def test_a_nested_submodule_is_built_at_its_parents_pin(self):
        built = commands(line(paths=("a3-motion/ui",)))
        self.assertEqual(built[0][3], "/umbrella/a3-motion/ui")
        self.assertEqual(built[0][5], SHA["ui-in-motion"])

    def test_a_repo_with_two_recipes_yields_two_debs(self):
        two = {"arch": "amd64", "builds": [
            {"path": "a3-core", "recipes": ["packaging/app", "packaging"]}]}
        built = commands(two)
        self.assertEqual(len(built), 2)
        self.assertEqual([c[-1] for c in built], ["packaging/app", "packaging"])
        self.assertEqual({c[3] for c in built}, {"/umbrella/a3-core"})
        self.assertEqual({c[5] for c in built}, {SHA["a3-core"]})

    def test_a_path_that_is_no_submodule_is_refused(self):
        with self.assertRaisesRegex(build_line.BuildLineError, "nowhere"):
            commands(line(paths=("nowhere",)))


class Main(unittest.TestCase):
    def run_main(self, argv, run, fields=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()) as err:
            code = build_line.main(argv, run=run)
        return code, out.getvalue(), err.getvalue()

    def test_an_unknown_suite_is_refused_with_the_known_ones(self):
        code, _, err = self.run_main(["bookworm"], FakeGit())
        self.assertEqual(code, 1)
        self.assertIn("bookworm", err)
        self.assertIn("forky", err)
        self.assertIn("trixie", err)

    def fake_builder(self, architecture):
        git = FakeGit()

        def run(command):
            if command[0] == "python3":
                return f"progress\n/out/{Path(command[3]).name}_1.0_amd64.deb\n"
            if command[0] == "dpkg-deb":
                return architecture + "\n"
            return git(command)
        return run

    def test_the_debs_are_printed_one_per_line(self):
        code, out, _ = self.run_main(["trixie", "--repo", str(UMBRELLA)],
                                     self.fake_builder("arm64"))
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines()[1], "/out/stemdeck_1.0_amd64.deb")
        self.assertEqual(len(out.splitlines()), 5)

    def test_every_deb_of_a_two_recipe_repo_is_architecture_checked(self):
        code, out, err = self.run_main(["forky", "--repo", str(UMBRELLA)],
                                       self.fake_builder("amd64"))
        self.assertEqual(code, 0, err)
        self.assertEqual(len(out.splitlines()), 6)

    def test_the_second_recipe_failing_names_the_repo_and_recipe(self):
        git = FakeGit()

        def run(command):
            if command[0] == "python3" and command[-1] == "packaging" and "a3-core" in command[3]:
                raise build_line.BuildLineError("boom")
            if command[0] == "python3":
                return f"/out/{Path(command[3]).name}_{command[-1].replace('/', '-')}.deb\n"
            if command[0] == "dpkg-deb":
                return "amd64\n"
            return git(command)
        code, _, err = self.run_main(["forky", "--repo", str(UMBRELLA)], run)
        self.assertEqual(code, 1)
        self.assertIn("a3-core (packaging)", err)

    def test_trixie_builds_the_program_package_only(self):
        lines = build_line.load_lines()
        core = [b for b in lines["trixie"]["builds"] if b["path"] == "a3-core"]
        self.assertEqual(core, [{"path": "a3-core", "recipes": ["packaging/app"]}])
        forky = [b for b in lines["forky"]["builds"] if b["path"] == "a3-core"]
        self.assertEqual(forky, [{"path": "a3-core", "recipes": ["packaging/app", "packaging"]}])

    def test_a_deb_whose_architecture_differs_from_the_line_stops_the_build(self):
        code, out, err = self.run_main(["forky", "--repo", str(UMBRELLA)],
                                       self.fake_builder("arm64"))
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("a3-core (packaging/app)", err)
        self.assertIn("arm64", err)


class BuildDepends(unittest.TestCase):
    def forky_depends(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(build_line.main(["forky", "--build-depends"]), 0)
        return out.getvalue().splitlines()

    def test_build_depends_cover_a3_cores_build_depends_file(self):
        git = FakeGit()
        pinned = git(["git", "-C", str(UMBRELLA / "a3-core"), "show",
                      f"{SHA['a3-core']}:packaging/build-depends"]).split()
        self.assertGreater(len(pinned), 0)
        self.assertLessEqual(set(pinned), set(self.forky_depends()))

    @unittest.skipUnless(Path("/home/aaa/a3-system/a3-core/packaging/build-depends").exists(),
                         "needs the main checkout's a3-core")
    def test_build_depends_cover_the_real_a3_core_file(self):
        real = Path("/home/aaa/a3-system/a3-core/packaging/build-depends").read_text().split()
        self.assertLessEqual(set(real), set(self.forky_depends()))

    def test_build_depends_are_sorted_and_unique(self):
        names = self.forky_depends()
        self.assertEqual(names, sorted(set(names)))

    def test_build_depends_work_when_run_as_a_script(self):
        done = subprocess.run([sys.executable, str(REPO / "ci" / "build_line.py"),
                               "trixie", "--build-depends"],
                              capture_output=True, text=True, cwd="/")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("ccache", done.stdout.split())

    def test_build_depends_include_the_ci_tools(self):
        self.assertLessEqual(set(build_line.CI_TOOLS), set(self.forky_depends()))


if __name__ == "__main__":
    unittest.main()
