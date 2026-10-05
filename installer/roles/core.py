"""A³ Core: the a3-core package, built from this release's a3-core.

The package is built here, from the submodule, rather than taken from the
apt repository: that repository holds one package, the newest, and a Core
installed from it is on a3-core's main whatever tag the rest is on. Built
from the submodule it is exactly the release's, also offline. It is then
held, so `apt upgrade` does not move it off the release.

Its debconf questions are asked here, with the rest, and handed over
preseeded and marked seen; the postinst takes them as given (a3-core
8573e2b, 8dcb2c7). The beat-analyzer comes with it: the package's
a3-user-install.service builds it from ~/a3-system/beat-analyzer.
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .base import SCREEN_PACKAGES, Role, RoleError

PACKAGE_DIR = Path("a3-core/platform-config/debian-x86_64/a3-core")
SHIPPED_CONFIG = PACKAGE_DIR / "home/aaa/.local/share/a3-core/config"
POSTINST = PACKAGE_DIR / "DEBIAN/postinst"
# The OSC truth: which host is which, among them the Core's address.
TRUTH = PACKAGE_DIR / "usr/share/a3/a3-osc.json"

# The user units the package puts into ~/.config/systemd/user (from
# SHIPPED_CONFIG) and enables through default.target.wants. Stopped and
# disabled when the Core leaves; the files stay with the rest of ~/.config.
CORE_UNITS = (
    "a3-main.service", "a3-jack.service", "a3-reaper.service", "a3-core.service",
    "beat-analyzer.service", "qjackctl.service", "zita-n2j.service",
    "zita-j2n.service", "a3-bar-per-workspace.service", "a3-user-install.service",
)

GROUP_LABELS = {
    "reaper": "REAPER: Template, OSC-Map, Presets, Effekte",
    "i3": "i3-Config",
    "systemd": "systemd-User-Units",
    "qjackctl": "QjackCtl und Patchbay",
    "iem": "IEM-Plugin-Settings",
    "other": "sonstige Dateien",
}


def postinst_function(repo, *names):
    """Functions from the package's own postinst, to run them here rather
    than keep a second copy of what they decide."""
    text = (repo / POSTINST).read_text()
    bodies = []
    for name in names:
        if f"\n{name}() {{" not in text:
            raise RoleError(f"a3-core in diesem Stand kennt {name}() nicht; er ist "
                            "älter als der Installer. Erst den a3-core-Pin hochziehen.")
        start = text.index(f"\n{name}() {{") + 1
        end = text.index("\n}\n", start) + 3
        bodies.append(text[start:end])
    return "\n".join(bodies)


def differing_groups(repo, home):
    """The parts of ~/.config that differ from what this release ships,
    by the package's own rule (differing_config_groups in the postinst)."""
    script = postinst_function(repo, "config_group", "differing_config_groups")
    found = subprocess.run(
        ["sh", "-c", f'{script}\ndiffering_config_groups "$1" "$2"', "sh",
         str(repo / SHIPPED_CONFIG), str(home / ".config")],
        check=True, capture_output=True, text=True).stdout.strip()
    return [g.strip() for g in found.split(",") if g.strip()]


def chosen_groups(setting, differing):
    """The setting ("all", "none", "reaper, i3") applied to what differs."""
    setting = setting.strip()
    if setting == "all":
        return list(differing)
    if setting in ("none", ""):
        return []
    wanted = {g.strip() for g in setting.split(",")}
    return [g for g in differing if g in wanted]


