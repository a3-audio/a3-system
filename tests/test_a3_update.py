# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""a3-update, each machine's updater: Core asks, it installs a signed release.

No network and no root: GitHub is a table of URLs, every command a fake."""

import hashlib
import importlib.machinery
import importlib.util
import json
import shutil
import stat
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from installer import archive  # noqa: E402

SERVICE = REPO / "update" / "a3-update"
API = "https://api.github.com/repos/a3-audio/a3-system/releases/tags/"


def load_service():
    loader = importlib.machinery.SourceFileLoader("a3_update", str(SERVICE))
    spec = importlib.util.spec_from_loader("a3_update", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def tmpdir(case):
    path = Path(tempfile.mkdtemp())
    case.addCleanup(shutil.rmtree, path, ignore_errors=True)
    return path


def truth(core="192.168.8.10", port=9081, host="any"):
    return {"hosts": {"core": core, "any": "0.0.0.0", "local": "127.0.0.1"},
            "listeners": [{"name": "update.control", "program": "update", "role": "control",
                           "host": host, "port": port, "protocol": "tcp", "carries": "x"}]}


class FakeSystem:
    """dpkg, sudo and systemctl as a table; every command written down."""

    def __init__(self, installed=None, arch="amd64", units=None, codes=None):
        self.installed = installed if installed is not None else {"stemdeck": "03.1+0",
                                                                  "a3-update": "03.1+0"}
        self.arch = arch
        self.units = units or {}
        self.codes = codes or {}
        self.commands = []
        self.release_dir_seen = None

    def __call__(self, args, **_kwargs):
        args = [str(a) for a in args]
        self.commands.append(args)
        code = self.codes.get(args[0], 0)
        if args[:2] == ["dpkg", "--print-architecture"]:
            return SimpleNamespace(returncode=0, stdout=self.arch + "\n", stderr="")
        if args[:2] == ["dpkg-query", "-W"]:
            names = args[4:]
            out = "".join(f"{n}\t{self.installed[n]}\tinstalled\n" for n in names
                          if n in self.installed)
            return SimpleNamespace(returncode=0 if out else 1, stdout=out, stderr="")
        if args[:2] == ["dpkg-query", "-L"]:
            return SimpleNamespace(returncode=0, stdout="\n".join(self.units.get(args[2], [])) + "\n",
                                   stderr="")
        if args[0] == "sudo":
            folder = Path(args[-1])
            self.release_dir_seen = (folder, sorted(p.name for p in folder.iterdir()),
                                     stat.S_IMODE(folder.stat().st_mode))
            return SimpleNamespace(returncode=code, stdout="",
                                   stderr="sudo: a password is required\n" if code else "")
        return SimpleNamespace(returncode=code, stdout="", stderr="")


class FakeGitHub:
    """The release's JSON and its assets, by URL."""

    def __init__(self, tag, assets, sums=None, missing=()):
        self.files = {}
        listing = []
        for name, data in assets.items():
            url = f"https://github.com/a3-audio/a3-system/releases/download/{tag}/{name}"
            self.files[url] = data
            listing.append({"name": name, "browser_download_url": url})
        debs = {n: d for n, d in assets.items() if n.endswith(".deb")}
        if sums is None:
            sums = "".join(f"{hashlib.sha256(d).hexdigest()}  {n}\n" for n, d in sorted(debs.items()))
        for name, data in (("SHA256SUMS", sums.encode()), ("SHA256SUMS.asc", b"sig")):
            if name in missing:
                continue
            url = f"https://github.com/a3-audio/a3-system/releases/download/{tag}/{name}"
            self.files[url] = data
            listing.append({"name": name, "browser_download_url": url})
        self.files[API + tag] = json.dumps({"tag_name": tag, "assets": listing}).encode()
        self.asked = []

    def get(self, url):
        self.asked.append(url)
        if url not in self.files:
            raise OSError(f"404 {url}")
        return self.files[url]

    def download(self, url, path):
        Path(path).write_bytes(self.get(url))


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = load_service()
        self.runtime = tmpdir(self)
        self.state = tmpdir(self) / "state" / "last-job.json"

    def updater(self, system, github, codename="forky", **kwargs):
        self.system, self.github = system, github
        return self.service.Updater(run=system, http_get=github.get, download=github.download,
                                    runtime_dir=self.runtime, state_file=self.state,
                                    hostname="a3nuc2", codename=codename,
                                    spawn=lambda work: work(), **kwargs)


