"""Motion UI and the panel's firmware, on whatever machine the PCB is on.

Motion UI comes as the Debian package `a3-motion-ui` (2026-10-08). It is built
from the ui commit that a3-motion pins, installed with apt and held. The
package carries the unit, its working directory and its seed. The old drop-in
that pointed the hand unit at a build in the checkout is set aside like any
drop-in that sets what is started.

The ESP32 panel is flashed with PlatformIO when its firmware changed since
the last flash -- told by the git tree of a3-motion/firmware -- and the user
gets the group dialout, which the PCB's serial port belongs to. The panel's
port is found by its USB ID, read from the firmware's board file, the same
entry PlatformIO finds it by: its tty number differs between machines.
"""

import getpass
import grp
import json
from pathlib import Path

from .. import package as debs
from . import apppackage
from .apppackage import has_packaging
from .base import (JUCE_PACKAGES, SCREEN_PACKAGES, Role, RoleError, ensure_juce,
                   enable_and_restart, systemctl_user)

UI = Path("a3-motion/ui")
FIRMWARE = Path("a3-motion/firmware")
BOARD_FILE = FIRMWARE / "boards" / "esp32-s3-devkitc-1-n16r8.json"
BY_ID = Path("/dev/serial/by-id")
SYS_TTY = Path("/sys/class/tty")
PIO_VENV = Path(".local/share/a3/platformio")
UNIT = "a3-motion.service"
# The drop-in the installer wrote before the package; only leaving removes it.
OLD_DROP_IN = "a3-system.conf"
PACKAGE = "a3-motion-ui"
APP = apppackage.AppPackage(PACKAGE, UNIT)


def pinned_commit(ctx):
    """The ui commit the release pins: the umbrella pins a3-motion, a3-motion pins ui."""
    motion = ctx.runner.output(["git", "-C", ctx.repo, "rev-parse", "HEAD:a3-motion"]).strip()
    return ctx.runner.output(["git", "-C", ctx.repo / "a3-motion", "rev-parse",
                              f"{motion}:ui"]).strip()


def package_is_installed(ctx):
    from ..leave import package_installed  # leave imports the roles
    return package_installed(PACKAGE)


def panel_usb_ids(board_file):
    """The panel's USB IDs as sysfs writes them: ("1a86", "55d3")."""
    hwids = json.loads(Path(board_file).read_text())["build"]["hwids"]
    return {(vid.lower().removeprefix("0x"), pid.lower().removeprefix("0x"))
            for vid, pid in hwids}


def usb_id(tty, sys_tty):
    """A tty's USB vendor and product, from the USB device above it in sysfs.

    An ACM tty sits directly under the USB interface, a usb-serial one a level
    deeper; the USB device is the first parent with an idVendor.
    """
    node = (sys_tty / tty / "device").resolve()
    for parent in (node, *node.parents):
        vendor, product = parent / "idVendor", parent / "idProduct"
        if vendor.is_file() and product.is_file():
            return vendor.read_text().strip(), product.read_text().strip()
    return None


def serial_candidates(usb_ids, by_id=None, sys_tty=None):
    """The panel's serial devices by their stable names."""
    by_id = by_id or BY_ID
    sys_tty = sys_tty or SYS_TTY
    if not by_id.is_dir():
        return []
    return sorted(str(link) for link in by_id.iterdir()
                  if usb_id(link.resolve().name, sys_tty) in usb_ids)


