"""StemDeck and Motion UI as Debian packages: the steps both roles take the
same way (extracted from roles/stemdeck.py at its second user, 2026-10-08).

The .deb is built from the pinned commit by installer/package.py into
~/.cache/a3-build and ~/a3-debs -- never in a checkout a unit starts from --
then installed with apt and held. A unit file in ~/.config/systemd/user
shadows the packaged one, and so does a drop-in that sets what the unit
starts or where: both are disabled and renamed, never deleted, right before
apt, and put back if apt does not finish -- a Ctrl-C at the sudo prompt
included. A drop-in that only adds settings (a3-core.conf, display.conf)
stays and applies to the packaged unit.
"""

from dataclasses import dataclass
from pathlib import Path

from .. import package as debs
from .base import RoleError, systemctl_user

BEFORE_PACKAGE = ".before-package"
# -j2: a -j4 build on a3nuc1 made the desk lag (2026-10-02).
BUILD_JOBS = 2
PACKAGED_UNITS = Path("/usr/lib/systemd/user")
# A drop-in setting one of these replaces what the packaged unit starts, or
# where (a3nuc1's zz-branch-test.conf, the installer's own a3-system.conf of
# before the package, a3nuc2's build.conf).
SHADOWING_KEYS = ("ExecStart", "ExecStartPre", "WorkingDirectory")
DISABLED = "disabled"


@dataclass(frozen=True)
class AppPackage:
    package: str
    unit: str

    @property
    def packaged_unit(self):
        return str(PACKAGED_UNITS / self.unit)


def build(ctx, app, source, commit, juce):
    """The .deb of `commit` of the repository at `source`, built through the
    CLI of installer/package.py (which lowers itself to nice 19); its path."""
    out = ctx.home / "a3-debs"
    cache = ctx.home / ".cache" / "a3-build"
    ctx.runner.run(["python3", ctx.repo / "installer" / "package.py", source,
                    "--rev", commit, "--out", out, "--cache", cache,
                    "--jobs", BUILD_JOBS, "--juce", juce])
    return debs.deb_path(out, app.package, debs.version_of(source, commit))


def _aside(path):
    return path.with_name(path.name + BEFORE_PACKAGE)


def hand_unit(ctx, app):
    return ctx.user_units / app.unit


def shadowing_lines(text):
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("#", ";")) or "=" not in stripped:
            continue
        if stripped.split("=", 1)[0].strip() in SHADOWING_KEYS:
            found.append(stripped)
    return found


def shadowing_drop_ins(ctx, app):
    folder = ctx.user_units / f"{app.unit}.d"
    if not folder.is_dir():
        return []
    return sorted(path for path in folder.glob("*.conf")
                  if path.is_file() and shadowing_lines(path.read_text(errors="replace")))


def refuse_shadowing_leftovers(ctx, app):
    """Up front, before anything is built: what the installer will not resolve."""
    hand = hand_unit(ctx, app)
    if hand.is_symlink():
        raise RoleError(f"{hand} is a symlink and would shadow the package's unit; "
                        "remove it by hand and run the installer again.")
    for path in ([hand] if hand.is_file() else []) + shadowing_drop_ins(ctx, app):
        if _aside(path).exists():
            raise RoleError(f"{path} and {_aside(path)} both exist; move one of them away "
                            "by hand -- the installer overwrites neither.")


def _set_aside(ctx, app, done):
    hand = hand_unit(ctx, app)
    targets = ([hand] if hand.is_file() else []) + shadowing_drop_ins(ctx, app)
    if hand.is_file():
        done.append(DISABLED)
        systemctl_user(ctx, "disable", app.unit, check=False)
    for path in targets:
        note = ""
        if path != hand:
            text = path.read_text(errors="replace")
            shadowing = shadowing_lines(text)
            others = [l.strip() for l in text.splitlines()
                      if "=" in l and not l.strip().startswith(("#", ";"))
                      and l.strip() not in shadowing]
            note = f" It also set: {'; '.join(others)}." if others else ""
        ctx.runner.log(f"{path} would shadow the package's unit: set aside as "
                       f"{_aside(path).name}.{note}")
        ctx.runner.run(["mv", "-n", path, _aside(path)])
        done.append(path)


def _put_back(ctx, app, done):
    if not done:
        return
    ctx.runner.log(f"the package did not go in: {app.unit} is put back as it was.")
    for path in reversed([d for d in done if d != DISABLED]):
        ctx.runner.run(["mv", "-n", _aside(path), path], check=False)
    if DISABLED in done:
        systemctl_user(ctx, "enable", app.unit, check=False)


def install(ctx, app, deb):
    done = []
    try:
        _set_aside(ctx, app, done)
        ctx.runner.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y",
                        "--allow-downgrades", "--allow-change-held-packages", deb], root=True)
    except BaseException:
        # BaseException: a Ctrl-C at the sudo prompt must not leave the
        # machine with its unit disabled, renamed and no package either.
        _put_back(ctx, app, done)
        raise
    ctx.runner.run(["apt-mark", "hold", app.package], root=True)


def fragment_path(ctx, app):
    return ctx.runner.output(["systemctl", "--user", "show", "-p", "FragmentPath",
                              "--value", app.unit]).strip()


def check_packaged_unit_wins(ctx, app):
    if ctx.runner.dry_run:
        ctx.runner.log(f"# dry run: the check that nothing shadows {app.packaged_unit} is skipped.")
        return
    found = fragment_path(ctx, app)
    if found != app.packaged_unit:
        raise RoleError(f"{app.unit} runs from {found}, not {app.packaged_unit}: a unit file "
                        "there shadows the package. Move it aside and run the installer again.")
    left = shadowing_drop_ins(ctx, app)
    if left:
        raise RoleError(f"{', '.join(str(p) for p in left)} still set what {app.unit} starts "
                        "or where; move them aside and run the installer again.")


def remove(ctx, app):
    ctx.runner.run(["apt-mark", "unhold", app.package], root=True)
    ctx.runner.run(["env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "remove", "-y",
                    app.package], root=True)