class TheTruth(ServiceTest):
    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
        return path

    def test_the_port_and_cores_address_come_from_the_truth(self):
        found = self.service.endpoint(truth(core="192.168.8.10", port=9081))
        self.assertEqual(("0.0.0.0", 9081, "192.168.8.10"), found)

    def test_a_truth_without_the_listener_is_refused(self):
        bare = {"hosts": {"core": "192.168.8.10"}, "listeners": []}
        with self.assertRaises(self.service.TruthError):
            self.service.endpoint(bare)

    def test_a3_osc_truth_first_then_cores_cache_then_the_packages(self):
        home = tmpdir(self)
        named = self.write(home / "named.json", truth(port=1))
        cache = self.write(home / ".cache/a3/a3-osc.json", truth(port=2))
        shipped = self.write(home / "shipped.json", truth(port=3))
        self.assertEqual(1, self.service.load_truth({"A3_OSC_TRUTH": str(named)}, home, shipped)
                         ["listeners"][0]["port"])
        self.assertEqual(2, self.service.load_truth({}, home, shipped)["listeners"][0]["port"])
        cache.unlink()
        self.assertEqual(3, self.service.load_truth({}, home, shipped)["listeners"][0]["port"])

    def test_a_cached_truth_from_an_older_core_without_the_listener_is_passed_over(self):
        home = tmpdir(self)
        self.write(home / ".cache/a3/a3-osc.json", {"hosts": {}, "listeners": []})
        shipped = self.write(home / "shipped.json", truth(port=3))
        self.assertEqual(3, self.service.load_truth({}, home, shipped)["listeners"][0]["port"])

    def test_no_usable_truth_is_an_error(self):
        home = tmpdir(self)
        with self.assertRaises(self.service.TruthError):
            self.service.load_truth({}, home, home / "none.json")

    def test_the_service_holds_no_port_literal(self):
        """The port is the truth's (second-truth rule)."""
        self.assertNotIn("9081", SERVICE.read_text())


class Status(ServiceTest):
    def test_this_machine_its_packages_and_the_job(self):
        updater = self.updater(FakeSystem(installed={"stemdeck": "03.1+2", "a3-update": "03.1+0"}),
                               FakeGitHub("v03.2", {}))
        status = updater.status()
        self.assertEqual("a3nuc2", status["host"])
        self.assertEqual("amd64", status["arch"])
        self.assertEqual("forky", status["codename"])
        self.assertEqual({"stemdeck": "03.1+2", "a3-update": "03.1+0"}, status["packages"])
        self.assertEqual("idle", status["job"]["state"])

    def test_it_asks_dpkg_only_for_a3_packages(self):
        updater = self.updater(FakeSystem(), FakeGitHub("v03.2", {}))
        updater.status()
        query = [c for c in self.system.commands if c[:2] == ["dpkg-query", "-W"]][0]
        self.assertEqual(list(self.service.A3_PACKAGES), query[4:])

    def test_the_package_list_is_a3_roots(self):
        self.assertEqual(self.service.A3_PACKAGES, archive.A3_PACKAGES)
        self.assertIn("a3-update", archive.A3_PACKAGES)


