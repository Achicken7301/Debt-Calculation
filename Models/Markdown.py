# import configparser 
from configparser import ConfigParser
from markdown import markdown
from pandas import DataFrame
from weasyprint import HTML
from Models.MultiLangues import MultiLanguages


class Style(enumerate):
    TABLE = 0
    ALIGN_LEFT = 1
    BOLD = 2


class MyMarkdown:
    def __init__(
        self, _cus_name="Unknown", _cus_number="001", _closing_date="01/01/2001"
    ) -> None:
        self.m_lang = MultiLanguages()
        self.html_summary = DataFrame(
            columns=[
                self.m_lang.trans("Date"),
                self.m_lang.trans("Total"),
                "m_diff",
                "Interest",
                "",
            ]
        )
        self.html_content_body = ""
        self.html_content_header = ""
        self.store_name = ""
        self.store_addr = ""
        self.store_street = ""
        self.store_district = ""
        self.store_provinces = ""
        self.store_city = ""
        self.store_phone_number = ""
        self.css = """
            body{
                font-family: Arial, Times New Roman;
            }
            table {
                width: 100%;
                margin-left: auto;
                margin-right: auto;
                border-collapse: collapse;
            }
            td {
                text-align: right;
            }
            th {
                color: white;
            }
            """
        self.m_lang = MultiLanguages()
        self.get_store_name()

        self.store_init(_cus_name, _cus_number, _closing_date)

    def store_init(self, _cus_name, _cus_number, _closing_date):
        self.html_content_header = "<style>" + self.css + "</style>\r\n"
        self.html_content_header += f""" <div style="margin: auto;"> <hr> <table> <tbody > <tr> <td style="text-align: left;">
        {self.m_lang.trans("Customer name")}: {_cus_name}.<br>
        {self.m_lang.trans("Customer books number")}: {_cus_number}.<br>
        {self.m_lang.trans("Customer address")}: <br>
        {self.m_lang.trans("Customer phone")}: <br> </td> <td style="text-align: right;">
        {self.store_name}<br>
        {self.store_street}<br>
        {self.store_district}<br>
        {self.store_city}<br>
        {self.store_phone_number}<br> </td> </tr> </tbody> </table> <hr> </div> <div class="dataframe"> <h2 style="text-align: center;">
        {self.m_lang.trans("Book calc title")} </h2> </div>
        <p style="text-align: right;">{self.m_lang.trans("Closing date")}: {_closing_date}.</p><br>
        """

    def generate_file_pdf_format(self, file_name: str):
        # file_name format before save
        # Remove commas
        no_commas = file_name.replace(",", "")
        # Replace spaces with underscores
        file_name_formatted_string = no_commas.replace(" ", "_")
        # print(self.html_content)
        # print(self.html_summary)

        # Convert HTML to PDF
        summary = markdown(
            self.html_summary.to_markdown(
                index=False,
                colalign=("left", "right", "center", "right", "right"),
            ),
            extensions=["markdown.extensions.tables"],
        )
        output = self.html_content_header + summary + self.html_content_body

        HTML(string=output).write_pdf(
            # "output_with_css.pdf", stylesheets=[self.css]
            f"{file_name_formatted_string}.pdf",
        )

    # def save(self, cus_name: str, cus_number: str):
    #     pass
    def summary_append(self, data: dict):
        self.html_summary.loc[len(self.html_summary)] = data

    def append(self, data: str, style: Style = None):
        if style == Style.BOLD:
            self.html_content_body += "<strong>"
            self.html_content_body += data
            self.html_content_body += "</strong>"
        elif style == "align-left":
            self.html_content_body += "<p style='text-align: left;'>"
            self.html_content_body += data
            self.html_content_body += "</p>"
        elif style == Style.TABLE:
            self.html_content_body += markdown(
                data, extensions=["markdown.extensions.tables"]
            )
        else:
            self.html_content_body += data

        self.html_content_body += "\n\n"

    def set_store_infos(self, name: str, addr: str, phone_number: str):
        self.store_name = name
        self.store_addr = addr
        self.store_phone_number = phone_number

    def get_store_name(self):
        config = ConfigParser()
        config.read(
            ".conf", encoding="utf-8"
        )  # Replace 'settings.conf' with your file name
        self.store_name = config["STORE"]["name"]
        self.store_addr = config["STORE"]["addr"]
        self.store_street = config["STORE"]["street"]
        self.store_district = config["STORE"]["district"]
        self.store_province = config["STORE"]["province"]
        self.store_city = config["STORE"]["city"]
        self.store_phone_number = config["STORE"]["phone"]

    def save_store_infos(self):
        """Save store infos into .csv or .xlsx file"""
        # pass
