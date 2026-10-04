"""Motion UI and the panel's firmware, on whatever machine the PCB is on.

Motion UI is built in the submodule (a3-motion/ui) with its own build.sh,
which also links resources/ and config/ next to the binary. Its unit comes
from its repository and was written for the Raspberry Pi; a drop-in gives
it what any other machine needs (found on a3nuc2, 2026-10-04): DISPLAY,
since the user manager starts it before the X session hands that over; the
working directory, since config/config.json is read relative to it; the
binary built here; and the screen wait from its own repository, since the
Core's copy is not on a machine without the Core.

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

from .base import (Role, RoleError, ensure_juce, enable_and_restart,
                   install_user_unit, systemctl_user, write_drop_in)

UI = Path("a3-motion/ui")
FIRMWARE = Path("a3-motion/firmware")
BOARD_FILE = FIRMWARE / "boards" / "esp32-s3-devkitc-1-n16r8.json"
BY_ID = Path("/dev/serial/by-id")
SYS_TTY = Path("/sys/class/tty")
BINARY = Path("build/src/a3-motion-ui/a3-motion-ui_artefacts/Release/Standalone/a3-motion-ui")
PIO_VENV = Path(".local/share/a3/platformio")


def drop_in_text(ui):
    return (
        "# Written by the a3-system installer. Motion UI's unit is the\n"
        "# Raspberry Pi's; what any machine needs on top (a3nuc2, 2026-10-04):\n"
        "[Service]\n"
        "Environment=DISPLAY=:0\n"
        f"WorkingDirectory={ui}\n"
        "ExecStartPre=\n"
        f"ExecStartPre={ui / 'platform_config' / 'a3-wait-for-the-screen'}\n"
        "ExecStart=\n"
        f"ExecStart={ui / BINARY}\n"
    )


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
    label = "Motion UI mit dem PCB an diesem Rechner (inkl. Firmware)"
    submodules = ("a3-motion",)
    platforms = ("debian",)

    def configure(self, ctx):
        s, ask = ctx.settings, ctx.prompter
        if ask.interactive:
            s.set("motion", "flash_firmware", ask.choose(
                "Firmware des Motion-Panels flashen, wenn sie sich geändert hat?",
                [("yes", "ja, immer"), ("ask", "jedes Mal fragen"), ("no", "nein")],
                s.get("motion", "flash_firmware")))

    def install(self, ctx):
        run = ctx.runner
        ui = ctx.repo / UI
        if not (ui / "build.sh").is_file():
            raise RoleError("a3-motion/ui hat in diesem Stand kein build.sh. "
                            "Der ui-Pin in a3-motion ist zu alt; erst hochziehen.")
        prefix = ensure_juce(ctx)
        run.run(["./build.sh", "-r"], cwd=ui, env={"JUCE_DIR": str(prefix)})

        install_user_unit(ctx, ui / "platform_config" / "a3-motion.service")
        write_drop_in(ctx, "a3-motion.service", "a3-system.conf", drop_in_text(ui))
        self._dialout(ctx)
        self._firmware(ctx)
        enable_and_restart(ctx, "a3-motion.service")

    def _dialout(self, ctx):
        user = getpass.getuser()
        try:
            members = grp.getgrnam("dialout").gr_mem
        except KeyError:
            return
        if user in members:
            return
        ctx.runner.run(["usermod", "-aG", "dialout", user], root=True)
        ctx.runner.log("Hinweis: dialout gilt erst nach dem nächsten Login "
                       "(oder Neustart). Bis dahin findet Motion UI das PCB nicht.")

    def _firmware(self, ctx):
        run, s = ctx.runner, ctx.settings
        tree = run.output(["git", "rev-parse", f"HEAD:{FIRMWARE.name}"],
                          cwd=ctx.repo / FIRMWARE.parent).strip()
        if ctx.answers.get("flash_firmware"):
            self.flash(ctx, tree)
            return
        if ctx.state.get("motion", "firmware_tree") == tree:
            run.log("Firmware unverändert seit dem letzten Flashen.")
            return
        mode = s.get("motion", "flash_firmware")
        if mode == "no":
            run.log("Firmware hat sich geändert, flashen ist abgeschaltet.")
            return
        if mode == "ask" and not ctx.prompter.yesno(
                "Die Firmware des Motion-Panels hat sich geändert. Jetzt flashen?", False):
            run.log("Firmware nicht geflasht. Nachholen: install --flash-firmware")
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
                port = ctx.prompter.choose("An welchem Port hängt das Motion-Panel?",
                                           [(p, p) for p in found], found[0])
            else:
                ids = ", ".join(f"{v}:{p}" for v, p in sorted(usb_ids))
                raise RoleError("Motion-Panel nicht eindeutig gefunden "
                                f"({', '.join(found) or f'kein Gerät mit USB-ID {ids}'}). "
                                "In install.conf unter [motion] serial_port setzen.")
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
