# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
""".github/workflows/release-debs.yml: a release's .debs attached to a3-system's release.

Plain text checks: there is no YAML library here, and adding one is a dependency.

Run with:  python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workflows import RELEASE_DEBS, job_blocks, run_commands, top_block  # noqa: E402

TAG = "${{ github.event.release.tag_name || inputs.tag }}"


class Triggers(unittest.TestCase):
    def setUp(self):
        self.on = top_block(RELEASE_DEBS.read_text(), "on")

    def test_a_published_release_triggers_it(self):
        self.assertRegex(self.on, r"release:\n\s+types: \[published\]")

    def test_by_hand_it_takes_a_required_tag(self):
        self.assertRegex(self.on, r"workflow_dispatch:\n\s+inputs:\n\s+tag:\n")
        self.assertIn("required: true", self.on)
        self.assertIn("type: string", self.on)

    def test_no_push_triggers_it(self):
        self.assertNotIn("push:", self.on)
        self.assertNotIn("pull_request", self.on)


class Jobs(unittest.TestCase):
    def setUp(self):
        self.text = RELEASE_DEBS.read_text()
        self.jobs = job_blocks(self.text)

    def test_the_jobs_are_the_build_call_and_the_upload(self):
        self.assertEqual(list(self.jobs), ["packages", "upload"])

    def test_it_builds_the_tags_pins_with_the_shared_workflow(self):
        self.assertIn("uses: ./.github/workflows/build-packages.yml", self.jobs["packages"])
        self.assertIn(f"ref: refs/tags/{TAG}", self.jobs["packages"])

    def test_the_archive_is_not_published_from_here(self):
        self.assertNotIn("workflows/packages.yml", self.text)
        for publishing in ("gh-pages", "GPG_PRIVATE_KEY", "archive.py sign", "secrets: inherit"):
            self.assertNotIn(publishing, self.text)

    def test_the_workflow_reads_and_only_the_upload_writes(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertEqual(self.text.count("contents: write"), 1)
        self.assertIn("contents: write", self.jobs["upload"])

    def test_one_tag_is_handled_at_a_time(self):
        self.assertIn(f"group: release-debs-{TAG}", self.text)


class Upload(unittest.TestCase):
    def setUp(self):
        self.job = job_blocks(RELEASE_DEBS.read_text())["upload"]
        self.commands = run_commands(self.job)

    def test_it_waits_for_the_install_test(self):
        self.assertIn("needs: packages", self.job)

    def test_it_runs_on_the_runner_where_gh_is(self):
        self.assertIn("runs-on: ubuntu-latest", self.job)
        self.assertNotRegex(self.job, r"(?m)^\s+container:")

    def test_every_line_is_downloaded_and_named_as_assets(self):
        self.assertIn("uses: actions/download-artifact@v4", self.job)
        self.assertIn("pattern: debs-*", self.job)
        self.assertIn("python3 ci/release_assets.py debs assets", self.commands)

    def test_the_assets_go_to_the_release_of_the_tag(self):
        upload = [c for c in self.commands if c.startswith("gh release upload")]
        self.assertEqual(upload, [
            'gh release upload "$TAG" assets/* --clobber --repo a3-audio/a3-system'])
        self.assertIn(f"TAG: {TAG}", self.job)
        self.assertIn("GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}", self.job)

    def test_the_tag_never_lands_in_a_script_unquoted(self):
        # A dispatch input in ${{ }} inside run: would be pasted into the shell.
        for command in self.commands:
            self.assertNotIn("${{", command)


if __name__ == "__main__":
    unittest.main()
