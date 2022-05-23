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

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial
from PySide6.QtCore import Signal

class QuadraticDial(QDial):
    step = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.last_value = self.value()
        self.valueChanged.connect(self.handle_valueChanged)

    def handle_valueChanged(self, value):
        # TODO: this works fine for mouse input because all values
        # [min, max] are received. when using keyboard input, going
        # upwards we get (min, max] and going downward we get
        # [min, max) for some reason, which will cause spurious steps
        # when wrapping.
        if(value > self.last_value):
            self.step.emit(-1 if self.last_value == self.minimum() and value == self.maximum() else  1)
        elif(value < self.last_value):
            self.step.emit( 1 if self.last_value == self.maximum() and value == self.minimum() else -1)
        self.last_value = value

    def sizeHint(self):
        return QSize(64, 64)
