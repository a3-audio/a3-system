import sys
import argparse

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDial
from PySide6.QtUiTools import QUiLoader

from InputAdapterUI import InputAdapterUI
from InputAdapterSerial import InputAdapterSerial

from widgets.QuadraticDial import QuadraticDial
from widgets.QuadraticPushButton import QuadraticPushButton
from widgets.MotionControllerDisplay import MotionControllerDisplay

from Track import Track

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAA Motion Controller.')
    parser.add_argument("--develop", help="run in development mode with mockup UI", action="store_true")
    parser.add_argument("--serial_device", help="the serial port device file to use", default="/dev/ttyACM0")
    parser.add_argument("--serial_baudrate", help="the serial port baud rate to use", default=115200)
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
        loader.registerCustomWidget(QuadraticDial)
        loader.registerCustomWidget(QuadraticPushButton)
        loader.registerCustomWidget(MotionControllerDisplay)

        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

        adapter = InputAdapterUI(window.findChild(QWidget, "centralwidget"))

        window.setFixedSize(318, 1050)
        window.show()
    else:
        window = QMainWindow()
        mocDisplay = MotionControllerDisplay()

        adapter = InputAdapterSerial(mocDisplay, args.serial_device, args.serial_baudrate)
        window.setCentralWidget(mocDisplay)
        window.showFullScreen()

    # create track objects and pass to display widget
    num_tracks = 4
    tracks = [Track() for i in range(num_tracks)]

    mocDisplay = window.findChild(MotionControllerDisplay)
    mocDisplay.setTracks(tracks)

    sys.exit(app.exec_())
