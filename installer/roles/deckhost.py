# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""A StemDeck deck on a machine without the Core (a3nuc2 plays deck B beside
Motion, 2026-10-27). The deck's audio reaches the Core over AES67.

The stemdeck package comes the StemDeck role's way (stemdeck.install_package).
The package also ships the AES67 base instance (stemdeck-aes67.service: PTP
clock and receiver) and the deck's sender (a3-aes67-deck@<X>.service); this role
only pulls them in and tells them the host's audio socket (STEMDECK_AUDIO_PORT,
because the truth on this machine is the Core's copy). Then one deck instance, stemdeck@<letter>, enabled by a link in
default.target.wants -- the template has no [Install] section -- with a
drop-in naming the AES67 link map, the path latency and the panel's
workspace. With Motion on the machine, Motion gets its own workspace for the panel; the
two hand the panel over by workspace instead of fighting for it. Which of the two
runs is the maintainer's to start and stop by hand.

PTP: the deck's AES67 stream needs the Core's clock. ptp4l runs as a client
on the audio socket with the Core's config made a client's: linuxptp's stock
file with step_threshold 0.001 (as the Core's), clientOnly 1, priority1 128.
It is derived from this machine's stock file -- the rule a3-core's own copy
follows -- so the installer carries no copy of it, and a deck host needs no
a3-core checkout. The stock /etc/linuxptp/ptp4l.conf is only read. A port
whose driver offers no PTP receive filter, only "all" (a Raspberry Pi 5's
macb), gets hwts_filter full, or ptp4l sees no timestamp on any frame. A udev
rule lets the audio group read /dev/ptp*: PipeWire's PTP0 driver opens the
port's clock as the user and falls back to CLOCK_MONOTONIC when it cannot.

Not beside the Core (deck A is local there) and not beside the role
stemdeck: the two-deck player and a deck instance fight over JACK names and
the panel. The package enables the two-deck player globally; a user drop-in
on stemdeck.service (ExecCondition=/bin/false, as on a Core) keeps it from
starting.

a3-core's leftovers of an AES67 base on a machine that never had the package
(a3-aes67.service, its copy in a3-core's deployment tree, pipewire-aes67.conf
and its .conf.d) are disabled and moved aside, never deleted, because two PTP
drivers must not run (plan ruling P27). Leaving puts them back.

Two more leftovers of an earlier a3-core, handled only when the a3-core package
is not installed: a ~/.config/pipewire/jack.conf.d file that sets node.latency
or a quantum other than the graph's (a3nuc2: 256/44100 in a 128 graph forced
StemDeck to 256 and gave 4000+ xruns) is moved aside like the AES67 files, and
the system service set_irq_prio.service, which puts the touchscreen/panel USB
IRQ at FIFO 95, is disabled; leaving enables it again if this role disabled it.