class Assets(ServiceTest):
    def names(self, *names):
        return [{"name": n, "browser_download_url": f"https://x/{n}"} for n in names]

    def test_this_machines_arch_and_all(self):
        chosen = self.service.choose_assets(
            self.names("stemdeck_03.2+0_amd64.deb", "stemdeck_03.2+0_arm64.deb",
                       "a3-update_03.2+0_all.deb", "a3-core_03.2+0_amd64.deb"),
            {"stemdeck", "a3-update"}, "amd64", "forky")
        self.assertEqual({"stemdeck": "stemdeck_03.2+0_amd64.deb",
                          "a3-update": "a3-update_03.2+0_all.deb"},
                         {p: a["name"] for p, a in chosen.items()})

    def test_an_all_package_two_lines_built_is_the_one_of_this_suite(self):
        chosen = self.service.choose_assets(
            self.names("a3-update_03.2+0_forky_all.deb", "a3-update_03.2+0_trixie_all.deb"),
            {"a3-update"}, "arm64", "trixie")
        self.assertEqual("a3-update_03.2+0_trixie_all.deb", chosen["a3-update"]["name"])

    def test_not_installed_is_not_downloaded(self):
        chosen = self.service.choose_assets(
            self.names("a3-core_03.2+0_amd64.deb", "a3-update_03.2+0_all.deb"),
            {"a3-update"}, "amd64", "forky")
        self.assertEqual(["a3-update"], list(chosen))

    def test_names_that_are_no_deb_or_no_a3_package_are_passed_over(self):
        chosen = self.service.choose_assets(
            self.names("SHA256SUMS", "notes.txt", "curl_8_amd64.deb", "../x_1_amd64.deb"),
            {"stemdeck"}, "amd64", "forky")
        self.assertEqual({}, chosen)


def deb(name):
    return f"{name} payload".encode()


TAG = "v03.2"


def a_release(**kwargs):
    return FakeGitHub(TAG, {"stemdeck_03.2+0_amd64.deb": deb("stemdeck"),
                            "stemdeck_03.2+0_arm64.deb": deb("stemdeck arm"),
                            "a3-core_03.2+0_amd64.deb": deb("core"),
                            "a3-update_03.2+0_forky_all.deb": deb("update"),
                            "a3-update_03.2+0_trixie_all.deb": deb("update t")},
                      **kwargs)


def a_machine(**kwargs):
    units = {"stemdeck": ["/usr/lib/systemd/user/stemdeck.service",
                          "/usr/lib/systemd/user/stemdeck@.service",
                          "/usr/lib/systemd/user/stemdeck.service.d/x.conf",
                          "/usr/bin/stemdeck"],
             "a3-update": ["/usr/lib/systemd/user/a3-update.service",
                           "/usr/lib/a3-update/a3-root"]}
    return FakeSystem(units=units, **kwargs)


