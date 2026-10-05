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


def discover_roles(user_units, core_installed=None):
    """The roles on a machine without an [installed] record, in install order."""
    if core_installed is None:
        core_installed = lambda: package_installed("a3-core")  # noqa: E731
    found = {
        "core": core_installed(),
        "stemdeck": (user_units / "stemdeck.service").exists(),
        "motion": (user_units / "a3-motion.service").exists(),
    }
    return [name for name in ("core", "stemdeck", "motion") if found[name]]


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
    lines = ["Diese Rollen sind installiert, aber nicht mehr gewählt:"]
    for name in names:
        lines.append("")
        lines.append(BY_NAME[name].label)
        lines.extend(BY_NAME[name].leaving_lines(ctx))
    lines.append("")
    lines.append("Pakete, die für die Rollen installiert wurden, bleiben, "
                 "ebenso Gruppen und alle Daten.")
    return "\n".join(lines)


def agree_to_leave(ctx, names):
    text = leaving_text(ctx, names)
    log = ctx.runner.log
    if ctx.prompter.interactive:
        if ctx.prompter.yesno(text + "\n\nDiese Rollen jetzt entfernen?", False):
            return True
        log("Nichts wird entfernt; die gewählten Rollen werden trotzdem installiert.")
        return False
    log("\n" + text)
    if ctx.settings.flag("uninstall", "allow"):
        return True
    log(f"Nicht entfernt: {ctx.settings.path} erlaubt es nicht "
        "([uninstall] allow = yes). Die gewählten Rollen werden trotzdem installiert.")
    return False


def uninstall_one(ctx, name):
    ctx.runner.log(f"\n=== {BY_NAME[name].label} entfernen ===")
    try:
        BY_NAME[name].uninstall(ctx)
    except (RoleError, CommandFailed) as error:
        return (name, f"FEHLER beim Entfernen: {error}")
    forget_installed(ctx, name)
    return (name, "entfernt")


def name_the_autologin(ctx, chosen, left):
    if needs_screen(chosen) or not any(BY_NAME[name].needs_screen for name in left):
        return
    ctx.runner.log("Keine gewählte Rolle braucht noch den Bildschirm. Der Autologin auf "
                   "tty1 bleibt trotzdem; entfernen mit "
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
        return [(name, "bleibt installiert (nicht entfernt)") for name in going]
    # Reverse install order: the Core last, so StemDeck still sees it.
    rows = [uninstall_one(ctx, name) for name in reversed(going)]
    name_the_autologin(ctx, chosen, [name for name, result in rows if result == "entfernt"])
    return rows[::-1]
