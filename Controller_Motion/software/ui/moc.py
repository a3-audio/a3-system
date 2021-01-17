import sys
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDial
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

from widgets.QuadraticDial import QuadraticDial
from widgets.QuadraticPushButton import QuadraticPushButton

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "moc.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
        sys.exit(-1)
    loader = QUiLoader()
    loader.registerCustomWidget(QuadraticDial)
    loader.registerCustomWidget(QuadraticPushButton)

    print(loader.availableWidgets())

    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.show()
    window.setFixedSize(318, 1000)

    sys.exit(app.exec_())
