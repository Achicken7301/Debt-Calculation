from os import makedirs
import os.path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm
from pandas import DataFrame

from Models.Global import *
from Models.MultiLangues import MultiLanguages


# A4 dimensions in inches (Width x Height)
A4_WIDTH = Mm(210)  # 210mm
A4_HEIGHT = Mm(297)  # 297mm
# Margin size in mm
MARGIN_SIZE = Mm(20)  # 20mm (2cm)

class MyDocx:
    def __init__(
        self, _cus_name="Unknown", _cus_number="001", _closing_date="01/01/2001"
    ) -> None:

        self.m_lang = MultiLanguages()

        # Document layout
        self.my_docx = Document()

        # Set to A4
        # Set page size to A4
        section = self.my_docx.sections[0]
        section.page_width = (A4_WIDTH)
        section.page_height = (A4_HEIGHT)

        # Set margins to 20mm (2cm) on all sides
        section.left_margin = MARGIN_SIZE
        section.right_margin = MARGIN_SIZE
        section.top_margin = MARGIN_SIZE
        section.bottom_margin = MARGIN_SIZE

        # add style
        self.my_docx.styles['Normal'].paragraph_format.space_before = 0
        self.my_docx.styles['Normal'].paragraph_format.space_after = 0
        self.my_docx.styles['Normal'].paragraph_format.line_spacing = 1

        # Title
        self.title = self.my_docx.add_heading(level=0)
        run = self.title.add_run(self.m_lang.trans("Book calc title"))
        run.bold = True

        # Paragraph and style
        self.closing_date = self.my_docx.add_paragraph()
        run = self.closing_date.add_run(self.m_lang.trans("Closing date"))
        run.italic = True
        self.interest_rate_paragraph = self.my_docx.add_paragraph()
        run = self.interest_rate_paragraph.add_run(self.m_lang.trans("Interest rate per month"))
        run.italic = True



        # Summary table
        self.summary_table = self.my_docx.add_table(rows=1, cols=5)
        cell = self.summary_table.rows[0].cells
        # This is hard code, I'll fix this later
        cell[1].text = "(1)"
        cell[2].text = "(2)"
        cell[3].text = "(3)"
        cell[4].text = "(4)"

        # Add explain paragraph
        self.explain_summary_table_paragraph = self.my_docx.add_paragraph()
        run = self.explain_summary_table_paragraph.add_run(self.m_lang.trans("Explain Summary Table Paragraph"))
        run.italic = True

        self.my_docx.add_page_break()
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
        new_r[3].text = (len(tt_p_i) + 2) * "_"
        # new_r[3].text = 20 * "_"
        new_r = invoice_detail_table.add_row().cells
        new_r[3].text = str(tt_p_i)

        # Align specific columns for all rows
        for row in invoice_detail_table.rows:
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    def addTableSummary(
        self, date, tt_per_i, m_diff, tt_interest_p_i, tt_cus_have_to_pay
    ):
        new_r = self.summary_table.add_row().cells
        new_r[0].text = str(date)
        new_r[1].text = str(tt_per_i)
        new_r[2].text = str(m_diff)
        new_r[3].text = str(tt_interest_p_i)
        new_r[4].text = str(tt_cus_have_to_pay)

        # Align specific columns for all rows
        for row in self.summary_table.rows:
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    def generate_file_docx_format(self, file_name, closing_date, interest_rate):
        run = self.title.add_run(text=f" {file_name}")
        run.bold = True

        run = self.closing_date.add_run(text=f" {closing_date}.")
        run.bold = True
        run.italic = True

        run = self.interest_rate_paragraph.add_run(text=f" {interest_rate}%.")
        run.bold = True
        run.italic = True

        # Save subfolder Granularity Monthly
        # Base on closing date
        _, m_dir, y_dir = closing_date.split('/')
        # Check if had  have current-year directory, if not create
        # Check if the folder exists
        if not os.path.exists(y_dir):
            # Create the folder if it doesn't exist
            makedirs(y_dir)
        # Check if had  have current-month directory, if not create
        if not os.path.exists(f"{y_dir}//{m_dir}"):
            # Create the folder if it doesn't exist
            makedirs(f"{y_dir}//{m_dir}")

        self.my_docx.save(f"{y_dir}//{m_dir}/{file_name}.docx")
