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

import json
import subprocess
from pathlib import Path

from ..archive import a3_root_command
from ..system import CommandFailed
from . import apppackage, desk, motion, stemdeck
from .base import Role, RoleError
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
        device (Task 14)."""

    def _units(self, ctx, letters):
        """The deck instances and the Core's units for one machine (Task 15)."""

