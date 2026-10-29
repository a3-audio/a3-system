"""The virtual desk -- the A³ Mixer on a screen -- as the Debian package
`a3-desk` (spec virtual-desk, 2026-10-16).

Built from the a3-mixer commit the umbrella pins by installer/package.py,
like StemDeck and Motion UI, installed with apt and held. No unit: it is an
app a person opens (a3-desk, or the launcher), on any machine with a screen --
a3nuc2 beside Motion, a notebook at the bar. Not the role `mixer`: that is
the hardware desk's Pi, and it stays as it is.
"""

from . import apppackage
from .apppackage import has_packaging
from .base import JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce

SOURCE = "a3-mixer"
PACKAGE = "a3-desk"
APP = apppackage.AppPackage(PACKAGE, unit="")


def pinned_commit(ctx):
    return apppackage.pinned_commit(ctx, SOURCE)


def package_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(PACKAGE)


def buildable_pin(ctx, source):
    """(the pinned commit, JUCE) for a build from source; refused when the
    pin predates the desk's packaging."""
    commit = pinned_commit(ctx)
    if not has_packaging(ctx, source, commit):
        raise RoleError(f"a3-mixer at {commit[:10]} has no packaging/stage: the a3-mixer pin "
                        "is older than the desk; raise it first.")
    return commit, ensure_juce(ctx)


class Desk(Role):
    name = "desk"
    label = "A³ Desk (the A³ Mixer on a screen)"
    submodules = (SOURCE,)
    platforms = ("debian",)
    packages = SCREEN_PACKAGES
    build_packages = JUCE_PACKAGES
    needs_screen = True
    stays = ("the build cache ~/.cache/a3-build/a3-desk and the packages in ~/a3-debs",)

    def install(self, ctx):
        source = ctx.repo / SOURCE
        commit, juce = buildable_pin(ctx, source) if ctx.from_source else (None, None)
        apppackage.install(ctx, APP, apppackage.obtain(ctx, APP, source, commit, juce))

    def leaving_packages(self, ctx):
        return [PACKAGE]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        if package_is_installed(ctx):
            apppackage.remove(ctx, APP)
