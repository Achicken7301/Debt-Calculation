import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class MyPdf:
    def __init__(self, pdf_filename) -> None:
        self.content = []
        self.doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
