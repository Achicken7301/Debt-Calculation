from PyQt5 import QtGui, QtCore, QtWidgets
import sys
from views.MainWindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("My App")
    window.show()

    # app_icon = QtGui.QIcon()
    # app_icon.addFile("icon/boss.png", QtCore.QSize(64, 64))
    # app.setWindowIcon(app_icon)

    sys.exit(app.exec_())
