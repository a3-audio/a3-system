"""StemDeck, on the Core or on a machine of its own.

Built in the submodule, in build-make: that is the path its unit starts.
The unit comes from StemDeck's own repository. On a machine without the Core
its zita units come too -- they carry the stems to the Core and two channels
back -- and JACK is that machine's own business: a3-jack exists only on a
Core.
"""

from .base import Role, ensure_juce, enable_and_restart, install_user_unit

SOURCE = "stemdeck"


class StemDeck(Role):
    name = "stemdeck"
    label = "StemDeck (Stem-Player)"
    submodules = (SOURCE,)
    platforms = ("debian",)

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
            for zita in ("zita-n2j.service", "zita-j2n.service"):
                install_user_unit(ctx, units / zita)
                enable_and_restart(ctx, zita)
            run.log("Hinweis: Ohne Core auf diesem Rechner muss JACK hier "
                    "anders gestartet werden; a3-jack gibt es nur auf dem Core.")
        enable_and_restart(ctx, "stemdeck.service")
