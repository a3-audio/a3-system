"""A³ Mixer: today a Raspberry Pi 3B with a Teensy. Not installed by this yet.

Named so the choice is visible and says why it cannot be made. The desk's
units live in a3-mixer under platform-config/raspianos/etc/systemd/system/;
a3-mixer.service starts /home/aaa/a3-mixer/software/scripts/a3-mixer.py on
the venv's Python. What is missing is the install itself: no desk install
steps are written yet, and they are not worth writing for this hardware,
because the Pi and the Teensy are to be replaced by a small microcontroller
board with Ethernet. The desk is set up by hand until then (a3-doc,
configuration/mic.md, "Running the desk").
"""

from .base import Role


class Mixer(Role):
    name = "mixer"
    label = "A³ Mixer (Raspberry Pi + Teensy)"
    submodules = ("a3-mixer",)
    platforms = ()

    def install(self, ctx):
        raise NotImplementedError
