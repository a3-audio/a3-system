# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""A whole A³ rig on one machine: the Core program and its engine, the
StemDeck decks, the desk, Motion UI and the beat-analyzer, for a laptop
(A³ Canvas step 2, 2026-10-28). Debian testing, i3 on Xorg, PipeWire.

Packages only (plan ruling R10): the five apps come by name from the archive
in one a3-root call, so apt sees them together. Not the package a3-core: that
is the rig's deployment (network, autologin, the rig's units) and has no
place on a laptop. Nothing names the user or a checkout, so the role runs as
whoever starts the installer, from wherever (cli.place_problems). The laptop
has its own session: no autologin on tty1.

Everything is local: no PTP, no AES67. The number of decks comes from the
truth the a3-core-app package ships, read once the apps are installed (R11).
The output is a PipeWire sink, asked from pw-dump; empty is PipeWire's
default sink, which WirePlumber also falls back to when a chosen USB card is
unplugged (R4).

It excludes every other role (cli.refused_together): they are this
machine's parts already.
"""

import copy
import hashlib
import json
import subprocess
from pathlib import Path

from ..archive import a3_root_command
from ..system import CommandFailed
from . import apppackage, desk, motion, stemdeck
from ..settings import DEFAULTS
from .base import (RATE_LINK, Role, RoleError, link_server_rate, systemctl_user,
                   two_deck_off_drop_in, write_drop_in, write_home_file)
from .core import ANALYZER, CORE_APP

SECTION = "laptop"
APP_PACKAGES = (CORE_APP, stemdeck.APP, desk.APP, motion.APP, ANALYZER)
APPS = tuple(app.package for app in APP_PACKAGES)
# The truth a3-core-app ships; the deck count's range is read from it.
TRUTH = Path("/usr/share/a3/a3-osc.json")
TRUTH_DECK_ADDRESS = "stemdeck.deck-hello"
# The loopback the laptop's wiring plays into; never an output choice. Its
# node.name and node.description both: pipewire-jack names a JACK client
# after node.description, and the engine links to "<this>:playback_FL".
OWN_LOOPBACK = "a3-laptop-out"
LOOPBACK_PLAYBACK_DESCRIPTION = f"{OWN_LOOPBACK} to the interface"
DEFAULT_OUTPUT = ("", "default (the internal card)")
SINK_CLASS = "Audio/Sink"
NODE_TYPE = "PipeWire:Interface:Node"
# The engine config a3-core-app ships, which the laptop's is made from.
ENGINE_CONFIG = Path("/usr/share/a3-engine/engine.json")
# Its keys the engine reads as paths, a relative one against the config
# file's own folder (a3-core app/ConfigFile.cpp): in the laptop's copy, under
# ~/.config, they would point into the home.
ENGINE_PATH_KEYS = ("spatial",)

# What the wiring writes, under the user's home. The one truth of the laptop
# (R8): ~/.config/a3/network.json is the rig's and never written here.
LAPTOP_TRUTH = Path(".config/a3/laptop/a3-osc.json")
ENGINE_JSON = Path(".config/a3/engine/engine.json")
LOOPBACK_CONF = Path(".config/pipewire/pipewire.conf.d/60-a3-laptop-out.conf")
ANALYZER_ENV = Path(".config/beat-analyzer/conf.d/60-a3-laptop.env")
WRITTEN_BY = "# Written by the a3-system installer (role laptop); rewritten on every run.\n"
LOCAL_HOST = "127.0.0.1"
CORE_OSC_LISTENER = "core.osc"
ANALYZER_INPUT = "beat-analyzer:bpm_1"
# [state] laptop engine_json: the sha256 of the engine.json the installer
# wrote last; a file that differs from it is the user's (Review Focus 4).
ENGINE_JSON_STATE = "engine_json"
ENGINE_JSON_LEFT = ("engine.json was changed by hand: the laptop's output links "
                    "are left as they are")
ENGINE_JSON_FOREIGN = ("engine.json exists and was not written by this installer: the "
                       "laptop's output links are left as they are")
PHONES_IGNORED = "phones need an output device; ignored"
DEFAULT_MAIN = DEFAULTS[SECTION]["output_main"]


# -- the decks ----------------------------------------------------------------

def deck_letters(count):
    """The engine's deck names: A ... Z, then AA, AB, ... (as spreadsheet
    columns)."""
    return [_deck_letter(number) for number in range(1, count + 1)]


def _deck_letter(number):
    letters = ""
    while number:
        number, rest = divmod(number - 1, 26)
        letters = chr(ord("A") + rest) + letters
    return letters


def truth_deck_count(truth):
    """The highest deck the truth's deck hello allows."""
    return int(truth["addresses"][TRUTH_DECK_ADDRESS]["deck"][1])


