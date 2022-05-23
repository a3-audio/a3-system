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

import time
import math

import numpy as np

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
from PySide6.QtCore import QObject, QThread, Signal, Slot, QPointF

from moc.MotionControllerPainter import *
from moc.engine.Channel import *
from moc.engine.TempoClock import *
from moc.engine.MotionRecorder import *
from moc.engine.MotionPlayer import *
from moc.engine.OscSender import *

led_color_empty = [0, 0, 0]
led_color_idle = [30, 30, 30]
led_color_recording = [100, 0, 0]
led_color_recording_light = [50, 40, 40]
led_color_playback = [0, 40, 0]
led_color_playback_light = [10, 40, 10]
led_color_playback_dark = [0, 20, 0]
led_color_selected = [40, 40, 40]
# led_color_empty = [0, 0, 0]
# led_color_idle = [80, 80, 80]
# led_color_recording = [255, 0, 0]
# led_color_recording_light = [255, 100, 100]
# led_color_playback = [0, 255, 0]
# led_color_playback_light = [100, 255, 100]
# led_color_playback_dark = [0, 100, 0]
# led_color_selected = [150, 150, 150]


class MotionController(QtOpenGLWidgets.QOpenGLWidget):
    """Main component for the motion controller logic.

    This class acts as the central event dispatcher for input that
    comes from the hardware controls (serial), the main widget and
    mockup UI (qt events), and the the server backend (OSC).

    It handles the UI state logic and delegates the specific tasks
    (drawing, recording and playback of channels, etc.) to designated
    classes.

    While being a QOpenGLWidget to receive input events, the drawing
    logic is delegated to MotionControllerPainter.

    """

    pad_led = Signal(int, int, object)

    @dataclass
    class UIState:
        mouse_pos: QPointF = QPointF(0, 0)
        pads: np.array = np.zeros((4, 4), dtype=bool)
        leds: np.array = np.full((4, 4, 3), led_color_idle)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.channels = None

        self.server_ip = ""
        self.server_port = 0
        self.encoder_base_port = 0

        self.ui_state = MotionController.UIState()
        self.interaction_params = {
            'double_press_time' : 0.250,
        }

        self.clear_press_times_encoder()
        self.clear_press_times_pads()

        self.mouse_pos = (0, 0)

        self.moc_painter = MotionControllerPainter(self)

        self.clock = TempoClock()
        self.recorder = MotionRecorder()
        self.player = MotionPlayer()

        self.clock.tick.connect(self.record_playback_tick)
        self.clock.beat.connect(self.update_pad_leds)

        self.recorder.recording_active.connect(self.recording_active_changed)

    def set_channels(self, channels):
        self.channels = channels
        self.moc_painter.set_channels(channels)
        self.recorder.set_channels(channels)
        self.player.set_channels(channels)

        self.osc_sender = OscSender(len(self.channels),
                                    self.server_ip,
                                    self.server_port,
                                    self.encoder_base_port)

        for channel in self.channels:
            channel.position_changed.connect(self.channel_position_changed)
            channel.position_changed.connect(self.osc_sender.channel_position_changed)

    def paintGL(self):
        self.moc_painter.paintGL()

    def mousePressEvent(self, event):
        self.ui_state.mouse_pos = QPointF(event.x(), event.y())
        if self.moc_painter.center_region_contains(event.pos()):
            if not self.recorder.is_recording() and self.any_pad_pressed():
                self.arm_pressed_patterns()
                self.recorder.prepare_recording(self.clock.measure.next_downbeat())
                self.prepare_play_pressed_patterns(self.clock.measure.next_downbeat())

    def mouseReleaseEvent(self, event):
        if self.recorder.is_recording():
            self.recorder.stop_recording()
            self.disarm_all_patterns()

    def mouseMoveEvent(self, event):
        self.ui_state.mouse_pos = QPointF(event.x(), event.y())
        self.repaint()

    def arm_pressed_patterns(self):
        arm_indices = self.pressed_pad_indices()
        for index in arm_indices:
            channel = self.channels[index[0]]
            channel.patterns[index[1]].arm(channel.record_params.length)
            print(f"armed pattern {index[0]}.{index[1]}")

    def prepare_play_pressed_patterns(self, measure):
        play_indices = self.pressed_pad_indices()
        for index in play_indices:
            channel = self.channels[index[0]]
            pattern_index=index[1]
            self.player.prepare_play_pattern(channel, pattern_index, measure)

    def disarm_all_patterns(self):
        for channel in range(4):
            for pattern in range(4):
                self.channels[channel].patterns[pattern].disarm()

    def pressed_pad_indices(self):
        return np.argwhere(self.ui_state.pads == True)

    def any_pad_pressed(self):
        return np.sum(self.ui_state.pads)

    def record_playback_tick(self, measure):
        normalized_pos = self.moc_painter.normalized_mouse_pos(self.ui_state.mouse_pos)
        self.recorder.record_tick(measure, normalized_pos)
        self.player.playback_tick(measure)

    def recording_active_changed(self, recording_active):
        print(f"recording: {recording_active}")
        self.update_pad_leds()

    def channel_position_changed(self, channel, pos):
        self.repaint()

    @Slot(int, int, float)
    def poti_changed(self, channel, row, value):
        print("channel " + str(channel) + " poti " + str(row) + " value changed: " + str(value))
        if row == 0:
            # TODO: this mapping should happen at a central location, see
            # https://github.com/ambisonic-audio-adventures/Ambijockey/issues/5
            width = np.interp(value, [0,1], [0,180])
            self.channels[channel].ambi_params.width = width
            self.osc_sender.send_width(channel, value)
        if row == 1:
            # TODO: same here
            reverb = np.interp(value, [0, 1], [-69, 0])
            self.channels[channel].ambi_params.side = reverb
            self.osc_sender.send_side(channel, value)
        self.repaint()

    def clear_press_times_encoder(self):
        self.press_times_encoder = np.zeros((4))

    def clear_press_times_pads(self):
        self.press_times_pads = np.zeros((4, 4))

    def detect_double_press_encoder(self, channel):
        press_time = time.time()
        if self.encoder_press_times[channel] + self.interaction_params['double_press_time'] >= press_time:
            self.encoder_double_pressed(channel)
            self.clear_press_times_encoder()
            return True
        else:
            self.press_times_encoder[channel] = press_time
        return False

    def detect_double_press_pads(self, channel, row):
        press_time = time.time()
        if self.press_times_pads[channel, row] + self.interaction_params['double_press_time'] >= press_time:
            self.pad_double_pressed(channel, row)
            self.clear_press_times_pads()
            return True
        else:
            self.press_times_pads[channel, row] = press_time
        return False

    @Slot(int)
    def encoder_pressed(self, channel):
        print("channel " + str(channel) + " encoder pressed")
        # if self.detect_double_press_encoder(channel):
        #     return

    @Slot(int)
    def encoder_double_pressed(self, channel):
        print("channel " + str(channel) + " encoder double pressed")

    @Slot(int)
    def encoder_released(self, channel):
        print("channel " + str(channel) + " encoder released")

    @Slot(int, int)
    def encoder_motion(self, channel, direction):
        print("channel " + str(channel) + " encoder moved in direction: " + str(direction))

    @Slot(int, int)
    def pad_pressed(self, channel, row):
        # print("channel " + str(channel) + " pad " + str(row) + " pressed ")
        if self.detect_double_press_pads(channel, row):
            return
        self.ui_state.pads[channel][row] = True
        if not self.channels[channel].is_pattern_empty(row):
            self.player.prepare_play_pattern(self.channels[channel], row, self.clock.measure.next_downbeat())
        self.update_pad_leds()

    @Slot(int, int)
    def pad_double_pressed(self, channel, row):
        # print(f"pad {channel} {row} double pressed")
        if not self.channels[channel].is_pattern_empty(row):
            if self.player.is_pattern_playing(self.channels[channel], row):
                self.player.stop_channel(self.channels[channel])
            else:
                self.player.play_pattern(self.channels[channel], row)
            self.update_pad_leds()

    @Slot(int, int)
    def pad_released(self, channel, row):
        # print("channel " + str(channel) + " pad " + str(row) + " released ")
        self.ui_state.pads[channel][row] = False
        self.update_pad_leds()

    def update_pad_leds(self, measure=None):
        if not measure:
            measure = self.clock.measure
        print(measure)

        for channel in self.channels:
            for row in range(4):
                # default: empty pattern slot
                color = led_color_empty

                # if pattern is armed light up red and blink during record
                # depending on wether pattern is playing simultaneously
                if channel.is_pattern_armed(row):
                    if self.recorder.is_recording():
                        color = (led_color_recording if measure.beat % 2 == 0
                                 else led_color_playback if self.player.is_pattern_playing(channel, row)
                                 else led_color_recording_light)
                    else:
                        color = led_color_recording_light
                # otherwise light up as selected if pressed,
                # depending on playback state
                elif [channel.index, row] in self.pressed_pad_indices().tolist():
                    if self.player.is_pattern_playing(channel, row):
                        color = led_color_playback_light
                    else:
                        color = led_color_selected

                # pattern is not pressed but playing
                elif self.player.is_pattern_playing(channel, row):
                    color = led_color_playback

                # pattern is not playing but prepared
                elif self.player.is_pattern_prepared(channel, row):
                    color = led_color_playback_dark

                # pattern is not (playing or prepared) and not empty
                elif not channel.is_pattern_empty(row):
                    color = led_color_idle

                # emit signal only if cached state differs
                if (color != self.ui_state.leds[row, channel.index]).any():
                    self.pad_led.emit(channel.index, row, color)
                    self.ui_state.leds[row, channel.index] = color
