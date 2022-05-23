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

from PySide6.QtCore import QObject, QThread, Signal

from moc.engine.TempoClock import *
from moc.engine.Pattern import *

class MotionPlayer(QObject):
    @dataclass
    class PlaybackState:
        prepared_pattern: Pattern = None
        playing_pattern: Pattern = None
        measure_trigger: TempoClock.Measure = None
        measure_start: TempoClock.Measure = None

    def __init__(self):
        super().__init__()
        self.channels = []
        self.playback_states = {}

    def set_channels(self, channels):
        self.channels = channels
        for channel in channels:
            self.playback_states[channel] = MotionPlayer.PlaybackState()

    def play_pattern(self, channel, pattern_index):
        self.playback_states[channel].playing_pattern = channel.patterns[pattern_index]

    def prepare_play_pattern(self, channel, pattern_index, measure):
        if not self.playback_states[channel].prepared_pattern is channel.patterns[pattern_index]:
            self.playback_states[channel].prepared_pattern = channel.patterns[pattern_index]
            self.playback_states[channel].measure_trigger = measure

    def is_pattern_prepared(self, channel, pattern_index):
        return self.playback_states[channel].prepared_pattern is channel.patterns[pattern_index]

    def is_pattern_playing(self, channel, pattern_index):
        return self.playback_states[channel].playing_pattern is channel.patterns[pattern_index]

    def playback_tick(self, measure):
        for channel in self.channels:
            state = self.playback_states[channel]
            if state.prepared_pattern is not None and \
               measure.tick_global() == state.measure_trigger.tick_global():
                state.playing_pattern = state.prepared_pattern
                state.prepared_pattern = None
                state.measure_start = state.measure_trigger
                state.measure_trigger = None
            if state.playing_pattern is not None:
                position = self.get_playback_position(channel, measure)
                channel.set_position(position)

    def get_playback_position(self, channel, measure):
        state = self.playback_states[channel]
        pattern = state.playing_pattern
        tick = pattern.tick_in_pattern_relative(measure, state.measure_start)
        return pattern.ticks[tick]

    def stop_channel(self, channel):
        self.playback_states[channel].playing_pattern = None
        self.playback_states[channel].prepared_pattern = None