class AnUpdate(ServiceTest):
    TAG = TAG

    def release(self, **kwargs):
        return a_release(**kwargs)

    def machine(self, **kwargs):
        return a_machine(**kwargs)

    def test_it_downloads_what_this_machine_has_and_hands_it_to_a3_root(self):
        updater = self.updater(self.machine(), self.release())
        self.assertEqual("downloading", updater.start(self.TAG)["state"])
        self.assertEqual("done", updater.status()["job"]["state"], updater.status()["job"])
        folder, names, mode = self.system.release_dir_seen
        self.assertEqual(["SHA256SUMS", "SHA256SUMS.asc", "a3-update_03.2+0_forky_all.deb",
                          "stemdeck_03.2+0_amd64.deb"], names)
        self.assertEqual(0o700, mode)
        self.assertEqual(self.runtime, folder.parent)
        sudo = [c for c in self.system.commands if c[0] == "sudo"]
        self.assertEqual([["sudo", "-n", "/usr/lib/a3-update/a3-root", "install-release",
                           str(folder)]], sudo)

    def test_the_release_is_read_by_its_tag_without_login(self):
        updater = self.updater(self.machine(), self.release())
        updater.start(self.TAG)
        self.assertEqual(API + self.TAG, self.github.asked[0])

    def test_the_folder_is_gone_afterwards(self):
        updater = self.updater(self.machine(), self.release())
        updater.start(self.TAG)
        self.assertEqual([], list(self.runtime.iterdir()))

    def test_the_updated_packages_user_services_restart_and_itself_last(self):
        updater = self.updater(self.machine(), self.release())
        updater.start(self.TAG)
        systemctl = [c for c in self.system.commands if c[0] == "systemctl"]
        self.assertEqual([["systemctl", "--user", "daemon-reload"],
                          ["systemctl", "--user", "try-restart", "stemdeck.service",
                           "stemdeck@*.service"],
                          ["systemctl", "--user", "--no-block", "try-restart",
                           "a3-update.service"]], systemctl)
        sudo_at = next(i for i, c in enumerate(self.system.commands) if c[0] == "sudo")
        reload_at = self.system.commands.index(["systemctl", "--user", "daemon-reload"])
        self.assertLess(sudo_at, reload_at)

    def test_the_result_is_kept_for_after_its_own_restart(self):
        updater = self.updater(self.machine(), self.release())
        updater.start(self.TAG)
        again = self.updater(self.machine(), self.release())
        job = again.status()["job"]
        self.assertEqual(("done", self.TAG), (job["state"], job["tag"]))
        self.assertEqual(["a3-update", "stemdeck"], sorted(job["packages"]))

    def test_states_run_in_order(self):
        seen = []
        updater = self.updater(self.machine(), self.release(), on_state=seen.append)
        updater.start(self.TAG)
        self.assertEqual(["downloading", "checking", "installing", "restarting", "done"], seen)

    def test_a_second_job_is_refused_while_one_runs(self):
        held = []
        updater = self.updater(self.machine(), self.release())
        updater.spawn = held.append
        updater.start(self.TAG)
        with self.assertRaises(self.service.Busy):
            updater.start(self.TAG)
        held[0]()
        self.assertEqual("done", updater.status()["job"]["state"])
        updater.spawn = lambda work: work()
        updater.start(self.TAG)

    def test_a_tag_that_is_no_version_is_refused(self):
        updater = self.updater(self.machine(), self.release())
        for tag in ("", "latest", "../v1", "v1/../x", "v1?x", "-v1", "v03.2 x"):
            with self.subTest(tag=tag), self.assertRaises(self.service.BadRequest):
                updater.start(tag)
        self.assertEqual([], self.github.asked)

    def failed(self, updater):
        updater.start(self.TAG)
        job = updater.status()["job"]
        self.assertEqual("failed", job["state"])
        return job["reason"]

    def test_an_unknown_tag_fails_with_a_reason(self):
        updater = self.updater(self.machine(), FakeGitHub("v09.9", {}))
        self.assertIn(self.TAG, self.failed(updater))
        self.assertFalse(any(c[0] == "sudo" for c in self.system.commands))

    def test_a_release_without_signed_sums_fails_before_downloading_a_deb(self):
        updater = self.updater(self.machine(), self.release(missing=("SHA256SUMS.asc",)))
        self.assertIn("SHA256SUMS.asc", self.failed(updater))
        self.assertFalse(any(u.endswith(".deb") for u in self.github.asked))

    def test_a_deb_that_does_not_match_its_sum_fails_before_root(self):
        sums = f"{'0' * 64}  stemdeck_03.2+0_amd64.deb\n"
        updater = self.updater(self.machine(), self.release(sums=sums))
        reason = self.failed(updater)
        self.assertIn("stemdeck_03.2+0_amd64.deb", reason)
        self.assertFalse(any(c[0] == "sudo" for c in self.system.commands))
        self.assertEqual([], list(self.runtime.iterdir()))

    def test_nothing_of_this_machine_in_the_release_fails(self):
        updater = self.updater(self.machine(installed={"beat-analyzer": "1"}),
                               FakeGitHub(self.TAG, {"stemdeck_03.2+0_amd64.deb": deb("s")}))
        self.assertIn("nothing", self.failed(updater))

    def test_a_refused_sudo_names_the_sudoers_line(self):
        updater = self.updater(self.machine(codes={"sudo": 1}), self.release())
        reason = self.failed(updater)
        self.assertIn("/etc/sudoers.d/a3-update", reason)
        self.assertIn("password is required", reason)
        self.assertFalse(any(c[0] == "systemctl" for c in self.system.commands))

    def test_a3_roots_refusal_is_reported(self):
        updater = self.updater(self.machine(codes={"sudo": 2}), self.release())
        self.assertIn("a3-root", self.failed(updater))

    def test_a_failure_is_kept_too(self):
        updater = self.updater(self.machine(), FakeGitHub("v09.9", {}))
        updater.start(self.TAG)
        self.assertEqual("failed", self.updater(self.machine(), self.release()).status()["job"]["state"])

    def test_without_its_own_package_in_the_release_it_does_not_restart_itself(self):
        github = FakeGitHub(self.TAG, {"stemdeck_03.2+0_amd64.deb": deb("s")})
        updater = self.updater(self.machine(), github)
        updater.start(self.TAG)
        self.assertEqual("done", updater.status()["job"]["state"])
        self.assertNotIn(["systemctl", "--user", "--no-block", "try-restart", "a3-update.service"],
                         self.system.commands)