def preseed_lines(settings, replace):
    """debconf-set-selections input: every question the postinst asks,
    answered and marked seen."""
    def flag(key):
        return "true" if settings.flag("core", key) else "false"

    lines = [("configure-network", "boolean", flag("configure_network"))]
    if settings.flag("core", "configure_network"):
        lines += [
            ("install-default-network", "boolean", "false"),
            ("interface", "string", settings.get("core", "interface")),
            ("address", "string", settings.get("core", "address")),
            ("gateway", "string", settings.get("core", "gateway")),
            ("dns", "string", settings.get("core", "dns")),
            ("bridge-with", "string", settings.get("core", "bridge_with")),
        ]
    lines.append(("headless-display", "boolean", flag("headless")))
    if replace is not None:
        lines.append(("replace-config", "multiselect", ", ".join(replace)))

    out = []
    for question, kind, value in lines:
        out.append(f"a3-core a3-core/{question} {kind} {value}")
        out.append(f"a3-core a3-core/{question} seen true")
    return "\n".join(out) + "\n"


def truth_core_address(repo):
    """hosts.core in this release's truth, or None when it names none."""
    try:
        return json.loads((repo / TRUTH).read_text())["hosts"]["core"]
    except (OSError, ValueError, KeyError, TypeError):
        return None


def addresses_in(ip_output):
    """The IPv4 addresses in `ip -o -4 addr show`, without their prefix."""
    found = []
    for line in ip_output.splitlines():
        words = line.split()
        if "inet" in words[:-1]:
            found.append(words[words.index("inet") + 1].split("/")[0])
    return found


def own_addresses(runner):
    """The IPv4 addresses on this machine's interfaces. Only looks, so it
    runs on --dry-run too."""
    try:
        return addresses_in(runner.output(["ip", "-o", "-4", "addr", "show"]))
    except (OSError, subprocess.CalledProcessError):
        return []


def answered_address(settings):
    """The address the Core's own network answers will set, or None when
    the installer is to leave the network as it is."""
    if not settings.flag("core", "configure_network"):
        return None
    return settings.get("core", "address").split("/")[0].strip() or None


def core_refusal(truth_address, own, answered):
    """None when this machine may be the Core, else why not. Only the
    machine with the truth's core address may: a second Core would announce
    itself (/core/here) in the same LAN and the desk could land on it."""
    if truth_address and (truth_address in own or truth_address == answered):
        return None
    if not truth_address:
        return ("Die Wahrheit (a3-osc.json) dieses Stands nennt keine Core-Adresse; "
                "ob dieser Rechner der Core ist, lässt sich nicht prüfen.")
    return (f"Dieser Rechner hat nicht die Core-Adresse der Wahrheit ({truth_address}), "
            "und die Netzwerk-Antworten des Cores setzen sie nicht. Ein zweiter Core "
            "würde sich im selben LAN melden (/core/here), und das Pult könnte beim "
            "falschen landen. Der Core wird nicht installiert, die anderen Rollen schon.")


def check_core(ctx, lookup=own_addresses):
    """The check before the Core installs, said out loud: None when it may,
    else the reason it is refused."""
    truth = truth_core_address(ctx.repo)
    own = lookup(ctx.runner)
    answered = answered_address(ctx.settings)
    ctx.runner.log(f"Core-Adresse der Wahrheit: {truth or 'keine'}; "
                   f"dieser Rechner: {', '.join(own) or 'keine'}; "
                   f"aus den Netzwerk-Antworten: {answered or 'keine'}")
    return core_refusal(truth, own, answered)


