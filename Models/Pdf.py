import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Replace 'YourFontName' and 'path_to_font_file.ttf' with the actual font name and file path
# pdfmetrics.registerFont(TTFont(""))

# Add Liberation Serif font to the list of available fonts
pdfmetrics.registerFont(TTFont("Open Sans", "fonts/OpenSans-Regular.ttf"))


class MyPdf_ReportLab:
    def __init__(self, pdf_filename) -> None:
        self.content = []
        self.doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        self.style = getSampleStyleSheet()

        self.default_font = "Open Sans"
        self.style["Normal"].fontName = self.default_font

    def append_paragraph(self, data: str):
        title = Paragraph(data, self.style["Normal"])
        self.content.append(title)

    def append_table(self, df: pd.DataFrame):
        table_data = [df.columns[:,].values.astype(str).tolist()] + df.values.tolist()
        table = Table(table_data)

        # Apply table style
        table.setStyle(
            TableStyle(
                [
                    # ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                    # ("TEXTCOLOR", (0, 0), (-1, 0), (0, 0, 0)),
                    # ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, -1), self.default_font),
                    # ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    # ("BACKGROUND", (0, 1), (-1, -1), (0.85, 0.85, 0.85)),
                    ("GRID", (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
                ]
            )
        )

        self.content.append(table)

    def export(self):
        self.doc.build(self.content)
