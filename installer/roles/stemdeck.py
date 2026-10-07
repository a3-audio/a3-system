"""StemDeck, on the Core or on a machine of its own, as the Debian package
`stemdeck` (2026-10-07).

The package is built from the pinned commit by installer/package.py into
~/.cache/a3-build and ~/a3-debs -- never in the checkout, whose build-make the
old unit started, so a rebuild can no longer leave the service without an
executable -- then installed with apt and held, like a3-core. The package
carries the unit (/usr/lib/systemd/user/stemdeck.service) and its runtime
dependencies. On a machine without the Core the zita units and
qjackctl-stemdeck.service still come from StemDeck's repository into
~/.config, now naming the packaged tools and patchbay; with the Core they
are taken away: two QjackCtls must not wire one JACK.

The stem library is asked for and handed to StemDeck as stemFolder in its
own settings file, a JUCE PropertiesFile (Source/MainComponent.cpp). StemDeck
writes that file when it quits, so it is stopped before the file is changed.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from .. import package as debs
from .base import (JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce,
                   enable_and_restart, install_user_unit, recorded_roles,
                   remove_files, systemctl_user)

SOURCE = "stemdeck"
UNIT = "stemdeck.service"
ZITA_UNITS = ("zita-n2j.service", "zita-j2n.service")
# Not qjackctl.service: that is the Core's, and a machine that becomes a Core
# would have one file for two owners.
PATCHBAY_UNIT = "qjackctl-stemdeck.service"
SETTINGS_FILE = Path(".config/StemDeck/StemDeck.settings")
STEM_FOLDER = "stemFolder"
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'
PACKAGE = "stemdeck"
PACKAGED_UNIT = f"/usr/lib/systemd/user/{UNIT}"
BEFORE_PACKAGE = ".before-package"
# -j2: a -j4 build on a3nuc1 made the desk lag (2026-10-02).
BUILD_JOBS = 2


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
        # without the Core, PATCHBAY_UNIT runs QjackCtl with StemDeck's patchbay
        # (the runtime tools of stemdeck.service are the package's Depends)
        "qjackctl")
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
        juce = ensure_juce(ctx)
        _refuse_shadowing_leftovers(ctx)
        deb = build_stemdeck(ctx, juce)
        done = []
        try:
            _set_aside_hand_unit(ctx, done)
            run.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                     "--allow-downgrades", "--allow-change-held-packages", deb], root=True)
        except BaseException:
            # BaseException: a Ctrl-C at the sudo prompt must not leave the
            # machine with its unit disabled, renamed and no package either.
            _put_hand_unit_back(ctx, done)
            raise
        run.run(["apt-mark", "hold", PACKAGE], root=True)

        units = ctx.repo / SOURCE / ".config" / "systemd" / "user"
        if "core" not in ctx.settings.roles():
            for unit in ZITA_UNITS + (PATCHBAY_UNIT,):
                install_user_unit(ctx, units / unit)
                enable_and_restart(ctx, unit)
            run.log("Hinweis: Ohne Core auf diesem Rechner muss JACK hier "
                    "anders gestartet werden; a3-jack gibt es nur auf dem Core.")
        else:
            _remove_patchbay_unit(ctx)
        self._hand_over_library(ctx)
        enable_and_restart(ctx, UNIT)
        _check_packaged_unit_wins(ctx)

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

    stays = ("the build cache ~/.cache/a3-build/stemdeck and the packages in ~/a3-debs",
             "Bibliothek, Sessions, Aufnahmen und Stems")

    def leaving_units(self, ctx):
        return ([UNIT, PATCHBAY_UNIT]
                + (list(ZITA_UNITS) if _owns_zita(ctx) else []))

    def leaving_files(self, ctx):
        """The units the installer put into ~/.config; stemdeck.service is the package's."""
        files = [ctx.user_units / unit for unit in self.leaving_units(ctx) if unit != UNIT]
        hand = ctx.user_units / UNIT
        if hand.is_file() and not hand.is_symlink():
            files.append(hand)  # an install from before the package
        return files

    def leaving_packages(self, ctx):
        return [PACKAGE]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        if not package_is_installed(ctx):
            return
        ctx.runner.run(["apt-mark", "unhold", PACKAGE], root=True)
        ctx.runner.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "remove", "-y",
                        PACKAGE], root=True)