The graph's rate and smallest block are the user's PipeWire server's: the
role links StemDeck's 10-stemdeck-rate.conf into ~/.config/pipewire/
pipewire.conf.d/ (ruling P32), because only the role knows the machine is a
deck host.
"""

import array
import fcntl
import re
import socket
import struct
import subprocess
from pathlib import Path

from .. import package as debs
from . import stemdeck
from .base import Role, RoleError, remove_files, systemctl_user, write_drop_in
from .motion import UNIT as MOTION_UNIT

LETTERS = "ABCD"
LINK_MAP = "/usr/share/stemdeck/links-aes67.json"
STEMDECK_WORKSPACE = "2:STEMDECK"
MOTION_WORKSPACE = "1:MOTION"
BASE_UNIT = "stemdeck-aes67.service"
SENDER_TEMPLATE = "a3-aes67-deck@.service"
LEFTOVER_UNIT = "a3-aes67.service"
LEFTOVER_PIPEWIRE = ("pipewire-aes67.conf", "pipewire-aes67.conf.d")
# a3-core's deployment copy of the unit, which stemdeck-aes67-deck's base-wanted checks too.
LEFTOVER_DEPLOYED_UNIT = Path(".local/share/a3-core/config/systemd/user") / LEFTOVER_UNIT
ASIDE = ".a3-system-aside"
JACK_CONF_D = Path(".config/pipewire/jack.conf.d")
IRQ_UNIT = "set_irq_prio.service"
GRAPH_QUANTUM = 128
_QUANTUM_SETTING = re.compile(
    r"(?:^|[\s{,])(?:node\.latency|node\.quantum|default\.clock\.(?:min-|max-)?quantum)"
    r"\s*=\s*\[?\s*(\d+)")
INSTANCE_TEMPLATE = Path("/usr/lib/systemd/user/stemdeck@.service")
DROP_IN = "deck-host.conf"
SHIPPED_RATE = Path("/usr/share/stemdeck/10-stemdeck-rate.conf")
RATE_LINK = Path(".config/pipewire/pipewire.conf.d") / SHIPPED_RATE.name
PANEL_DROP_IN = "panel-follows.conf"
# Written by an earlier run that had the "Motion here too" option; only cleaned up now.
MOTION_CONFLICT_DROP_IN = "deck-host.conf"
TWO_DECK_UNIT = stemdeck.UNIT
TWO_DECK_OFF = "ExecCondition=/bin/false"
WRITTEN_BY = "# Written by the a3-system installer (role deck-host); removed when it leaves.\n"

STOCK_PTP4L = Path("/etc/linuxptp/ptp4l.conf")
PTP4L_CONF = Path("/etc/linuxptp/a3-ptp4l.conf")
PTP4L_DROP_IN = Path("/etc/systemd/system/ptp4l@.service.d/a3.conf")
CLIENT_KEYS = {"clientOnly": "1", "priority1": "128", "step_threshold": "0.001"}
PTP_UDEV_RULE = Path("/etc/udev/rules.d/60-a3-ptp.rules")
UDEV_TRIGGER_PTP = ["udevadm", "trigger", "--action=change", "--subsystem-match=ptp"]

# linux/net_tstamp.h, enum hwtstamp_rx_filters, by bit; named as ethtool -T names them.
RX_FILTER_NAMES = ("none", "all", "some", "ptpv1-l4-event", "ptpv1-l4-sync",
                   "ptpv1-l4-delay-req", "ptpv2-l4-event", "ptpv2-l4-sync",
                   "ptpv2-l4-delay-req", "ptpv2-l2-event", "ptpv2-l2-sync",
                   "ptpv2-l2-delay-req", "ptpv2-event", "ptpv2-sync", "ptpv2-delay-req",
                   "ntp-all")
# What ptp4l's hwts_filter normal asks for, in the order it tries them.
PTP_EVENT_FILTERS = {"ptpv2-event", "ptpv2-l4-event", "ptpv2-l2-event"}
SIOCETHTOOL = 0x8946
ETHTOOL_GET_TS_INFO = 0x41
# struct ethtool_ts_info: cmd, so_timestamping, phc_index, tx_types, tx_reserved[3],
# rx_filters, rx_reserved[3].
TS_INFO = struct.Struct("IIiI3II3I")

# PipeWire's libjack before jackd's, as a3-core's package ships it: without it jack_wait and
# StemDeck load jackd's libjack and wait for a jack server that PipeWire does not run as one.
# Named by the machine's multiarch triplet, as pipewire-jack's own example file is: a3nuc2
# is x86_64-linux-gnu, a Raspberry Pi 5 aarch64-linux-gnu. ld.so.conf.d is read in name
# order and the first libjack wins, so the name starts with 00-: on aarch64
# aarch64-linux-gnu.conf sorts before pipewire-jack-aarch64-linux-gnu.conf and jackd's
# libjack won. (a3-core's own file keeps pipewire-jack-x86_64-linux-gnu.conf: x86_64
# sorts after "pipewire" there.)
JACK_LD_DIR = Path("/etc/ld.so.conf.d")
JACK_LD_OWN_MARK = "role deck-host"


def jack_ld_conf(multiarch):
    return JACK_LD_DIR / f"00-pipewire-jack-{multiarch}.conf"


def old_jack_ld_conf(multiarch):
    """The name this role wrote before it sorted first."""
    return JACK_LD_DIR / f"pipewire-jack-{multiarch}.conf"


def jack_ld_text(multiarch):
    return ("# PipeWire's libjack before jackd's: every JACK program on this deck host --\n"
            "# StemDeck, jack_wait, one started by hand -- talks to PipeWire.\n"
            "# Written by the a3-system installer (role deck-host); a3-core ships the same file.\n"
            f"/usr/lib/{multiarch}/pipewire-0.3/jack/\n")

I3_CONFIG = Path(".config/i3/config")
I3_BEGIN = "# >>> a3-system deck-host >>>"
I3_END = "# <<< a3-system deck-host <<<"
# Marks a line the role commented out, so leaving can give it back.
I3_DISABLED = "# [a3-system deck-host disabled] "
I3_STEMDECK = re.compile(r'class="StemDeck"')
I3_SET = re.compile(r'^\s*set\s+(\$\S+)\s+(.*?)\s*$')
I3_TITLE = re.compile(r'title="([^"]*)"')
# StemDeck's longest path latency (LaunchOptions.cpp): beyond it the instance exits 2 and stays down.
LONGEST_PATH_LATENCY_MS = 200.0
PATH_LATENCY = re.compile(r"\d+(\.\d+)?")


# -- settings -------------------------------------------------------------------

def deck_letter(settings):
    letter = settings.get("deck-host", "letter").strip().upper()
    if len(letter) != 1 or letter not in LETTERS:
        raise RoleError(f"[deck-host] letter = {letter!r}: a deck is one of "
                        f"{', '.join(LETTERS)}.")
    return letter


def path_latency_ms(settings):
    """The setting as written, once StemDeck would take it: 0..200 ms, decimals allowed."""
    value = settings.get("deck-host", "path_latency_ms").strip()
    if not PATH_LATENCY.fullmatch(value) or float(value) > LONGEST_PATH_LATENCY_MS:
        raise RoleError(f"[deck-host] path_latency_ms = {value!r}: milliseconds from 0 "
                        f"to {LONGEST_PATH_LATENCY_MS:g}, decimals allowed (StemDeck refuses "
                        "anything else and deck B stays down).")
    return value


def stemdeck_workspace(settings):
    """The i3 workspace StemDeck lives on, as written: a name or a bare number."""
    value = settings.get("deck-host", "stemdeck_workspace").strip()
    if not value or '"' in value or "\n" in value:
        raise RoleError(f"[deck-host] stemdeck_workspace = {value!r}: a workspace name "
                        "('2:STEMDECK') or a number ('1'), without quotes.")
    return value


def i3_workspace_ref(workspace):
    """How an assign names it: a bare number as it is, a name quoted."""
    return workspace if workspace.isdigit() else f'"{workspace}"'


def instance_unit(letter):
    return f"stemdeck@{letter}.service"


def deck_drop_in(latency_ms, workspace=STEMDECK_WORKSPACE):
    return (WRITTEN_BY
            + "[Unit]\n"
            f"Wants={BASE_UNIT}\n"
            f"After={BASE_UNIT}\n"
            "Wants=a3-aes67-deck@%i.service\n"
            "After=a3-aes67-deck@%i.service\n"
            "\n"
            "[Service]\n"
            f"Environment=STEMDECK_LINK_MAP={LINK_MAP}\n"
            f"Environment=STEMDECK_PATH_LATENCY_MS={latency_ms}\n"
            f"Environment=STEMDECK_PANEL_WORKSPACE={workspace}\n")


def audio_port_drop_in(port):
    return (WRITTEN_BY
            + "[Service]\n"
            f"Environment=STEMDECK_AUDIO_PORT={port}\n")


def two_deck_off_drop_in():
    return (WRITTEN_BY
            + "# The package enables the two-deck player globally; a deck host plays its\n"
            "# deck as stemdeck@. No Conflicts=: a conflict inside one transaction drops a\n"
            "# start job before any condition runs.\n"
            "[Service]\n"
            f"{TWO_DECK_OFF}\n")


def panel_drop_in(workspace=MOTION_WORKSPACE):
    return (WRITTEN_BY
            + "[Service]\n"
            f"Environment=A3_MOTION_PANEL_WORKSPACE={workspace}\n")


# -- PTP ------------------------------------------------------------------------

def _ptp4l_entry(line):
    """(key, value) of a setting line in a ptp4l config, else None."""
    stripped = line.strip()
    if not stripped or stripped.startswith(("#", ";", "[")):
        return None
    parts = stripped.split(None, 1)
    return parts[0], (parts[1].strip() if len(parts) > 1 else "")


def ptp4l_keys(text):
    return dict(entry for line in text.splitlines() if (entry := _ptp4l_entry(line)))


def rx_filter_names(bitmap):
    return {name for bit, name in enumerate(RX_FILTER_NAMES) if bitmap >> bit & 1}


def port_rx_filters(port):
    """The receive timestamp filters the port's driver offers (ethtool -T, without
    ethtool: Raspberry Pi OS has none), or None when the port cannot be asked."""
    request = array.array("B", TS_INFO.pack(ETHTOOL_GET_TS_INFO, *[0] * 10))
    ifreq = struct.pack("16sP", port.encode(), request.buffer_info()[0])
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            fcntl.ioctl(sock, SIOCETHTOOL, ifreq)
    except OSError:
        return None
    return rx_filter_names(TS_INFO.unpack(request.tobytes())[7])


def hwts_filter_for(rx_filters):
    """"full" for a port that stamps all frames but offers no PTP event filter (a
    Raspberry Pi 5's macb: with ptp4l's default it stamps no PTP frame at all),
    else None: ptp4l's default stays."""
    if rx_filters is None or "all" not in rx_filters or rx_filters & PTP_EVENT_FILTERS:
        return None
    return "full"


