# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""The root helper: a fixed verb list, nothing else."""

import base64
import contextlib
import hashlib
import io
import importlib.machinery
import importlib.util
import os
import pwd
import shutil
import stat
import subprocess
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

    def test_apt_runs_noninteractive_with_the_rest_of_the_environment(self):
        """Parity with the build path: the installer preseeds every a3-core
        question first, and sudo's env_reset would drop the caller's anyway."""
        for verb in ("install", "remove"):
            with self.subTest(verb):
                seen = []

                def run(args, **kwargs):
                    seen.append(kwargs.get("env"))
                    return SimpleNamespace(returncode=0)

                self.helper.main([verb, "a3-core"], run=run,
                                 env={"DEBIAN_FRONTEND": "dialog", "PATH": "/usr/bin"})
                self.assertTrue(seen)
                for env in seen:
                    self.assertEqual("noninteractive", env["DEBIAN_FRONTEND"])
                    self.assertEqual("/usr/bin", env["PATH"])


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

    def test_a_missing_checksum_writes_nothing(self):
        text = armor(b"some key bytes")
        paths = self.paths("\n".join(l for l in text.split("\n") if not l.startswith("=")))
        out = io.StringIO()
        with contextlib.redirect_stderr(out):
            self.assertEqual(self.main("source", "trixie", **paths), 2)
        self.assertIn("no armor checksum", out.getvalue())
        self.assertFalse(paths["keyring"].exists())

    def test_a_malformed_checksum_writes_nothing(self):
        text = armor(b"some key bytes")
        paths = self.paths("\n".join("=AAAAAAAA" if l.startswith("=") else l
                                      for l in text.split("\n")))
        out = io.StringIO()
        with contextlib.redirect_stderr(out):
            self.assertEqual(self.main("source", "trixie", **paths), 2)
        self.assertIn("malformed armor checksum", out.getvalue())
        self.assertFalse(paths["keyring"].exists())

    def test_an_unknown_suite_writes_nothing(self):
        paths = self.paths(armor(b"k"))
        self.assertEqual(self.main("source", "sid", **paths), 2)
        self.assertFalse(paths["keyring"].exists())
        self.assertFalse(paths["sources"].exists())

    def test_no_temporary_file_stays_behind(self):
        paths = self.paths(armor(b"k" * 10))
        self.main("source", "forky", **paths)
        self.assertEqual([p.name for p in paths["keyring"].parent.iterdir()], ["a3.gpg"])

    def test_a_failing_update_puts_back_what_was_there(self):
        paths = self.paths(armor(b"new key"))
        paths["keyring"].parent.mkdir()
        paths["keyring"].write_bytes(b"old key")
        self.run_ = Recorder(codes=[100])
        self.assertEqual(self.main("source", "forky", **paths), 100)
        self.assertEqual(b"old key", paths["keyring"].read_bytes())
        self.assertFalse(paths["sources"].exists())

    def test_a_failing_update_restores_an_older_source(self):
        paths = self.paths(armor(b"new key"))
        paths["sources"].parent.mkdir()
        paths["sources"].write_text(archive.sources_text("trixie"))
        self.run_ = Recorder(codes=[100])
        self.assertEqual(self.main("source", "forky", **paths), 100)
        self.assertEqual(archive.sources_text("trixie"), paths["sources"].read_text())
        self.assertFalse(paths["keyring"].exists())

    def failing_sources_write(self, paths):
        written = self.helper.write_atomically

        def write(path, data, mode):
            if path == paths["sources"]:
                raise OSError("disk full")
            written(path, data, mode)
        self.helper.write_atomically = write

    def test_a_failing_sources_write_puts_the_key_back(self):
        paths = self.paths(armor(b"new key"))
        paths["keyring"].parent.mkdir()
        paths["keyring"].write_bytes(b"old key")
        self.failing_sources_write(paths)
        self.assertEqual(self.main("source", "forky", **paths), 1)
        self.assertEqual(b"old key", paths["keyring"].read_bytes())
        self.assertEqual(self.run_.commands, [])

    def test_a_failing_sources_write_removes_a_new_key(self):
        paths = self.paths(armor(b"new key"))
        self.failing_sources_write(paths)
        self.assertEqual(self.main("source", "forky", **paths), 1)
        self.assertFalse(paths["keyring"].exists())
        self.assertFalse(paths["sources"].exists())

    def test_the_committed_key_dearmors(self):
        committed = REPO / "installer" / "keys" / "a3-audio-archive.asc"
        if not committed.exists():
            self.skipTest("key not committed yet")
        paths = self.paths(committed.read_text())
        self.assertEqual(self.main("source", "trixie", **paths), 0)
        self.assertGreater(paths["keyring"].stat().st_size, 0)


