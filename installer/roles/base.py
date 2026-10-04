"""What every role has: a name, the platforms it installs on, questions, and
the install itself. And what the roles share: the run's context, the state
file, systemd user units and JUCE."""

import configparser
import os
from pathlib import Path


class RoleError(Exception):
    """A role cannot be installed as asked; the message says why."""


class Context:
    def __init__(self, repo, settings, runner, prompter, platform, home=None):
        self.repo = Path(repo)
        self.settings = settings
        self.runner = runner
        self.prompter = prompter
        self.platform = platform
        self.home = Path(home) if home else Path.home()
        self.state = State(self.home / ".config" / "a3" / "install.state")
        # Answers that hold for this run only, e.g. which parts to replace.
        self.answers = {}

    @property
    def user_units(self):
        return self.home / ".config" / "systemd" / "user"

    def jobs(self):
        return str(os.cpu_count() or 2)


class State:
    """What the installer did that the repository does not record, e.g.
    which firmware was flashed last. Not the settings: those are choices,
    this is history."""

    def __init__(self, path):
        self.path = Path(path)
        self._parser = configparser.ConfigParser()
        if self.path.exists():
            self._parser.read(self.path)

    def get(self, section, key, default=""):
        return self._parser.get(section, key, fallback=default)

    def set(self, section, key, value, dry_run=False):
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)
        if dry_run:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as out:
            self._parser.write(out)


class Role:
    name = ""
    label = ""
    platforms = ()
    # The submodules of this repository the role builds from. Only these are
    # checked out on its machine.
    submodules = ()

    def supported(self, platform):
        return platform in self.platforms

    def configure(self, ctx):
        """Ask what this role needs to know. Answers go to ctx.settings
        (kept) or ctx.answers (this run only)."""

    def install(self, ctx):
        raise NotImplementedError


# -- systemd user units -------------------------------------------------------

def install_user_unit(ctx, source, name=None):
    """The unit file from a component's repository, into ~/.config/systemd/user."""
    source = Path(source)
    if not source.is_file():
        raise RoleError(f"{source.relative_to(ctx.repo)} fehlt in diesem Stand. "
                        "Der Pin im a3-system-Repo ist älter als die Unit; "
                        "erst den Pin hochziehen.")
    target = ctx.user_units / (name or source.name)
    ctx.runner.run(["install", "-D", "-m", "644", source, target])
    return target


def write_drop_in(ctx, unit, name, text):
    target = ctx.user_units / f"{unit}.d" / name
    ctx.runner.log(f"# {target}:\n" + "".join(f"#   {line}\n" for line in text.splitlines()))
    if not ctx.runner.dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    return target


def systemctl_user(ctx, *args, check=True):
    return ctx.runner.run(["systemctl", "--user", *args], check=check)


def enable_and_restart(ctx, unit):
    """Enabled for the next boot, and running the new build now."""
    systemctl_user(ctx, "daemon-reload")
    systemctl_user(ctx, "enable", unit)
    systemctl_user(ctx, "restart", unit)


# -- JUCE -----------------------------------------------------------------------

# The JUCE StemDeck and Motion UI build against, the same on every machine
# and on the developer's. Not the newest: a new JUCE is a change to test
# like any other, and goes into a release on purpose.
JUCE_VERSION = "8.0.12"


def juce_prefix(ctx):
    return ctx.home / "local" / "juce"


def ensure_juce(ctx):
    """JUCE installed to ~/local/juce, where StemDeck and Motion UI look."""
    prefix = juce_prefix(ctx)
    if (prefix / "lib" / "cmake" / f"JUCE-{JUCE_VERSION}").is_dir():
        ctx.runner.log(f"JUCE {JUCE_VERSION} ist da ({prefix}).")
        return prefix
    source = ctx.home / "src" / "JUCE"
    ctx.runner.run(["rm", "-rf", source])
    ctx.runner.run(["git", "clone", "--quiet", "--depth", "1", "--branch", JUCE_VERSION,
                    "https://github.com/juce-framework/JUCE.git", source])
    ctx.runner.run(["cmake", "-S", source, "-B", source / "build",
                    f"-DCMAKE_INSTALL_PREFIX={prefix}", "-DCMAKE_BUILD_TYPE=Release"])
    ctx.runner.run(["cmake", "--build", source / "build", "--target", "install",
                    "-j", ctx.jobs()])
    return prefix
