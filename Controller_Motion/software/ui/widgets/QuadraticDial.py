from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial
from PySide6.QtCore import Signal

class QuadraticDial(QDial):
    step = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.last_value = self.value()
        self.actionTriggered.connect(self.handle_actionTriggered)

    def handle_actionTriggered(self, action):
        # TODO: clean handling of increment/decrement calculation on keyboard input

        v = self.value()
        if(v > self.last_value):
            if(self.last_value == self.minimum() and v == self.maximum()):
                self.step.emit(-1)
            else:
                self.step.emit(1)
        elif(v < self.last_value):
            if(self.last_value == self.maximum() and v == self.minimum()):
                self.step.emit(1)
            else:
                self.step.emit(-1)

        self.last_value = v

    def sizeHint(self):
        return QSize(64, 64)