def gpg(home, *args):
    return subprocess.run(["gpg", "--homedir", str(home), "--batch", *args],
                          check=True, capture_output=True).stdout


def make_deb(folder, package, arch, version="1.0", name=None):
    tree = Path(tempfile.mkdtemp(dir=folder.parent)) / "tree"
    (tree / "DEBIAN").mkdir(parents=True)
    (tree / "DEBIAN" / "control").write_text(
        f"Package: {package}\nVersion: {version}\nArchitecture: {arch}\n"
        "Maintainer: A3 <contact@a3-audio.com>\nDescription: test package\n")
    deb = folder / (name or f"{package}_{version}_{arch}.deb")
    subprocess.run(["dpkg-deb", "--build", str(tree), str(deb)],
                   check=True, capture_output=True)
    return deb


class ReleaseRunner(Recorder):
    """Records everything; really runs the checks (gpgv, dpkg-deb), answers
    the machine's architecture, and pretends apt succeeds."""

    REAL = ("gpgv", "dpkg-deb")

    def __init__(self, arch="amd64", codes=()):
        super().__init__(codes)
        self.arch = arch

    def __call__(self, args, **kwargs):
        if args[0] in self.REAL:
            self.commands.append(list(args))
            return subprocess.run(args, **{k: v for k, v in kwargs.items() if k != "check"})
        if list(args) == ["dpkg", "--print-architecture"]:
            self.commands.append(list(args))
            return SimpleNamespace(returncode=0, stdout=f"{self.arch}\n", stderr="")
        return super().__call__(args, **kwargs)

    def installing(self):
        return [c for c in self.commands if c[0] in ("apt-get", "apt-mark")]


@unittest.skipUnless(shutil.which("gpg") and shutil.which("gpgv") and shutil.which("dpkg-deb"),
                     "install-release tests need gpg, gpgv and dpkg-deb")
