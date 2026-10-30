"""install: set up this machine as a part of the A³ system, or update it.

    install                      ask: version, roles, their settings
    install --update [VERSION]   no questions: the stored roles and settings,
                                 at VERSION (default: the stored branch, or
                                 the newest tag when a tag is stored)
    install --config FILE        no questions: FILE's roles and settings
    install --network            ask the Core's network questions again (otherwise
                                 only the first install asks; the stored answers stand)
    install --dry-run            show every command, run none
    install --from-source        build the apps from the pinned submodules
                                 instead of taking the archive's packages
    install --flash-firmware     flash the Motion panel even if unchanged
    install --ssh-key FILE       the Core lets FILE's public key log in as aaa

The stored answers are in ~/.config/a3/install.conf. The apps come from the
apt archive by default ([system] archive = public, or lan for the rig's own
apt source set up by hand), which holds only the newest of each package: a
named version (--update VERSION) needs --from-source.
"""

import argparse
import getpass
import sys
from pathlib import Path

from . import archive, release
from .leave import deselected, discover_roles, installed_now, leave_roles
from .prompt import make_prompter
from .roles import ALL, BY_NAME, needed_packages, needed_submodules, needs_screen
from .roles.base import STATE_FILE, Context, RoleError, State, record_installed
from .roles.core import check_core, read_ssh_key
from .roles.screen import set_up_screen
from .settings import DEFAULT_PATH, Settings
from .system import APT_PLATFORMS, CommandFailed, Runner, os_release, platform_name

REPO = Path(__file__).resolve().parents[1]

# Every unit the components ship names /home/aaa/a3-system. Until that is
# written relative, the installer runs from there and as aaa.
EXPECTED_USER = "aaa"
EXPECTED_REPO = Path("/home/aaa/a3-system")

OS_RELEASE = Path("/etc/os-release")
# [system] archive: the public archive, whose source the installer writes, or
# the rig's LAN archive, whose source is set up by hand.
ARCHIVES = ("public", "lan")
LAN_SOURCE = "http://192.168.8.5/apt a3 main"


