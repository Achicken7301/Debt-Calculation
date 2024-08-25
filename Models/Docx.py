from docx import Document
from pandas import DataFrame

from Models.Global import *
from Models.MultiLangues import MultiLanguages


class MyDocx:
    def __init__(
        self, _cus_name="Unknown", _cus_number="001", _closing_date="01/01/2001"
    ) -> None:

        self.m_lang = MultiLanguages()

        # Document layout
        self.my_docx = Document()
        # Title
        self.title = self.my_docx.add_heading(self.m_lang.trans("Book calc title"), 0)
        self.closing_date = self.my_docx.add_paragraph(
            self.m_lang.trans("Closing date")
        )
        self.summary_table = self.my_docx.add_table(rows=1, cols=5)
        self.my_docx.add_heading(self.m_lang.trans("Invoice detail"), level=1)

    def addParagraph(self, text: str):
        self.my_docx.add_paragraph(text)

    def addTableDetail(self, date, tt_p_i, cols, df_datas: DataFrame):
        datas = tuple(df_datas.itertuples(index=0, name=None))
        invoice_detail_table = self.my_docx.add_table(rows=1, cols=cols)
        hdr_cell = invoice_detail_table.rows[0].cells
        hdr_cell[0].text = str(date)
        hdr_cell[0].paragraphs[0].runs[0].font.bold = True

        # p - product, u_p - unit_price, q - quantity, tt - total
        for p, u_p, q, tt in datas:
            new_r = invoice_detail_table.add_row().cells
            new_r[0].text = str(p)
            new_r[1].text = str(u_p)
            new_r[2].text = str(q)
            new_r[3].text = str(tt)

        # Add summary row
        new_r = invoice_detail_table.add_row().cells
        new_r[3].text = 20 * "_"
        new_r = invoice_detail_table.add_row().cells
        new_r[3].text = str(tt_p_i)

    def addTableSummary(
        self, date, tt_per_i, m_diff, tt_interest_p_i, tt_cus_have_to_pay
    ):
        new_r = self.summary_table.add_row().cells
        new_r[0].text = date
        new_r[1].text = tt_per_i
        new_r[2].text = m_diff
        new_r[3].text = tt_interest_p_i
        new_r[4].text = tt_cus_have_to_pay

    def generate_file_docx_format(self, file_name, closing_date):
        self.title.add_run(text=f" {file_name}")
        self.closing_date.add_run(text=f" {closing_date}")
        self.my_docx.save(f"{file_name}.docx")
