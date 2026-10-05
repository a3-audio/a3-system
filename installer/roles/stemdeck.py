"""StemDeck, on the Core or on a machine of its own.

Built in the submodule, in build-make: that is the path its unit starts.
The unit comes from StemDeck's own repository. On a machine without the Core
its zita units come too -- they carry the stems to the Core and two channels
back -- and JACK is that machine's own business: a3-jack exists only on a
Core.

The stem library is asked for and handed to StemDeck as stemFolder in its
own settings file, a JUCE PropertiesFile (Source/MainComponent.cpp). StemDeck
writes that file when it quits, so it is stopped before the file is changed.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from .base import (JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce,
                   enable_and_restart, install_user_unit, recorded_roles,
                   systemctl_user)

SOURCE = "stemdeck"
UNIT = "stemdeck.service"
ZITA_UNITS = ("zita-n2j.service", "zita-j2n.service")
SETTINGS_FILE = Path(".config/StemDeck/StemDeck.settings")
STEM_FOLDER = "stemFolder"
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'


def settings_path(ctx):
    return ctx.home / SETTINGS_FILE


def stem_folder_in(text):
    """The stemFolder a settings file names, or None."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    for value in root.findall("VALUE"):
        if value.get("name") == STEM_FOLDER:
            return value.get("val") or None
    return None


def with_stem_folder(text, folder):
    """The settings file `text` (None: there is none yet) with stemFolder set
    to `folder` and every other VALUE as it was."""
    if text is None:
        root = ET.Element("PROPERTIES")
    else:
        try:
            root = ET.fromstring(text)
        except ET.ParseError as error:
            raise RoleError(f"{SETTINGS_FILE} ist kein lesbares XML ({error}); "
                            "von Hand prüfen, der Installer ändert es so nicht.")
    entry = next((v for v in root.findall("VALUE") if v.get("name") == STEM_FOLDER), None)
    if entry is None:
        entry = ET.Element("VALUE", {"name": STEM_FOLDER})
        root.insert(0, entry)
    entry.set("val", str(folder))
    ET.indent(root, space="  ")
    return f"{XML_DECLARATION}\n\n{ET.tostring(root, encoding='unicode')}\n"


def stemdeck_library(ctx):
    """The stemFolder StemDeck uses now, or None when its settings name no
    usable one: no file, no entry, or a relative path StemDeck ignores."""
    path = settings_path(ctx)
    found = stem_folder_in(path.read_text()) if path.is_file() else None
    return found if found and Path(found).is_absolute() else None


def absolute_folder(ctx, answer):
    """StemDeck takes an absolute stemFolder only; ~ and relative answers are
    the user's home."""
    answer = answer.strip()
    if answer == "~" or answer.startswith("~/"):
        answer = str(ctx.home) + answer[1:]
    return str(ctx.home / answer) if not Path(answer).is_absolute() else answer


class StemDeck(Role):
    name = "stemdeck"
    label = "StemDeck (Stem-Player)"
    submodules = (SOURCE,)
    platforms = ("debian",)
    packages = SCREEN_PACKAGES + JUCE_PACKAGES + (
        "libflac-dev", "libvorbis-dev", "libogg-dev", "libjack-jackd2-dev",
        # jack_wait: its unit waits for whatever JACK runs, Core or not
        "jack-example-tools",
        # StemDeck's on-screen keyboard starts onboard
        "onboard")
    needs_screen = True

    def configure(self, ctx):
        """StemDeck's own choice wins: the DJ may have changed the folder in
        StemDeck since the last install. Without anyone to ask, the stored
        answer is only used where StemDeck names no folder."""
        s, ask = ctx.settings, ctx.prompter
        now, stored = stemdeck_library(ctx), s.get("stemdeck", "library")
        default = now or stored or str(ctx.home / "stems")
        if ask.interactive:
            answer = ask.text("Wo liegt die Stem-Bibliothek von StemDeck "
                              "(Artist/Album/Sets)?", default) or default
        else:
            answer = default
            if now and stored and absolute_folder(ctx, stored) != now:
                ctx.runner.log(f"Stem-Bibliothek: {stored} aus den Einstellungen "
                               f"nicht übernommen, StemDeck nutzt {now}.")
        s.set("stemdeck", "library", absolute_folder(ctx, answer))

    def install(self, ctx):
        run = ctx.runner
        source = ctx.repo / SOURCE
        prefix = ensure_juce(ctx)
        run.run(["cmake", "-S", source, "-B", source / "build-make",
                 "-DCMAKE_BUILD_TYPE=Release", f"-DCMAKE_PREFIX_PATH={prefix}"])
        run.run(["cmake", "--build", source / "build-make", "-j", ctx.jobs()])

        units = source / ".config" / "systemd" / "user"
        install_user_unit(ctx, units / UNIT)
        if "core" not in ctx.settings.roles():
            for zita in ZITA_UNITS:
                install_user_unit(ctx, units / zita)
                enable_and_restart(ctx, zita)
            run.log("Hinweis: Ohne Core auf diesem Rechner muss JACK hier "
                    "anders gestartet werden; a3-jack gibt es nur auf dem Core.")
        self._hand_over_library(ctx)
        enable_and_restart(ctx, UNIT)

    def _hand_over_library(self, ctx):
        """The library folder made if missing and written into StemDeck's
        settings, unless StemDeck uses it already: then nothing is stopped
        or written. StemDeck is stopped first: it writes the file when it
        quits and would put the old folder back."""
        run = ctx.runner
        now = stemdeck_library(ctx)
        folder = Path(ctx.settings.get("stemdeck", "library")
                      or now or ctx.home / "stems")
        if now == str(folder):
            run.log(f"Stem-Bibliothek: StemDeck nutzt bereits {folder}.")
            return
        path = settings_path(ctx)
        # check=False: on the first install there is no unit to stop yet.
        systemctl_user(ctx, "stop", UNIT, check=False)
        try:
            text = with_stem_folder(path.read_text() if path.is_file() else None, folder)
        except RoleError:
            # The file stays as it is, and StemDeck runs on with it.
            systemctl_user(ctx, "start", UNIT, check=False)
            raise
        if not folder.is_dir():
            run.log(f"# Stem-Bibliothek {folder} fehlt, wird angelegt.")
        run.log(f"Stem-Bibliothek: {folder}, eingetragen in {path} ({STEM_FOLDER}).")
        if run.dry_run:
            return
        folder.mkdir(parents=True, exist_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    stays = ("der Build-Ordner stemdeck/build-make",
             "Bibliothek, Sessions, Aufnahmen und Stems")

    def leaving_units(self, ctx):
        return [UNIT] + (list(ZITA_UNITS) if _owns_zita(ctx) else [])

    def leaving_files(self, ctx):
        return [ctx.user_units / unit for unit in self.leaving_units(ctx)]


def _owns_zita(ctx):
    """The zita units are StemDeck's only on a machine without a Core: a Core
    chosen keeps them running, a Core still installed stops them itself."""
    return ("core" not in ctx.settings.roles()
            and "core" not in (recorded_roles(ctx) or []))
