# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""ci/release_assets.py: the built .debs as GitHub release assets, with SHA256SUMS.

Run with:  python3 -m unittest discover -s tests
"""

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from ci import release_assets  # noqa: E402


def tmpdir(case):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    return Path(tmp.name)


def downloaded(case, layout):
    """download-artifact's layout: one debs-<suite>/ folder per line."""
    root = tmpdir(case) / "debs"
    for suite, names in layout.items():
        folder = root / f"debs-{suite}"
        folder.mkdir(parents=True)
        for name in names:
            (folder / name).write_bytes(f"{suite}/{name}".encode())
    return root


class Names(unittest.TestCase):
    def test_a_name_only_one_line_builds_is_kept(self):
        names = release_assets.asset_names([
            ("forky", Path("a/a3-core_03.1_amd64.deb")),
            ("trixie", Path("b/a3-core_03.1_arm64.deb"))])
        self.assertEqual(sorted(names.values()),
                         ["a3-core_03.1_amd64.deb", "a3-core_03.1_arm64.deb"])

    def test_a_name_two_lines_build_carries_the_suite_before_the_arch(self):
        names = release_assets.asset_names([
            ("forky", Path("a/a3-mixer_03.1+2_all.deb")),
            ("trixie", Path("b/a3-mixer_03.1+2_all.deb"))])
        self.assertEqual(names, {
            Path("a/a3-mixer_03.1+2_all.deb"): "a3-mixer_03.1+2_forky_all.deb",
            Path("b/a3-mixer_03.1+2_all.deb"): "a3-mixer_03.1+2_trixie_all.deb"})

    def test_a_file_that_is_no_debian_package_name_is_refused(self):
        with self.assertRaises(release_assets.AssetError):
            release_assets.with_suite("a3-mixer.deb", "forky")


class Collect(unittest.TestCase):
    def collect(self, layout):
        out = tmpdir(self) / "assets"
        with contextlib.redirect_stdout(io.StringIO()):
            code = release_assets.main([str(downloaded(self, layout)), str(out)])
        self.assertEqual(code, 0)
        return out

    def test_every_deb_is_copied_under_its_asset_name(self):
        out = self.collect({"forky": ["a3-core_1_amd64.deb", "a3-mixer_1_all.deb"],
                            "trixie": ["a3-core_1_arm64.deb", "a3-mixer_1_all.deb"]})
        self.assertEqual(sorted(p.name for p in out.glob("*.deb")), [
            "a3-core_1_amd64.deb", "a3-core_1_arm64.deb",
            "a3-mixer_1_forky_all.deb", "a3-mixer_1_trixie_all.deb"])
        self.assertEqual((out / "a3-mixer_1_trixie_all.deb").read_bytes(),
                         b"trixie/a3-mixer_1_all.deb")

    def test_sha256sums_lists_every_asset_in_sha256sum_check_format(self):
        out = self.collect({"forky": ["a3-core_1_amd64.deb"],
                            "trixie": ["a3-core_1_arm64.deb"]})
        lines = (out / "SHA256SUMS").read_text().splitlines()
        expected = [f"{hashlib.sha256((out / name).read_bytes()).hexdigest()}  {name}"
                    for name in ("a3-core_1_amd64.deb", "a3-core_1_arm64.deb")]
        self.assertEqual(lines, expected)

    def test_no_debs_is_an_error(self):
        root = downloaded(self, {"forky": []})
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = release_assets.main([str(root), str(tmpdir(self) / "assets")])
        self.assertEqual(code, 1)
        self.assertIn("no .deb", err.getvalue())

    def test_a_folder_that_is_no_line_is_refused(self):
        root = tmpdir(self) / "debs"
        (root / "something-else").mkdir(parents=True)
        (root / "something-else" / "x_1_all.deb").write_bytes(b"x")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            code = release_assets.main([str(root), str(tmpdir(self) / "assets")])
        self.assertEqual(code, 1)
        self.assertIn("something-else", err.getvalue())


if __name__ == "__main__":
    unittest.main()
