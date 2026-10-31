"""ci/archive.py and ci/lines.json: one apt archive index for both package lines.

Run with:  python3 -m unittest discover -s tests
"""

import contextlib
import gzip
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from ci import archive  # noqa: E402

DATE = "Wed, 28 Oct 2026 00:00:00 +0000"


def tmpdir(case):
    tmp = tempfile.TemporaryDirectory()
    case.addCleanup(tmp.cleanup)
    return Path(tmp.name)


def make_deb(folder, package, arch, version="1.0"):
    tree = folder / f"{package}_{arch}-tree"
    (tree / "DEBIAN").mkdir(parents=True)
    (tree / "DEBIAN" / "control").write_text(
        f"Package: {package}\nVersion: {version}\nArchitecture: {arch}\n"
        "Maintainer: A3 <contact@a3-audio.com>\nDescription: test package\n")
    deb = folder / f"{package}_{version}_{arch}.deb"
    subprocess.run(["dpkg-deb", "--build", str(tree), str(deb)],
                   check=True, capture_output=True)
    return deb


def throwaway_gpg_home(case, uid="a3 test <test@example.invalid>"):
    home = tmpdir(case) / "gnupg"
    home.mkdir(mode=0o700)
    subprocess.run(["gpg", "--homedir", str(home), "--batch", "--quick-gen-key",
                    "--passphrase", "", uid, "ed25519", "sign", "never"],
                   check=True, capture_output=True)
    return home


def export_public(home, target):
    out = subprocess.run(["gpg", "--homedir", str(home), "--armor", "--export"],
                         check=True, capture_output=True).stdout
    target.write_bytes(out)
    return target


class ReleaseText(unittest.TestCase):
    def test_hashes_name_paths_relative_to_the_suite(self):
        text = archive.release_text("forky", ["amd64"],
            {"main/binary-amd64/Packages": b"x"}, DATE)
        self.assertIn("Codename: forky\n", text)
        self.assertIn("Architectures: amd64\n", text)
        self.assertIn(" 2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881 1 main/binary-amd64/Packages\n", text)
        self.assertNotIn("MD5Sum", text)
        self.assertFalse(any(l.startswith(" ") and "Release" in l for l in text.splitlines()))

    def test_origin_label_suite_and_components(self):
        text = archive.release_text("trixie", ["arm64"], {}, DATE)
        for line in ("Origin: a3-audio", "Label: a3-system", "Suite: trixie",
                     "Components: main", f"Date: {DATE}"):
            self.assertIn(line + "\n", text)


class IndexSuite(unittest.TestCase):
    def test_two_lines_share_one_root_and_keep_their_own_dists(self):
        work = tmpdir(self)
        root = work / "archive"
        forky = make_deb(work, "a3-core", "amd64")
        trixie = make_deb(work, "stemdeck", "arm64")
        release_f = archive.index_suite(root, "forky", "amd64", [forky])
        release_t = archive.index_suite(root, "trixie", "arm64", [trixie])
        self.assertEqual(release_f, root / "dists/forky/Release")
        self.assertEqual(release_t, root / "dists/trixie/Release")
        packages_f = (root / "dists/forky/main/binary-amd64/Packages").read_text()
        packages_t = (root / "dists/trixie/main/binary-arm64/Packages").read_text()
        self.assertIn("Package: a3-core\n", packages_f)
        self.assertNotIn("stemdeck", packages_f)
        self.assertIn("Package: stemdeck\n", packages_t)
        self.assertNotIn("a3-core", packages_t)
        self.assertIn("Filename: pool/main/a/a3-core/a3-core_1.0_amd64.deb\n", packages_f)
        self.assertTrue((root / "pool/main/s/stemdeck/stemdeck_1.0_arm64.deb").is_file())

    def test_packages_gz_matches_packages_and_release_hashes_both(self):
        work = tmpdir(self)
        root = work / "archive"
        release = archive.index_suite(root, "forky", "amd64", [make_deb(work, "a3-core", "amd64")])
        folder = root / "dists/forky/main/binary-amd64"
        self.assertEqual(gzip.decompress((folder / "Packages.gz").read_bytes()),
                         (folder / "Packages").read_bytes())
        text = release.read_text()
        self.assertIn(" main/binary-amd64/Packages\n", text)
        self.assertIn(" main/binary-amd64/Packages.gz\n", text)

    def test_a_deb_of_the_wrong_architecture_is_refused(self):
        work = tmpdir(self)
        deb = make_deb(work, "stemdeck", "arm64")
        with self.assertRaises(archive.ArchiveError):
            archive.index_suite(work / "archive", "forky", "amd64", [deb])

    def test_arch_all_is_accepted(self):
        work = tmpdir(self)
        root = work / "archive"
        archive.index_suite(root, "forky", "amd64", [make_deb(work, "a3-mixer", "all")])
        self.assertIn("Package: a3-mixer\n",
                      (root / "dists/forky/main/binary-amd64/Packages").read_text())


