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
            line = data.decode('utf-8')
            words = line.split(":")
            identifier = words[0]
            value = words[1]

            print('identifier: ', identifier)
            print('value: ', value)

            value_normalized = numpy.interp(value, [0, 1023], [0, 1])

            # Potis
            if identifier == "P0":
                self.poti_changed.emit(0, 0, value_normalized)

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