class Motion(Role):
    name = "motion"
    label = "Motion UI with the PCB on this machine (incl. firmware)"
    submodules = ("a3-motion",)
    platforms = ("debian",)
    # gsl for the motion engine, serial and gpiod for the V3 hardware interface.
    packages = SCREEN_PACKAGES + JUCE_PACKAGES + (
        "libgsl-dev", "libgpiod-dev", "libserial-dev")
    needs_screen = True

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        if ask.interactive:
            s.set("motion", "flash_firmware", ask.choose(
                "Flash the Motion panel firmware when it has changed?",
                [("yes", "yes, always"), ("ask", "ask each time"), ("no", "no")],
                s.get("motion", "flash_firmware")))

    def install(self, ctx):
        ui = ctx.repo / UI
        commit = pinned_commit(ctx)
        if not has_packaging(ctx, ui, commit):
            raise RoleError(f"a3-motion/ui at {commit[:10]} has no packaging/stage: a3-motion's "
                            "ui pin is older than the package; raise it first.")
        juce = ensure_juce(ctx)
        apppackage.refuse_shadowing_leftovers(ctx, APP)
        deb = apppackage.build(ctx, APP, ui, commit, juce)
        apppackage.install(ctx, APP, deb)
        self._dialout(ctx)
        self._firmware(ctx)
        enable_and_restart(ctx, UNIT)
        apppackage.check_packaged_unit_wins(ctx, APP)

    stays = ("the build cache ~/.cache/a3-build/a3-motion-ui and the packages in ~/a3-debs",
             "~/.local/share/a3-motion (config, skins, patterns, takes) "
             "and the log in ~/.local/state/a3-motion",
             "drop-ins made by hand", "the membership in dialout")

    def leaving_units(self, ctx):
        # A hand unit is the service that runs; it is not ours to stop.
        return [] if apppackage.hand_made_unit(ctx, APP) else [UNIT]

    def leaving_files(self, ctx):
        """The installer's drop-in of before the package; the unit is the package's."""
        return [ctx.user_units / f"{UNIT}.d" / OLD_DROP_IN]

    def leaving_kept(self, ctx):
        hand = apppackage.hand_made_unit(ctx, APP)
        return [hand] if hand else []

    def leaving_packages(self, ctx):
        return [PACKAGE]

    def uninstall(self, ctx):
        super().uninstall(ctx)
        if not package_is_installed(ctx):
            return
        apppackage.remove(ctx, APP)

    def _dialout(self, ctx):
        user = getpass.getuser()
        try:
            members = grp.getgrnam("dialout").gr_mem
        except KeyError:
            return
        if user in members:
            return
        ctx.runner.run(["usermod", "-aG", "dialout", user], root=True)
        ctx.runner.log("Note: dialout only takes effect after the next login "
                       "(or reboot). Until then Motion UI cannot find the PCB.")

    def _firmware(self, ctx):
        run, s = ctx.runner, ctx.settings
        tree = run.output(["git", "rev-parse", f"HEAD:{FIRMWARE.name}"],
                          cwd=ctx.repo / FIRMWARE.parent).strip()
        if ctx.answers.get("flash_firmware"):
            self.flash(ctx, tree)
            return
        if ctx.state.get("motion", "firmware_tree") == tree:
            run.log("Firmware unchanged since the last flash.")
            return
        mode = s.get("motion", "flash_firmware")
        if mode == "no":
            run.log("Firmware has changed, flashing is turned off.")
            return
        if mode == "ask" and not ctx.prompter.yesno(
                "The Motion panel firmware has changed. Flash it now?", False):
            run.log("Firmware not flashed. To do it later: install --flash-firmware")
            return
        self.flash(ctx, tree)

    def flash(self, ctx, tree):
        run, s = ctx.runner, ctx.settings
        port = s.get("motion", "serial_port")
        if port == "auto":
            usb_ids = panel_usb_ids(ctx.repo / BOARD_FILE)
            found = serial_candidates(usb_ids)
            if len(found) == 1:
                port = found[0]
            elif ctx.prompter.interactive and found:
                port = ctx.prompter.choose("Which port is the Motion panel on?",
                                           [(p, p) for p in found], found[0])
            else:
                ids = ", ".join(f"{v}:{p}" for v, p in sorted(usb_ids))
                raise RoleError("Motion panel not found unambiguously "
                                f"({', '.join(found) or f'no device with USB ID {ids}'}). "
                                "Set serial_port under [motion] in install.conf.")
        pio = self._platformio(ctx)
        # Motion UI holds the port; it is stopped for the flash and started
        # again even when the flash fails, so a failed flash is not also a
        # dark screen.
        systemctl_user(ctx, "stop", "a3-motion.service", check=False)
        try:
            run.run([pio, "run", "--target", "upload", "--upload-port", port],
                    cwd=ctx.repo / FIRMWARE)
        finally:
            systemctl_user(ctx, "start", "a3-motion.service", check=False)
        ctx.state.set("motion", "firmware_tree", tree, dry_run=run.dry_run)

    def _platformio(self, ctx):
        venv = ctx.home / PIO_VENV
        pio = venv / "bin" / "pio"
        if not pio.exists():
            ctx.runner.run(["python3", "-m", "venv", venv])
            ctx.runner.run([venv / "bin" / "pip", "install", "--quiet", "platformio"])
        return pio