def parse(argv):
    parser = argparse.ArgumentParser(
        prog="install", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", nargs="?", const="", metavar="VERSION")
    parser.add_argument("--config", type=Path, metavar="FILE")
    parser.add_argument("--network", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-source", action="store_true")
    parser.add_argument("--flash-firmware", action="store_true")
    parser.add_argument("--ssh-key", type=Path, metavar="FILE")
    return parser.parse_args(argv)


def place_problems(repo, user, names):
    """where_problems, unless every named role runs as any user anywhere
    (the laptop: packages only, units with %h). No roles yet: the check holds."""
    roles = [BY_NAME[name] for name in names]
    if roles and all(role.any_user_anywhere for role in roles):
        return []
    return where_problems(repo, user)


def where_problems(repo, user):
    problems = []
    if user != EXPECTED_USER:
        problems.append(f"running as {user}, the units expect {EXPECTED_USER}")
    if repo != EXPECTED_REPO:
        problems.append(f"located in {repo}, the units expect {EXPECTED_REPO}")
    return problems


def refusal(args, settings, state, platform=None, release_info=None):
    """Why this run cannot start, before it changes anything; or None.
    `state` is the installer's history here: a machine installed before
    keeps its archive until it is named (the rig is on lan, and a public
    source apt cannot update from breaks its apt). With `platform` and
    `release_info` a public archive for a codename it has no suite for is
    refused here too, before the checkout moves."""
    chosen = settings.get("system", "archive")
    if chosen not in ARCHIVES:
        return (f"[system] archive = {chosen} in {settings.path}: allowed are "
                "public (the public A3 archive) and lan (the rig's own apt source).")
    if (not args.from_source and state.path.is_file()
            and not settings.in_file("system", "archive")):
        return ("`[system] archive` is not set: set it to public (the GitHub archive) "
                "or lan (the forge on 192.168.8.5), or run with --from-source to build "
                "as before.")
    if args.update and not args.from_source:
        return (f"--update {args.update}: the archive holds only the newest packages, "
                "not a named version. To install a version, build it from source: "
                f"install --from-source --update {args.update}")
    return unsupported_codename(args, chosen, platform, release_info)


def unsupported_codename(args, chosen, platform, release_info):
    if args.from_source or chosen != "public" or platform not in APT_PLATFORMS:
        return None
    try:
        archive.suite_for(release_info)
    except archive.ArchiveError as error:
        return str(error)
    return None


def update_version(requested, stored, tags, here):
    """--update's version: the one named; else a branch the machine was set
    to follows that branch (a tag of 2026-09 has no StemDeck submodule, and
    a machine on main went back to it, 2026-10-05); else the newest tag."""
    if requested:
        return requested
    if stored and not release.TAG.match(stored):
        return stored
    return tags[0] if tags else here


def name_a_version_not_in_the_archive(ctx, version, tags):
    if ctx.from_source or not tags or version == tags[0]:
        return
    ctx.runner.log("Packages come from the archive's newest whatever version is "
                   "checked out; use --from-source to build this version.")


def choose_version(ctx, args):
    version, tags = _chosen_version(ctx, args)
    name_a_version_not_in_the_archive(ctx, version, tags)
    return version


def _chosen_version(ctx, args):
    """(the version to run, the release tags, newest first)."""
    run, repo = ctx.runner, ctx.repo
    try:
        release.fetch(run, repo)
    except CommandFailed:
        run.log("No connection to GitHub: only the versions already here are available.")
    tags = release.tags(run, repo)
    here = release.current(run, repo)
    if args.update is not None:
        return update_version(args.update, ctx.settings.get("system", "version"),
                              tags, here), tags
    stored = ctx.settings.get("system", "version") or here
    if not ctx.prompter.interactive:
        return stored, tags
    options = [(here, f"{here} (as now)")] + [(t, t) for t in tags if t != here]
    return ctx.prompter.choose("Which version of the system?", options,
                               stored if stored in dict(options) else here), tags


def choose_roles(ctx):
    s, ask = ctx.settings, ctx.prompter
    if not ask.interactive:
        return s.roles()
    options = []
    for role in ALL:
        label = role.label
        if not role.supported(ctx.platform):
            label += f"  -- not yet on {ctx.platform}"
        options.append((role.name, label))
    picked = ask.checklist("What should run on this machine?", options, s.roles())
    for role in ALL:
        s.set_flag("roles", role.name, role.name in picked)
    return picked


def archive_source_in_place(suite):
    """Whether the archive's source for `suite` and its key are both there."""
    try:
        return (archive.KEYRING.is_file()
                and archive.SOURCES.read_text() == archive.sources_text(suite))
    except OSError:
        return False


def ensure_archive(ctx):
    """The public archive's apt source, written through a3-root when it is
    missing or differs: once, before the roles, when the apps come from it."""
    if ctx.from_source or ctx.platform not in APT_PLATFORMS:
        return
    if ctx.settings.get("system", "archive") == "lan":
        ctx.runner.log(f"Archive: lan -- the apt source {LAN_SOURCE}, set up by hand, "
                       "is used; nothing is written.")
        return
    try:
        suite = archive.suite_for(os_release(OS_RELEASE))
    except archive.ArchiveError as error:
        raise RoleError(str(error))
    if archive_source_in_place(suite):
        return
    ctx.runner.log("\n=== The A3 archive ===")
    ctx.runner.run(archive.a3_root_command(ctx, "source", suite), root=True)


def install_packages(ctx, names):
    """What the roles need, in one apt call before any of them: each role
    names its own, none relies on another's package."""
    packages = needed_packages(names, from_source=ctx.from_source)
    if not packages or ctx.platform not in APT_PLATFORMS:
        return
    ctx.runner.log("\n=== Packages for the roles ===")
    ctx.runner.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                    *packages], root=True)


