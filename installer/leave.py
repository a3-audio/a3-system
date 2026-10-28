"""Roles that leave: a role installed here and no longer chosen is
uninstalled, after the person at the machine says yes -- or, with no one to
ask (--config, --update), when the settings file says [uninstall] allow = yes.

What is installed comes from the state file's [installed] section. A machine
set up before that section existed has its roles found by what is there.
"""

import subprocess

from .roles import ALL, BY_NAME, needs_screen
from .roles.base import RoleError, forget_installed, record_installed, recorded_roles
from .roles.screen import AUTOLOGIN_DROP_IN
from .system import CommandFailed


def dpkg_status(package):
    """dpkg's Status field for `package`, or None when dpkg does not know it."""
    try:
        done = subprocess.run(["dpkg-query", "-W", "-f=${Status}", package],
                              capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def package_installed(package, status=dpkg_status):
    found = status(package)
    return bool(found) and found.split()[-1] == "installed"


def discover_roles(user_units, core_installed=None, stemdeck_installed=None,
                   motion_installed=None, desk_installed=None):
    """The roles on a machine without an [installed] record, in install order."""
    if core_installed is None:
        core_installed = lambda: package_installed("a3-core")  # noqa: E731
    if stemdeck_installed is None:
        stemdeck_installed = lambda: package_installed("stemdeck")  # noqa: E731
    if motion_installed is None:
        motion_installed = lambda: package_installed("a3-motion-ui")  # noqa: E731
    if desk_installed is None:
        desk_installed = lambda: package_installed("a3-desk")  # noqa: E731
    # The deck host has the stemdeck package too, but plays no two-deck StemDeck.
    deck_host = any(user_units.glob("stemdeck@*.service.d/deck-host.conf"))
    found = {
        "core": core_installed(),
        "deck-host": deck_host,
        "stemdeck": (user_units / "stemdeck.service").exists()
        or (stemdeck_installed() and not deck_host),
        "motion": (user_units / "a3-motion.service").exists() or motion_installed(),
        "desk": desk_installed(),
    }
    return [name for name in ("core", "stemdeck", "deck-host", "motion", "desk")
            if found[name]]


def installed_now(ctx, discover=discover_roles):
    """(the installed roles, whether they were found rather than recorded)."""
    recorded = recorded_roles(ctx)
    if recorded is not None:
        return recorded, False
    return discover(ctx.user_units), True


def deselected(installed, chosen):
    """Installed and no longer chosen, in install order. A name no role
    has (a state file edited by hand) is not a role that can leave."""
    return [role.name for role in ALL if role.name in installed and role.name not in chosen]


def leaving_text(ctx, names):
    lines = ["These roles are installed but no longer chosen:"]
    for name in names:
        lines.append("")
        lines.append(BY_NAME[name].label)
        lines.extend(BY_NAME[name].leaving_lines(ctx))
    lines.append("")
    lines.append("Packages installed for the roles stay, "
                 "as do groups and all data.")
    return "\n".join(lines)


def agree_to_leave(ctx, names):
    text = leaving_text(ctx, names)
    log = ctx.runner.log
    if ctx.prompter.interactive:
        if ctx.prompter.yesno(text + "\n\nRemove these roles now?", False):
            return True
        log("Nothing is removed; the chosen roles are installed anyway.")
        return False
    log("\n" + text)
    if ctx.settings.flag("uninstall", "allow"):
        return True
    log(f"Not removed: {ctx.settings.path} does not allow it "
        "([uninstall] allow = yes). The chosen roles are installed anyway.")
    return False


def uninstall_one(ctx, name):
    ctx.runner.log(f"\n=== Removing {BY_NAME[name].label} ===")
    try:
        BY_NAME[name].uninstall(ctx)
    except (RoleError, CommandFailed) as error:
        return (name, f"ERROR while removing: {error}")
    forget_installed(ctx, name)
    return (name, "removed")


def name_the_autologin(ctx, chosen, left):
    if needs_screen(chosen) or not any(BY_NAME[name].needs_screen for name in left):
        return
    ctx.runner.log("No chosen role needs the screen any more. The autologin on "
                   "tty1 stays anyway; remove it with "
                   f"sudo rm {AUTOLOGIN_DROP_IN}")


def leave_roles(ctx, chosen, discover=discover_roles):
    """Uninstall the deselected roles, if agreed. A result row per role
    that was to leave."""
    installed, found = installed_now(ctx, discover)
    going = deselected(installed, chosen)
    agreed = bool(going) and agree_to_leave(ctx, going)
    # Found roles are recorded only now, after they were shown.
    for name in installed if found else ():
        record_installed(ctx, name)
    if not agreed:
        return [(name, "stays installed (not removed)") for name in going]
    # Reverse install order: the Core last, so StemDeck still sees it.
    rows = [uninstall_one(ctx, name) for name in reversed(going)]
    name_the_autologin(ctx, chosen, [name for name, result in rows if result == "removed"])
    return rows[::-1]
