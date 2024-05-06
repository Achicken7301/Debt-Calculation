from pickle import NONE
import configparser
import pandas as pd
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

from Models.MultiLangues import MultiLanguages


class MyMarkdown:
    def __init__(self) -> None:
        self.content = ""
        self.store_name = ""
        self.store_addr = ""
        self.store_street = ""
        self.store_district = ""
        self.store_provinces = ""
        self.store_city = ""
        self.store_phone_number = ""
        self.css = """
            body{
                font-family: Lora;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                border-bottom: 1px solid black;
                border-top: 1px solid black;
                align: center;
            }

            td {
                padding: 0.5em;
                text-align: right;
            }
            """
        self.m_lang = MultiLanguages()
        self.get_store_name()
        self.pdf = MarkdownPdf()

        self.store_init()

    def store_init(self):
        self.content += "<html>"
        self.content = "<style>" + self.css + "</style>\r\n"
        self.content += f"""
<body >
<table class="dataframe" style="align: center;">
    <tbody>
        <tr>
            <td style="text-align: left;">
                {self.m_lang.trans("Customer name")}: <br>
                {self.m_lang.trans("Customer books number")}: <br>
                {self.m_lang.trans("Customer address")}: <br>
                {self.m_lang.trans("Customer phone")}: <br>
            </td>
            <td style="text-align: right;">
                {self.store_name} <br>
                {self.store_street}<br>
                {self.store_district}<br>
                {self.store_city}<br>
                {self.store_phone_number} <br>
            </td>
        </tr>
    </tbody>
</table>
<div class="dataframe">
    <h2 style="text-align: center;">
        {self.m_lang.trans("Customer debt")}
    </h2>
<div>
<p style="text-align: left;">{self.m_lang.trans("Closing date")}: </p><br>
        """

    def save2pdf(self, file_name: str):
        self.content += "</body>"
        self.content += "</html>"
        self.pdf.add_section(Section(self.content, toc=False))

        self.pdf.meta["title"] = file_name
        self.pdf.save(f"{file_name}.pdf")

    # def save(self, cus_name: str, cus_number: str):
    #     pass

    def append(self, data: str, style=NONE):
        if style == "bold":
            self.content += "<strong>"
            self.content += data
            self.content += "</strong>"
        elif style == "align-left":
            self.content += "<p style='text-align: left;'>"
            self.content += data
            self.content += "</p>"
        else:
            self.content += data

        self.content += "\n\n"

    def set_store_infos(self, name: str, addr: str, phone_number: str):
        self.store_name = name
        self.store_addr = addr
        self.store_phone_number = phone_number

    def get_store_name(self):
        config = configparser.ConfigParser()
        config.read(".conf")  # Replace 'settings.conf' with your file name
        self.store_name = config["STORE"]["name"]
        self.store_addr = config["STORE"]["addr"]
        self.store_street = config["STORE"]["street"]
        self.store_district = config["STORE"]["district"]
        self.store_province = config["STORE"]["province"]
        self.store_city = config["STORE"]["city"]
        self.store_phone_number = config["STORE"]["phone"]

    def save_store_infos(self):
        """Save store infos into .csv or .xlsx file"""
        pass