def wanted_decks(settings):
    """[laptop] decks as a number, or None when empty (the truth's range)."""
    value = settings.get(SECTION, "decks").strip()
    if not value:
        return None
    # ASCII decimals only: isdigit takes "²", which int() refuses.
    if not (value.isascii() and value.isdecimal()) or int(value) < 1:
        raise RoleError(f"[laptop] decks = {value!r}: a whole number from 1, "
                        "or empty for as many as the system knows.")
    return int(value)


def deck_count(settings, truth):
    """How many decks the laptop plays (R11)."""
    highest = truth_deck_count(truth)
    wanted = wanted_decks(settings)
    if wanted is None:
        return highest
    if wanted > highest:
        raise RoleError(f"[laptop] decks = {wanted}, but this system knows {highest} decks "
                        f"at most ({TRUTH}); set {highest} or fewer.")
    return wanted


def read_truth(ctx):
    try:
        return json.loads(TRUTH.read_text())
    except (OSError, ValueError) as error:
        raise RoleError(f"{TRUTH} is not readable ({error}): the a3-core-app package "
                        "should have installed it.")


# -- the output device ----------------------------------------------------------

def _sink_props(entry):
    if not isinstance(entry, dict) or entry.get("type") != NODE_TYPE:
        return None
    props = (entry.get("info") or {}).get("props") or {}
    if props.get("media.class") != SINK_CLASS or not props.get("node.name"):
        return None
    return props


def output_device_choices(dump):
    """(value, label) for the output question from pw-dump's objects: the
    default first, then every sink but the laptop's own loopback."""
    choices = [DEFAULT_OUTPUT]
    for entry in dump:
        props = _sink_props(entry)
        if props is None or props["node.name"] == OWN_LOOPBACK:
            continue
        name = props["node.name"]
        label = props.get("node.description") or props.get("node.nick") or name
        choices.append((name, label))
    return choices


def pipewire_objects(ctx):
    """pw-dump's objects, or [] (and one log line) when it is missing or fails."""
    try:
        return json.loads(ctx.runner.output(["pw-dump"]))
    except (OSError, ValueError, subprocess.CalledProcessError, CommandFailed) as error:
        ctx.runner.log(f"pw-dump gave no sinks ({error}): only the default output is offered.")
        return []


# -- the local wiring ---------------------------------------------------------------

def laptop_truth(shipped):
    """The shipped truth with the Core and the mixer on this machine."""
    truth = copy.deepcopy(shipped)
    truth["hosts"]["core"] = LOCAL_HOST
    truth["hosts"]["mixer"] = LOCAL_HOST
    return truth


def _loopback_port(position):
    return f"{OWN_LOOPBACK}:playback_{position}"


def anchored_paths(config, folder):
    """Each of ENGINE_PATH_KEYS that is relative, made absolute against
    `folder`, the shipped file's; an absolute one stays."""
    for key in ENGINE_PATH_KEYS:
        value = config.get(key)
        if isinstance(value, str) and value and not Path(value).is_absolute():
            config[key] = str(Path(folder) / value)


def laptop_engine_config(shipped, decks, phones):
    """The shipped engine config with the laptop's links only: rec, the
    binaural main (R3), to the loopback and the analyzer; phones to its rear
    pair. No analog, no main or booth: a laptop has no rig behind it. The
    decks link themselves (unnamed slots are local StemDecks). Its paths
    point where the shipped file's did (ENGINE_CONFIG's folder)."""
    config = copy.deepcopy(shipped)
    anchored_paths(config, ENGINE_CONFIG.parent)
    if decks is None:
        config["engine"].pop("decks", None)   # as many as the truth knows
    else:
        config["engine"]["decks"] = decks
    links = {"rec_L": [_loopback_port("FL"), ANALYZER_INPUT],
             "rec_R": [_loopback_port("FR")]}
    if phones:
        links["phones_L"] = [_loopback_port("RL")]
        links["phones_R"] = [_loopback_port("RR")]
    config["io"]["jack"] = links
    return config