class InstallRelease(HelperTest):
    """install-release <dir>: signed sums, A3 names, this machine's arch, or nothing."""

    @classmethod
    def setUpClass(cls):
        cls.keys = Path(tempfile.mkdtemp())
        cls.home = cls.keys / "gnupg"
        cls.home.mkdir(mode=0o700)
        gpg(cls.home, "--passphrase", "", "--quick-gen-key",
            "a3 test <test@example.invalid>", "ed25519", "sign", "never")
        cls.keyring = cls.keys / "a3-audio.gpg"
        cls.keyring.write_bytes(gpg(cls.home, "--export"))
        cls.other = cls.keys / "other"
        cls.other.mkdir(mode=0o700)
        gpg(cls.other, "--passphrase", "", "--quick-gen-key",
            "other <other@example.invalid>", "ed25519", "sign", "never")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.keys)

    def setUp(self):
        super().setUp()
        self.run_ = ReleaseRunner()
        self.release = self.tmp / "release"
        self.release.mkdir(mode=0o755)

    def release_of(self, *debs, sign_with=None):
        """SHA256SUMS over the folder's .debs, signed (by default with the A3 key)."""
        lines = [f"{hashlib.sha256(deb.read_bytes()).hexdigest()}  {deb.name}" for deb in debs]
        self.write_sums(lines, sign_with)

    def write_sums(self, lines, sign_with=None):
        sums = self.release / "SHA256SUMS"
        sums.write_text("\n".join(lines) + "\n")
        signature = self.release / "SHA256SUMS.asc"
        signature.unlink(missing_ok=True)
        gpg(sign_with or self.home, "--armor", "--detach-sign",
            "--output", str(signature), str(sums))

    def install(self, folder=None, keyring=None, package_keyring=None):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = self.main("install-release", str(folder or self.release),
                             keyring=keyring or self.keyring,
                             package_keyring=package_keyring or self.tmp / "no-package-keyring")
        self.stderr = err.getvalue()
        return code

    def assertRefused(self, why):
        self.assertEqual(self.install(), 2)
        self.assertEqual(self.run_.installing(), [])
        self.assertEqual(len(self.stderr.strip().splitlines()), 1, self.stderr)
        self.assertIn(why, self.stderr)

    def good_release(self):
        debs = [make_deb(self.release, "a3-core-app", "amd64"),
                make_deb(self.release, "stemdeck", "all")]
        self.release_of(*debs)
        return debs

    # The happy path.

    def test_a_good_release_is_installed_and_held(self):
        self.good_release()
        self.assertEqual(self.install(), 0, self.stderr)
        update, install, hold = self.run_.installing()
        self.assertEqual(update, ["apt-get", "update"])
        self.assertEqual(install[:4], ["apt-get", "install", "-y", "--allow-change-held-packages"])
        self.assertEqual(sorted(Path(path).name for path in install[4:]),
                         ["a3-core-app_1.0_amd64.deb", "stemdeck_1.0_all.deb"])
        for path in install[4:]:
            self.assertTrue(Path(path).is_absolute(), path)
        self.assertEqual(hold[:2], ["apt-mark", "hold"])
        self.assertEqual(sorted(hold[2:]), ["a3-core-app", "stemdeck"])

    def test_the_signature_is_checked_against_the_a3_keyring(self):
        self.good_release()
        self.install()
        gpgv = [c for c in self.run_.commands if c[0] == "gpgv"]
        self.assertEqual(len(gpgv), 1)
        self.assertIn(str(self.keyring), gpgv[0])
        self.assertEqual(self.helper.KEYRING, Path("/usr/share/keyrings/a3-audio.gpg"))

    def test_the_packages_keyring_comes_first(self):
        self.good_release()
        missing = self.tmp / "no-checkout-keyring"
        self.assertEqual(self.install(keyring=missing, package_keyring=self.keyring), 0, self.stderr)
        gpgv = [c for c in self.run_.commands if c[0] == "gpgv"]
        self.assertIn(str(self.keyring), gpgv[0])

    def test_the_packages_keyring_wins_over_the_checkouts(self):
        """A release signed for the package's key is refused against the other one."""
        self.good_release()
        wrong = self.tmp / "wrong.gpg"
        wrong.write_bytes(gpg(self.other, "--export"))
        self.assertEqual(self.install(keyring=self.keyring, package_keyring=wrong), 2)
        self.assertIn(str(wrong), self.stderr)

    def test_without_the_package_the_default_keyring_is_the_fallback(self):
        self.good_release()
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual(self.helper.PACKAGE_KEYRING, Path("/usr/lib/a3-update/a3-audio.gpg"))

    def test_no_keyring_at_all_is_refused_with_a_reason(self):
        self.good_release()
        none = self.tmp / "none"
        self.assertEqual(self.install(keyring=none, package_keyring=none), 2)
        self.assertEqual(self.run_.installing(), [])
        self.assertIn("keyring", self.stderr)
        self.assertEqual(len(self.stderr.strip().splitlines()), 1, self.stderr)

    def test_apt_installs_private_copies_not_the_callers_files(self):
        """The caller owns <dir> and could swap a file after the checks."""
        self.good_release()
        self.install()
        install = self.run_.installing()[1]
        for path in install[4:]:
            self.assertNotEqual(Path(path).parent, self.release)

    def test_no_copy_stays_behind(self):
        self.good_release()
        self.install()
        install = self.run_.installing()[1]
        self.assertFalse(Path(install[4]).parent.exists())

    def test_apt_runs_noninteractive(self):
        self.good_release()
        seen = []

        def run(args, **kwargs):
            if args[0] in ("apt-get", "apt-mark"):
                seen.append(kwargs.get("env"))
            return self.run_(args, **kwargs)
        self.helper.main(["install-release", str(self.release)], run=run,
                         env={"PATH": os.environ["PATH"]}, keyring=self.keyring)
        self.assertEqual(len(seen), 3)
        for env in seen:
            self.assertEqual("noninteractive", env["DEBIAN_FRONTEND"])

    def test_a_failing_install_passes_its_code(self):
        self.good_release()
        self.run_ = ReleaseRunner(codes=[0, 100])
        self.assertEqual(self.install(), 100)
        self.assertEqual(len(self.run_.installing()), 2)

    def test_the_sums_may_list_other_machines_assets(self):
        debs = self.good_release()
        lines = (self.release / "SHA256SUMS").read_text().splitlines()
        self.write_sums(lines + ["0" * 64 + "  a3-core-app_1.0_arm64.deb"])
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual(len(self.run_.installing()[1]), 4 + len(debs))

    # Refusals: nothing installed, one line, exit 2.

    def test_a_package_that_is_not_a3_is_refused(self):
        self.release_of(make_deb(self.release, "curl", "amd64"))
        self.assertRefused("not an A3 package")

    def test_a_removed_package_is_refused(self):
        self.release_of(make_deb(self.release, "a3-canvas", "amd64"))
        self.assertRefused("not an A3 package")

    def test_another_architecture_is_refused(self):
        self.release_of(make_deb(self.release, "a3-core-app", "arm64"))
        self.assertRefused("arm64")

    def test_the_machines_architecture_comes_from_dpkg(self):
        self.run_ = ReleaseRunner(arch="arm64")
        self.release_of(make_deb(self.release, "a3-core-app", "arm64"))
        self.assertEqual(self.install(), 0, self.stderr)

    def test_a_wrong_sum_is_refused(self):
        deb = make_deb(self.release, "a3-core-app", "amd64")
        self.write_sums(["0" * 64 + f"  {deb.name}"])
        self.assertRefused("checksum")

    def test_a_deb_not_in_the_sums_is_refused(self):
        listed = make_deb(self.release, "a3-core-app", "amd64")
        make_deb(self.release, "stemdeck", "all")
        self.release_of(listed)
        self.assertRefused("not in SHA256SUMS")

    def test_a_missing_signature_is_refused(self):
        self.good_release()
        (self.release / "SHA256SUMS.asc").unlink()
        self.assertRefused("SHA256SUMS.asc")

    def test_missing_sums_are_refused(self):
        self.good_release()
        (self.release / "SHA256SUMS").unlink()
        self.assertRefused("SHA256SUMS")

    def test_a_signature_by_another_key_is_refused(self):
        debs = [make_deb(self.release, "a3-core-app", "amd64")]
        self.release_of(*debs, sign_with=self.other)
        self.assertRefused("signature")

    def test_sums_changed_after_signing_are_refused(self):
        deb = make_deb(self.release, "a3-core-app", "amd64")
        self.release_of(deb)
        with (self.release / "SHA256SUMS").open("a") as sums:
            sums.write("0" * 64 + "  stemdeck_1.0_all.deb\n")
        self.assertRefused("signature")

    def test_an_option_like_argument_is_refused(self):
        self.good_release()
        for argv in (["install-release", "--allow-unauthenticated"],
                     ["install-release", "-o", str(self.release)]):
            with self.subTest(argv), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.main(*argv, keyring=self.keyring), 2)
        self.assertEqual(self.run_.commands, [])

    def test_an_option_like_file_name_is_refused(self):
        deb = make_deb(self.release, "a3-core-app", "amd64", name="--force-all.deb")
        self.release_of(deb)
        self.assertRefused("looks like an option")

    def test_exactly_one_folder_is_taken(self):
        self.good_release()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.main("install-release", keyring=self.keyring), 2)
            self.assertEqual(self.main("install-release", str(self.release), str(self.release),
                                       keyring=self.keyring), 2)
        self.assertEqual(self.run_.commands, [])

    def test_a_relative_folder_is_refused(self):
        self.good_release()
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(self.main("install-release", "release", keyring=self.keyring), 2)
        self.assertIn("absolute", err.getvalue())
        self.assertEqual(self.run_.commands, [])

    def test_a_world_writable_folder_is_refused(self):
        self.good_release()
        os.chmod(self.release, 0o777)
        self.assertRefused("world-writable")

    def test_a_symlinked_folder_is_refused(self):
        self.good_release()
        link = self.tmp / "link"
        link.symlink_to(self.release)
        self.assertEqual(self.install(link), 2)
        self.assertEqual(self.run_.installing(), [])

    def test_a_symlinked_deb_is_refused(self):
        outside = self.tmp / "outside"
        outside.mkdir()
        target = make_deb(outside, "a3-core-app", "amd64")
        (self.release / target.name).symlink_to(target)
        self.release_of(target)
        self.assertRefused("symlink")

    def test_a_symlinked_sums_file_is_refused(self):
        self.good_release()
        sums = self.release / "SHA256SUMS"
        moved = self.tmp / "SHA256SUMS"
        sums.rename(moved)
        sums.symlink_to(moved)
        self.assertRefused("symlink")

    def test_a_subfolder_is_refused(self):
        self.good_release()
        (self.release / "more.deb").mkdir()
        self.assertRefused("not a regular file")

    def test_a_file_that_is_not_a_deb_is_refused(self):
        self.good_release()
        (self.release / "postinst.sh").write_text("#!/bin/sh\n")
        self.assertRefused("not a .deb")

    def test_a_folder_without_debs_is_refused(self):
        self.write_sums(["0" * 64 + "  a3-core-app_1.0_amd64.deb"])
        self.assertRefused("no .deb")

    def test_a_file_that_is_not_a_package_is_refused(self):
        fake = self.release / "a3-core-app_1.0_amd64.deb"
        fake.write_bytes(b"not a deb")
        self.release_of(fake)
        self.assertRefused("not a Debian package")

    def test_an_unreadable_file_is_refused(self):
        deb, _ = self.good_release()
        os.chmod(deb, 0)
        if os.access(deb, os.R_OK):
            self.skipTest("running as root reads anything")
        self.assertRefused(deb.name)

    def test_a_failing_copy_is_refused_and_leaves_nothing(self):
        self.good_release()

        def full(source, target):
            raise OSError(28, "No space left on device")
        self.helper.copy_private = full
        self.assertRefused("No space left on device")

    def test_two_files_of_one_package_are_refused(self):
        self.release_of(make_deb(self.release, "a3-core-app", "amd64", "1.0"),
                        make_deb(self.release, "a3-core-app", "amd64", "2.0"))
        self.assertRefused("twice")


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