def _with_hwts_filter(text, hwts_filter):
    """The config with hwts_filter set: its own line if the stock file has one,
    else a new line right under [global]."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        entry = _ptp4l_entry(line)
        if entry and entry[0] == "hwts_filter":
            lines[i] = f"hwts_filter\t\t{hwts_filter}\n"
            return "".join(lines)
    at = next(i for i, line in enumerate(lines) if line.strip() == "[global]") + 1
    lines.insert(at, f"hwts_filter\t\t{hwts_filter}\n")
    return "".join(lines)


def client_ptp4l_config(stock, hwts_filter=None):
    """linuxptp's stock config with CLIENT_KEYS set (and hwts_filter, if given),
    every other line as it was."""
    missing = set(CLIENT_KEYS) - set(ptp4l_keys(stock))
    if missing:
        raise RoleError(f"{STOCK_PTP4L} has no {', '.join(sorted(missing))}; "
                        "the PTP client config cannot be made from it.")
    lines = []
    for line in stock.splitlines(keepends=True):
        entry = _ptp4l_entry(line)
        if entry and entry[0] in CLIENT_KEYS:
            key = entry[0]
            line = re.sub(r"(\S+)$", CLIENT_KEYS[key], line.rstrip("\n"), count=1) + "\n"
        lines.append(line)
    body = "".join(lines)
    if hwts_filter:
        body = _with_hwts_filter(body, hwts_filter)
    header = ("# SPDX-FileCopyrightText: linuxptp authors (stock ptp4l.conf, copied)\n"
              "# SPDX-FileCopyrightText: 2026 Raphael Eismann "
              "(step_threshold, clientOnly, priority1)\n"
              "# SPDX-License-Identifier: GPL-2.0-or-later\n"
              "#\n"
              "# ptp4l as a client of the Core, written by the a3-system installer\n"
              "# (role deck-host) from this machine's stock ptp4l.conf. step_threshold\n"
              "# 0.001: after a Core reboot the client steps instead of slewing for days.\n"
              "# Selected by ptp4l@.service.d/a3.conf; the stock file stays untouched.\n"
              + ("# hwts_filter full: this port's driver stamps all frames or none, and\n"
                 "# with ptp4l's default filter no PTP frame carries a timestamp.\n"
                 if hwts_filter else ""))
    return header + body


def ptp_udev_rule():
    return ("# Written by the a3-system installer (role deck-host).\n"
            "# PipeWire's PTP0 driver (clock.interface) reads the port's hardware clock as the\n"
            "# user; udev leaves /dev/ptp* root's own, and the driver then runs on\n"
            "# CLOCK_MONOTONIC instead of the clock ptp4l keeps on the Core's. Read only:\n"
            "# adjusting a PTP clock needs it open for writing.\n"
            'SUBSYSTEM=="ptp", GROUP="audio", MODE="0640"\n')


def ptp4l_drop_in():
    return ("# Written by the a3-system installer (role deck-host).\n"
            "[Service]\n"
            "ExecStart=\n"
            f"ExecStart=/usr/sbin/ptp4l -f {PTP4L_CONF} -i %I\n")


# -- i3 -------------------------------------------------------------------------

def i3_block(workspace=STEMDECK_WORKSPACE):
    return (f"{I3_BEGIN}\n"
            "# StemDeck's deck on this deck host, on its workspace; as a3-core's i3 config,\n"
            "# the main window tiles without a border and every other window (a dialog) floats.\n"
            f'assign [class="StemDeck"] number {i3_workspace_ref(workspace)}\n'
            'for_window [class="StemDeck" title="^StemDeck( [A-D])?$"] floating disable, border none\n'
            'for_window [class="StemDeck" title="^(?!StemDeck( [A-D])?$)"] floating enable\n'
            f"{I3_END}\n")


def without_i3_block(text):
    begin = text.find(I3_BEGIN + "\n")
    end = text.find(I3_END + "\n", begin)
    if begin < 0 or end < 0:
        return text
    return text[:begin] + text[end + len(I3_END) + 1:]


def own_stemdeck_rules(text):
    """The config's own StemDeck lines, outside the installer's block."""
    return [line for line in without_i3_block(text).splitlines()
            if I3_STEMDECK.search(line) and not line.strip().startswith("#")]


def has_own_stemdeck_rule(text):
    """Whether the config places StemDeck itself, outside the installer's block."""
    return bool(own_stemdeck_rules(text))