def output_channels(value):
    """"1,2" as (1, 2): two channels of the device, counted from one."""
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 2 or not all(p.isascii() and p.isdecimal() and int(p) >= 1
                                  for p in parts):
        raise RoleError(f"Output channels {value!r}: two channel numbers from 1, "
                        "like 1,2.")
    return int(parts[0]), int(parts[1])


def _positions(names):
    return "[ " + " ".join(names) + " ]"


def loopback_conf(device, main, phones):
    """The PipeWire sink a3-laptop-out the engine plays into. Its playback
    side follows `device` and, unlike a pinned stream, falls back to the
    default sink while the device is gone and returns to it when it is back:
    the fallback is PipeWire's job (R4). No device: the default sink."""
    capture = ["FL", "FR"] + (["RL", "RR"] if phones else [])
    playback = [f'node.description = "{LOOPBACK_PLAYBACK_DESCRIPTION}"']
    if device:
        # Remixing stays on (no stream.dont-remix, P29): when the device is
        # gone, the AUX channels are paired by index onto the fallback's
        # FL/FR and the sound goes on. Channels other than 1,2 need the
        # measurement in the laptop checklist.
        channels = list(main) + (list(phones) if phones else [])
        positions = [f"AUX{channel - 1}" for channel in channels]
        playback += [f'target.object = "{device}"',
                     f"audio.position = {_positions(positions)}"]
    # dont-fallback = false is WirePlumber's default; written out because the
    # fallback to the internal card is the point of this sink (R4).
    playback += ["node.dont-fallback = false", "node.passive = false"]
    return (WRITTEN_BY
            + "context.modules = [\n"
            "{   name = libpipewire-module-loopback\n"
            "    args = {\n"
            "        capture.props = {\n"
            f'            node.name = "{OWN_LOOPBACK}"\n'
            f'            node.description = "{OWN_LOOPBACK}"\n'
            f'            media.class = "{SINK_CLASS}"\n'
            f"            audio.position = {_positions(capture)}\n"
            "        }\n"
            "        playback.props = {\n"
            f'            node.name = "playback.{OWN_LOOPBACK}"\n'
            + "".join(f"            {line}\n" for line in playback)
            + "        }\n"
            "    }\n"
            "}\n"
            "]\n")


def analyzer_env(truth):
    """The beat-analyzer's /beat to the Core on this machine."""
    listener = next((entry for entry in truth.get("listeners", [])
                     if entry.get("name") == CORE_OSC_LISTENER), None)
    if listener is None:
        raise RoleError(f"The truth {TRUTH} has no listener {CORE_OSC_LISTENER}: the "
                        "beat-analyzer would not know the Core's port.")
    return WRITTEN_BY + f"OSC_HOST_core={LOCAL_HOST}:{listener['port']}\n"


def wiring_files(home):
    """Every file the wiring writes and owns, for leaving. Not engine.json:
    that one is owned only while it is as written (ENGINE_JSON_STATE)."""
    home = Path(home)
    return [home / LAPTOP_TRUTH, home / LOOPBACK_CONF, home / ANALYZER_ENV,
            home / RATE_LINK]


def read_shipped_engine():
    try:
        return json.loads(ENGINE_CONFIG.read_text())
    except (OSError, ValueError) as error:
        raise RoleError(f"{ENGINE_CONFIG} is not readable ({error}): the a3-core-app "
                        "package should have installed it.")


def _sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write_engine_config(ctx, text):
    """engine.json, unless the user changed the one written last."""
    path = ctx.home / ENGINE_JSON
    if path.exists():
        recorded = ctx.state.get(SECTION, ENGINE_JSON_STATE)
        if not recorded:
            ctx.runner.log(ENGINE_JSON_FOREIGN)
            return
        if _sha256(path.read_text()) != recorded:
            ctx.runner.log(ENGINE_JSON_LEFT)
            return
    write_home_file(ctx, path, text)
    ctx.state.set(SECTION, ENGINE_JSON_STATE, _sha256(text), dry_run=ctx.runner.dry_run)


def _json_text(data):
    return json.dumps(data, indent=1) + "\n"


# -- the units ------------------------------------------------------------------

# The units that read the truth and draw on the screen; each gets UNIT_DROP_IN.
UNITS_WITH_TRUTH = ("a3-engine.service", "a3-core.service", "a3-core-window.service",
                    "a3-motion.service", "stemdeck@.service")
