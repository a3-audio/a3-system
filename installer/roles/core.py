"""A³ Core: the a3-core package, built from this release's a3-core.

The package is built here, from the submodule, rather than taken from the
apt repository: that repository holds one package, the newest, and a Core
installed from it is on a3-core's main whatever tag the rest is on. Built
from the submodule it is exactly the release's, also offline. It is then
held, so `apt upgrade` does not move it off the release.

Its debconf questions are asked here, with the rest, and handed over
preseeded and marked seen, the network answers with the a3-core/preseeded
marker; the postinst takes them as given (a3-core 8573e2b, 8dcb2c7, #68).

The beat-analyzer comes with it as a package of its own, `beat-analyzer`,
built from the pinned commit like StemDeck and held. a3-core only recommends
it and adds what is A3 about its unit as a drop-in (a3-core.conf: part of
a3-main, after JACK, off CPU 0); the package does not enable its unit,
a3-main wants it. Before the package, a3-core's a3-user-install.service
built it in ~/a3-system/beat-analyzer and its unit ran that build.

a3-core is one package now: the C++ program, its window and the deployment
(units, i3, PipeWire, the postinst), built from the one a3-core submodule by
installer/package.py. It Conflicts with and Replaces the a3-engine package
of before, which is unheld here if a machine still has it. The beat-analyzer
is the beat-clock only; the meters come from the program.
"""

import json
import re
import subprocess
from pathlib import Path

from . import apppackage
from .apppackage import has_packaging
from .base import (JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce,
                   juce_prefix, systemctl_user)

PACKAGE_DIR = Path("a3-core/platform-config/debian-x86_64/a3-core")
SHIPPED_CONFIG = PACKAGE_DIR / "home/aaa/.local/share/a3-core/config"
POSTINST = Path("a3-core/packaging/DEBIAN/postinst")
# The OSC truth: which host is which, among them the Core's address.
TRUTH = PACKAGE_DIR / "usr/share/a3/a3-osc.json"

# The user units the package puts into ~/.config/systemd/user (from
# SHIPPED_CONFIG) and enables through default.target.wants. Stopped and
# disabled when the Core leaves; the files stay with the rest of ~/.config.
CORE_UNITS = (
    "a3-main.service", "a3-core.service", "a3-aes67.service",
    "a3-bar-per-workspace.service", "a3-screencast.service",
)

ANALYZER_SOURCE = "beat-analyzer"
ANALYZER_UNIT = "beat-analyzer.service"
ANALYZER = apppackage.AppPackage("beat-analyzer", ANALYZER_UNIT,
                                 kept_drop_ins=("a3-core.conf",))
# What the beat-analyzer's packaging/stage builds with (no JUCE): CMake and a
# compiler, curl for the pinned BTrack, JACK and libsamplerate.
ANALYZER_BUILD_PACKAGES = ("cmake", "g++", "pkg-config", "patch", "curl",
                           "libjack-jackd2-dev", "libsamplerate0-dev")

CORE_SOURCE = "a3-core"
# The unit whose shadowing is checked: the program's, a3-core's own.
CORE = apppackage.AppPackage("a3-core", "a3-engine.service")
# What a3-core's packaging/stage builds with: JUCE's build packages and the
# JACK development files.
CORE_BUILD_PACKAGES = tuple(dict.fromkeys(
    JUCE_PACKAGES + ("libjack-jackd2-dev",) + ANALYZER_BUILD_PACKAGES))

GROUP_LABELS = {
    "i3": "i3 config",
    "systemd": "systemd user units",
    "pipewire": "PipeWire: rate + block + AES67",
    "other": "other files",
}


def postinst_function(repo, *names):
    """Functions from the package's own postinst, to run them here rather
    than keep a second copy of what they decide."""
    text = (repo / POSTINST).read_text()
    bodies = []
    for name in names:
        if f"\n{name}() {{" not in text:
            raise RoleError(f"a3-core in this version does not know {name}(); it is "
                            "older than the installer. Raise the a3-core pin first.")
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
    """The setting ("all", "none", "i3, systemd") applied to what differs."""
    setting = setting.strip()
    if setting == "all":
        return list(differing)
    if setting in ("none", ""):
        return []
    wanted = {g.strip() for g in setting.split(",")}
    return [g for g in differing if g in wanted]