def i3_variables(text):
    variables = {}
    for line in text.splitlines():
        if match := I3_SET.match(line):
            variables[match.group(1)] = match.group(2).strip('"')
    return variables


def _workspace_of(rule, variables):
    """(workspace, by number) a rule puts its windows on, or None for a rule that places nothing."""
    if rule.lstrip().startswith("assign"):
        target = rule.split("]", 1)[1]
    elif "to workspace" in rule:
        target = rule.split("to workspace", 1)[1]
    else:
        return None
    words = target.replace("\u2192", " ").split()
    by_number = bool(words) and words[0] == "number"
    name = " ".join(words[1:] if by_number else words).strip('"')
    return variables.get(name, name).strip('"'), by_number


def _same_workspace(target, by_number, wanted):
    if by_number:
        return target.split(":", 1)[0] == wanted.split(":", 1)[0]
    return target == wanted


def rules_moving_deck_away(text, letter, workspace=STEMDECK_WORKSPACE):
    """(rule, workspace) for every own rule that puts "StemDeck <letter>" on a
    workspace other than the one its panel follows."""
    variables, window = i3_variables(text), f"StemDeck {letter}"
    found = []
    for rule in own_stemdeck_rules(text):
        title = I3_TITLE.search(rule)
        if title and not re.search(title.group(1), window):
            continue
        placed = _workspace_of(rule, variables)
        if placed and not _same_workspace(*placed, workspace):
            found.append((rule.strip(), placed[0]))
    return found


def missing_workspace_names(text, names):
    """The names no line of the config carries: i3 then names its workspaces otherwise."""
    lines = [line for line in text.splitlines() if not line.strip().startswith("#")]
    return [name for name in names if not any(name in line for line in lines)]


def neutralised_i3_rules(text, letter, workspace=STEMDECK_WORKSPACE):
    """(the config with the conflicting old StemDeck rules commented out, those
    rules). Conflicting: every for_window rule for the class (it would float or
    frame the deck against the block) and every rule putting this deck on a
    workspace its panel does not follow. An assign to the right workspace stays.
    The installer's block is left alone."""
    away = {rule for rule, _ in rules_moving_deck_away(text, letter, workspace)}
    lines, touched, in_block = [], [], False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        in_block = (in_block or stripped == I3_BEGIN) and stripped != I3_END
        if (not in_block and stripped != I3_END and I3_STEMDECK.search(line)
                and not stripped.startswith("#")
                and (stripped.startswith("for_window") or stripped in away)):
            touched.append(stripped)
            line = I3_DISABLED + line.lstrip()
        lines.append(line)
    return "".join(lines), touched


