import os

from PySide6 import QtCore
from PySide6.QtCore import SIGNAL, QObject, QMetaObject, QThread
from widgets.MotionControllerDisplay import MotionControllerDisplay

import asyncio
import serial_asyncio

class InputAdapterSerial(QThread):
    class SerialProtocol(asyncio.Protocol):
        def __init__(self, mocDisplay):
            self.mocDisplay = mocDisplay

        def connection_made(self, transport):
            self.transport = transport
            print('serial port opened', transport)

        def connection_lost(self, exc):
            print('serial port closed')
            self.transport.loop.stop()

        def data_received(self, data):
            print('serial data received', repr(data))
            QMetaObject.invokeMethod(self.mocDisplay, self.mocDisplay.button_pressed(channel=0, row=0), QtCore.Qt.QueuedConnection)

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