def _owns_zita(ctx):
    """The zita units are StemDeck's only on a machine without a Core: a Core
    chosen keeps them running, a Core still installed stops them itself."""
    return ("core" not in ctx.settings.roles()
            and "core" not in (recorded_roles(ctx) or []))


def _remove_patchbay_unit(ctx):
    """A machine that becomes a Core: StemDeck's QjackCtl goes, the Core's
    own qjackctl.service and patchbay take over."""
    target = ctx.user_units / PATCHBAY_UNIT
    if not target.is_file():
        return
    systemctl_user(ctx, "disable", "--now", PATCHBAY_UNIT, check=False)
    remove_files(ctx, [target])
    systemctl_user(ctx, "daemon-reload")


def pinned_commit(ctx):
    """The commit the umbrella pins for StemDeck -- the release's, whatever the
    submodule's working copy holds."""
    return ctx.runner.output(["git", "-C", ctx.repo, "rev-parse", f"HEAD:{SOURCE}"]).strip()


def build_stemdeck(ctx, juce):
    """The .deb of the pinned commit, built by installer/package.py (whose CLI
    lowers its own priority to nice 19); its path."""
    source = ctx.repo / SOURCE
    commit = pinned_commit(ctx)
    out = ctx.home / "a3-debs"
    cache = ctx.home / ".cache" / "a3-build"
    ctx.runner.run(["python3", ctx.repo / "installer" / "package.py", source,
                    "--rev", commit, "--out", out, "--cache", cache,
                    "--jobs", BUILD_JOBS, "--juce", juce])
    return debs.deb_path(out, PACKAGE, debs.version_of(source, commit))


DISABLED, MOVED = "disabled", "moved"


def _hand_unit(ctx):
    return ctx.user_units / UNIT


def _aside_name(ctx):
    return _hand_unit(ctx).with_name(UNIT + BEFORE_PACKAGE)


def _refuse_shadowing_leftovers(ctx):
    """Up front, before anything is built: what the installer will not resolve
    by itself."""
    hand, aside = _hand_unit(ctx), _aside_name(ctx)
    if hand.is_symlink():
        raise RoleError(f"{hand} is a symlink and would shadow the package's unit; "
                        "remove it by hand and run the installer again.")
    if hand.is_file() and aside.exists():
        raise RoleError(f"{hand} and {aside} both exist; move one of them away by hand -- "
                        "the installer overwrites neither.")


def _set_aside_hand_unit(ctx, done):
    """A stemdeck.service in ~/.config/systemd/user -- the copy earlier installs
    put there, or one made by hand -- shadows the packaged unit: the package
    would seem to change nothing. It is disabled (its wants links go) and
    renamed, never deleted; its drop-ins (a3-core.conf) stay and apply to the
    packaged unit. Done right before apt, so a failed build leaves it running.
    Each step is noted in `done` (the disable before it is tried, the rename
    once it is made) so that _put_hand_unit_back undoes exactly those."""
    hand, aside = _hand_unit(ctx), _aside_name(ctx)
    if not hand.is_file():
        return
    ctx.runner.log(f"{hand} would shadow the package's unit: set aside as {aside.name}.")
    done.append(DISABLED)
    systemctl_user(ctx, "disable", UNIT, check=False)
    ctx.runner.run(["mv", "-n", hand, aside])
    done.append(MOVED)


def _put_hand_unit_back(ctx, done):
    """The package did not go in: the machine keeps the unit it had."""
    if not done:
        return
    ctx.runner.log(f"the package did not go in: {UNIT} is put back as it was.")
    if MOVED in done:
        ctx.runner.run(["mv", "-n", _aside_name(ctx), _hand_unit(ctx)], check=False)
    systemctl_user(ctx, "enable", UNIT, check=False)


def package_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(PACKAGE)


def fragment_path(ctx):
    return ctx.runner.output(["systemctl", "--user", "show", "-p", "FragmentPath",
                              "--value", UNIT]).strip()


def _check_packaged_unit_wins(ctx):
    if ctx.runner.dry_run:
        ctx.runner.log(f"# dry run: the check that no unit file shadows {PACKAGED_UNIT} is skipped.")
        return
    found = fragment_path(ctx)
    if found != PACKAGED_UNIT:
        raise RoleError(f"{UNIT} runs from {found}, not {PACKAGED_UNIT}: a unit file there "
                        "shadows the package. Move it aside and run the installer again.")