DECK_TEMPLATE = "stemdeck@.service"
TWO_DECK_UNIT = "stemdeck.service"
UNIT_DROP_IN = "laptop.conf"
# What the Environment= reset drops from a unit and the laptop still needs.
# DISPLAY=:0 is dropped on purpose and never set again (Review Focus 2).
KEPT_ENVIRONMENT = {
    "a3-engine.service": ("LD_PRELOAD=/usr/lib/a3-core/libjack-rt-priority.so",),
    # Empty: the decks run windowed beside the session's other windows (Task 12).
    DECK_TEMPLATE: ("STEMDECK_WINDOW=",),
}
# The switch the laptop's rig runs under, in the user manager's environment
# (systemctl --user set-environment A3_LAPTOP_RIG=on, by the Canvas or by
# hand), which the units' Environment= reset does not touch.
RIG_SWITCH = "A3_LAPTOP_RIG"
# Units a package enables globally (systemctl --global enable), which no
# user-level disable undoes: a3-motion-ui's postinst, so default.target pulls
# Motion UI in at every login (R9). Their start is skipped unless the switch
# is on; a skipped condition is no failure. stemdeck.service, enabled the same
# way, stays off altogether (two_deck_off_drop_in).
STARTED_BY_THE_SWITCH = ("a3-motion.service",)
SWITCH_CONDITION = f'ExecCondition=/usr/bin/test "${{{RIG_SWITCH}}}" = on\n'
SINK_GOES_LATER = (f"the {OWN_LOOPBACK} sink: it disappears at the next PipeWire restart "
                   "or login")
# [state] laptop letters: the deck instances the last install was for.
LETTERS_STATE = "letters"


def unit_drop_in(unit):
    """The laptop's drop-in for one of UNITS_WITH_TRUTH."""
    environment = (f"A3_OSC_TRUTH=%h/{LAPTOP_TRUTH}", "A3_SCREEN_TRIES=1",
                   *KEPT_ENVIRONMENT.get(unit, ()))
    return (WRITTEN_BY
            + "# Environment= first: the unit's own display line goes, so the display the\n"
            "# session imported into the user manager (with its authority) is used.\n"
            "# One round of the screen's DPI check: a session's screen has its mode\n"
            "# before its apps start. The wait for X itself is not bounded by it.\n"
            "# CPUAffinity= empty: the rig's core layout is not this machine's.\n"
            "[Service]\n"
            "Environment=\n"
            + "".join(f"Environment={line}\n" for line in environment)
            + "CPUAffinity=\n"
            + (SWITCH_CONDITION if unit in STARTED_BY_THE_SWITCH else ""))


def deck_instance(letter):
    return f"stemdeck@{letter}.service"


def recorded_letters(ctx):
    value = ctx.state.get(SECTION, LETTERS_STATE)
    return value.split(",") if value else []


def drop_in_paths(ctx):
    """Every drop-in the laptop writes, by name."""
    return [ctx.user_units / f"{unit}.d" / UNIT_DROP_IN
            for unit in UNITS_WITH_TRUTH + (TWO_DECK_UNIT,)]


def _written_by_us(path):
    """A drop-in of the laptop's name that carries its mark; one written by
    hand is not ours to delete."""
    return not path.exists() or carries_the_mark(path)


def carries_the_mark(path):
    return path.is_file() and WRITTEN_BY in path.read_text(errors="replace")


def deck_drop_in(user_units):
    """The drop-in by which leave.discover_roles finds the laptop."""
    return Path(user_units) / f"{DECK_TEMPLATE}.d" / UNIT_DROP_IN


# -- the role ---------------------------------------------------------------------

