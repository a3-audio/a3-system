# A³ Motion is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³ Motion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³ Motion.  If not, see <https://www.gnu.org/licenses/>.

# © Copyright 2021 Patric Schmitz

from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import QObject, Signal

from moc.engine.Pattern import *

@dataclass
class AmbisonicParams:
    class SpatializationMode(Enum):
        MONO = 1
        STEREO = 2
        VBAP = 3
        AMBI = 4

    width: float = 45
    side: float = 0
    mode: SpatializationMode = SpatializationMode.MONO

@dataclass
class PlaybackParams:
    class PlaybackMode(Enum):
        LOOP = 1
        ONESHOT = 2
        PINGPONG = 3
        FREE = 4

    mode: PlaybackMode = PlaybackMode.LOOP
    invert: bool = False

@dataclass
class RecordParams:
    length: int = 8

class Channel(QObject):
    # channel object, position tuple
    position_changed = Signal(object, object)

    def __init__(self, index):
        super().__init__()

        self.index = index

        self.ambi_params = AmbisonicParams()
        self.playback_params = PlaybackParams()
        self.record_params = RecordParams()

        self.position = None

        # for now each channel owns 4 patterns that are one-to-one
        # mapped to the pads. this is probably subject to change.
        self.patterns = [Pattern() for _ in range(4)]

    def set_position(self, position):
        self.position = position
        self.position_changed.emit(self, position)

    def is_pattern_empty(self, pattern_index):
        return self.patterns[pattern_index].length == 0

    def is_pattern_armed(self, pattern_index):
        return self.patterns[pattern_index].armed