def restored_i3_rules(text):
    return "".join(line[len(I3_DISABLED):] if line.startswith(I3_DISABLED) else line
                   for line in text.splitlines(keepends=True))


def with_i3_block(text, force=False, workspace=STEMDECK_WORKSPACE):
    """The config with the block, or None when it has its own StemDeck rule
    (unless forced: the conflicting ones are out of the way then)."""
    if has_own_stemdeck_rule(text) and not force:
        return None
    if I3_BEGIN + "\n" in text:
        begin = text.index(I3_BEGIN + "\n")
        return text[:begin] + i3_block(workspace) + without_i3_block(text)[begin:]
    if text and not text.endswith("\n"):
        text += "\n"
    # No blank line before it: leaving takes out the block and gives the file back as it was.
    return text + i3_block(workspace)


def _write_home_file(ctx, path, text):
    ctx.runner.log(f"# {path}:\n" + "".join(f"#   {line}\n" for line in text.splitlines()))
    if not ctx.runner.dry_run:
        path.write_text(text)


# -- the role -------------------------------------------------------------------

class DeckHost(Role):
    name = "deck-host"
    label = "StemDeck deck on a machine without the Core (AES67 to the Core)"
    submodules = stemdeck.StemDeck.submodules
    platforms = stemdeck.StemDeck.platforms
    # ptp4l@ is linuxptp's unit.
    packages = stemdeck.StemDeck.packages + ("linuxptp",)
    build_packages = stemdeck.StemDeck.build_packages
    needs_screen = True

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        if not ask.interactive:
            return
        s.set("deck-host", "letter", ask.text(
            "Which deck does this machine play (B, C or D; A is the Core's)?",
            s.get("deck-host", "letter")))
        s.set("deck-host", "path_latency_ms", ask.text(
            "AES67 path latency to the Core in ms (0 until measured)",
            s.get("deck-host", "path_latency_ms")))
        s.set("deck-host", "audio_port", ask.text(
            "Socket on the audio network, for PTP (empty: no PTP)",
            s.get("deck-host", "audio_port")))
        s.set("deck-host", "stemdeck_workspace", ask.text(
            "On which i3 workspace does StemDeck live? (a name such as 2:STEMDECK, "
            "or a number such as 1)", s.get("deck-host", "stemdeck_workspace")))

    def install(self, ctx):
        _refuse_beside(ctx.settings.roles())
        letter, latency = deck_letter(ctx.settings), path_latency_ms(ctx.settings)
        workspace = stemdeck_workspace(ctx.settings)
        stemdeck.install_package(ctx)
        self._set_aside_leftovers(ctx)
        self._leave_old_letter(ctx, letter)
        write_drop_in(ctx, instance_unit(letter), DROP_IN,
                      deck_drop_in(latency, workspace))
        self._two_deck_player_off(ctx)
        self._audio_port_drop_ins(ctx)
        self._server_rate(ctx)
        self._panel(ctx)
        self._forget_motion_exclusion(ctx)
        self._i3_rule(ctx, letter, workspace)
        self._ptp_client(ctx)
        self._pipewire_jack_path(ctx)
        self._enable_instance(ctx, letter)

    def _leave_old_letter(self, ctx, letter):
        old = ctx.state.get("deck-host", "letter")
        if old and old != letter:
            ctx.runner.log(f"# [deck-host] letter {old} -> {letter}: deck {old}'s instance goes.")
            for unit in _letter_units(old):
                systemctl_user(ctx, "disable", "--now", unit, check=False)
            remove_files(ctx, _letter_files(ctx, old))
        ctx.state.set("deck-host", "letter", letter, dry_run=ctx.runner.dry_run)

    def _audio_port_drop_ins(self, ctx):
        port = _audio_port(ctx)
        for unit in (BASE_UNIT, SENDER_TEMPLATE):
            if port:
                write_drop_in(ctx, unit, DROP_IN, audio_port_drop_in(port))
            else:
                _drop_stale(ctx, _audio_port_path(ctx, unit))

    def _set_aside_leftovers(self, ctx):
        if core_package_installed():
            return
        run = ctx.runner
        self._irq_service_off(ctx)
        aes67 = _aes67_leftovers(ctx)
        if any(path.exists() for path in aes67):
            # Stopped before the move: a running unit would keep PTP0.
            systemctl_user(ctx, "disable", "--now", LEFTOVER_UNIT, check=False)
        for path in [*aes67, *_jack_conf_leftovers(ctx)]:
            aside = _aside(path)
            if not path.exists():
                continue
            if aside.exists():
                run.log(f"# {path} left where it is: {aside} is there already "
                        "(a3-core wrote it again?); compare the two by hand.")
                continue
            run.log(f"# {path} -> {aside}")
            if not run.dry_run:
                path.rename(aside)

    def _irq_service_off(self, ctx):
        if not system_unit_enabled(IRQ_UNIT):
            return
        ctx.runner.log(f"# {IRQ_UNIT} (from an a3-core package that is gone) is disabled: "
                       "it puts the USB IRQ of the touchscreen and panel at FIFO 95.")
        ctx.runner.run(["systemctl", "disable", IRQ_UNIT], root=True)
        ctx.state.set("deck-host", "irq_service_disabled", "yes", dry_run=ctx.runner.dry_run)

    def _irq_service_back(self, ctx):
        if not ctx.state.get("deck-host", "irq_service_disabled"):
            return
        ctx.runner.run(["systemctl", "enable", IRQ_UNIT], root=True)
        ctx.state.remove("deck-host", "irq_service_disabled", dry_run=ctx.runner.dry_run)

    def _put_leftovers_back(self, ctx):
        for path in [*_aes67_leftovers(ctx), *_asides_of_jack_confs(ctx)]:
            aside = _aside(path)
            if not aside.exists() or path.exists():
                continue
            ctx.runner.log(f"# {aside} -> {path}")
            if not ctx.runner.dry_run:
                aside.rename(path)

    def _server_rate(self, ctx):
        link = _rate_link(ctx)
        ctx.runner.log(f"# {link} -> {SHIPPED_RATE}")
        if ctx.runner.dry_run:
            return
        link.parent.mkdir(parents=True, exist_ok=True)
        link.unlink(missing_ok=True)
        link.symlink_to(SHIPPED_RATE)

    def _two_deck_player_off(self, ctx):
        write_drop_in(ctx, TWO_DECK_UNIT, DROP_IN, two_deck_off_drop_in())
        for hand in _hand_two_deck_off(ctx):
            ctx.runner.log(f"# {hand} does what {DROP_IN} does here; it can be removed "
                           "(left where it is).")
        systemctl_user(ctx, "daemon-reload")
        systemctl_user(ctx, "stop", TWO_DECK_UNIT, check=False)

    def _forget_motion_exclusion(self, ctx):
        """An earlier run with the "Motion here too" option: take its drop-in away."""
        if ctx.state.get("deck-host", "motion_here"):
            self._motion_back(ctx)

    def _motion_back(self, ctx):
        """Undo _motion_never_beside: the drop-in goes, Motion is enabled at boot again."""
        ctx.runner.log(f"# {MOTION_UNIT} enabled at boot again (an earlier deck-host run "
                       "kept it from running beside StemDeck).")
        remove_files(ctx, [_motion_conflict_path(ctx)])
        systemctl_user(ctx, "enable", MOTION_UNIT, check=False)
        ctx.state.remove("deck-host", "motion_here", dry_run=ctx.runner.dry_run)

    def _panel(self, ctx):
        if "motion" in ctx.settings.roles():
            write_drop_in(ctx, MOTION_UNIT, PANEL_DROP_IN, panel_drop_in())
            return
        stale = _panel_path(ctx)
        if stale.is_file():
            remove_files(ctx, [stale])

    def _i3_rule(self, ctx, letter, workspace):
        run, path = ctx.runner, ctx.home / I3_CONFIG
        if not path.is_file():
            # i3 then reads /etc/i3/config; a file of one rule would replace it.
            run.log(f"{path} is missing: no StemDeck rule written; i3's own "
                    "config places no deck.")
            return
        original = path.read_text()
        self._check_workspace_names(ctx, path, original, workspace)
        text, touched = neutralised_i3_rules(original, letter, workspace)
        for rule in touched:
            run.log(f"{path}: old StemDeck rule commented out (given back when the role "
                    f"leaves): {rule}")
        wanted = with_i3_block(text, force=bool(touched), workspace=workspace)
        if wanted is None:
            run.log(f"{path} places StemDeck itself; left as it is:\n"
                    + "".join(f"#   {rule}\n" for rule in own_stemdeck_rules(text)))
            return
        if wanted != original:
            _write_home_file(ctx, path, wanted)

    def _check_workspace_names(self, ctx, path, text, workspace):
        names = [workspace]
        if "motion" in ctx.settings.roles():
            names.append(MOTION_WORKSPACE)
        for name in missing_workspace_names(text, names):
            ctx.runner.log(f"WARNING: {path} names no workspace {name!r}: the panel follows "
                           "workspaces by that name and never moves to one named otherwise.")

    def _pipewire_jack_path(self, ctx):
        if core_package_installed():
            return
        run, multiarch = ctx.runner, debs.host_multiarch()
        conf, text = jack_ld_conf(multiarch), jack_ld_text(multiarch)
        old = _own_old_jack_conf(multiarch)
        if old:
            run.run(["rm", "-f", old], root=True)
        elif conf.is_file() and conf.read_text() == text:
            return
        run.run(["install", "-D", "-m", "644", "/dev/stdin", conf], root=True, input=text)
        run.run(["ldconfig"], root=True)

    def _ptp_client(self, ctx):
        run, port = ctx.runner, _audio_port(ctx)
        if not port:
            run.log("No audio port under [deck-host]: ptp4l not set up.")
            return
        ctx.state.set("deck-host", "audio_port", port, dry_run=run.dry_run)
        if not STOCK_PTP4L.is_file():
            if run.dry_run:
                run.log(f"# dry run: {STOCK_PTP4L} is missing (linuxptp not installed yet); "
                        "the PTP client config is skipped.")
                return
            raise RoleError(f"{STOCK_PTP4L} is missing: is linuxptp installed?")
        hwts_filter = hwts_filter_for(port_rx_filters(port))
        if hwts_filter:
            run.log(f"# {port} stamps all frames or none: ptp4l gets hwts_filter {hwts_filter}.")
        config = client_ptp4l_config(STOCK_PTP4L.read_text(), hwts_filter)
        for target, text in ((PTP4L_CONF, config), (PTP4L_DROP_IN, ptp4l_drop_in()),
                             (PTP_UDEV_RULE, ptp_udev_rule())):
            run.run(["install", "-D", "-m", "644", "/dev/stdin", target], root=True, input=text)
        run.run(["udevadm", "control", "--reload-rules"], root=True)
        run.run(UDEV_TRIGGER_PTP, root=True)
        run.run(["systemctl", "daemon-reload"], root=True)
        # Enabled, not started, as the Core's postinst does: it comes up with the next boot.
        run.run(["systemctl", "enable", f"ptp4l@{port}.service"], root=True)

    def _enable_instance(self, ctx, letter):
        link = _wants_link(ctx, letter)
        ctx.runner.log(f"# {link} -> {INSTANCE_TEMPLATE}")
        if not ctx.runner.dry_run:
            link.parent.mkdir(parents=True, exist_ok=True)
            link.unlink(missing_ok=True)
            link.symlink_to(INSTANCE_TEMPLATE)
        systemctl_user(ctx, "daemon-reload")
        systemctl_user(ctx, "restart", instance_unit(letter))

    # -- leaving

    stays = ("the stemdeck package (the StemDeck role removes it when it leaves)",
             "a3-core's AES67 files and jack.conf.d files moved aside, which are put back (see below)",
             "the stock /etc/linuxptp/ptp4l.conf",
             "library, sessions, recordings and stems")

    def leaving_units(self, ctx):
        return [unit for letter in _letters(ctx) for unit in _letter_units(letter)] + [BASE_UNIT]

    def _candidate_files(self, ctx):
        return [*(path for letter in _letters(ctx) for path in _letter_files(ctx, letter)),
                _panel_path(ctx),
                ctx.user_units / f"{TWO_DECK_UNIT}.d" / DROP_IN,
                *([_motion_conflict_path(ctx)] if _motion_excluded(ctx) else []),
                *(_audio_port_path(ctx, unit) for unit in (BASE_UNIT, SENDER_TEMPLATE)),
                _rate_link(ctx)]

    def leaving_files(self, ctx):
        return [path for path in self._candidate_files(ctx) if _written_by_us(path)]

    def leaving_kept(self, ctx):
        return [path for path in self._candidate_files(ctx) if not _written_by_us(path)
                and path.exists()]

    def leaving_lines(self, ctx):
        return super().leaving_lines(ctx) + [
            *([f"  Motion is enabled at boot again ({MOTION_UNIT}, not started now): an "
               "earlier run kept it from running beside StemDeck."]
              if _motion_excluded(ctx) else []),
            "  System files, deleted (as root):",
            *(f"    {path}" for path in (PTP4L_CONF, PTP4L_DROP_IN, PTP_UDEV_RULE)),
            f"  The deck-host block in ~/{I3_CONFIG}, removed; StemDeck rules it commented out come back.",
            f"  {jack_ld_conf(debs.host_multiarch())} (and the file of this name without "
            "00-, if the installer wrote it), deleted (as root) unless the a3-core "
            "package is installed.",
            "  a3-core's AES67 files moved aside, put back where they were:",
            *(f"    {path}" for path in _aes67_leftovers(ctx)),
            f"  Files in ~/{JACK_CONF_D} that set node.latency or a quantum other than the graph's "
            f"({GRAPH_QUANTUM}), moved aside the same way (*{ASIDE}), put back where they were.",
            f"  {IRQ_UNIT} (as root): enabled again if this role disabled it.",
            "    (put back only: a3-aes67.service is not re-enabled and there is no",
            "    systemctl --user daemon-reload for it; do both by hand if this",
            "    machine runs a3-core's AES67 again)"]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        run = ctx.runner
        if _motion_excluded(ctx):
            self._motion_back(ctx)
        # The port enabled at install, too: the setting may have been emptied since.
        ports = {_audio_port(ctx), ctx.state.get("deck-host", "audio_port")} - {""}
        for port in sorted(ports):
            run.run(["systemctl", "disable", f"ptp4l@{port}.service"], root=True, check=False)
        ctx.state.remove("deck-host", "audio_port", dry_run=run.dry_run)
        ctx.state.remove("deck-host", "letter", dry_run=run.dry_run)
        for path in (PTP4L_CONF, PTP4L_DROP_IN, PTP_UDEV_RULE):
            run.run(["rm", "-f", path], root=True)
        if PTP4L_DROP_IN.parent.is_dir():
            run.run(["rmdir", "--ignore-fail-on-non-empty", PTP4L_DROP_IN.parent], root=True)
        run.run(["udevadm", "control", "--reload-rules"], root=True)
        run.run(UDEV_TRIGGER_PTP, root=True)
        run.run(["systemctl", "daemon-reload"], root=True)
        if not core_package_installed():
            multiarch = debs.host_multiarch()
            run.run(["rm", "-f", jack_ld_conf(multiarch)], root=True)
            if old := _own_old_jack_conf(multiarch):
                run.run(["rm", "-f", old], root=True)
            run.run(["ldconfig"], root=True)
        path = ctx.home / I3_CONFIG
        if path.is_file():
            text = path.read_text()
            restored = restored_i3_rules(without_i3_block(text))
            if restored != text:
                _write_home_file(ctx, path, restored)
        self._put_leftovers_back(ctx)
        self._irq_service_back(ctx)


