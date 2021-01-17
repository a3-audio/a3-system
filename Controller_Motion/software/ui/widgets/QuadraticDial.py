from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial

class QuadraticDial(QDial):
    def __init__(self, parent):
        super().__init__(parent)
        print("instantiating QuadraticDial")

    def sizeHint(self):
        print("calling sizeHint")
        return QSize(64, 64)
