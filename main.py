from PyQt5 import QtWidgets
from sys import argv, exit
from requests import get
from views.MainWindowView import MainWindow
import os.path

APP_NAME = "Debt Calculation"
EXAMPLE_CONF_FILE = "example.conf"
EXAMPLE_CONF_URL = "https://raw.githubusercontent.com/Achicken7301/Debt-Calculation/develop/example.conf"
TRANSLATE_URL = (
    "https://github.com/Achicken7301/Debt-Calculation/tree/develop/translate"
)

if __name__ == "__main__":
    # Download initial files
    if not os.path.isfile(EXAMPLE_CONF_FILE):
        example_conf_reponse = get(EXAMPLE_CONF_URL)
        if example_conf_reponse.status_code == 200:
            with open(EXAMPLE_CONF_FILE, "wb") as file:
                file.write(example_conf_reponse.content)

    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.setWindowTitle(APP_NAME)
    window.show()

    # app_icon = QtGui.QIcon()
    # app_icon.addFile("icon/boss.png", QtCore.QSize(64, 64))
    # app.setWindowIcon(app_icon)

    exit(app.exec_())
