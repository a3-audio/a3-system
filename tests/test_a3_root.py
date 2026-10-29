# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The root helper: a fixed verb list, nothing else."""

import base64
import importlib.machinery
import importlib.util
import os
import pwd
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import archive  # noqa: E402

HELPER = REPO / "installer" / "a3-root"


def load_helper():
    loader = importlib.machinery.SourceFileLoader("a3_root", str(HELPER))
    spec = importlib.util.spec_from_loader("a3_root", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def crc24(data):
    crc = 0xB704CE
    for byte in data:
        crc ^= byte << 16
        for _ in range(8):
            crc <<= 1
            if crc & 0x1000000:
                crc ^= 0x864CFB
    return crc & 0xFFFFFF


def armor(binary, crc=None):
    body = base64.b64encode(binary).decode()
    lines = [body[i:i + 64] for i in range(0, len(body), 64)]
    crc = crc24(binary) if crc is None else crc
    checksum = base64.b64encode(crc.to_bytes(3, "big")).decode()
    return "\n".join(["-----BEGIN PGP PUBLIC KEY BLOCK-----", "Version: test", "",
                      *lines, "=" + checksum, "-----END PGP PUBLIC KEY BLOCK-----", ""])


class Recorder:
    def __init__(self, codes=()):
        self.commands = []
        self.codes = list(codes)

    def __call__(self, args, **_kwargs):
        self.commands.append(list(args))
        return SimpleNamespace(returncode=self.codes.pop(0) if self.codes else 0)


class HelperTest(unittest.TestCase):
    def setUp(self):
        self.helper = load_helper()
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.run_ = Recorder()

    def main(self, *argv, env=None, **paths):
        return self.helper.main(list(argv), run=self.run_, env=env or {}, **paths)


class RefusalsComeBeforeAnyCommand(HelperTest):
    def test_an_unknown_package_is_refused_before_apt_runs(self):
        self.assertEqual(self.main("install", "curl"), 2)
        self.assertEqual(self.run_.commands, [])

    def test_one_unknown_among_good_ones_refuses_all(self):
        self.assertEqual(self.main("install", "a3-core", "curl"), 2)
        self.assertEqual(self.run_.commands, [])

    def test_an_option_as_a_package_is_refused(self):
        self.assertEqual(self.main("install", "--allow-unauthenticated"), 2)
        self.assertEqual(self.main("remove", "-y"), 2)
        self.assertEqual(self.main("source", "-o"), 2)
        self.assertEqual(self.run_.commands, [])

    def test_an_unknown_verb_is_refused(self):
        self.assertEqual(self.main("shell"), 2)
        self.assertEqual(self.main(), 2)
        self.assertEqual(self.run_.commands, [])

    def test_no_packages_is_refused(self):
        self.assertEqual(self.main("install"), 2)
        self.assertEqual(self.run_.commands, [])


class InstallAndRemove(HelperTest):
    def test_install_holds_what_it_installed(self):
        self.assertEqual(self.main("install", "a3-core", "stemdeck"), 0)
        self.assertEqual(self.run_.commands, [
            ["apt-get", "update"],
            ["apt-get", "install", "-y", "--allow-change-held-packages", "a3-core", "stemdeck"],
            ["apt-mark", "hold", "a3-core", "stemdeck"],
        ])

    def test_a_failing_install_stops_and_passes_its_code(self):
        self.run_ = Recorder(codes=[0, 100])
        self.assertEqual(self.main("install", "a3-core"), 100)
        self.assertEqual(len(self.run_.commands), 2)

    def test_remove_unholds_first(self):
        self.assertEqual(self.main("remove", "a3-core"), 0)
        self.assertEqual(self.run_.commands, [
            ["apt-mark", "unhold", "a3-core"],
            ["apt-get", "remove", "-y", "a3-core"],
        ])

    def test_the_environment_is_not_made_noninteractive(self):
        seen = []

        def run(args, **kwargs):
            seen.append(kwargs.get("env"))
            return SimpleNamespace(returncode=0)

        self.helper.main(["install", "a3-core"], run=run, env={"DEBIAN_FRONTEND": "dialog"})
        for env in seen:
            self.assertNotEqual((env or {}).get("DEBIAN_FRONTEND"), "noninteractive")


class JoinAudio(HelperTest):
    def test_join_audio_takes_the_caller_not_root(self):
        name = pwd.getpwuid(os.getuid()).pw_name
        self.assertEqual(self.main("join-audio", env={"PKEXEC_UID": str(os.getuid())}), 0)
        self.assertEqual(self.run_.commands, [["usermod", "-aG", "audio", name]])

    def test_sudo_uid_is_the_fallback(self):
        name = pwd.getpwuid(os.getuid()).pw_name
        self.assertEqual(self.main("join-audio", env={"SUDO_UID": str(os.getuid())}), 0)
        self.assertEqual(self.run_.commands, [["usermod", "-aG", "audio", name]])

    def test_no_calling_user_is_refused(self):
        self.assertEqual(self.main("join-audio", env={}), 2)
        self.assertEqual(self.run_.commands, [])

    def test_root_is_not_a_calling_user(self):
        self.assertEqual(self.main("join-audio", env={"PKEXEC_UID": "0"}), 2)
        self.assertEqual(self.run_.commands, [])


class Source(HelperTest):
    def paths(self, key_text):
        key_file = self.tmp / "key.asc"
        key_file.write_text(key_text)
        return dict(key_file=key_file, keyring=self.tmp / "ring" / "a3.gpg",
                    sources=self.tmp / "src" / "a3.sources")

    def test_it_dearmors_the_key_and_writes_the_sources(self):
        binary = bytes(range(256)) * 3
        paths = self.paths(armor(binary))
        self.assertEqual(self.main("source", "trixie", **paths), 0)
        self.assertEqual(paths["keyring"].read_bytes(), binary)
        self.assertEqual(stat.S_IMODE(paths["keyring"].stat().st_mode), 0o644)
        self.assertEqual(paths["sources"].read_text(), archive.sources_text("trixie"))
        self.assertEqual(self.run_.commands, [["apt-get", "update"]])

    def test_a_bad_checksum_writes_nothing(self):
        paths = self.paths(armor(b"some key bytes", crc=1))
        self.assertEqual(self.main("source", "trixie", **paths), 2)
        self.assertFalse(paths["keyring"].exists())
        self.assertFalse(paths["sources"].exists())
        self.assertEqual(self.run_.commands, [])

    def test_an_unknown_suite_writes_nothing(self):
        paths = self.paths(armor(b"k"))
        self.assertEqual(self.main("source", "sid", **paths), 2)
        self.assertFalse(paths["keyring"].exists())
        self.assertFalse(paths["sources"].exists())

    def test_no_temporary_file_stays_behind(self):
        paths = self.paths(armor(b"k" * 10))
        self.main("source", "forky", **paths)
        self.assertEqual([p.name for p in paths["keyring"].parent.iterdir()], ["a3.gpg"])

    def test_the_committed_key_dearmors(self):
        committed = REPO / "installer" / "keys" / "a3-audio-archive.asc"
        if not committed.exists():
            self.skipTest("key not committed yet")
        paths = self.paths(committed.read_text())
        self.assertEqual(self.main("source", "trixie", **paths), 0)
        self.assertGreater(paths["keyring"].stat().st_size, 0)


class OneSourceOfTruth(HelperTest):
    def test_the_sources_text_agrees_for_each_suite(self):
        for suite in ("forky", "trixie"):
            self.assertEqual(self.helper.sources_text(suite), archive.sources_text(suite))

    def test_constants_agree(self):
        self.assertEqual(self.helper.A3_PACKAGES, archive.A3_PACKAGES)
        self.assertEqual(self.helper.ARCHIVE_URL, archive.ARCHIVE_URL)
        self.assertEqual(Path(self.helper.KEYRING), archive.KEYRING)
        self.assertEqual(Path(self.helper.SOURCES), archive.SOURCES)
        self.assertEqual(self.helper.SUITES, archive.SUITES)

    def test_it_looks_for_the_key_beside_itself(self):
        self.assertEqual(self.helper.KEY_FILE, HELPER.parent / "keys" / "a3-audio-archive.asc")

    def test_it_is_executable_with_the_isolated_shebang(self):
        self.assertTrue(os.access(HELPER, os.X_OK))
        self.assertEqual(HELPER.read_text().splitlines()[0], "#!/usr/bin/python3 -I")

    def test_it_imports_nothing_from_the_installer(self):
        text = HELPER.read_text()
        self.assertNotIn("import installer", text)
        self.assertNotIn("from installer", text)


if __name__ == "__main__":
    unittest.main()
