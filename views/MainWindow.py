from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.main_ui_ui import Ui_MainWindow
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.default_headers = [
            "Unknown",
            "Date",
            "Product",
            "Unit Price",
            "Quantity",
            "Total",
        ]

    def dragEnterEvent(self, event: QDragEnterEvent | None) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, a0: QDragMoveEvent) -> None:
        return super().dragMoveEvent(a0)

    def dropEvent(self, event: QDropEvent) -> None:
        """Process file path when drop

        Args:
            event (QDropEvent):
        """
        print("This is drop event")
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile():
                    current_file = str(url.toLocalFile())
                    self.check_file(current_file)
                else:
                    print("This is something else file")
                    print(str(url.toString()))
        else:
            event.ignore()

    def check_file(self, file_path: str):
        """Check file if .xlsx or .csv

        Args:
            file_path (str): file absolute path
        """
        # Find the index of the last dot
        last_dot_index = file_path.rfind(".")
        ext = file_path[last_dot_index:]

        if ext == ".xlsx":
            print("This file is .xlsx")
            # create table, header is drop box
            self.load_file_to_table(file_path, ext)
        elif ext == ".csv":
            print("This file is .csv")
            # create table, header is drop box
            self.load_file_to_table(file_path, ext)
        else:
            # Create dialog warning
            print("This is either .xlsx nor .csv")

    def load_file_to_table(self, file_path: str, type: str):
        if type == ".xlsx":
            # print("Start loading .xlsx")
            df = pd.read_excel(file_path)

        if type == ".csv":
            df = pd.read_csv(file_path)

        rows = len(df)
        columns = len(df.columns)
        print(f"df has {rows} rows")
        print(f"df has {columns} columnes")

        self.main_ui.tableWidget.setColumnCount(columns)
        self.main_ui.tableWidget.setRowCount(rows)
        # print(df.columns.values)

        headers = df.columns.values

        for i in range(columns):
            self.main_ui.tableWidget.setHorizontalHeaderItem(
                i, QTableWidgetItem(headers[i])
            )

        for i in range(rows):
            combobox = QComboBox()
            combobox.addItems(self.default_headers)
            self.main_ui.tableWidget.setCellWidget(0, i, combobox)

        for i in range(1, rows):
            for j in range(columns):
                self.main_ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(df.iloc[i, j]))
                )
