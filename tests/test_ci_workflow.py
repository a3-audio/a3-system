# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The package workflows: build-packages.yml builds and install-tests every line,
packages.yml calls it and publishes the apt archive.

Plain text checks: there is no YAML library here, and adding one is a dependency.

Run with:  python3 -m unittest discover -s tests
"""

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from installer.roles import base  # noqa: E402
from workflows import (BUILD_PACKAGES, PACKAGES, all_workflows, job_blocks,  # noqa: E402
                       run_commands, top_block)

COMMITTED_KEY = REPO / "installer" / "keys" / "a3-audio-archive.asc"
CALL_BUILD = "uses: ./.github/workflows/build-packages.yml"


class Packages(unittest.TestCase):
    def setUp(self):
        self.text = PACKAGES.read_text()
        self.jobs = job_blocks(self.text)

    def test_the_jobs_are_the_build_call_and_publish(self):
        self.assertEqual(list(self.jobs), ["packages", "publish"])

    def test_the_build_is_the_reusable_workflow_at_the_pushed_commit(self):
        self.assertIn(CALL_BUILD, self.jobs["packages"])
        # No `with: ref`: the called checkouts take the push's own commit, as before.
        self.assertNotIn("with:", self.jobs["packages"])
        self.assertNotIn("secrets:", self.jobs["packages"])

    def test_the_signing_key_is_named_and_only_publish_sees_it(self):
        self.assertEqual(self.text.count("secrets.GPG_PRIVATE_KEY"), 1)
        self.assertIn("secrets.GPG_PRIVATE_KEY", self.jobs["publish"])
        self.assertIn("ubuntu-24.04-arm", (REPO / "ci" / "lines.json").read_text())
        self.assertIn("debian:trixie", (REPO / "ci" / "lines.json").read_text())
        self.assertNotIn("pages-deploy", self.text)

    def test_triggers_are_main_tags_and_by_hand(self):
        on_block = top_block(self.text, "on")
        self.assertIn("branches: [main]", on_block)
        self.assertIn('tags: ["v*"]', on_block)
        self.assertIn("workflow_dispatch:", on_block)
        self.assertNotIn("pull_request", on_block)
        self.assertNotIn("release", on_block)

    def test_the_workflow_reads_and_only_publish_writes(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertEqual(self.text.count("contents: write"), 1)
        self.assertIn("contents: write", self.jobs["publish"])


class BuildPackages(unittest.TestCase):
    def setUp(self):
        self.text = BUILD_PACKAGES.read_text()
        self.jobs = job_blocks(self.text)

    def test_the_jobs_are_matrix_build_install_test(self):
        self.assertEqual(list(self.jobs), ["matrix", "build", "install-test"])

    def test_it_is_only_called_never_triggered(self):
        on_block = top_block(self.text, "on")
        self.assertIn("workflow_call:", on_block)
        for trigger in ("push:", "release:", "workflow_dispatch:", "pull_request"):
            self.assertNotIn(trigger, on_block)

    def test_ref_is_an_optional_string_input(self):
        on_block = top_block(self.text, "on")
        self.assertRegex(on_block, r"inputs:\n(?:\s+#.*\n)*\s+ref:\n")
        self.assertIn("type: string", on_block)
        self.assertIn("required: false", on_block)
        self.assertIn('default: ""', on_block)

    def test_every_checkout_takes_the_ref(self):
        checkouts = self.text.count("uses: actions/checkout@v4")
        self.assertEqual(checkouts, 3)
        self.assertEqual(self.text.count("ref: ${{ inputs.ref }}"), checkouts)

    def test_it_reads_and_publishes_nothing(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertNotIn("contents: write", self.text)
        self.assertNotIn("secrets.", self.text)
        self.assertNotIn("gh-pages", self.text)
        self.assertNotIn("gh release", self.text)

    def test_a_ref_without_package_lines_stops_with_a_message(self):
        self.assertLess(self.jobs["matrix"].index("test -f ci/lines.json"),
                        self.jobs["matrix"].index("python3 ci/matrix.py"))
        self.assertIn("::error::", self.jobs["matrix"])

    def test_the_matrix_comes_from_lines_json(self):
        self.assertIn("python3 ci/matrix.py", self.jobs["matrix"])
        for job in ("build", "install-test"):
            self.assertIn("fromJSON(needs.matrix.outputs.matrix)", self.jobs[job])
            self.assertIn("runs-on: ${{ matrix.runner }}", self.jobs[job])
            self.assertIn("container: ${{ matrix.image }}", self.jobs[job])


class EveryWorkflow(unittest.TestCase):
    def test_every_action_is_pinned_to_a_major_tag_or_is_local(self):
        for workflow in all_workflows():
            uses = re.findall(r"uses:\s*(\S+)", workflow.read_text())
            self.assertTrue(uses, workflow.name)
            for action in uses:
                if action.startswith("./.github/workflows/"):
                    self.assertTrue((REPO / action).is_file(), action)
                    continue
                self.assertRegex(action, r"^[\w.-]+/[\w.-]+@v\d+$")


class Shell(unittest.TestCase):
    def test_apt_never_waits_for_a_prompt(self):
        for workflow in (PACKAGES, BUILD_PACKAGES):
            top = workflow.read_text().split("\njobs:", 1)[0]
            self.assertRegex(top, r"(?m)^env:\n(?:\s+#.*\n)*  DEBIAN_FRONTEND: noninteractive$",
                             workflow.name)

    def test_a_failing_script_in_a_pipe_fails_the_step(self):
        # GitHub runs `shell: bash` as bash -eo pipefail; its default is bash -e.
        for workflow in all_workflows():
            top = workflow.read_text().split("\njobs:", 1)[0]
            self.assertRegex(top, r"(?m)^defaults:\n  run:\n(?:\s+#.*\n)*    shell: bash$",
                             workflow.name)

    def test_an_empty_package_list_installs_nothing(self):
        self.assertIn("| xargs -r apt-get install", BUILD_PACKAGES.read_text())


class Build(unittest.TestCase):
    def setUp(self):
        self.build = job_blocks(BUILD_PACKAGES.read_text())["build"]

    def test_the_checkout_has_history_submodules_and_their_tags(self):
        self.assertIn("fetch-depth: 0", self.build)
        self.assertIn("submodules: recursive", self.build)
        self.assertIn("git submodule foreach --recursive git fetch --tags", self.build)

    def test_git_comes_before_the_checkout(self):
        self.assertLess(self.build.index("git ca-certificates python3"),
                        self.build.index("actions/checkout@v4"))

    def test_build_depends_come_from_the_line(self):
        self.assertIn("python3 ci/build_line.py ${{ matrix.suite }} --build-depends", self.build)

    def test_juce_is_cached_per_suite_and_arch(self):
        self.assertIn("key: juce-9.0.3-${{ matrix.suite }}-${{ matrix.arch }}-v1", self.build)
        self.assertIn("--branch 9.0.3", self.build)

    def test_juce_is_the_installers_version(self):
        version = base.JUCE_VERSION
        self.assertIn(f"--branch {version} ", self.build)
        self.assertIn(f"key: juce-{version}-", self.build)
        self.assertEqual(set(re.findall(r"--branch (\S+)", self.build)), {version})
        self.assertEqual(set(re.findall(r"key: juce-([^-]+)-", self.build)), {version})

    def test_ccache_is_bounded(self):
        self.assertIn("CCACHE_MAXSIZE: 1500M", self.build)

    def test_the_line_is_built_and_uploaded_by_suite(self):
        self.assertIn("python3 ci/build_line.py ${{ matrix.suite }} --out", self.build)
        self.assertIn("name: debs-${{ matrix.suite }}", self.build)


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.job = job_blocks(BUILD_PACKAGES.read_text())["install-test"]

    def test_it_needs_build_and_installs_from_an_index(self):
        self.assertIn("needs: [matrix, build]", self.job)
        self.assertIn("name: debs-${{ matrix.suite }}", self.job)
        self.assertLess(self.job.index("python3 ci/archive.py index"),
                        self.job.index("python3 ci/install_test.py"))

    def test_it_needs_no_submodules(self):
        self.assertIn("submodules: false", self.job)


class Publish(unittest.TestCase):
    def setUp(self):
        self.job = job_blocks(PACKAGES.read_text())["publish"]

    def test_it_runs_after_the_install_test_on_main_and_tags_only(self):
        # The called workflow ends with the install test: needing it waits for both lines.
        self.assertIn("needs: packages", self.job)
        self.assertIn("if: github.ref == 'refs/heads/main' || "
                      "startsWith(github.ref, 'refs/tags/v')", self.job)

    def test_it_runs_in_debian_testing(self):
        self.assertIn("runs-on: ubuntu-latest", self.job)
        self.assertIn("container: debian:testing", self.job)

    def test_two_pushes_do_not_race(self):
        self.assertIn("concurrency:", self.job)
        self.assertIn("cancel-in-progress: false", self.job)

    def test_the_key_must_match_before_anything_is_signed(self):
        self.assertIn("python3 ci/archive.py key-matches installer/keys/a3-audio-archive.asc",
                      self.job)
        self.assertLess(self.job.index("ci/archive.py key-matches"),
                        self.job.index("ci/archive.py sign"))

    def test_the_public_key_and_nojekyll_are_published(self):
        self.assertIn("installer/keys/a3-audio-archive.asc", self.job)
        self.assertIn("KEY.gpg", self.job)
        self.assertIn(".nojekyll", self.job)

    def test_the_archive_keeps_no_history(self):
        self.assertIn("peaceiris/actions-gh-pages@v4", self.job)
        self.assertIn("force_orphan: true", self.job)
        self.assertIn("github_token: ${{ secrets.GITHUB_TOKEN }}", self.job)


class RunLines(unittest.TestCase):
    def test_every_python_call_is_a_ci_script(self):
        for workflow in all_workflows():
            commands = run_commands(workflow.read_text())
            # An apt-get line names python3 as a package, not as a call.
            python_calls = [command for command in commands if "python3" in command
                            and not command.startswith("apt-get")]
            for command in python_calls:
                self.assertRegex(command, r"python3 ci/\w+\.py", workflow.name)
                self.assertNotIn("python3 -c", command)

    def test_no_inline_hashing_or_index_making(self):
        for workflow in all_workflows():
            commands = "\n".join(run_commands(workflow.read_text()))
            for tool in ("sha256sum", "md5sum", "dpkg-scanpackages", "--detach-sign"):
                self.assertNotIn(tool, commands, workflow.name)


class CommittedKey(unittest.TestCase):
    def test_the_committed_key_is_a_public_key(self):
        self.assertTrue(COMMITTED_KEY.read_text().startswith(
            "-----BEGIN PGP PUBLIC KEY BLOCK-----"))


if __name__ == "__main__":
    unittest.main()