def _refuse_beside(roles):
    if "core" in roles:
        raise RoleError("deck-host is for a machine without the Core: "
                        "deck A is local there.")
    if "stemdeck" in roles:
        raise RoleError("deck-host and the role stemdeck exclude each other: the two-deck "
                        "player and a deck instance would fight over JACK names and the panel.")


def _written_by_us(path):
    """A link, or a file that carries the installer's mark; a file of the
    role's name that someone else wrote is not ours to delete."""
    if path.is_symlink() or not path.exists():
        return True
    return path.is_file() and WRITTEN_BY in path.read_text(errors="replace")


def _letters(ctx):
    """The configured letter and the one installed last, if it differs."""
    recorded = ctx.state.get("deck-host", "letter")
    return list(dict.fromkeys([deck_letter(ctx.settings)] + ([recorded] if recorded else [])))


def _letter_units(letter):
    return [instance_unit(letter), f"a3-aes67-deck@{letter}.service"]


def _letter_files(ctx, letter):
    return [ctx.user_units / f"{instance_unit(letter)}.d" / DROP_IN, _wants_link(ctx, letter)]


def _rate_link(ctx):
    return ctx.home / RATE_LINK


def _audio_port(ctx):
    return ctx.settings.get("deck-host", "audio_port").strip()


