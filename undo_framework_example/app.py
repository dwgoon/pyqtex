import sys
from qtpy.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()
