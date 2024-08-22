from urllib import response
from PyQt5 import QtGui, QtCore, QtWidgets
import requests
import sys
from views.MainWindow import MainWindow
import tabulate
import openpyxl
import os

example_conf_url = "https://raw.githubusercontent.com/Achicken7301/Debt-Calculation/develop/example.conf"
translate_url = (
    "https://github.com/Achicken7301/Debt-Calculation/tree/develop/translate"
)

if __name__ == "__main__":
    # Download initial files
    if not os.path.isfile("example.conf"):
        example_conf_reponse = requests.get(example_conf_url)
        if example_conf_reponse.status_code == 200:
            with open("example.conf", "wb") as file:
                file.write(example_conf_reponse.content)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Debt Calculation")
    window.show()

    # app_icon = QtGui.QIcon()
    # app_icon.addFile("icon/boss.png", QtCore.QSize(64, 64))
    # app.setWindowIcon(app_icon)

    sys.exit(app.exec_())