def _wants_link(ctx, letter):
    return ctx.user_units / "default.target.wants" / instance_unit(letter)


def _motion_conflict_path(ctx):
    return ctx.user_units / f"{MOTION_UNIT}.d" / MOTION_CONFLICT_DROP_IN


def _motion_excluded(ctx):
    """Whether an earlier run kept Motion from running beside StemDeck."""
    return bool(ctx.state.get("deck-host", "motion_here"))


def _own_old_jack_conf(multiarch):
    """The pre-00- file, if this role wrote it (a3-core's file of that name is its own)."""
    old = old_jack_ld_conf(multiarch)
    if old.is_file() and JACK_LD_OWN_MARK in old.read_text():
        return old
    return None


def _hand_two_deck_off(ctx):
    """Drop-ins on the two-deck player, not the role's, that switch it off the same way."""
    folder = ctx.user_units / f"{TWO_DECK_UNIT}.d"
    if not folder.is_dir():
        return []
    return [path for path in sorted(folder.glob("*.conf"))
            if path.name != DROP_IN and TWO_DECK_OFF in path.read_text().splitlines()]


def _panel_path(ctx):
    return ctx.user_units / f"{MOTION_UNIT}.d" / PANEL_DROP_IN


def core_package_installed():
    from ..leave import package_installed  # leave imports the roles
    return package_installed("a3-core")