class Laptop(Role):
    name = "laptop"
    label = "Laptop rig (Core, decks, desk, Motion UI on one machine)"
    platforms = ("debian",)
    packages = ("pipewire-bin", "xdotool")
    # The laptop has its own session and display manager: no autologin.
    needs_screen = False
    any_user_anywhere = True
    runs_without_checkout = True
    excludes_other_roles = True
    packages_only = True

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        if not ask.interactive:
            return
        choices = output_device_choices(pipewire_objects(ctx))
        stored = s.get(SECTION, "output_device")
        default = stored if stored in dict(choices) else DEFAULT_OUTPUT[0]
        device = ask.choose("Which output does the laptop play main on?", choices, default)
        s.set(SECTION, "output_device", device)
        if device:
            s.set(SECTION, "output_main", ask.text(
                "Which of its channels carry main? (e.g. 1,2)",
                s.get(SECTION, "output_main")))

    def install(self, ctx):
        if ctx.from_source:
            raise RoleError("The laptop role is packages only: its apps come from the "
                            "archive. Run the installer without --from-source.")
        wanted_decks(ctx.settings)   # a malformed count is refused before any change
        self._install_apps(ctx)
        letters = deck_letters(deck_count(ctx.settings, read_truth(ctx)))
        self._wire(ctx, letters)
        self._units(ctx, letters)
        ctx.runner.run(a3_root_command(ctx, "join-audio"), root=True)

    def _install_apps(self, ctx):
        """All five in one a3-root call, which also holds them."""
        for app in APP_PACKAGES:
            if app.unit:
                apppackage.refuse_shadowing_leftovers(ctx, app)
        names = [apppackage.obtain(ctx, app, None, None, None) for app in APP_PACKAGES]
        apppackage.install_together(ctx, APP_PACKAGES, names)

    def _wire(self, ctx, letters):
        """The local links between the decks, the engine and the output
        device. `letters` are the units' (Task 15); the engine counts its
        decks from [laptop] decks or the truth."""
        s = ctx.settings
        device = s.get(SECTION, "output_device").strip()
        # Parsed before any file: a bad channel is refused with nothing written.
        main, phones = self._channels(ctx, device)
        truth = read_truth(ctx)
        engine = laptop_engine_config(read_shipped_engine(), wanted_decks(s), phones is not None)
        write_home_file(ctx, ctx.home / LAPTOP_TRUTH, _json_text(laptop_truth(truth)))
        write_engine_config(ctx, _json_text(engine))
        write_home_file(ctx, ctx.home / LOOPBACK_CONF, loopback_conf(device, main, phones))
        write_home_file(ctx, ctx.home / ANALYZER_ENV, analyzer_env(truth))
        link_server_rate(ctx)

    def _channels(self, ctx, device):
        """(main, phones) on the device, or (None, None) without one: on the
        default sink the phones would be remixed onto main."""
        s = ctx.settings
        phones_value = s.get(SECTION, "output_phones").strip()
        if not device:
            if phones_value:
                ctx.runner.log(PHONES_IGNORED)
            return None, None
        main = output_channels(s.get(SECTION, "output_main").strip() or DEFAULT_MAIN)
        phones = output_channels(phones_value) if phones_value else None
        return main, phones

    def _units(self, ctx, letters):
        """The drop-ins that put the rig's units on this session's screen with
        the laptop's truth. Nothing is enabled or started (R9): they run when
        started by hand or by the Canvas app."""
        for unit in UNITS_WITH_TRUTH:
            write_drop_in(ctx, unit, UNIT_DROP_IN, unit_drop_in(unit))
        write_drop_in(ctx, TWO_DECK_UNIT, UNIT_DROP_IN, two_deck_off_drop_in(WRITTEN_BY))
        # a3-core-app's postinst reloads no user manager.
        systemctl_user(ctx, "daemon-reload")
        # The ExecCondition keeps it from starting; one that runs goes now.
        systemctl_user(ctx, "stop", TWO_DECK_UNIT, check=False)
        for letter in recorded_letters(ctx):
            if letter not in letters:
                systemctl_user(ctx, "stop", deck_instance(letter), check=False)
        ctx.state.set(SECTION, LETTERS_STATE, ",".join(letters), dry_run=ctx.runner.dry_run)

    # -- leaving

    stays = ("~/.config/a3/engine/engine.json: it may carry the user's own links "
             "(the installer cannot tell after the packages are gone)",
             SINK_GOES_LATER,
             "library, sessions, recordings, stems and Motion UI's data")

    def leaving_units(self, ctx):
        return ([unit for unit in UNITS_WITH_TRUTH if unit != DECK_TEMPLATE]
                + [deck_instance(letter) for letter in recorded_letters(ctx)])

    def leaving_files(self, ctx):
        return ([path for path in drop_in_paths(ctx) if _written_by_us(path)]
                + wiring_files(ctx.home))

    def leaving_kept(self, ctx):
        return [path for path in drop_in_paths(ctx) if not _written_by_us(path)]

    def leaving_packages(self, ctx):
        return list(APPS)

    def uninstall(self, ctx):
        super().uninstall(ctx)
        ctx.state.remove(SECTION, LETTERS_STATE, dry_run=ctx.runner.dry_run)
        ctx.runner.log(f"Note: {SINK_GOES_LATER}.")
        # Through the helper whatever this run's mode: the laptop's apps came
        # from the archive and a3-root holds them.
        ctx.runner.run(a3_root_command(ctx, "remove", *self.leaving_packages(ctx)), root=True)

