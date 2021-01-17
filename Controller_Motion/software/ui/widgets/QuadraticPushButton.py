from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton

class QuadraticPushButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        print("instantiating QuadraticPushButton")

    def sizeHint(self):
        return QSize(64, 64)