#: The public keys a3-core's postinst takes for a3-core/ssh-key, the same
#: pattern: no options in front, nothing but the key and a comment.
PUBLIC_KEY = re.compile(
    r"^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(256|384|521)|sk-ssh-ed25519@openssh\.com"
    r"|sk-ecdsa-sha2-nistp256@openssh\.com) AAAA[A-Za-z0-9+/]+={0,3}( .*)?$")


def read_ssh_key(path):
    """The one public key line in `path` (install --ssh-key), or a RoleError
    saying why not -- before anything is installed."""
    try:
        text = Path(path).read_text()
    except (OSError, UnicodeDecodeError) as error:
        raise RoleError(f"--ssh-key: {path} cannot be read ({error})")
    if "PRIVATE KEY" in text:
        raise RoleError(f"--ssh-key: {path} is a private key; "
                        "the public one (.pub) is meant")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RoleError(f"--ssh-key: {path} must have exactly one line with a "
                        f"public key, it has {len(lines)}")
    if not PUBLIC_KEY.match(lines[0]):
        raise RoleError(f"--ssh-key: {path} is not a public ssh key "
                        "(e.g. \"ssh-ed25519 AAAA... you@laptop\")")
    return lines[0]


def preseed_lines(settings, replace, ssh_key=None):
    """debconf-set-selections input: every question the postinst asks,
    answered and marked seen. a3-core/ssh-key only with a key; without one
    the question keeps whatever answer it has."""
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
            ("audio-port", "string", settings.get("core", "audio_port")),
            ("audio-address", "string", settings.get("core", "audio_address")),
        ]
    # The sign the postinst takes the network answers by, and clears; seen
    # is none, an older package left it set (a3-core#68).
    lines.append(("preseeded", "boolean", "true"))
    lines.append(("headless-display", "boolean", flag("headless")))
    if replace is not None:
        lines.append(("replace-config", "multiselect", ", ".join(replace)))
    if ssh_key:
        lines.append(("ssh-key", "string", ssh_key))

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
        return ("The truth (a3-osc.json) of this version names no Core address; "
                "whether this machine is the Core cannot be checked.")
    return (f"This machine does not have the truth's Core address ({truth_address}), "
            "and the Core's network answers do not set it. A second Core "
            "would announce itself on the same LAN (/core/here), and the desk could end up on "
            "the wrong one. The Core is not installed, the other roles are.")


def check_core(ctx, lookup=own_addresses):
    """The check before the Core installs, said out loud: None when it may,
    else the reason it is refused."""
    truth = truth_core_address(ctx.repo)
    own = lookup(ctx.runner)
    answered = answered_address(ctx.settings)
    ctx.runner.log(f"Core address of the truth: {truth or 'none'}; "
                   f"this machine: {', '.join(own) or 'none'}; "
                   f"from the network answers: {answered or 'none'}")
    return core_refusal(truth, own, answered)


