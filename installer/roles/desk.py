"""The virtual desk -- the A³ Mixer on a screen -- as the Debian package
`a3-desk` (spec virtual-desk, 2026-10-16).

Built by installer/package.py from the commit of a3-mixer-ui -- a3-mixer's
submodule a3-mixer-ui since 2026-10-31, as a3-motion-ui is a3-motion's -- that the
umbrella's a3-mixer pin records, like StemDeck and Motion UI; installed with
apt and held. No unit: it is an
app a person opens (a3-desk, or the launcher), on any machine with a screen --
a3nuc2 beside Motion, a notebook at the bar. Not the role `mixer`: that is
the hardware desk's Pi, and it stays as it is.
"""

from . import apppackage
from .apppackage import has_packaging
from .base import JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce
from .updater import install_updater

# The umbrella pins a3-mixer, a3-mixer pins a3-mixer-ui.
PIN_PATH = ("a3-mixer", "a3-mixer-ui")
SOURCE = "/".join(PIN_PATH)
PACKAGE = "a3-desk"
APP = apppackage.AppPackage(PACKAGE, unit="")


def pinned_commit(ctx):
    return apppackage.pinned_commit(ctx, *PIN_PATH)


def package_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(PACKAGE)


def buildable_pin(ctx, source):
    """(the pinned commit, JUCE) for a build from source; refused when the
    pin predates the desk's packaging."""
    commit = pinned_commit(ctx)
    if not has_packaging(ctx, source, commit, APP.recipe):
        raise RoleError(f"{SOURCE} at {commit[:10]} has no {APP.recipe}/stage: a3-mixer's "
                        "a3-mixer-ui pin is older than the desk's own repository; raise it first.")
    return commit, ensure_juce(ctx)


class Desk(Role):
    name = "desk"
    label = "A³ Desk (the A³ Mixer on a screen)"
    # a3-mixer with its a3-mixer-ui, recursively.
    submodules = (PIN_PATH[0],)
    platforms = ("debian",)
    packages = SCREEN_PACKAGES
    build_packages = JUCE_PACKAGES
    needs_screen = True
    stays = ("the build cache ~/.cache/a3-build/a3-desk and the packages in ~/a3-debs",)

    def install(self, ctx):
        source = ctx.repo / SOURCE
        commit, juce = buildable_pin(ctx, source) if ctx.from_source else (None, None)
        apppackage.install(ctx, APP, apppackage.obtain(ctx, APP, source, commit, juce))
        install_updater(ctx)

    def leaving_packages(self, ctx):
        return [PACKAGE]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        if package_is_installed(ctx):
            apppackage.remove(ctx, APP)
