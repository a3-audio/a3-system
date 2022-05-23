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
from PySide6.QtWidgets import QPushButton

class QuadraticPushButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

    def sizeHint(self):
        return QSize(64, 64)
