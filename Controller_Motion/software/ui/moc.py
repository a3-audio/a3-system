import sys
import argparse

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader

from widgets.QuadraticDial import QuadraticDial
from widgets.QuadraticPushButton import QuadraticPushButton
from widgets.MotionControllerDisplay import MotionControllerDisplay

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AAA Motion Controller.')
    parser.add_argument("--develop", help="run in development mode with mockup UI", action="store_true")
    args = parser.parse_args()
    if args.develop:
        print("running in develop mode")
    else:
        print("running in fullscreen mode")

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

        window.setFixedSize(318, 1000)
        window.show()
    else:
        window = QMainWindow()
        window.setCentralWidget(MotionControllerDisplay())
        window.showFullScreen()

    # create track objects and pass to display widget
    # num_tracks = 4
    # tracks = [Track() for i in range(num_tracks)]

    sys.exit(app.exec_())
