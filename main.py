from PyQt5 import QtGui, QtCore, QtWidgets
import sys
from views.MainWindow import MainWindow
import tabulate
import openpyxl

if __name__ == "__main__":
    # Check file (.conf,...) if not create one.
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Debt Calculation")
    window.show()

    # app_icon = QtGui.QIcon()
    # app_icon.addFile("icon/boss.png", QtCore.QSize(64, 64))
    # app.setWindowIcon(app_icon)

    sys.exit(app.exec_())
