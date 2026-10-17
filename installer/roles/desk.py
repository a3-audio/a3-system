"""The virtual desk -- the A³ Mixer on a screen -- as the Debian package
`a3-desk` (spec virtual-desk, 2026-10-16).

Built from the a3-mixer commit the umbrella pins by installer/package.py,
like StemDeck and Motion UI, installed with apt and held. No unit: it is an
app a person opens (a3-desk, or the launcher), on any machine with a screen --
a3nuc2 beside Motion, a notebook at the bar. Not the role `mixer`: that is
the hardware desk's Pi, and it stays as it is.
"""

from . import apppackage
from .base import JUCE_PACKAGES, SCREEN_PACKAGES, Role, ensure_juce

SOURCE = "a3-mixer"
PACKAGE = "a3-desk"
APP = apppackage.AppPackage(PACKAGE, unit="")


def pinned_commit(ctx):
    return apppackage.pinned_commit(ctx, SOURCE)


def package_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(PACKAGE)


class Desk(Role):
    name = "desk"
    label = "A³ Desk (the A³ Mixer on a screen)"
    submodules = (SOURCE,)
    platforms = ("debian",)
    packages = SCREEN_PACKAGES + JUCE_PACKAGES
    needs_screen = True
    stays = ("the build cache ~/.cache/a3-build/a3-desk and the packages in ~/a3-debs",)

    def install(self, ctx):
        juce = ensure_juce(ctx)
        deb = apppackage.build(ctx, APP, ctx.repo / SOURCE, pinned_commit(ctx), juce)
        apppackage.install(ctx, APP, deb)

    def leaving_packages(self, ctx):
        return [PACKAGE]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        if package_is_installed(ctx):
            apppackage.remove(ctx, APP)
