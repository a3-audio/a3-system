# SPDX-FileCopyrightText: 2026 Raphael Eismann
# SPDX-License-Identifier: GPL-3.0-or-later
"""a3-update, the per-machine updater Core asks to install a signed release
(plan 2026-10-31-rig-updater, step 3). Every role brings it, once per run:
whichever roles a machine has, it gets the one updater.

From the archive by name through a3-root, like the apps; with --from-source
built from the umbrella's own recipe (update/packaging) at the checked-out
commit, without the submodules. Its root right is one sudoers line, which the
installer prints with its check and never writes: that step is the
maintainer's.
"""

from . import apppackage
from .base import systemctl_user

UPDATER = apppackage.AppPackage("a3-update", "a3-update.service", recipe="update/packaging",
                                without_submodules=True, arch_all=True)
A3_ROOT = "/usr/lib/a3-update/a3-root"
SUDOERS_FILE = "/etc/sudoers.d/a3-update"
SUDOERS_DRAFT = "/tmp/a3-update"
# ctx.answers: the updater is in place for this run.
DONE = "a3-update"


def umbrella_commit(ctx):
    return ctx.runner.output(["git", "-C", ctx.repo, "rev-parse", "HEAD"]).strip()


def sudoers_line(user):
    return f"{user} ALL=(root) NOPASSWD: {A3_ROOT} install-release *"


def sudoers_note(user):
    """The one-time root right, as the maintainer types it."""
    return "\n".join([
        f"a3-update needs one sudoers line, once per machine ({SUDOERS_FILE}).",
        "The installer does not write it. Run, checked by visudo first:",
        f"  echo '{sudoers_line(user)}' > {SUDOERS_DRAFT}",
        f"  sudo visudo -cf {SUDOERS_DRAFT}",
        f"  sudo install -m 0440 -o root -g root {SUDOERS_DRAFT} {SUDOERS_FILE}",
    ])


def _obtain(ctx):
    """What apt installs, or None when this version has no updater to build."""
    if not ctx.from_source:
        return apppackage.obtain(ctx, UPDATER, None, None, None)
    commit = umbrella_commit(ctx)
    if not apppackage.has_packaging(ctx, ctx.repo, commit, UPDATER.recipe):
        ctx.runner.log(f"a3-update: the umbrella at {commit[:10]} has no {UPDATER.recipe}/stage; "
                       "left out (a version before the updater).")
        return None
    return apppackage.build(ctx, UPDATER, ctx.repo, commit, juce=None)


def install_updater(ctx):
    if ctx.answers.get(DONE):
        return
    ctx.answers[DONE] = True
    ctx.runner.log("\n=== a3-update ===")
    what = _obtain(ctx)
    if what is None:
        return
    apppackage.install(ctx, UPDATER, what)
    systemctl_user(ctx, "daemon-reload")
    systemctl_user(ctx, "restart", UPDATER.unit)
    ctx.runner.log(sudoers_note(ctx.user))
