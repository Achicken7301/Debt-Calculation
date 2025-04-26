from PyQt5 import QtGui, QtCore, QtWidgets
import requests
import sys
from views.MainWindowView import MainWindow
import tabulate
import openpyxl
import os

APP_NAME = "Debt Calculation"
EXAMPLE_CONF_FILE = "example.conf"
example_conf_url = "https://raw.githubusercontent.com/Achicken7301/Debt-Calculation/develop/example.conf"
translate_url = (
    "https://github.com/Achicken7301/Debt-Calculation/tree/develop/translate"
)

if __name__ == "__main__":
    # Download initial files
    if not os.path.isfile(EXAMPLE_CONF_FILE):
        example_conf_reponse = requests.get(example_conf_url)
        if example_conf_reponse.status_code == 200:
            with open(EXAMPLE_CONF_FILE, "wb") as file:
                file.write(example_conf_reponse.content)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(APP_NAME)
    window.show()

    # app_icon = QtGui.QIcon()
    # app_icon.addFile("icon/boss.png", QtCore.QSize(64, 64))
    # app.setWindowIcon(app_icon)

    sys.exit(app.exec_())
