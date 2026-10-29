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
from .base import RATE_LINK, Role, RoleError, link_server_rate, write_home_file
from .core import ANALYZER, CORE_APP

SECTION = "laptop"
APP_PACKAGES = (CORE_APP, stemdeck.APP, desk.APP, motion.APP, ANALYZER)
APPS = tuple(app.package for app in APP_PACKAGES)
# The truth a3-core-app ships; the deck count's range is read from it.
TRUTH = Path("/usr/share/a3/a3-osc.json")
TRUTH_DECK_ADDRESS = "stemdeck.deck-hello"
# The loopback the laptop's wiring plays into; never an output choice.
OWN_LOOPBACK = "a3-laptop-out"
DEFAULT_OUTPUT = ("", "default (the internal card)")
SINK_CLASS = "Audio/Sink"
NODE_TYPE = "PipeWire:Interface:Node"
# The engine config a3-core-app ships, which the laptop's is made from.
ENGINE_CONFIG = Path("/usr/share/a3-engine/engine.json")

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


def laptop_engine_config(shipped, decks, phones):
    """The shipped engine config with the laptop's links only: rec, the
    binaural main (R3), to the loopback and the analyzer; phones to its rear
    pair. No analog, no main or booth: a laptop has no rig behind it. The
    decks link themselves (unnamed slots are local StemDecks)."""
    config = copy.deepcopy(shipped)
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
    playback = []
    if device:
        channels = list(main) + (list(phones) if phones else [])
        positions = [f"AUX{channel - 1}" for channel in channels]
        playback += [f'target.object = "{device}"',
                     f"audio.position = {_positions(positions)}"]
    playback += ["node.dont-fallback = false", "node.passive = false"]
    return (WRITTEN_BY
            + "context.modules = [\n"
            "{   name = libpipewire-module-loopback\n"
            "    args = {\n"
            '        node.description = "A3 laptop out"\n'
            "        capture.props = {\n"
            f'            node.name = "{OWN_LOOPBACK}"\n'
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
    listener = next(entry for entry in truth["listeners"]
                    if entry["name"] == CORE_OSC_LISTENER)
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
        if _sha256(path.read_text()) != recorded:
            ctx.runner.log(ENGINE_JSON_LEFT)
            return
    write_home_file(ctx, path, text)
    ctx.state.set(SECTION, ENGINE_JSON_STATE, _sha256(text), dry_run=ctx.runner.dry_run)


def _json_text(data):
    return json.dumps(data, indent=1) + "\n"


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
        phones_value = s.get(SECTION, "output_phones").strip()
        # Parsed before any file: a bad channel is refused with nothing written.
        main = output_channels(s.get(SECTION, "output_main")) if device else None
        phones = output_channels(phones_value) if phones_value else None
        truth = read_truth(ctx)
        engine = laptop_engine_config(read_shipped_engine(), wanted_decks(s), phones is not None)
        write_home_file(ctx, ctx.home / LAPTOP_TRUTH, _json_text(laptop_truth(truth)))
        write_engine_config(ctx, _json_text(engine))
        write_home_file(ctx, ctx.home / LOOPBACK_CONF, loopback_conf(device, main, phones))
        write_home_file(ctx, ctx.home / ANALYZER_ENV, analyzer_env(truth))
        link_server_rate(ctx)

    def _units(self, ctx, letters):
        """The deck instances and the Core's units for one machine (Task 15)."""