class LinesJson(unittest.TestCase):
    def setUp(self):
        self.lines = json.loads((REPO / "ci/lines.json").read_text())

    def paths(self, suite):
        return [b["path"] for b in self.lines[suite]["builds"]]

    def test_forky_and_trixie_definitions(self):
        self.assertEqual(self.lines["forky"]["arch"], "amd64")
        self.assertEqual(self.lines["forky"]["runner"], "ubuntu-latest")
        self.assertEqual(self.lines["forky"]["image"], "debian:testing")
        self.assertEqual(self.lines["trixie"]["arch"], "arm64")
        self.assertEqual(self.lines["trixie"]["runner"], "ubuntu-24.04-arm")
        self.assertEqual(self.lines["trixie"]["image"], "debian:trixie")

    def test_builds(self):
        self.assertEqual(self.paths("forky"),
            ["a3-core", "a3-stemdeck", "a3-mixer/ui", "a3-motion/ui", "a3-core/beat-analyzer", "."])
        self.assertEqual(self.paths("trixie"),
            ["a3-core", "a3-stemdeck", "a3-mixer/ui", "a3-motion/ui", "a3-core/beat-analyzer", "."])
        for line in self.lines.values():
            for build in line["builds"]:
                if build["path"] == ".":
                    self.assertEqual(build["recipes"], ["update/packaging"])
                elif build["path"] != "a3-core":
                    self.assertEqual(build["recipes"], ["packaging"])


class Signing(unittest.TestCase):
    def signed_release(self):
        work = tmpdir(self)
        home = throwaway_gpg_home(self)
        release = work / "Release"
        release.write_text("Codename: forky\n")
        archive.sign(release, home)
        return release, home

    def test_sign_writes_detached_and_clearsigned_files_that_verify(self):
        release, home = self.signed_release()
        self.assertTrue((release.parent / "Release.gpg").is_file())
        self.assertTrue((release.parent / "InRelease").is_file())
        for args in (["--verify", str(release.parent / "Release.gpg"), str(release)],
                     ["--verify", str(release.parent / "InRelease")]):
            done = subprocess.run(["gpg", "--homedir", str(home), *args], capture_output=True)
            self.assertEqual(done.returncode, 0, done.stderr)

    def test_sign_detached_writes_an_armored_signature_beside_the_file(self):
        work = tmpdir(self)
        home = throwaway_gpg_home(self)
        sums = work / "SHA256SUMS"
        sums.write_text("0" * 64 + "  a3-core_1.0_amd64.deb\n")
        archive.sign_detached(sums, home)
        signature = work / "SHA256SUMS.asc"
        self.assertTrue(signature.read_text().startswith("-----BEGIN PGP SIGNATURE-----"))
        self.assertEqual(sorted(p.name for p in work.iterdir()), ["SHA256SUMS", "SHA256SUMS.asc"])
        keyring = tmpdir(self) / "a3.gpg"
        keyring.write_bytes(subprocess.run(["gpg", "--homedir", str(home), "--export"],
                                           check=True, capture_output=True).stdout)
        done = subprocess.run(["gpgv", "--keyring", str(keyring), str(signature), str(sums)],
                              capture_output=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_key_matches_the_committed_public_key(self):
        home = throwaway_gpg_home(self)
        committed = export_public(home, tmpdir(self) / "a3.asc")
        self.assertTrue(archive.key_matches(home, committed))

    def test_key_does_not_match_another_key(self):
        home = throwaway_gpg_home(self)
        other = export_public(throwaway_gpg_home(self, "other <o@example.invalid>"),
                              tmpdir(self) / "other.asc")
        self.assertFalse(archive.key_matches(home, other))


class CommandLine(unittest.TestCase):
    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = archive.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_index_prints_the_release_path_as_its_last_line(self):
        work = tmpdir(self)
        deb = make_deb(work, "a3-core", "amd64")
        code, out, _ = self.run_main(["index", str(work / "archive"), "forky", "amd64", str(deb)])
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines()[-1], str(work / "archive/dists/forky/Release"))

    def test_sign_dispatch(self):
        work = tmpdir(self)
        home = throwaway_gpg_home(self)
        release = work / "Release"
        release.write_text("x\n")
        code, _, _ = self.run_main(["sign", str(release), "--gpg-home", str(home)])
        self.assertEqual(code, 0)
        self.assertTrue((work / "InRelease").is_file())

    def test_sign_detached_dispatch(self):
        work = tmpdir(self)
        home = throwaway_gpg_home(self)
        sums = work / "SHA256SUMS"
        sums.write_text("x\n")
        code, _, _ = self.run_main(["sign-detached", str(sums), "--gpg-home", str(home)])
        self.assertEqual(code, 0)
        self.assertTrue((work / "SHA256SUMS.asc").is_file())

    def test_key_matches_exit_codes_and_message_names_both_fingerprints(self):
        home = throwaway_gpg_home(self)
        committed = export_public(home, tmpdir(self) / "a3.asc")
        code, _, _ = self.run_main(["key-matches", str(committed), "--gpg-home", str(home)])
        self.assertEqual(code, 0)
        other_home = throwaway_gpg_home(self, "other <o@example.invalid>")
        other = export_public(other_home, tmpdir(self) / "other.asc")
        code, _, err = self.run_main(["key-matches", str(other), "--gpg-home", str(home)])
        self.assertEqual(code, 1)
        self.assertIn(archive.fingerprints(home, secret=True)[0], err)
        self.assertIn(archive.fingerprints_of_file(other)[0], err)


if __name__ == "__main__":
    unittest.main()