def install_screen(ctx, names):
    """The autologin into X, once for all screen roles. A result row, or
    None when no chosen role needs a screen."""
    if not needs_screen(names):
        return None
    ctx.runner.log("\n=== Screen: autologin on tty1, X with i3 ===")
    try:
        problems = set_up_screen(ctx)
    except CommandFailed as error:
        return ("autologin", f"ERROR: {error}")
    if problems:
        return ("autologin", "WARNING: " + "; ".join(problems))
    return ("autologin", "ok")


def install_roles(ctx, names):
    """The archive, the packages, the screen, then each role in turn until
    one fails. A screen that only warns does not stop the roles."""
    if names:
        ensure_archive(ctx)
    install_packages(ctx, names)
    results = []
    screen = install_screen(ctx, names)
    if screen:
        results.append(screen)
        if screen[1].startswith("ERROR"):
            return results
    for name in names:
        ctx.runner.log(f"\n=== {BY_NAME[name].label} ===")
        try:
            BY_NAME[name].install(ctx)
            record_installed(ctx, name)
            results.append((name, "ok"))
        except (RoleError, CommandFailed) as error:
            results.append((name, f"ERROR: {error}"))
            break
    return results


def apply_roles(ctx, names, discover=discover_roles, refused=None):
    """The deselected roles leave first -- a Core leaving frees JACK and the
    ports a new role may need -- then the chosen ones install.
    A refused role ({name: why}) is still chosen, so an installed one does
    not leave, but it does not install either.
    (rows of the roles that were to leave, rows of the install)."""
    refused = refused or {}
    left = leave_roles(ctx, names, discover)
    rows = [(name, f"REFUSED: {refused[name]}") for name in names if name in refused]
    return left, rows + install_roles(ctx, [n for n in names if n not in refused])


def refused_roles(ctx, names):
    """{name: why} for the chosen roles this machine may not have: the Core
    anywhere but on the truth's core address."""
    if "core" not in names:
        return {}
    ctx.runner.log("\n=== One Core on the LAN ===")
    why = check_core(ctx)
    if why is None:
        return {}
    ctx.runner.log(f"A³ Core refused: {why}")
    return {"core": why}


def refused_together(names):
    """Why the named roles cannot share a machine, or None: a role that
    excludes every other (the laptop is a whole rig by itself)."""
    for name in names:
        others = [other for other in names if other != name]
        if BY_NAME[name].excludes_other_roles and others:
            return (f"The role {name} excludes every other role on its machine, here "
                    f"{', '.join(others)}: choose {name} alone or without it.")
    return None


def refused_from_source(names, from_source):
    """Why --from-source cannot install the named roles, or None: a role
    whose apps come from the archive only. Asked before the old roles leave."""
    if not from_source:
        return None
    packages_only = [name for name in names if BY_NAME[name].packages_only]
    if not packages_only:
        return None
    return (f"The role {', '.join(packages_only)} is packages only: its apps come from "
            "the archive. Run the installer without --from-source.")


NO_CHECKOUT_VERSION = "the archive's packages"


def choose_checkout(ctx, args, roles):
    """The version, its checkout and catch-up; none of it for roles that need
    no checkout (their apps come from the archive, they read no submodule)."""
    if roles and all(BY_NAME[name].runs_without_checkout for name in roles):
        return NO_CHECKOUT_VERSION
    version = choose_version(ctx, args)
    if version != release.current(ctx.runner, REPO):
        release.check_out(ctx.runner, REPO, version)
    release.catch_up(ctx.runner, REPO, version)
    ctx.settings.set("system", "version", version)
    return version