def _audio_port_path(ctx, unit):
    return ctx.user_units / f"{unit}.d" / DROP_IN


def _drop_stale(ctx, path):
    if not path.is_file():
        return
    ctx.runner.log(f"# {path} removed: no audio port under [deck-host].")
    if ctx.runner.dry_run:
        return
    path.unlink()
    try:
        path.parent.rmdir()
    except OSError:
        pass  # drop-ins written by hand stay


def system_unit_enabled(unit):
    done = subprocess.run(["systemctl", "is-enabled", unit], capture_output=True, text=True)
    return done.returncode == 0 and done.stdout.strip() == "enabled"


def graph_quantum():
    """The smallest block the deck host's graph runs, from the file the role links."""
    try:
        text = SHIPPED_RATE.read_text()
    except OSError:
        return GRAPH_QUANTUM
    found = re.search(r"default\.clock\.quantum\s*=\s*(\d+)", text)
    return int(found.group(1)) if found else GRAPH_QUANTUM


def sets_other_quantum(text, quantum):
    """Whether a pipewire conf sets node.latency or a quantum other than `quantum`."""
    return any((m := _QUANTUM_SETTING.search(line)) and int(m.group(1)) != quantum
               for line in text.splitlines() if not line.lstrip().startswith(("#", ";")))


def _jack_conf_leftovers(ctx):
    folder = ctx.home / JACK_CONF_D
    if not folder.is_dir():
        return []
    quantum = graph_quantum()
    return [path for path in sorted(folder.glob("*.conf"))
            if path.is_file() and sets_other_quantum(path.read_text(errors="replace"), quantum)]


def _asides_of_jack_confs(ctx):
    folder = ctx.home / JACK_CONF_D
    if not folder.is_dir():
        return []
    return [path.with_name(path.name.removesuffix(ASIDE))
            for path in sorted(folder.glob(f"*.conf{ASIDE}"))]


def _aes67_leftovers(ctx):
    return [ctx.user_units / LEFTOVER_UNIT,
            ctx.home / LEFTOVER_DEPLOYED_UNIT,
            *(ctx.home / ".config" / "pipewire" / name for name in LEFTOVER_PIPEWIRE)]


def _aside(path):
    return path.with_name(path.name + ASIDE)