class OnlyCoreAsks(unittest.TestCase):
    def test_cores_address(self):
        service = load_service()
        self.assertTrue(service.from_core("192.168.8.10", "192.168.8.10", core_is_here=False))
        self.assertFalse(service.from_core("192.168.8.20", "192.168.8.10", core_is_here=False))
        self.assertFalse(service.from_core("127.0.0.1", "192.168.8.10", core_is_here=False))

    def test_loopback_counts_on_cores_own_machine(self):
        service = load_service()
        self.assertTrue(service.from_core("127.0.0.1", "192.168.8.10", core_is_here=True))
        self.assertTrue(service.from_core("::ffff:127.0.0.1", "192.168.8.10", core_is_here=True))
        self.assertFalse(service.from_core("192.168.8.20", "192.168.8.10", core_is_here=True))

    def test_an_ipv4_mapped_address_is_its_ipv4(self):
        service = load_service()
        self.assertTrue(service.from_core("::ffff:192.168.8.10", "192.168.8.10", core_is_here=False))


class OverHttp(ServiceTest):
    """The server on loopback, the way Core's window asks (HTTP/1.0, JSON)."""

    def serve(self, core="127.0.0.1", updater=None):
        updater = updater or self.updater(a_machine(), a_release())
        server = self.service.make_server(updater, "127.0.0.1", 0, core, core_is_here=False)
        import threading
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_address[1]}"

    def ask(self, url, body=None, method=None):
        data = None if body is None else body.encode()
        request = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(request, timeout=5) as answer:
                return answer.status, json.loads(answer.read())
        except urllib.error.HTTPError as error:
            with error:
                return error.code, json.loads(error.read())

    def test_status(self):
        code, body = self.ask(self.serve() + "/status")
        self.assertEqual(200, code)
        self.assertEqual("a3nuc2", body["host"])
        self.assertEqual("idle", body["job"]["state"])

    def test_update(self):
        base = self.serve()
        code, body = self.ask(base + "/update", json.dumps({"tag": "v03.2"}))
        self.assertEqual(202, code)
        self.assertEqual("v03.2", body["job"]["tag"])
        self.assertEqual("done", self.ask(base + "/status")[1]["job"]["state"])

    def test_not_from_core_is_forbidden(self):
        base = self.serve(core="192.0.2.1")
        self.assertEqual(403, self.ask(base + "/status")[0])
        self.assertEqual(403, self.ask(base + "/update", json.dumps({"tag": "v03.2"}))[0])
        self.assertEqual([], self.github.asked)

    def test_a_bad_body_is_a_bad_request(self):
        base = self.serve()
        for body in ("", "not json", "[]", json.dumps({"tag": "latest"}), json.dumps({})):
            with self.subTest(body=body):
                self.assertEqual(400, self.ask(base + "/update", body, method="POST")[0])

    def test_busy_is_a_conflict(self):
        held = []
        updater = self.updater(a_machine(), a_release())
        updater.spawn = held.append
        base = self.serve(updater=updater)
        self.assertEqual(202, self.ask(base + "/update", json.dumps({"tag": "v03.2"}))[0])
        code, body = self.ask(base + "/update", json.dumps({"tag": "v03.2"}))
        self.assertEqual(409, code)
        self.assertEqual("downloading", body["job"]["state"])

    def test_anything_else_is_not_found(self):
        base = self.serve()
        self.assertEqual(404, self.ask(base + "/")[0])
        self.assertEqual(404, self.ask(base + "/update")[0])
        self.assertEqual(404, self.ask(base + "/status", "{}")[0])


if __name__ == "__main__":
    unittest.main()
