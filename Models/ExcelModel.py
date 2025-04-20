from copy import copy
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime
import shutil
import os
import requests
from Models.MultiLangues import MultiLanguages

SUMMARY_ROWS_INDEX = 12
DETAIL_ROWS_INDEX = 18
EXCEL_TEMPLATE_FILE = "template.xlsx"
EXCEL_TEMPLATE_FILE_URL = "https://github.com/Achicken7301/Debt-Calculation/raw/refs/heads/develop/template.xlsx"

class ExcelModel:
    def __init__(self):
        self.excel_source_file = EXCEL_TEMPLATE_FILE
        # Check if there's no template file, start download one.
        if not os.path.isfile(EXCEL_TEMPLATE_FILE):
            r = requests.get(EXCEL_TEMPLATE_FILE_URL)
            if r.status_code == 200:
                with open(EXCEL_TEMPLATE_FILE, "wb") as file:
                    file.write(r.content)
            else:
                print(f"Cannot download {EXCEL_TEMPLATE_FILE}")


        self.e_temp = pd.read_excel(self.excel_source_file)
        self.m_lang = MultiLanguages()
        self.summary_table = pd.DataFrame(columns=[self.m_lang.trans("Date"), self.m_lang.trans("Total per invoice"), self.m_lang.trans("Date"), self.m_lang.trans("Date"), self.m_lang.trans("Date")])
        self.output_headers = [
            f"{self.m_lang.trans('Product')}",
            f"{self.m_lang.trans('Unit price')}",
            f"{self.m_lang.trans('Quantity')}",
            f"{self.m_lang.trans('Total (Unit price * Quantity)')}",
        ]
        self.detail_table = pd.DataFrame(columns=[self.m_lang.trans("Date"), 
            f"{self.m_lang.trans('Product')}",
            f"{self.m_lang.trans('Unit price')}",
            f"{self.m_lang.trans('Quantity')}",
            f"{self.m_lang.trans('Total (Unit price * Quantity)')}",
                                                  ])

    def _duplicate(self, closing_date):
        """This will copy template into a new file with formated, then passing the data only
        """
        self.output_file = f"{closing_date}_testing_new_file.xlsx"
        shutil.copyfile(self.excel_source_file, self.output_file)
    
    def _addSummaryTable(self, date, tt_per_i, m_diff, tt_interest_p_i, tt_cus_have_to_pay="-"):
        new_row = [date, tt_per_i, m_diff, tt_interest_p_i, tt_cus_have_to_pay]
        self.summary_table.loc[len(self.summary_table)] = new_row
    
    def _addTableDetail(self,date, total_per_invoice, df_datas:pd.DataFrame):
        new_row = [date, "", "", "", ""]
        # new_row = [date, self.m_lang.trans('Product'), self.m_lang.trans('Quantity'), self.m_lang.trans('Unit price'), self.m_lang.trans('Total (Unit price * Quantity)')]
        self.detail_table.loc[len(self.detail_table) ]= new_row
        self.detail_table = pd.concat([self.detail_table, df_datas], ignore_index=True)
        new_row = ["", "", "", "Tổng cộng", total_per_invoice]
        self.detail_table.loc[len(self.detail_table) ]=new_row

    def _calc_interest(self, total, interest, _m_diff):
        if self.m_lang.get_locale() == "vi_VN":
            return int(total * interest * _m_diff)
        else:
            return float(total * interest * _m_diff)

    def _month_difference(self, date1: str, date2: str) -> int:
        date1_obj = datetime.strptime(date1, r"%d/%m/%Y")
        date2_obj = datetime.strptime(date2, r"%d/%m/%Y")
        diff_months = (
            (date2_obj.year - date1_obj.year) * 12 + date2_obj.month - date1_obj.month
        )

        return diff_months
    
    def _insert_formatted_rows(self, filepath, sheetname, start_row, num_rows):
        wb = load_workbook(filepath)
        ws = wb[sheetname]

        # Step 1: Insert blank rows
        ws.insert_rows(start_row, amount=num_rows)

        # Step 2: Copy style from the row just above (or below if start_row == 1)
        style_row_idx = start_row + num_rows  # the original row that was pushed down
        template_row = ws[style_row_idx]

        for i in range(num_rows):
            target_row = ws[start_row + i]
            for col_idx, cell in enumerate(template_row):
                new_cell = target_row[col_idx]
                if cell.has_style:
                    new_cell._style = copy(cell._style)
                if cell.number_format:
                    new_cell.number_format = cell.number_format
                if cell.font:
                    new_cell.font = copy(cell.font)
                if cell.border:
                    new_cell.border = copy(cell.border)
                if cell.fill:
                    new_cell.fill = copy(cell.fill)
                if cell.alignment:
                    new_cell.alignment = copy(cell.alignment)
        # Save changes
        wb.save(filepath)

    def export(self,raw_data:pd.DataFrame, closing_date:str, i:float):
        """This function will export to excel file

        Args:
            raw_data (pd.DataFrame): _description_
            closing_date (str): _description_
            i (float): interest rate
        """
        self._duplicate(closing_date.replace("/", "-"))
        self.file_data = raw_data
        unique_dates = self.file_data[self.m_lang.trans("Date")].unique()
        total = 0
        total_interest = 0
        for date in unique_dates:

            m_diff = self._month_difference(date, closing_date)
            # Find total per invoice (day)
            df_sort_by_date = self.file_data[
                self.file_data[self.m_lang.trans("Date")] == date
            ]
            total_per_invoice = df_sort_by_date[
                self.m_lang.trans("Total (Unit price * Quantity)")
            ].sum()

            # Find interest
            total_interest_per_invoice = self._calc_interest(
                total_per_invoice,i, m_diff
            )

            total += total_per_invoice
            total_interest += total_interest_per_invoice


            self._addSummaryTable(date, total_per_invoice, m_diff, total_interest_per_invoice)
            self._addTableDetail(date, total_per_invoice, df_sort_by_date[self.output_headers])


        # Add detail table
        self._insert_formatted_rows(self.output_file, "Sheet1", DETAIL_ROWS_INDEX, len(self.detail_table))
        with pd.ExcelWriter(self.output_file, mode="a", if_sheet_exists="overlay") as writer:
            self.detail_table.to_excel(writer, startrow=DETAIL_ROWS_INDEX, startcol=0, index=False, header=False)
        
        self._addSummaryTable("-", total, "-", total_interest, total+total_interest)
        # Add summary table
        self._insert_formatted_rows(self.output_file, "Sheet1", SUMMARY_ROWS_INDEX, len(self.summary_table))
        with pd.ExcelWriter(self.output_file, mode="a", if_sheet_exists="overlay") as writer:
            self.summary_table.to_excel(writer, startrow=SUMMARY_ROWS_INDEX, startcol=0, index=False, header=False)



    
