"""StemDeck, on the Core or on a machine of its own.

Built in the submodule, in build-make: that is the path its unit starts.
The unit comes from StemDeck's own repository. On a machine without the Core
its zita units come too -- they carry the stems to the Core and two channels
back -- and JACK is that machine's own business: a3-jack exists only on a
Core.
"""

from .base import (JUCE_PACKAGES, SCREEN_PACKAGES, Role, ensure_juce,
                   enable_and_restart, install_user_unit, recorded_roles)

SOURCE = "stemdeck"
ZITA_UNITS = ("zita-n2j.service", "zita-j2n.service")


class StemDeck(Role):
    name = "stemdeck"
    label = "StemDeck (Stem-Player)"
    submodules = (SOURCE,)
    platforms = ("debian",)
    packages = SCREEN_PACKAGES + JUCE_PACKAGES + (
        "libflac-dev", "libvorbis-dev", "libogg-dev", "libjack-jackd2-dev")
    needs_screen = True

    def install(self, ctx):
        run = ctx.runner
        source = ctx.repo / SOURCE
        prefix = ensure_juce(ctx)
        run.run(["cmake", "-S", source, "-B", source / "build-make",
                 "-DCMAKE_BUILD_TYPE=Release", f"-DCMAKE_PREFIX_PATH={prefix}"])
        run.run(["cmake", "--build", source / "build-make", "-j", ctx.jobs()])

        units = source / ".config" / "systemd" / "user"
        install_user_unit(ctx, units / "stemdeck.service")
        if "core" not in ctx.settings.roles():
            for zita in ZITA_UNITS:
                install_user_unit(ctx, units / zita)
                enable_and_restart(ctx, zita)
            run.log("Hinweis: Ohne Core auf diesem Rechner muss JACK hier "
                    "anders gestartet werden; a3-jack gibt es nur auf dem Core.")
        enable_and_restart(ctx, "stemdeck.service")

    stays = ("der Build-Ordner stemdeck/build-make",
             "Bibliothek, Sessions, Aufnahmen und Stems")

    def leaving_units(self, ctx):
        return ["stemdeck.service"] + (list(ZITA_UNITS) if _owns_zita(ctx) else [])

    def leaving_files(self, ctx):
        return [ctx.user_units / unit for unit in self.leaving_units(ctx)]


def _owns_zita(ctx):
    """The zita units are StemDeck's only on a machine without a Core: a Core
    chosen keeps them running, a Core still installed stops them itself."""
    return ("core" not in ctx.settings.roles()
            and "core" not in (recorded_roles(ctx) or []))
