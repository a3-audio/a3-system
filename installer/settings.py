"""What a machine was set up as, kept between runs.

~/.config/a3/install.conf, plain INI so it can be read and edited by hand and
copied to set up a second machine the same way (`install --config <file>`).
A run starts from what is stored, so Enter keeps every earlier answer.
"""

import configparser
from pathlib import Path

DEFAULT_PATH = Path.home() / ".config" / "a3" / "install.conf"

ROLES = ("core", "stemdeck", "motion", "mixer")

DEFAULTS = {
    "system": {
        # A tag (v03.0) or a branch; empty is "whatever is checked out".
        "version": "",
    },
    "roles": {role: "no" for role in ROLES},
    "core": {
        "configure_network": "no",
        "interface": "eno1",
        "address": "192.168.8.10/24",
        "gateway": "192.168.8.1",
        "dns": "192.168.8.1",
        "bridge_with": "",
        "headless": "no",
        # Which differing parts of ~/.config to replace: "all", "none", or a
        # list like "reaper, i3". Decided 2026-10-04: all, with a backup.
        "replace": "all",
    },
    "motion": {
        # Flash the panel's firmware when its source changed since the last
        # flash: yes, no, or ask.
        "flash_firmware": "ask",
        # A serial device, or "auto".
        "serial_port": "auto",
    },
}


class Settings:
    def __init__(self, path=DEFAULT_PATH):
        self.path = Path(path)
        self._parser = configparser.ConfigParser()
        self._parser.read_dict(DEFAULTS)
        if self.path.exists():
            self._parser.read(self.path)

    def get(self, section, key):
        return self._parser.get(section, key)

    def set(self, section, key, value):
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, str(value))

    def flag(self, section, key):
        return self._parser.getboolean(section, key)

    def set_flag(self, section, key, value):
        self.set(section, key, "yes" if value else "no")

    def roles(self):
        """The roles chosen for this machine, in a fixed order."""
        return [role for role in ROLES if self.flag("roles", role)]

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as out:
            out.write("# a3-system installer: what this machine was set up as.\n"
                      "# Read by the next run; edit by hand or copy to another\n"
                      "# machine and run `install --config <file>`.\n\n")
            self._parser.write(out)
