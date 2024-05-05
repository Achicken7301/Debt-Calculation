from pickle import NONE
import pandas as pd
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section


class MyMarkdown:
    def __init__(self) -> None:
        self.content = ""
        self.store_name = ""
        self.store_addr = ""
        self.store_phone_number = ""

        self.get_store_name()
        self.css = """
            @page {
                size: A4;
                margin-left: 2cm;
                margin-top: 1cm;
                margin-right: 1cm;
                margin-bottom: 1cm;
            }
            body {
                font-family: Open Sans;
            }

            table {
                width: 100%;
                border: none;
                border-collapse: collapse;
                border-bottom: 1px solid black;
                border-top: 1px solid black;
            }

            th {
                padding: 0.5em;
                border: none;
                text-align: left;
            }

            td {
                border: none;
                padding: 0.5em;
                text-align: left;
            }
            """
        self.content = "<style>" + self.css + "</style>"
        self.pdf = MarkdownPdf()

    def save(self, file_name: str):
        self.pdf.meta["title"] = file_name
        self.pdf.add_section(Section(self.content, toc=False))
        self.pdf.save(f"{file_name}.pdf")

        # with open(f"md/{file_name}", "w", encoding="utf-8") as f:
        #     f.write(self.content)

    def append(self, data: str, style=NONE):
        if style == "bold":
            self.content += "<strong>"
            self.content += data
            self.content += "</strong>"

        else:
            self.content += data

        self.content += "\n\n"

    def set_store_infos(self, name: str, addr: str, phone_number: str):
        self.store_name = name
        self.store_addr = addr
        self.store_phone_number = phone_number

    def get_store_name(self):
        """Get store infos which saved in .csv for .xlsx file"""
        # Access to .csv or .xlsx file

        # Sign to store infos by using `set_store_info()`
        pass

    def save_store_infos(self):
        """Save store infos into .csv or .xlsx file"""
        pass
