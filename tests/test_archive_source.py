# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The public archive's source text and the command that runs the root helper."""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import archive  # noqa: E402


class TheSuiteComesFromTheCodename(unittest.TestCase):
    def test_suite_comes_from_the_codename(self):
        self.assertEqual(archive.suite_for({"VERSION_CODENAME": "forky"}), "forky")
        self.assertEqual(archive.suite_for({"VERSION_CODENAME": "trixie"}), "trixie")

    def test_testing_without_codename_is_refused_plainly(self):
        with self.assertRaises(archive.ArchiveError) as caught:
            archive.suite_for({"PRETTY_NAME": "Debian GNU/Linux forky/sid"})
        self.assertIn("forky", str(caught.exception))
        self.assertIn("trixie", str(caught.exception))

    def test_another_release_is_refused(self):
        with self.assertRaises(archive.ArchiveError):
            archive.suite_for({"VERSION_CODENAME": "bookworm"})


class TheSourcesText(unittest.TestCase):
    def test_it_is_deb822_with_the_keyring(self):
        text = archive.sources_text("trixie")
        self.assertEqual(text.splitlines(), [
            "Types: deb",
            "URIs: https://a3-audio.github.io/a3-system",
            "Suites: trixie",
            "Components: main",
            "Signed-By: /usr/share/keyrings/a3-audio.gpg",
        ])

    def test_an_unknown_suite_is_refused(self):
        with self.assertRaises(archive.ArchiveError):
            archive.sources_text("sid")


class TheRootCommand(unittest.TestCase):
    def test_it_is_the_helper_beside_the_installer_without_sudo(self):
        helper = REPO / "installer" / "a3-root"
        self.assertEqual(archive.a3_root_command(None, "install", "a3-core"),
                         [str(helper), "install", "a3-core"])


if __name__ == "__main__":
    unittest.main()
