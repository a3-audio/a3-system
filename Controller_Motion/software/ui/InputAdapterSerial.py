import os

from PySide6 import QtCore
from PySide6.QtCore import SIGNAL, QObject, QMetaObject, QThread
from widgets.MotionControllerDisplay import MotionControllerDisplay

import numpy
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
            line = data.decode('utf-8')
            words = line.split(":")
            identifier = words[0]
            value = words[1]

            # Potis
            if identifier == "P0":
                print('identifier', identifier)
                print('value', value)
                value_normalized = numpy.interp(value, [0, 1023], [0, 1])
                QMetaObject.invokeMethod(self.mocDisplay, self.mocDisplay.poti_changed(0, 0, value_normalized), QtCore.Qt.QueuedConnection)

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
