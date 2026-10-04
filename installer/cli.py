"""install: set up this machine as a part of the A³ system, or update it.

    install                      ask: version, roles, their settings
    install --update [VERSION]   no questions: the stored roles and settings,
                                 at VERSION (default: the newest tag)
    install --config FILE        no questions: FILE's roles and settings
    install --dry-run            show every command, run none
    install --flash-firmware     flash the Motion panel even if unchanged

The stored answers are in ~/.config/a3/install.conf.
"""

import argparse
import getpass
import sys
from pathlib import Path

from . import release
from .prompt import make_prompter
from .roles import ALL, BY_NAME, needed_submodules
from .roles.base import Context, RoleError
from .settings import DEFAULT_PATH, Settings
from .system import CommandFailed, Runner, platform_name

REPO = Path(__file__).resolve().parents[1]

# Every unit the components ship names /home/aaa/a3-system. Until that is
# written relative, the installer runs from there and as aaa.
EXPECTED_USER = "aaa"
EXPECTED_REPO = Path("/home/aaa/a3-system")


def parse(argv):
    parser = argparse.ArgumentParser(
        prog="install", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", nargs="?", const="", metavar="VERSION")
    parser.add_argument("--config", type=Path, metavar="FILE")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--flash-firmware", action="store_true")
    return parser.parse_args(argv)


def where_problems(repo, user):
    problems = []
    if user != EXPECTED_USER:
        problems.append(f"läuft als {user}, die Units erwarten {EXPECTED_USER}")
    if repo != EXPECTED_REPO:
        problems.append(f"liegt in {repo}, die Units erwarten {EXPECTED_REPO}")
    return problems


def choose_version(ctx, args):
    run, repo = ctx.runner, ctx.repo
    try:
        release.fetch(run, repo)
    except CommandFailed:
        run.log("Keine Verbindung zu GitHub: es gibt nur die Versionen, die schon da sind.")
    tags = release.tags(run, repo)
    here = release.current(run, repo)
    if args.update is not None:
        return args.update or (tags[0] if tags else here)
    stored = ctx.settings.get("system", "version") or here
    if not ctx.prompter.interactive:
        return stored
    options = [(here, f"{here} (wie jetzt)")] + [(t, t) for t in tags if t != here]
    return ctx.prompter.choose("Welcher Stand des Systems?", options,
                               stored if stored in dict(options) else here)


def choose_roles(ctx):
    s, ask = ctx.settings, ctx.prompter
    if not ask.interactive:
        return s.roles()
    options = []
    for role in ALL:
        label = role.label
        if not role.supported(ctx.platform):
            label += f"  -- noch nicht auf {ctx.platform}"
        options.append((role.name, label))
    picked = ask.checklist("Was soll auf diesem Rechner laufen?", options, s.roles())
    for role in ALL:
        s.set_flag("roles", role.name, role.name in picked)
    return picked


def main(argv=None):
    args = parse(sys.argv[1:] if argv is None else argv)
    settings = Settings(args.config or DEFAULT_PATH)
    interactive = args.update is None and args.config is None
    runner = Runner(dry_run=args.dry_run)
    ctx = Context(REPO, settings, runner, make_prompter(interactive), platform_name())
    if args.flash_firmware:
        ctx.answers["flash_firmware"] = True

    problems = where_problems(REPO, getpass.getuser())
    if problems and not args.dry_run:
        print("Der Installer kann so nicht laufen:\n  " + "\n  ".join(problems)
              + "\nMit --dry-run lässt er sich trotzdem ansehen.", file=sys.stderr)
        return 2

    try:
        version = choose_version(ctx, args)
        if version != release.current(runner, REPO):
            release.check_out(runner, REPO, version)
        settings.set("system", "version", version)

        roles = choose_roles(ctx)
        unsupported = [r for r in roles if not BY_NAME[r].supported(ctx.platform)]
        if unsupported:
            raise RoleError(f"Auf {ctx.platform} noch nicht möglich: "
                            + ", ".join(BY_NAME[r].label for r in unsupported))
        # Before the questions: the Core's read what this release ships.
        release.update_submodules(runner, REPO, needed_submodules(roles))
        for name in roles:
            BY_NAME[name].configure(ctx)

        summary = (f"Stand: {version}\nRollen: "
                   + (", ".join(BY_NAME[r].label for r in roles) or "keine"))
        if ctx.prompter.interactive and not ctx.prompter.yesno(
                summary + "\n\nSo installieren?", True):
            print("Abgebrochen, nichts installiert.")
            return 1
        if not args.dry_run and args.config is None:
            settings.save()

        results = []
        for name in roles:
            runner.log(f"\n=== {BY_NAME[name].label} ===")
            try:
                BY_NAME[name].install(ctx)
                results.append((name, "ok"))
            except (RoleError, CommandFailed) as error:
                results.append((name, f"FEHLER: {error}"))
                break
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        return 1
    except (RoleError, CommandFailed) as error:
        print(f"\n{error}", file=sys.stderr)
        return 1

    print(f"\n{getpass.getuser()}@{platform_name()} auf {version}:")
    for name, result in results:
        print(f"  {name:10} {result}")
    skipped = roles[len(results):]
    for name in skipped:
        print(f"  {name:10} übersprungen (nach einem Fehler)")
    return 0 if all(r == "ok" for _, r in results) and not skipped else 1
