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

from PySide6.QtCore import QObject, Signal

from moc.engine.TempoClock import *

class MotionRecorder(QObject):
    recording_active = Signal(bool)

    def __init__(self):
        super().__init__()

        self.channels = []
        self.prepared = False
        self.recording = False
        self.measure_trigger = TempoClock.Measure()

    def set_channels(self, channels):
        self.channels = channels

    def prepare_recording(self, measure):
        self.measure_start = measure
        self.prepared = True

    def stop_recording(self):
        self.recording = False
        self.recording_active.emit(False)
        self.prepared = False

    def is_recording(self):
        return self.recording

    def record_tick(self, measure, position):
        if self.prepared and measure.tick_global() == self.measure_start.tick_global():
            self.recording = True
            self.recording_active.emit(True)

        if self.recording:
            for channel in self.channels:
                for pattern in channel.patterns:
                    if pattern.armed:
                        tick_to_write = pattern.tick_in_pattern_relative(measure, self.measure_start)
                        pattern.ticks[tick_to_write] = position