class Core(Role):
    name = "core"
    label = "A³ Core (Sound-Server: JACK, REAPER, a3-core, Beat-Analyzer)"
    submodules = ("a3-core", "beat-analyzer")
    platforms = ("debian",)
    # REAPER runs on X; a headless Core runs it on the dummy screen.
    packages = SCREEN_PACKAGES
    needs_screen = True

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        s.set_flag("core", "configure_network", ask.yesno(
            "Netzwerk dieses Cores einrichten?\n(Nein lässt das Netzwerk, wie es ist.)",
            s.flag("core", "configure_network")))
        if s.flag("core", "configure_network"):
            for key, question in (("interface", "Netzwerk-Schnittstelle (z.B. eno1)"),
                                  ("address", "Statische Adresse mit Präfix (z.B. 192.168.8.10/24)"),
                                  ("gateway", "Gateway"),
                                  ("dns", "DNS-Server"),
                                  ("bridge_with", "Zweite Buchse für die Bridge (leer: keine)")):
                s.set("core", key, ask.text(question, s.get("core", key)))
        s.set_flag("core", "headless", ask.yesno(
            "Ohne Monitor betreiben (Dummy-Bildschirm, nur VNC)?",
            s.flag("core", "headless")))

        differing = differing_groups(ctx.repo, ctx.home)
        if not differing:
            ctx.answers["replace"] = []
            return
        default = chosen_groups(s.get("core", "replace"), differing)
        if ask.interactive:
            picked = ask.checklist(
                "Diese Teile von ~/.config weichen von diesem Stand ab.\n"
                "Welche sollen ersetzt werden? (Gesichert nach ~/.config/a3-replaced/)",
                [(g, GROUP_LABELS.get(g, g)) for g in differing], default)
            ctx.answers["replace"] = picked
            if set(picked) == set(differing):
                s.set("core", "replace", "all")
            elif not picked:
                s.set("core", "replace", "none")
            else:
                s.set("core", "replace", ", ".join(picked))
        else:
            ctx.answers["replace"] = default

    def install(self, ctx):
        run = ctx.runner
        work = Path(tempfile.mkdtemp(prefix="a3-core-"))
        try:
            deb = build_package(ctx, work)
            run.run(["debconf-set-selections"], root=True,
                    input=preseed_lines(ctx.settings, ctx.answers.get("replace")))
            run.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                     "--allow-downgrades", "--allow-change-held-packages", deb], root=True)
            run.run(["apt-mark", "hold", "a3-core"], root=True)
        finally:
            shutil.rmtree(work, ignore_errors=True)

    stays = ("~/.config: REAPER-Template, i3, qjackctl, die Unit-Dateien",
             "die Sicherungen in ~/.config/a3-replaced",
             "~/.ssh/authorized_keys (beim Entfernen gesichert und zurückgelegt)")

    def leaving_units(self, ctx):
        return list(CORE_UNITS)

    def leaving_packages(self, ctx):
        return ["a3-core"]

    def leaving_lines(self, ctx):
        return super().leaving_lines(ctx) + [
            "  Mit dem Paket gehen seine Dateien in ~/.local (bin, lib, share/a3-core)."]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        run = ctx.runner
        # The package ships ~/.ssh/authorized_keys, so dpkg removes it with
        # the package; a machine run over ssh would be locked out.
        keys = ctx.home / ".ssh" / "authorized_keys"
        kept = keys.with_name("authorized_keys.a3-keep")
        keep_keys = keys.exists()
        if keep_keys:
            run.run(["cp", "-p", keys, kept])
        try:
            run.run(["apt-mark", "unhold", "a3-core"], root=True)
            run.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "remove", "-y",
                     "a3-core"], root=True)
        finally:
            if keep_keys:
                run.run(["mv", "-f", kept, keys])


def build_package(ctx, work):
    """The a3-core .deb of this release, built into `work`. Versioned like
    a3-core's own workflow does it (tools/package_version.py: 03.0+258)."""
    run = ctx.runner
    if not shutil.which("dpkg-deb"):
        raise RoleError("dpkg-deb fehlt -- ist das ein Debian?")
    version = run.output(["python3", "a3-core/tools/package_version.py"],
                         cwd=ctx.repo).strip()
    tree = work / "a3-core"
    deb = work / f"a3-core_{version}_amd64.deb"
    run.log(f"Baue a3-core {version} aus {ctx.repo / PACKAGE_DIR}")
    if not run.dry_run:
        shutil.copytree(ctx.repo / PACKAGE_DIR, tree, symlinks=True)
        control = tree / "DEBIAN" / "control"
        control.write_text("".join(
            f"Version: {version}\n" if line.startswith("Version:") else line
            for line in control.read_text().splitlines(keepends=True)))
        # apt reads a local package as the user _apt.
        work.chmod(0o755)
    run.run(["dpkg-deb", "--build", "--root-owner-group", tree, deb])
    return deb
