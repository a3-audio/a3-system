"""A³ Mixer: a Raspberry Pi with a Teensy. Not installed by this yet.

Named so the choice is visible and says why it cannot be made: the mixer runs
Raspberry Pi OS, and its unit (a3-mixer.service) starts
/home/aaa/a3-mixer/engine/scripts/a3-mixer.py, a path its repository no
longer has (software/scripts since). Both want settling before an installer
lays them down.
"""

from .base import Role


class Mixer(Role):
    name = "mixer"
    label = "A³ Mixer (Raspberry Pi + Teensy)"
    platforms = ()

    def install(self, ctx):
        raise NotImplementedError
