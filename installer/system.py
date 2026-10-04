"""Running commands, and what kind of machine this is.

Every command goes through Runner, so `--dry-run` shows the whole install
without doing any of it, and the tests can see what would have been run.
"""

import os
import platform
import shlex
import subprocess
from pathlib import Path


class CommandFailed(Exception):
    pass


class Runner:
    def __init__(self, dry_run=False, log=print):
        self.dry_run = dry_run
        self.log = log

    def run(self, args, cwd=None, env=None, root=False, check=True, input=None):
        """Run `args`; as root through sudo when `root`. Returns the exit code."""
        args = [str(a) for a in args]
        if root and os.geteuid() != 0:
            args = ["sudo", *args]
        where = f"  (in {cwd})" if cwd else ""
        self.log(f"$ {shlex.join(args)}{where}")
        if input and self.dry_run:
            self.log("".join(f"    | {line}\n" for line in input.splitlines()).rstrip())
        if self.dry_run:
            return 0
        full_env = None
        if env:
            full_env = dict(os.environ)
            full_env.update(env)
        done = subprocess.run(args, cwd=cwd, env=full_env, text=True, input=input)
        if check and done.returncode != 0:
            raise CommandFailed(f"{shlex.join(args)} ended with {done.returncode}")
        return done.returncode

    def output(self, args, cwd=None):
        """The standard output of a command that only looks. Runs on --dry-run
        too: what it learns decides what the dry run shows."""
        return subprocess.run([str(a) for a in args], cwd=cwd, check=True,
                              capture_output=True, text=True).stdout


def os_release(path="/etc/os-release"):
    values = {}
    try:
        for line in Path(path).read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key] = value.strip('"')
    except OSError:
        pass
    return values


def platform_name():
    """debian, raspios, macos, windows, or other.

    Raspberry Pi OS calls itself debian in ID; it is told apart by the
    machine. Only debian is installed onto today; the others are named so a
    role can say plainly that it does not support them yet.
    """
    system = platform.system()
    if system == "Darwin":
        return "macos"
    if system == "Windows":
        return "windows"
    release = os_release()
    if release.get("ID") == "raspbian" or (
            release.get("ID") == "debian"
            and platform.machine() in ("aarch64", "armv7l")
            and Path("/proc/device-tree/model").exists()
            and "Raspberry Pi" in Path("/proc/device-tree/model").read_text(errors="ignore")):
        return "raspios"
    if release.get("ID") == "debian" or "debian" in release.get("ID_LIKE", ""):
        return "debian"
    return "other"
