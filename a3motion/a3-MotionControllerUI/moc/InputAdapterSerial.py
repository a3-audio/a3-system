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

import os

from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject, QMetaObject, QThread

import moc.MotionController

import numpy
import asyncio
import serial_asyncio

class InputAdapterSerial(QThread):
    class SerialProtocol(asyncio.Protocol, QObject):
        poti_changed = Signal(int, int, float)
        encoder_motion = Signal(int, int)
        encoder_pressed = Signal(int)
        encoder_released = Signal(int)
        pad_pressed = Signal(int, int)
        pad_released = Signal(int, int)

        def __init__(self, moc):
            super().__init__()

            self.moc = moc

            self.poti_changed.connect(moc.poti_changed, QtCore.Qt.QueuedConnection)
            self.encoder_motion.connect(moc.encoder_motion, QtCore.Qt.QueuedConnection)
            self.encoder_pressed.connect(moc.encoder_pressed, QtCore.Qt.QueuedConnection)
            self.encoder_released.connect(moc.encoder_released, QtCore.Qt.QueuedConnection)
            self.pad_pressed.connect(moc.pad_pressed, QtCore.Qt.QueuedConnection)
            self.pad_released.connect(moc.pad_released, QtCore.Qt.QueuedConnection)

        def connection_made(self, transport):
            self.transport = transport
            self.transport.serial.rts = False
            print('serial port opened', transport)

        def connection_lost(self, exc):
            print('serial port closed')
            self.transport.loop.stop()

        def data_received(self, data):
            for line in data.decode('utf-8').splitlines():
                words = line.split(":")
                identifier = words[0]

                # Potis
                prefix_poti = "P"
                if identifier.startswith(prefix_poti):
                    value_normalized = numpy.interp(int(words[1]), [0, 1023], [0, 1])
                    poti = int(identifier[len(prefix_poti):])
                    self.poti_changed.emit(poti % 4, poti / 4, value_normalized)

                # Encoder
                prefix_encoder = "Enc"
                if identifier.startswith(prefix_encoder):
                    encoder = int(identifier[len(prefix_encoder):])
                    self.encoder_motion.emit(encoder, step)

                # Encoder Buttons
                prefix_encoder_buttons = "EB"
                if identifier.startswith(prefix_encoder_buttons):
                    encoder_button = int(identifier[len(prefix_encoder_buttons):])
                    self.encoder_pressed.emit(encoder_button)

                # Buttons
                prefix_buttons = "B"
                if identifier.startswith(prefix_buttons):
                    button = int(identifier[len(prefix_buttons):])
                    if int(words[1]) == 1:
                        self.pad_pressed.emit(button % 4, button / 4)
                    else:
                        self.pad_released.emit(button % 4, button / 4)


    def __init__(self, moc, serialDevice, baudRate):
        super(InputAdapterSerial, self).__init__()
        self.moc = moc
        self.serialDevice = serialDevice
        self.baudRate = baudRate
        self.coro = None
        self.moc.pad_led.connect(self.handle_pad_led, QtCore.Qt.QueuedConnection)

        if serialDevice != "":
            self.start()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.protocol = InputAdapterSerial.SerialProtocol(self.moc)
            coro = serial_asyncio.create_serial_connection(loop, lambda: self.protocol, self.serialDevice, baudrate=self.baudRate)
            loop.run_until_complete(coro)
            loop.run_forever()
        except Exception as e:
            print(e)
            os._exit(1)

    def handle_pad_led(self, channel, row, color):
        index = row * 4 + channel
        message = "L," + str(index) + "," + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "\n"
        self.protocol.transport.write(message.encode('utf-8'))
