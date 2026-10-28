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
workspace. With Motion on the machine, Motion gets the panel's workspace as
well, so the two hand the panel over by workspace instead of fighting for it.

PTP: the deck's AES67 stream needs the Core's clock. ptp4l runs as a client
on the audio socket with the Core's config made a client's: linuxptp's stock
file with step_threshold 0.001 (as the Core's), clientOnly 1, priority1 128.
It is derived from this machine's stock file -- the rule a3-core's own copy
follows -- so the installer carries no copy of it, and a deck host needs no
a3-core checkout. The stock /etc/linuxptp/ptp4l.conf is only read.

Not beside the Core (deck A is local there) and not beside the role
stemdeck: the two-deck player and a deck instance fight over JACK names and
the panel.

a3-core's leftovers of an AES67 base on a machine that never had the package
(a3-aes67.service, its copy in a3-core's deployment tree, pipewire-aes67.conf
and its .conf.d) are disabled and moved aside, never deleted, because two PTP
drivers must not run (plan ruling P27). Leaving puts them back.

The graph's rate and smallest block are the user's PipeWire server's: the
role links StemDeck's 10-stemdeck-rate.conf into ~/.config/pipewire/
pipewire.conf.d/ (ruling P32), because only the role knows the machine is a
deck host.
"""

import re
from pathlib import Path

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
INSTANCE_TEMPLATE = Path("/usr/lib/systemd/user/stemdeck@.service")
DROP_IN = "deck-host.conf"
SHIPPED_RATE = Path("/usr/share/stemdeck/10-stemdeck-rate.conf")
RATE_LINK = Path(".config/pipewire/pipewire.conf.d") / SHIPPED_RATE.name
PANEL_DROP_IN = "panel-follows.conf"
WRITTEN_BY = "# Written by the a3-system installer (role deck-host); removed when it leaves.\n"

STOCK_PTP4L = Path("/etc/linuxptp/ptp4l.conf")
PTP4L_CONF = Path("/etc/linuxptp/a3-ptp4l.conf")
PTP4L_DROP_IN = Path("/etc/systemd/system/ptp4l@.service.d/a3.conf")
CLIENT_KEYS = {"clientOnly": "1", "priority1": "128", "step_threshold": "0.001"}

I3_CONFIG = Path(".config/i3/config")
I3_BEGIN = "# >>> a3-system deck-host >>>"
I3_END = "# <<< a3-system deck-host <<<"
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


def instance_unit(letter):
    return f"stemdeck@{letter}.service"


def deck_drop_in(latency_ms):
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
            f"Environment=STEMDECK_PANEL_WORKSPACE={STEMDECK_WORKSPACE}\n")


def audio_port_drop_in(port):
    return (WRITTEN_BY
            + "[Service]\n"
            f"Environment=STEMDECK_AUDIO_PORT={port}\n")


def panel_drop_in():
    return (WRITTEN_BY
            + "[Service]\n"
            f"Environment=A3_MOTION_PANEL_WORKSPACE={MOTION_WORKSPACE}\n")


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


def client_ptp4l_config(stock):
    """linuxptp's stock config with CLIENT_KEYS set, every other line as it was."""
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
    header = ("# SPDX-FileCopyrightText: linuxptp authors (stock ptp4l.conf, copied)\n"
              "# SPDX-FileCopyrightText: 2026 Raphael Eismann "
              "(step_threshold, clientOnly, priority1)\n"
              "# SPDX-License-Identifier: GPL-2.0-or-later\n"
              "#\n"
              "# ptp4l as a client of the Core, written by the a3-system installer\n"
              "# (role deck-host) from this machine's stock ptp4l.conf. step_threshold\n"
              "# 0.001: after a Core reboot the client steps instead of slewing for days.\n"
              "# Selected by ptp4l@.service.d/a3.conf; the stock file stays untouched.\n")
    return header + "".join(lines)


def ptp4l_drop_in():
    return ("# Written by the a3-system installer (role deck-host).\n"
            "[Service]\n"
            "ExecStart=\n"
            f"ExecStart=/usr/sbin/ptp4l -f {PTP4L_CONF} -i %I\n")


# -- i3 -------------------------------------------------------------------------

def i3_block():
    return (f"{I3_BEGIN}\n"
            "# StemDeck's deck on this deck host, on its workspace; as a3-core's i3 config,\n"
            "# the main window tiles without a border and every other window (a dialog) floats.\n"
            f'assign [class="StemDeck"] number "{STEMDECK_WORKSPACE}"\n'
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


def rules_moving_deck_away(text, letter):
    """(rule, workspace) for every own rule that puts "StemDeck <letter>" on a
    workspace other than the one its panel follows."""
    variables, window = i3_variables(text), f"StemDeck {letter}"
    found = []
    for rule in own_stemdeck_rules(text):
        title = I3_TITLE.search(rule)
        if title and not re.search(title.group(1), window):
            continue
        placed = _workspace_of(rule, variables)
        if placed and not _same_workspace(*placed, STEMDECK_WORKSPACE):
            found.append((rule.strip(), placed[0]))
    return found


def missing_workspace_names(text, names):
    """The names no line of the config carries: i3 then names its workspaces otherwise."""
    lines = [line for line in text.splitlines() if not line.strip().startswith("#")]
    return [name for name in names if not any(name in line for line in lines)]


def with_i3_block(text):
    """The config with the block, or None when it has its own StemDeck rule."""
    if has_own_stemdeck_rule(text):
        return None
    if I3_BEGIN + "\n" in text:
        begin = text.index(I3_BEGIN + "\n")
        return text[:begin] + i3_block() + without_i3_block(text)[begin:]
    if text and not text.endswith("\n"):
        text += "\n"
    # No blank line before it: leaving takes out the block and gives the file back as it was.
    return text + i3_block()


def _write_home_file(ctx, path, text):
    ctx.runner.log(f"# {path}:\n" + "".join(f"#   {line}\n" for line in text.splitlines()))
    if not ctx.runner.dry_run:
        path.write_text(text)


# -- the role -------------------------------------------------------------------

class DeckHost(Role):
    name = "deck-host"
    label = "StemDeck deck on a machine without the Core (AES67 to the Core)"
    submodules = stemdeck.StemDeck.submodules
    platforms = ("debian",)
    # ptp4l@ is linuxptp's unit.
    packages = stemdeck.StemDeck.packages + ("linuxptp",)
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

    def install(self, ctx):
        _refuse_beside(ctx.settings.roles())
        letter, latency = deck_letter(ctx.settings), path_latency_ms(ctx.settings)
        stemdeck.install_package(ctx)
        self._set_aside_leftovers(ctx)
        self._leave_old_letter(ctx, letter)
        write_drop_in(ctx, instance_unit(letter), DROP_IN, deck_drop_in(latency))
        self._audio_port_drop_ins(ctx)
        self._server_rate(ctx)
        self._panel(ctx)
        self._i3_rule(ctx, letter)
        self._ptp_client(ctx)
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
        leftovers = _leftovers(ctx)
        if not any(path.exists() for path in leftovers):
            return
        # Stopped before the move: a running unit would keep PTP0.
        systemctl_user(ctx, "disable", "--now", LEFTOVER_UNIT, check=False)
        for path in leftovers:
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

    def _put_leftovers_back(self, ctx):
        for path in _leftovers(ctx):
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

    def _panel(self, ctx):
        if "motion" in ctx.settings.roles():
            write_drop_in(ctx, MOTION_UNIT, PANEL_DROP_IN, panel_drop_in())
            return
        stale = _panel_path(ctx)
        if stale.is_file():
            remove_files(ctx, [stale])

    def _i3_rule(self, ctx, letter):
        run, path = ctx.runner, ctx.home / I3_CONFIG
        if not path.is_file():
            # i3 then reads /etc/i3/config; a file of one rule would replace it.
            run.log(f"{path} is missing: no StemDeck rule written; i3's own "
                    "config places no deck.")
            return
        text = path.read_text()
        self._check_workspace_names(ctx, path, text)
        wanted = with_i3_block(text)
        if wanted is None:
            run.log(f"{path} places StemDeck itself; left as it is:\n"
                    + "".join(f"#   {rule}\n" for rule in own_stemdeck_rules(text)))
            for rule, workspace in rules_moving_deck_away(text, letter):
                run.log(f"WARNING: {path}: {rule!r} puts StemDeck {letter} on workspace "
                        f"{workspace!r}, but its panel follows {STEMDECK_WORKSPACE}: the panel "
                        "never reaches the deck. Change or remove that rule.")
            return
        if wanted != text:
            _write_home_file(ctx, path, wanted)

    def _check_workspace_names(self, ctx, path, text):
        names = [STEMDECK_WORKSPACE] + ([MOTION_WORKSPACE] if "motion" in ctx.settings.roles() else [])
        for name in missing_workspace_names(text, names):
            ctx.runner.log(f"WARNING: {path} names no workspace {name!r}: the panel follows "
                           "workspaces by that name and never moves to one named otherwise.")

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
        for target, text in ((PTP4L_CONF, client_ptp4l_config(STOCK_PTP4L.read_text())),
                             (PTP4L_DROP_IN, ptp4l_drop_in())):
            run.run(["install", "-D", "-m", "644", "/dev/stdin", target], root=True, input=text)
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
             "a3-core's AES67 files moved aside, which are put back (see below)",
             "the stock /etc/linuxptp/ptp4l.conf",
             "library, sessions, recordings and stems")

    def leaving_units(self, ctx):
        return [unit for letter in _letters(ctx) for unit in _letter_units(letter)] + [BASE_UNIT]

    def leaving_files(self, ctx):
        return [*(path for letter in _letters(ctx) for path in _letter_files(ctx, letter)),
                _panel_path(ctx),
                *(_audio_port_path(ctx, unit) for unit in (BASE_UNIT, SENDER_TEMPLATE)),
                _rate_link(ctx)]

    def leaving_lines(self, ctx):
        return super().leaving_lines(ctx) + [
            "  System files, deleted (as root):",
            *(f"    {path}" for path in (PTP4L_CONF, PTP4L_DROP_IN)),
            f"  The deck-host block in ~/{I3_CONFIG}, removed.",
            "  a3-core's AES67 files moved aside, put back where they were:",
            *(f"    {path}" for path in _leftovers(ctx)),
            "    (put back only: a3-aes67.service is not re-enabled and there is no",
            "    systemctl --user daemon-reload for it; do both by hand if this",
            "    machine runs a3-core's AES67 again)"]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        run = ctx.runner
        # The port enabled at install, too: the setting may have been emptied since.
        ports = {_audio_port(ctx), ctx.state.get("deck-host", "audio_port")} - {""}
        for port in sorted(ports):
            run.run(["systemctl", "disable", f"ptp4l@{port}.service"], root=True, check=False)
        ctx.state.remove("deck-host", "audio_port", dry_run=run.dry_run)
        ctx.state.remove("deck-host", "letter", dry_run=run.dry_run)
        for path in (PTP4L_CONF, PTP4L_DROP_IN):
            run.run(["rm", "-f", path], root=True)
        run.run(["rmdir", "--ignore-fail-on-non-empty", PTP4L_DROP_IN.parent], root=True)
        run.run(["systemctl", "daemon-reload"], root=True)
        path = ctx.home / I3_CONFIG
        if path.is_file():
            text = path.read_text()
            if without_i3_block(text) != text:
                _write_home_file(ctx, path, without_i3_block(text))
        self._put_leftovers_back(ctx)


def _refuse_beside(roles):
    if "core" in roles:
        raise RoleError("deck-host is for a machine without the Core: "
                        "deck A is local there.")
    if "stemdeck" in roles:
        raise RoleError("deck-host and the role stemdeck exclude each other: the two-deck "
                        "player and a deck instance would fight over JACK names and the panel.")


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


def _leftovers(ctx):
    return [ctx.user_units / LEFTOVER_UNIT,
            ctx.home / LEFTOVER_DEPLOYED_UNIT,
            *(ctx.home / ".config" / "pipewire" / name for name in LEFTOVER_PIPEWIRE)]


def _aside(path):
    return path.with_name(path.name + ASIDE)