def touched_roles(ctx, chosen):
    """The chosen roles and those that leave this run: the place check and
    the checkout hold for both (leaving the laptop needs neither)."""
    installed, _found = installed_now(ctx, discover_roles)
    return list(chosen) + deselected(installed, chosen)


def refuse_place(names, dry_run):
    """Whether this user and checkout may not install `names`; says why."""
    problems = place_problems(REPO, getpass.getuser(), names)
    if not problems or dry_run:
        return False
    print("The installer cannot run like this:\n  " + "\n  ".join(problems)
          + "\nWith --dry-run you can still look at what it would do.", file=sys.stderr)
    return True


def summary_text(version, names, refused):
    installing = [n for n in names if n not in refused]
    text = (f"Version: {version}\nRoles: "
            + (", ".join(BY_NAME[r].label for r in installing) or "none"))
    for name, why in refused.items():
        text += f"\n\nNot installed: {BY_NAME[name].label}\n{why}"
    return text


def main(argv=None):
    args = parse(sys.argv[1:] if argv is None else argv)
    try:
        ssh_key = read_ssh_key(args.ssh_key) if args.ssh_key else None
    except RoleError as error:
        print(error, file=sys.stderr)
        return 2
    settings = Settings(args.config or DEFAULT_PATH)
    platform = platform_name()
    refused_run = refusal(args, settings, State(Path.home() / STATE_FILE),
                          platform, os_release(OS_RELEASE))
    if refused_run:
        print(refused_run, file=sys.stderr)
        return 2
    if not args.from_source:
        # The next run of this machine is an installed one, refused without it (P25).
        settings.set("system", "archive", settings.get("system", "archive"))
    interactive = args.update is None and args.config is None
    runner = Runner(dry_run=args.dry_run)
    ctx = Context(REPO, settings, runner, make_prompter(interactive), platform,
                  from_source=args.from_source)
    ctx.ask_network = args.network
    if args.flash_firmware:
        ctx.answers["flash_firmware"] = True
    if ssh_key:
        ctx.answers["ssh_key"] = ssh_key

    try:
        # The roles before the version: who may run this, from where, and
        # whether the checkout moves at all, all depend on them, and nothing
        # may change before a refusal.
        roles = choose_roles(ctx)
        refused_now = (refused_together(roles)
                    or refused_from_source(roles, ctx.from_source))
        if refused_now:
            print(refused_now, file=sys.stderr)
            return 2
        touched = touched_roles(ctx, roles)
        if refuse_place(touched, args.dry_run):
            return 2
        version = choose_checkout(ctx, args, touched)
        unsupported = [r for r in roles if not BY_NAME[r].supported(ctx.platform)]
        if unsupported:
            raise RoleError(f"Not yet possible on {ctx.platform}: "
                            + ", ".join(BY_NAME[r].label for r in unsupported))
        # Before the questions: the Core's read what this release ships.
        release.update_submodules(runner, REPO, needed_submodules(roles, ctx.from_source))
        for name in roles:
            BY_NAME[name].configure(ctx)

        refused = refused_roles(ctx, roles)
        if ctx.prompter.interactive and not ctx.prompter.yesno(
                summary_text(version, roles, refused) + "\n\nInstall like this?", True):
            print("Cancelled, nothing installed.")
            return 1
        if not args.dry_run and args.config is None:
            settings.save()

        left, results = apply_roles(ctx, roles, refused=refused)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 1
    except (RoleError, CommandFailed) as error:
        print(f"\n{error}", file=sys.stderr)
        return 1

    print(f"\n{getpass.getuser()}@{platform_name()} on {version}:")
    for name, result in left + results:
        print(f"  {name:10} {result}")
    done = {name for name, _ in results}
    skipped = [name for name in roles if name not in done]
    for name in skipped:
        print(f"  {name:10} skipped (after an error)")
    left_failed = any(r.startswith("ERROR") for _, r in left)
    return 0 if all(r == "ok" for _, r in results) and not skipped and not left_failed else 1
