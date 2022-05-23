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

import sys
import argparse
import signal

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDial
from PySide6.QtUiTools import QUiLoader

import moc.MotionController
import moc.InputAdapterUI
import moc.InputAdapterSerial

import moc.widgets.QuadraticDial
import moc.widgets.QuadraticPushButton

import moc.engine.Channel

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A3motion Controller.')
    parser.add_argument("--develop", help="run in development mode with mockup UI", action="store_true")
    parser.add_argument("--serial_device", help="the serial port device file to use", default="")
    parser.add_argument("--serial_baudrate", help="the serial port baud rate to use", default=115200)
    parser.add_argument("--server_ip", help="address of the A3core audio server", default="127.0.0.1")
    parser.add_argument("--server_port", help="port of the OSC control server", type=int, default=9000)
    parser.add_argument("--encoder_base_port", help="base port of the StereoEncoder instances", type=int, default=1337)
    args = parser.parse_args()

    # print(args)

    app = QApplication(sys.argv)

    if args.develop:
        ui_file_name = "moc.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        loader.registerCustomWidget(moc.widgets.QuadraticDial.QuadraticDial)
        loader.registerCustomWidget(moc.widgets.QuadraticPushButton.QuadraticPushButton)
        loader.registerCustomWidget(moc.MotionController.MotionController)

        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

        adapter = moc.InputAdapterUI.InputAdapterUI(window.findChild(QWidget, "centralwidget"))
        app.installEventFilter(adapter)

        window.setFixedSize(318, 1050)
        window.show()
    else:
        window = QMainWindow()
        motion_controller = moc.MotionController.MotionController()

        adapter = moc.InputAdapterSerial.InputAdapterSerial(motion_controller, args.serial_device, args.serial_baudrate)
        window.setCentralWidget(motion_controller)
        window.showFullScreen()

    # create channel objects and pass to display widget
    channels = []
    num_channels = 4
    for c in range(num_channels):
        channel = moc.engine.Channel.Channel(c)
        # evenly space channels along circle for initialization
        channel_angle_interval = (360/num_channels)
        channel.ambi_params.azimuth = -180 + channel_angle_interval/2 + c*channel_angle_interval
        channel.ambi_params.width = 45
        channels.append(channel)

    motion_controller = window.findChild(moc.MotionController.MotionController)
    motion_controller.server_ip = args.server_ip
    motion_controller.server_port = args.server_port
    motion_controller.encoder_base_port = args.encoder_base_port
    motion_controller.set_channels(channels)

    sys.exit(app.exec())
