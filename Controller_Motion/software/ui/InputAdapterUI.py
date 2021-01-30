from PySide6.QtCore import SIGNAL, QObject
from PySide6.QtWidgets import QDial, QPushButton

from MotionControllerDisplay import MotionControllerDisplay
from widgets.QuadraticDial import QuadraticDial

class InputAdapterUI:

    def dialTop11_valueChanged(self, value):
        self.mocDisplay.poti_changed(0, 0, value / 1023)
    def dialTop12_valueChanged(self, value):
        self.mocDisplay.poti_changed(0, 1, value / 1023)
    def dialTop21_valueChanged(self, value):
        self.mocDisplay.poti_changed(1, 0, value / 1023)
    def dialTop22_valueChanged(self, value):
        self.mocDisplay.poti_changed(1, 1, value / 1023)
    def dialTop31_valueChanged(self, value):
        self.mocDisplay.poti_changed(2, 0, value / 1023)
    def dialTop32_valueChanged(self, value):
        self.mocDisplay.poti_changed(2, 1, value / 1023)
    def dialTop41_valueChanged(self, value):
        self.mocDisplay.poti_changed(3, 0, value / 1023)
    def dialTop42_valueChanged(self, value):
        self.mocDisplay.poti_changed(3, 1, value / 1023)

    def buttonEncoder1_pressed(self):
        self.mocDisplay.encoder_pressed(0)
    def buttonEncoder1_released(self):
        self.mocDisplay.encoder_released(0)
    def buttonEncoder2_pressed(self):
        self.mocDisplay.encoder_pressed(1)
    def buttonEncoder2_released(self):
        self.mocDisplay.encoder_released(1)
    def buttonEncoder3_pressed(self):
        self.mocDisplay.encoder_pressed(2)
    def buttonEncoder3_released(self):
        self.mocDisplay.encoder_released(2)
    def buttonEncoder4_pressed(self):
        self.mocDisplay.encoder_pressed(3)
    def buttonEncoder4_released(self):
        self.mocDisplay.encoder_released(3)

    def dialBottom1_step(self, step):
        self.mocDisplay.encoder_motion(0, step)
    def dialBottom2_step(self, step):
        self.mocDisplay.encoder_motion(1, step)
    def dialBottom3_step(self, step):
        self.mocDisplay.encoder_motion(2, step)
    def dialBottom4_step(self, step):
        self.mocDisplay.encoder_motion(3, step)

    def button11_pressed(self):
        self.mocDisplay.button_pressed(0, 0)
    def button11_released(self):
        self.mocDisplay.button_released(0, 0)
    def button12_pressed(self):
        self.mocDisplay.button_pressed(0, 1)
    def button12_released(self):
        self.mocDisplay.button_released(0, 1)
    def button13_pressed(self):
        self.mocDisplay.button_pressed(0, 2)
    def button13_released(self):
        self.mocDisplay.button_released(0, 2)
    def button14_pressed(self):
        self.mocDisplay.button_pressed(0, 3)
    def button14_released(self):
        self.mocDisplay.button_released(0, 3)

    def button21_pressed(self):
        self.mocDisplay.button_pressed(1, 0)
    def button21_released(self):
        self.mocDisplay.button_released(1, 0)
    def button22_pressed(self):
        self.mocDisplay.button_pressed(1, 1)
    def button22_released(self):
        self.mocDisplay.button_released(1, 1)
    def button23_pressed(self):
        self.mocDisplay.button_pressed(1, 2)
    def button23_released(self):
        self.mocDisplay.button_released(1, 2)
    def button24_pressed(self):
        self.mocDisplay.button_pressed(1, 3)
    def button24_released(self):
        self.mocDisplay.button_released(1, 3)

    def button31_pressed(self):
        self.mocDisplay.button_pressed(2, 0)
    def button31_released(self):
        self.mocDisplay.button_released(2, 0)
    def button32_pressed(self):
        self.mocDisplay.button_pressed(2, 1)
    def button32_released(self):
        self.mocDisplay.button_released(2, 1)
    def button33_pressed(self):
        self.mocDisplay.button_pressed(2, 2)
    def button33_released(self):
        self.mocDisplay.button_released(2, 2)
    def button34_pressed(self):
        self.mocDisplay.button_pressed(2, 3)
    def button34_released(self):
        self.mocDisplay.button_released(2, 3)

    def button41_pressed(self):
        self.mocDisplay.button_pressed(3, 0)
    def button41_released(self):
        self.mocDisplay.button_released(3, 0)
    def button42_pressed(self):
        self.mocDisplay.button_pressed(3, 1)
    def button42_released(self):
        self.mocDisplay.button_released(3, 1)
    def button43_pressed(self):
        self.mocDisplay.button_pressed(3, 2)
    def button43_released(self):
        self.mocDisplay.button_released(3, 2)
    def button44_pressed(self):
        self.mocDisplay.button_pressed(3, 3)
    def button44_released(self):
        self.mocDisplay.button_released(3, 3)

    def __init__(self, centralWidget):
        self.mocDisplay = centralWidget.findChild(MotionControllerDisplay, "mocDisplay")
        self.centralWidget = centralWidget

        dialTop11 = self.centralWidget.findChild(QDial, "dialTop11")
        dialTop11.valueChanged.connect(self.dialTop11_valueChanged)
        dialTop12 = self.centralWidget.findChild(QDial, "dialTop12")
        dialTop12.valueChanged.connect(self.dialTop12_valueChanged)
        dialTop21 = self.centralWidget.findChild(QDial, "dialTop21")
        dialTop21.valueChanged.connect(self.dialTop21_valueChanged)
        dialTop22 = self.centralWidget.findChild(QDial, "dialTop22")
        dialTop22.valueChanged.connect(self.dialTop22_valueChanged)
        dialTop31 = self.centralWidget.findChild(QDial, "dialTop31")
        dialTop31.valueChanged.connect(self.dialTop31_valueChanged)
        dialTop32 = self.centralWidget.findChild(QDial, "dialTop32")
        dialTop32.valueChanged.connect(self.dialTop32_valueChanged)
        dialTop41 = self.centralWidget.findChild(QDial, "dialTop41")
        dialTop41.valueChanged.connect(self.dialTop41_valueChanged)
        dialTop42 = self.centralWidget.findChild(QDial, "dialTop42")
        dialTop42.valueChanged.connect(self.dialTop42_valueChanged)

        buttonEncoder1 = self.centralWidget.findChild(QPushButton, "buttonEncoder1")
        buttonEncoder1.pressed.connect(self.buttonEncoder1_pressed)
        buttonEncoder1.released.connect(self.buttonEncoder1_released)
        buttonEncoder2 = self.centralWidget.findChild(QPushButton, "buttonEncoder2")
        buttonEncoder2.pressed.connect(self.buttonEncoder2_pressed)
        buttonEncoder2.released.connect(self.buttonEncoder2_released)
        buttonEncoder3 = self.centralWidget.findChild(QPushButton, "buttonEncoder3")
        buttonEncoder3.pressed.connect(self.buttonEncoder3_pressed)
        buttonEncoder3.released.connect(self.buttonEncoder3_released)
        buttonEncoder4 = self.centralWidget.findChild(QPushButton, "buttonEncoder4")
        buttonEncoder4.pressed.connect(self.buttonEncoder4_pressed)
        buttonEncoder4.released.connect(self.buttonEncoder4_released)

        dialBottom1 = self.centralWidget.findChild(QuadraticDial, "dialBottom1")
        dialBottom1.step.connect(self.dialBottom1_step)
        dialBottom2 = self.centralWidget.findChild(QuadraticDial, "dialBottom2")
        dialBottom2.step.connect(self.dialBottom2_step)
        dialBottom3 = self.centralWidget.findChild(QuadraticDial, "dialBottom3")
        dialBottom3.step.connect(self.dialBottom3_step)
        dialBottom4 = self.centralWidget.findChild(QuadraticDial, "dialBottom4")
        dialBottom4.step.connect(self.dialBottom4_step)

        button11 = self.centralWidget.findChild(QPushButton, "button11")
        button11.pressed.connect(self.button11_pressed)
        button11.released.connect(self.button11_released)
        button12 = self.centralWidget.findChild(QPushButton, "button12")
        button12.pressed.connect(self.button12_pressed)
        button12.released.connect(self.button12_released)
        button13 = self.centralWidget.findChild(QPushButton, "button13")
        button13.pressed.connect(self.button13_pressed)
        button13.released.connect(self.button13_released)
        button14 = self.centralWidget.findChild(QPushButton, "button14")
        button14.pressed.connect(self.button14_pressed)
        button14.released.connect(self.button14_released)

        button21 = self.centralWidget.findChild(QPushButton, "button21")
        button21.pressed.connect(self.button21_pressed)
        button21.released.connect(self.button21_released)
        button22 = self.centralWidget.findChild(QPushButton, "button22")
        button22.pressed.connect(self.button22_pressed)
        button22.released.connect(self.button22_released)
        button23 = self.centralWidget.findChild(QPushButton, "button23")
        button23.pressed.connect(self.button23_pressed)
        button23.released.connect(self.button23_released)
        button24 = self.centralWidget.findChild(QPushButton, "button24")
        button24.pressed.connect(self.button24_pressed)
        button24.released.connect(self.button24_released)

        button31 = self.centralWidget.findChild(QPushButton, "button31")
        button31.pressed.connect(self.button31_pressed)
        button31.released.connect(self.button31_released)
        button32 = self.centralWidget.findChild(QPushButton, "button32")
        button32.pressed.connect(self.button32_pressed)
        button32.released.connect(self.button32_released)
        button33 = self.centralWidget.findChild(QPushButton, "button33")
        button33.pressed.connect(self.button33_pressed)
        button33.released.connect(self.button33_released)
        button34 = self.centralWidget.findChild(QPushButton, "button34")
        button34.pressed.connect(self.button34_pressed)
        button34.released.connect(self.button34_released)

        button41 = self.centralWidget.findChild(QPushButton, "button41")
        button41.pressed.connect(self.button41_pressed)
        button41.released.connect(self.button41_released)
        button42 = self.centralWidget.findChild(QPushButton, "button42")
        button42.pressed.connect(self.button42_pressed)
        button42.released.connect(self.button42_released)
        button43 = self.centralWidget.findChild(QPushButton, "button43")
        button43.pressed.connect(self.button43_pressed)
        button43.released.connect(self.button43_released)
        button44 = self.centralWidget.findChild(QPushButton, "button44")
        button44.pressed.connect(self.button44_pressed)
        button44.released.connect(self.button44_released)
