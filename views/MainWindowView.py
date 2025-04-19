import PyQt5
import PyQt5.QtCore
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt5.QtWidgets import (
    QMessageBox,
    QTableWidgetItem,
    QMainWindow,
    QComboBox,
)
from PyQt5.QtCore import Qt

# Models
from Controller import Controller
from Models.Docx import MyDocx
from Models.Global import ErrorHandler, ExportFormat, FileFormat, Option, Section
from Models.Markdown import MyMarkdown, Style
from Models.MultiLangues import MultiLanguages

# Main ui
from Models.ProgramConfigModel import ProgramConfig
from ui.main_ui_ui import Ui_MainWindow

# Depencences???
from datetime import datetime, date
import pandas as pd

# View
from views.SettingsView import Settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.m_lang = MultiLanguages()
        self.conf = ProgramConfig()
        self.file_format = FileFormat.NONE
        self.col_format = {f"{self.m_lang.trans('Unit price')}": "{:,}"}

        # Base on default language content here will change
        self.default_headers_comboBox = [
            "-",
            f"{self.m_lang.trans('Date')}",
            f"{self.m_lang.trans('Product')}",
            f"{self.m_lang.trans('Unit price')}",
            f"{self.m_lang.trans('Quantity')}",
            f"{self.m_lang.trans('Total (Unit price * Quantity)')}",
        ]

        self.output_headers = [
            f"{self.m_lang.trans('Product')}",
            f"{self.m_lang.trans('Unit price')}",
            f"{self.m_lang.trans('Quantity')}",
            f"{self.m_lang.trans('Total (Unit price * Quantity)')}",
        ]
        self.is_load_file = 0
        self.main_ui.file_generate.clicked.connect(self.file_generate_btn)
        self.main_ui.actionStore_Infos.triggered.connect(self.edit_store_info)

        self.main_ui.closing_date.setDate(PyQt5.QtCore.QDate(date.today()))

    def edit_store_info(self):
        edit_store_infos_ui = Settings()
        edit_store_infos_ui.exec()

    def file_generate_btn(self):

        # Check file confition
        if self.is_load_file == 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Please drag and drop file first!!!",
                buttons=QMessageBox.Close,
                defaultButton=QMessageBox.Close,
            )
            return

        # Get all colums of row 0 for check header list
        list_headers = []
        for i in range(self.column):
            comboBox = self.main_ui.tableWidget.cellWidget(0, i)
            list_headers.append(comboBox.currentText())

        # Check headers list
        if self.check_headers_list(list_headers) == ErrorHandler.NOT_OK:
            return ErrorHandler.NOT_OK

        # Replace old header to new selected one
        self.file_data.columns = list_headers

        # Create local variable
        cus_name = self.main_ui.cus_name.text()
        cus_book_number = self.main_ui.cus_number.text()
        closing_date = self.main_ui.closing_date.date().toString("dd/MM/yyyy")
        if len(cus_name) == 0:
            QMessageBox.warning(
                self,
                self.m_lang.trans("Warning"),
                self.m_lang.trans("Please input customer name"),
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )

            return


        if self.file_format == FileFormat.XLSX:
            try:
                self.file_data[self.m_lang.trans("Date")] = self.file_data[
                    self.m_lang.trans("Date")
                ].dt.strftime(r"%d/%m/%Y")
            except:
                """
                TODO The point is, when i use this 2nd time, 
                the self.file_data is already formated, so cause conflict, 
                i'll more condition on this later
                """
                print("I WILL FIX THIS IN THE FUTURE")

        # Find diff in months -> total -> interest -> add to pdf -> save as .pdf file
        # List all unique dates in columns
        unique_dates = self.file_data[self.m_lang.trans("Date")].unique()
        interest_rate = float(self.main_ui.interest_rate.text()) / 100.0
        total = 0
        total_interest = 0

        """Why do i init md and docx here, but not in the contructor??
        Initiate temp for export pdf or docx format
        This is crucial cuz the whole system i use "add to temp" NOT overwrite them.
        So... this temp variables need to be init right here.
        """
        if self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.PDF:
            self.md = MyMarkdown(cus_name, cus_book_number, closing_date)
        elif self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.DOCX:
            self.docx = MyDocx()
        elif self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.EXCEL:
            self.xlsx = Controller().generate_xlsx_format(self.file_data, closing_date, interest_rate)
        else:
            self.docx = MyDocx()

        for date in unique_dates:

            m_diff = self.month_difference(date, closing_date)
            # Find total per invoice (day)
            df_sort_by_date = self.file_data[
                self.file_data[self.m_lang.trans("Date")] == date
            ]
            total_per_invoice = df_sort_by_date[
                self.m_lang.trans("Total (Unit price * Quantity)")
            ].sum()

            # Add style for dataframe
            df_sort_by_date = self.cols_format(df_sort_by_date)

            # Find interest
            total_interest_per_invoice = self.calc_interest(
                total_per_invoice, interest_rate, m_diff
            )

            total += total_per_invoice
            total_interest += total_interest_per_invoice

            if (
                self.conf.read(Section.GENERAL, Option.export_format)
                == ExportFormat.PDF
            ):
                # Add to pdf
                self.md.append("<br>")
                self.md.append(f"{date}", Style.BOLD)

                # Add total/interest
                _temp_table = ""
                _temp_table += (
                    df_sort_by_date[self.output_headers].to_markdown(
                        index=False, colalign=("left", "left", "right", "right")
                    )
                    + "\r\n"
                )
                _temp_table += f"||||<hr style='margin-right:0; width: 75%'>|\r\n"
                _temp_table += f"||||{total_per_invoice:,}|\r\n"

                self.md.append(_temp_table, Style.TABLE)
                self.md.summary_append(
                    [
                        date,
                        f"{total_per_invoice:,}",
                        f"x{m_diff}",
                        f"{total_interest_per_invoice:,}",
                        "",
                    ]
                )

            if (
                self.conf.read(Section.GENERAL, Option.export_format)
                == ExportFormat.DOCX
            ):
                self.docx.addTableDetail(
                    date,
                    f"{total_per_invoice:,}",
                    len(self.output_headers),
                    df_sort_by_date[self.output_headers],
                )

                self.docx.addTableSummary(
                    date,
                    f"{total_per_invoice:,}",
                    f"x{m_diff}",
                    f"{total_interest_per_invoice:,}",
                    "",
                )
                pass

        if self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.PDF:
            self.md.summary_append(["", "<hr>", "", "<hr>", ""])
            self.md.summary_append(
                [
                    "",
                    "+",
                    f"{total:,}",
                    f"{total_interest:,}",
                    f"= {(total + total_interest):,}",
                ]
            )
            self.md.generate_file_pdf_format(f"{cus_name}_{cus_book_number}")
        elif self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.DOCX:
            self.docx.addTableSummary(
                "",
                f"{total:,}",
                "+",
                f"{total_interest:,}",
                f"= {(total + total_interest):,}",
            )
            self.docx.generate_file_docx_format(
                f"{cus_name}_{cus_book_number}", closing_date, self.main_ui.interest_rate.text()
            )

        QMessageBox.information(
            self,
            "Success",
            f"Output {'DOCX' if self.conf.read(Section.GENERAL, Option.export_format) == ExportFormat.DOCX else 'PDF'} file successfully!!!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
        )

    def cols_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """This magical function will format dataframe columes

        Args:
            df (pd.DataFrame): _description_

        Returns:\n
            pd.DataFrame: _description_
        """
        df.loc[:, self.m_lang.trans("Unit price")] = df.loc[
            :, self.m_lang.trans("Unit price")
        ].map("{:,}".format)

        df.loc[:, self.m_lang.trans("Total (Unit price * Quantity)")] = df.loc[
            :, self.m_lang.trans("Total (Unit price * Quantity)")
        ].map("{:,}".format)

        return df

    def calc_interest(self, total, interest, _m_diff):
        if self.m_lang.get_locale() == "vi_VN":
            return int(total * interest * _m_diff)
        else:
            return float(total * interest * _m_diff)

    def month_difference(self, date1: str, date2: str) -> int:
        date1_obj = datetime.strptime(date1, r"%d/%m/%Y")
        date2_obj = datetime.strptime(date2, r"%d/%m/%Y")
        diff_months = (
            (date2_obj.year - date1_obj.year) * 12 + date2_obj.month - date1_obj.month
        )

        return diff_months

    def check_headers_list(self, header_list: list) -> ErrorHandler:
        """
        Check if list has any more than 1 or missing some of the members

        Given some examples:
        [ "Date", "Product", "Unit Price", "Quantity", "Total"] -> return true, no duplicate && no missing any members\n
        [ "Date", "Product","Date", "Unit Price", "Quantity", "Total"] -> return false, "Date" duplicate more than 1 \n
        [ "Date", "Unit Price", "Quantity", "Total"] -> return false, for missing "Product"\n
        """

        for header in self.output_headers:
            count = header_list.count(header)
            if count == 0 or count > 1:
                QMessageBox.warning(
                    self,
                    f"{self.m_lang.trans('Warning')}",
                    f"Not selected headers at row 1\nor duplicate headers\n({header})",
                    buttons=QMessageBox.Close,
                    defaultButton=QMessageBox.Close,
                )
                return ErrorHandler.NOT_OK

        # TODO: Check confitions for data columns
        # Check if Product is str

        # Check if Unit Price is int or flaot

        # Check if Quantity is int or float

        # Check if Total is int or float

        return ErrorHandler.OK

    def dragEnterEvent(self, event: QDragEnterEvent | None) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, a0: QDragMoveEvent) -> None:
        return super().dragMoveEvent(a0)

    def dropEvent(self, event: QDropEvent) -> None:
        """Process file path when drop.\n

        Args:
            event (QDropEvent):
        """

        # I better refactor this code for better maintenance
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile():
                    file_abs_path = str(url.toLocalFile())
                    self.file_format = self.check_file_format(file_abs_path)

                    # File format handler error
                    temp_text = self.m_lang.trans(
                        "This file is NOT .xlsx or .csv format\r\nPlease try again"
                    )
                    if self.file_format == FileFormat.NONE:
                        # Create dialog warning
                        QMessageBox.warning(
                            self,
                            self.m_lang.trans("Warning"),
                            temp_text,
                            buttons=QMessageBox.Close,
                            # buttons=QMessageBox.Discard | QMessageBox.NoToAll | QMessageBox.Ignore,
                            defaultButton=QMessageBox.Close,
                        )
                        return

                    # Load file to table
                    self.load_file_to_table(file_abs_path, self.file_format)
                else:
                    print("This is something else file")
                    print(str(url.toString()))
        else:
            event.ignore()

    def check_file_format(self, file_path: str) -> FileFormat:
        """_Check file if .xlsx or .csv format

        Args:
            file_path (str): Absolute path

        Returns:
            FileFormat: XLSX or CSV or NONE
        """
        # Find the index of the last dot
        last_dot_index = file_path.rfind(".")
        ext = file_path[last_dot_index:]

        if ext == ".xlsx":
            return FileFormat.XLSX
        elif ext == ".csv":
            return FileFormat.CSV
        else:
            return FileFormat.NONE

    def load_file_to_table(self, file_path: str, type: FileFormat):
        """Load data from .xlsx or .csv to tableWidget

        NOTE: .csv has NOT working, YET

        Args:
            file_path (str): absolute file path
            type (FileFormat): .xlsx or .csv
        """

        self.file_data = pd.DataFrame()
        self.is_load_file = 1

        if type == FileFormat.XLSX:
            # print("Start loading .xlsx")
            self.file_data = pd.read_excel(file_path)

        if type == FileFormat.CSV:
            # NOTE: This is not implement, YET
            self.file_data = pd.read_csv(file_path)

        self.row = len(self.file_data)
        self.column = len(self.file_data.columns)

        self.main_ui.tableWidget.setColumnCount(self.column)
        self.main_ui.tableWidget.setRowCount(self.row)

        headers = self.file_data.columns.values

        # Load headers
        for i in range(self.column):
            self.main_ui.tableWidget.setHorizontalHeaderItem(
                i, QTableWidgetItem(headers[i])
            )

        # Load header selections
        for i in range(self.row):
            combobox = QComboBox()
            combobox.addItems(self.default_headers_comboBox)
            self.main_ui.tableWidget.setCellWidget(0, i, combobox)

        # Load data, `1` here is a every magic number, it works, sooooooooo dont ask
        for i in range(1, self.row):
            for j in range(self.column):
                self.main_ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(self.file_data.iloc[i - 1, j]))
                )