class Core(Role):
    name = "core"
    label = "A³ Core (sound server: the a3-core program, beat analyzer)"
    submodules = ("a3-core", "beat-analyzer")
    platforms = ("debian",)
    # The Core's windows run on X; a headless Core uses the dummy screen.
    packages = SCREEN_PACKAGES + tuple(
        p for p in CORE_BUILD_PACKAGES if p not in SCREEN_PACKAGES)
    needs_screen = True

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        s.set_flag("core", "configure_network", ask.yesno(
            "Set up this Core's network?\n(No leaves the network as it is.)",
            s.flag("core", "configure_network")))
        if s.flag("core", "configure_network"):
            for key, question in (("interface", "Network interface (e.g. eno1)"),
                                  ("address", "Static address with prefix (e.g. 192.168.8.10/24)"),
                                  ("gateway", "Gateway"),
                                  ("dns", "DNS server"),
                                  ("audio_port", "Second socket for AES67 audio and PTP (empty: none)"),
                                  ("audio_address", "Address on the audio network (e.g. 192.168.9.10/24)")):
                s.set("core", key, ask.text(question, s.get("core", key)))
        s.set_flag("core", "headless", ask.yesno(
            "Run without a monitor (dummy screen, VNC only)?",
            s.flag("core", "headless")))

        differing = differing_groups(ctx.repo, ctx.home)
        if not differing:
            ctx.answers["replace"] = []
            return
        default = chosen_groups(s.get("core", "replace"), differing)
        if ask.interactive:
            picked = ask.checklist(
                "These parts of ~/.config differ from this version.\n"
                "Which should be replaced? (Backed up to ~/.config/a3-replaced/)",
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
        # Up front, before anything is built: what would stop either package.
        source, commit = ctx.repo / ANALYZER_SOURCE, analyzer_commit(ctx)
        core_source, core_pin = ctx.repo / CORE_SOURCE, core_commit(ctx)
        if not has_packaging(ctx, core_source, core_pin):
            raise RoleError(f"a3-core at {core_pin[:10]} has no packaging/stage: the "
                            "umbrella's a3-core pin is older than its package; "
                            "raise the a3-core pin first.")
        if not has_packaging(ctx, source, commit):
            raise RoleError(f"{ANALYZER_SOURCE} at {commit[:10]} has no packaging/stage: the "
                            f"umbrella's {ANALYZER_SOURCE} pin is older than its package; "
                            "raise it first.")
        apppackage.refuse_shadowing_leftovers(ctx, CORE)
        apppackage.refuse_shadowing_leftovers(ctx, ANALYZER)
        deb = apppackage.build(ctx, CORE, core_source, core_pin, ensure_juce(ctx))
        # The package of before: a3-core Conflicts with and Replaces it, but a
        # held package is not replaced unless it is unheld first.
        if leftover_engine_installed(ctx):
            run.run(["apt-mark", "unhold", "a3-engine"], root=True)
        run.run(["debconf-set-selections"], root=True,
                input=preseed_lines(ctx.settings, ctx.answers.get("replace"),
                                  ctx.answers.get("ssh_key")))
        run.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                 "--allow-downgrades", "--allow-change-held-packages", deb], root=True)
        run.run(["apt-mark", "hold", "a3-core"], root=True)
        # The postinst clears the marker, but apt runs no postinst when the
        # deb is the installed version: the marker then stayed, and the next
        # dpkg-reconfigure took these network answers unasked (a3-system#76).
        run.run(["debconf-set-selections"], root=True,
                input="a3-core a3-core/preseeded boolean false\n")
        # The program's unit is a3-main's to start (as the analyzer's), so it
        # is not enabled here; a running one moves over.
        systemctl_user(ctx, "daemon-reload")
        systemctl_user(ctx, "try-restart", CORE.unit)
        apppackage.check_packaged_unit_wins(ctx, CORE)
        self._analyzer(ctx, source, commit)

    def _analyzer(self, ctx, source, commit):
        """After a3-core, whose postinst moves its old checkout unit aside and
        writes the drop-in and the OSC targets. Not enabled: a3-main wants
        it; a running one is restarted onto the package."""
        deb = apppackage.build(ctx, ANALYZER, source, commit, juce_prefix(ctx))
        apppackage.install(ctx, ANALYZER, deb)
        systemctl_user(ctx, "daemon-reload")
        systemctl_user(ctx, "try-restart", ANALYZER_UNIT)
        apppackage.check_packaged_unit_wins(ctx, ANALYZER)

    stays = ("~/.config: i3, the unit files",
             "the backups in ~/.config/a3-replaced",
             "~/.ssh/authorized_keys (backed up and put back on removal)")

    def leaving_units(self, ctx):
        return list(CORE_UNITS) + [ANALYZER_UNIT, CORE.unit]

    def leaving_packages(self, ctx):
        return [CORE.package, ANALYZER.package]

    def leaving_lines(self, ctx):
        return super().leaving_lines(ctx) + [
            "  With the package go its files in ~/.local (bin, lib, share/a3-core)."]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        run = ctx.runner
        # a3-core before #66 shipped ~/.ssh/authorized_keys, so removing such
        # a package takes the file with it; a machine run over ssh would be
        # locked out. Newer packages leave it alone, and the copy is harmless.
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
        if analyzer_is_installed(ctx):
            apppackage.remove(ctx, ANALYZER)


def analyzer_commit(ctx):
    return apppackage.pinned_commit(ctx, ANALYZER_SOURCE)


def core_commit(ctx):
    return apppackage.pinned_commit(ctx, CORE_SOURCE)


def leftover_engine_installed(ctx):
    """The a3-engine package of before a3-core carried the program."""
    from ..leave import package_installed  # leave imports the roles
    return package_installed("a3-engine")


def analyzer_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(ANALYZER.package)
