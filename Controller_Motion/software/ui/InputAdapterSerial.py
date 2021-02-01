import os

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject, QMetaObject, QThread
from MotionControllerDisplay import MotionControllerDisplay

import numpy
import asyncio
import serial_asyncio

class InputAdapterSerial(QThread):
    class SerialProtocol(asyncio.Protocol, QObject):
        poti_changed = Signal(int, int, float)
        encoder_motion = Signal(int, int)
        encoder_pressed = Signal(int)
        encoder_released = Signal(int)
        button_pressed = Signal(int, int)
        button_released = Signal(int, int)

        def __init__(self, mocDisplay):
            super().__init__()

            self.mocDisplay = mocDisplay

            self.poti_changed.connect(mocDisplay.poti_changed, QtCore.Qt.QueuedConnection)
            self.encoder_motion.connect(mocDisplay.encoder_motion, QtCore.Qt.QueuedConnection)
            self.encoder_pressed.connect(mocDisplay.encoder_pressed, QtCore.Qt.QueuedConnection)
            self.encoder_released.connect(mocDisplay.encoder_released, QtCore.Qt.QueuedConnection)
            self.button_pressed.connect(mocDisplay.button_pressed, QtCore.Qt.QueuedConnection)
            self.button_released.connect(mocDisplay.button_released, QtCore.Qt.QueuedConnection)

        def connection_made(self, transport):
            self.transport = transport
            print('serial port opened', transport)

        def connection_lost(self, exc):
            print('serial port closed')
            self.transport.loop.stop()

        def data_received(self, data):
            for line in data.decode('utf-8').splitlines():
                words = line.split(":")
                identifier = words[0]
                value = words[1]

                print('identifier: ', identifier)
                print('value: ', value)

                value_normalized = numpy.interp(value, [0, 1023], [0, 1])

                # Potis
                if identifier == "P0":
                    self.poti_changed.emit(0, 0, value_normalized)
                if identifier == "P1":
                    self.poti_changed.emit(1, 0, value_normalized)
                if identifier == "P2":
                    self.poti_changed.emit(2, 0, value_normalized)
                if identifier == "P3":
                    self.poti_changed.emit(3, 0, value_normalized)
                if identifier == "P4":
                    self.poti_changed.emit(0, 1, value_normalized)
                if identifier == "P5":
                    self.poti_changed.emit(1, 1, value_normalized)
                if identifier == "P6":
                    self.poti_changed.emit(2, 1, value_normalized)
                if identifier == "P7":
                    self.poti_changed.emit(3, 1, value_normalized)

                # Encoder
                if identifier == "Enc0":
                    self.mocDisplay.encoder_motion(0, step)
                if identifier == "Enc1":
                    self.mocDisplay.encoder_motion(1, step)
                if identifier == "Enc2":
                    self.mocDisplay.encoder_motion(2, step)
                if identifier == "Enc3":
                    self.mocDisplay.encoder_motion(3, step)

                # Encoder Buttons
                if identifier == "EB0":
                    self.mocDisplay.encoder_pressed(0)
                if identifier == "EB1":
                    self.mocDisplay.encoder_pressed(1)
                if identifier == "EB2":
                    self.mocDisplay.encoder_pressed(2)
                if identifier == "EB3":
                    self.mocDisplay.encoder_pressed(3)

                # Buttons
                if identifier == "B0":
                    self.mocDisplay.button_pressed(3,0)
                if identifier == "B1":
                    self.mocDisplay.button_pressed(2,0)
                if identifier == "B2":
                    self.mocDisplay.button_pressed(1,0)
                if identifier == "B3":
                    self.mocDisplay.button_pressed(0,0)
                if identifier == "B4":
                    self.mocDisplay.button_pressed(3,1)
                if identifier == "B5":
                    self.mocDisplay.button_pressed(2,1)
                if identifier == "B6":
                    self.mocDisplay.button_pressed(1,1)
                if identifier == "B7":
                    self.mocDisplay.button_pressed(0,1)
                if identifier == "B8":
                    self.mocDisplay.button_pressed(3,2)
                if identifier == "B9":
                    self.mocDisplay.button_pressed(2,2)
                if identifier == "B10":
                    self.mocDisplay.button_pressed(1,2)
                if identifier == "B11":
                    self.mocDisplay.button_pressed(0,2)
                if identifier == "B12":
                    self.mocDisplay.button_pressed(3,3)
                if identifier == "B13":
                    self.mocDisplay.button_pressed(2,3)
                if identifier == "B14":
                    self.mocDisplay.button_pressed(1,3)
                if identifier == "B15":
                    self.mocDisplay.button_pressed(0,3)

    def __init__(self, mocDisplay, serialDevice, baudRate):
        super(InputAdapterSerial, self).__init__()
        self.mocDisplay = mocDisplay
        self.serialDevice = serialDevice
        self.baudRate = baudRate
        self.start()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            coro = serial_asyncio.create_serial_connection(loop, lambda: InputAdapterSerial.SerialProtocol(self.mocDisplay), self.serialDevice, baudrate=self.baudRate)
            loop.run_until_complete(coro)
            loop.run_forever()
        except Exception as e:
            print(e)
            os._exit(1)
