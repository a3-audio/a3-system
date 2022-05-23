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

from PySide6.QtCore import SIGNAL, QObject, QEvent
from PySide6.QtWidgets import QDial, QPushButton

import moc.MotionController
import moc.widgets.QuadraticDial

class InputAdapterUI(QObject):
    def __init__(self, centralWidget):
        super().__init__()

        self.moc = centralWidget.findChild(moc.MotionController.MotionController, "motionController")
        self.centralWidget = centralWidget

        for channel in range(4):
            for row in range(2):
                name = "dialTop{}{}".format(channel, row)
                dial = self.centralWidget.findChild(QDial, name)
                dial.valueChanged.connect(lambda x, c=channel, r=row: self.dialTop_valueChanged(c, r, x))

        for channel in range(4):
            name = "buttonEncoder{}".format(channel)
            button = self.centralWidget.findChild(QPushButton, name)
            button.pressed.connect(lambda c=channel: self.buttonEncoder_pressed(c))
            button.released.connect(lambda c=channel: self.buttonEncoder_released(c))

        for channel in range(4):
            name = "dialBottom{}".format(channel)
            dial = self.centralWidget.findChild(moc.widgets.QuadraticDial.QuadraticDial, name)
            dial.step.connect(lambda x, c=channel: self.dialBottom_step(c, x))

        for channel in range(4):
            for row in range(4):
                name = "button{}{}".format(channel, row)
                button = self.centralWidget.findChild(QPushButton, name)
                button.pressed.connect(lambda c=channel, r=row: self.button_pressed(c, r))
                button.released.connect(lambda c=channel, r=row: self.button_released(c, r))

        self.moc.pad_led.connect(self.handle_pad_led)

        self.keyCodeMap = {
            10: (0, 0),
            11: (1, 0),
            12: (2, 0),
            13: (3, 0),
            24: (0, 1),
            25: (1, 1),
            26: (2, 1),
            27: (3, 1),
            38: (0, 2),
            39: (1, 2),
            40: (2, 2),
            41: (3, 2),
            52: (0, 3),
            53: (1, 3),
            54: (2, 3),
            55: (3, 3),
        }

    def eventFilter(self, obj, event):
        is_handled = False
        if event.type() == QEvent.KeyPress or event.type() == QEvent.KeyRelease:
            code = event.nativeScanCode()
            # print(str(code))
            if code in self.keyCodeMap:
                if not event.isAutoRepeat():
                    index = self.keyCodeMap[code]
                    if event.type() == QEvent.KeyPress:
                        self.button_pressed(index[0], index[1])
                    else:
                        self.button_released(index[0], index[1])
                is_handled = True

        if not is_handled:
            # standard event processing
            return QObject.eventFilter(self, obj, event)
        else:
            return True

    def dialTop_valueChanged(self, channel, row, value):
        self.moc.poti_changed(channel, row, value / 1023)

    def buttonEncoder_pressed(self, channel):
        self.moc.encoder_pressed(channel)
    def buttonEncoder_released(self, channel):
        self.moc.encoder_released(channel)

    def dialBottom_step(self, channel, step):
        self.moc.encoder_motion(channel, step)

    def button_pressed(self, channel, row):
        self.moc.pad_pressed(channel, row)
    def button_released(self, channel, row):
        self.moc.pad_released(channel, row)

    def handle_pad_led(self, channel, row, color):
        color_string = "rgb({},{},{})".format(color[0], color[1], color[2])
        style = "QPushButton {background-color: " + color_string + "}"

        button_name = f'button{channel}{row}'
        button = self.centralWidget.findChild(QPushButton, button_name)
        button.setStyleSheet(style)
