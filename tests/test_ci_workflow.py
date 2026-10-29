# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
""".github/workflows/packages.yml: build, install-test and publish every package.

Plain text checks: there is no YAML library here, and adding one is a dependency.

Run with:  python3 -m unittest discover -s tests
"""

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer.roles import base  # noqa: E402

WORKFLOW = REPO / ".github" / "workflows" / "packages.yml"
COMMITTED_KEY = REPO / "installer" / "keys" / "a3-audio-archive.asc"
JOB_INDENT = "  "


def workflow_text():
    return WORKFLOW.read_text()


def job_blocks(text):
    """Each job's lines, keyed by name: a job starts at two-space indent under `jobs:`."""
    blocks, current, in_jobs = {}, None, False
    for line in text.splitlines():
        if line.startswith("jobs:"):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            break
        heading = re.match(rf"^{JOB_INDENT}([A-Za-z0-9_-]+):\s*$", line)
        if heading:
            current = heading.group(1)
            blocks[current] = []
        elif current:
            blocks[current].append(line)
    return {name: "\n".join(lines) for name, lines in blocks.items()}


def run_commands(text):
    """Every command line of every `run:`, inline or in a `run: |` block."""
    commands, block_indent = [], None
    for line in text.splitlines():
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if block_indent is not None:
            if stripped and indent < block_indent:
                block_indent = None
            elif stripped:
                commands.append(stripped)
                continue
        found = re.match(r"^\s*(?:- )?run:\s*(.*)$", line)
        if not found:
            continue
        if found.group(1) in ("|", ">"):
            block_indent = indent + 2
        else:
            commands.append(found.group(1))
    return commands


class Jobs(unittest.TestCase):
    def setUp(self):
        self.text = workflow_text()
        self.jobs = job_blocks(self.text)

    def test_the_jobs_are_matrix_build_install_test_publish(self):
        self.assertEqual(list(self.jobs), ["matrix", "build", "install-test", "publish"])

    def test_the_signing_key_is_named_and_only_publish_sees_it(self):
        self.assertEqual(self.text.count("secrets.GPG_PRIVATE_KEY"), 1)
        self.assertIn("secrets.GPG_PRIVATE_KEY", self.jobs["publish"])
        self.assertIn("ubuntu-24.04-arm", (REPO / "ci" / "lines.json").read_text())
        self.assertIn("debian:trixie", (REPO / "ci" / "lines.json").read_text())
        self.assertNotIn("pages-deploy", self.text)

    def test_the_matrix_comes_from_lines_json(self):
        self.assertIn("python3 ci/matrix.py", self.jobs["matrix"])
        for job in ("build", "install-test"):
            self.assertIn("fromJSON(needs.matrix.outputs.matrix)", self.jobs[job])
            self.assertIn("runs-on: ${{ matrix.runner }}", self.jobs[job])
            self.assertIn("container: ${{ matrix.image }}", self.jobs[job])

    def test_every_action_is_pinned_to_a_major_tag(self):
        uses = re.findall(r"uses:\s*(\S+)", self.text)
        self.assertTrue(uses)
        for action in uses:
            self.assertRegex(action, r"^[\w.-]+/[\w.-]+@v\d+$")

    def test_triggers_are_main_tags_and_by_hand(self):
        on_block = self.text.split("\non:", 1)[1].split("\npermissions:", 1)[0]
        self.assertIn("branches: [main]", on_block)
        self.assertIn('tags: ["v*"]', on_block)
        self.assertIn("workflow_dispatch:", on_block)
        self.assertNotIn("pull_request", on_block)

    def test_the_workflow_reads_and_only_publish_writes(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertEqual(self.text.count("contents: write"), 1)
        self.assertIn("contents: write", self.jobs["publish"])


class Shell(unittest.TestCase):
    def setUp(self):
        self.text = workflow_text()
        self.top = self.text.split("\njobs:", 1)[0]

    def test_apt_never_waits_for_a_prompt(self):
        self.assertRegex(self.top, r"(?m)^env:\n(?:\s+#.*\n)*  DEBIAN_FRONTEND: noninteractive$")

    def test_a_failing_script_in_a_pipe_fails_the_step(self):
        # GitHub runs `shell: bash` as bash -eo pipefail; its default is bash -e.
        self.assertRegex(self.top, r"(?m)^defaults:\n  run:\n(?:\s+#.*\n)*    shell: bash$")

    def test_an_empty_package_list_installs_nothing(self):
        self.assertIn("| xargs -r apt-get install", self.text)


class Build(unittest.TestCase):
    def setUp(self):
        self.build = job_blocks(workflow_text())["build"]

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
        self.job = job_blocks(workflow_text())["install-test"]

    def test_it_needs_build_and_installs_from_an_index(self):
        self.assertIn("needs: [matrix, build]", self.job)
        self.assertIn("name: debs-${{ matrix.suite }}", self.job)
        self.assertLess(self.job.index("python3 ci/archive.py index"),
                        self.job.index("python3 ci/install_test.py"))

    def test_it_needs_no_submodules(self):
        self.assertIn("submodules: false", self.job)


class Publish(unittest.TestCase):
    def setUp(self):
        self.job = job_blocks(workflow_text())["publish"]

    def test_it_runs_after_the_install_test_on_main_and_tags_only(self):
        self.assertIn("needs: install-test", self.job)
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
        commands = run_commands(workflow_text())
        # An apt-get line names python3 as a package, not as a call.
        python_calls = [command for command in commands if "python3" in command
                        and not command.startswith("apt-get")]
        self.assertTrue(python_calls)
        for command in python_calls:
            self.assertRegex(command, r"python3 ci/\w+\.py")
            self.assertNotIn("python3 -c", command)

    def test_no_inline_hashing_or_index_making(self):
        commands = "\n".join(run_commands(workflow_text()))
        for tool in ("sha256sum", "md5sum", "dpkg-scanpackages", "--detach-sign"):
            self.assertNotIn(tool, commands)


class CommittedKey(unittest.TestCase):
    def test_the_committed_key_is_a_public_key(self):
        self.assertTrue(COMMITTED_KEY.read_text().startswith(
            "-----BEGIN PGP PUBLIC KEY BLOCK-----"))


if __name__ == "__main__":
    unittest.main()
