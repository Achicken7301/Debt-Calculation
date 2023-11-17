import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import shutil
import pdfkit
import markdown
import argparse


def month_diff(_date, _date_now, date_format: str):
    # Given date
    # print(f"_date: {_date}, date_format: {date_format}")
    given_date = datetime.strptime(_date, date_format)

    # Current date
    # now = datetime.now()
    now = datetime.strptime(_date_now, date_format)

    # Calculate the difference in months
    diff = relativedelta(now, given_date)
    months_diff = diff.years * 12 + diff.months
    return months_diff


def debt_cal(
    file_name: str,
    total_of_all_invoice: float,
    total_of_all_invoice_debt: float,
    _date_now: str,
) -> str:
    md_string = ""
    # df = pd.read_excel(file_name, index_col=None)
    df = pd.read_csv(file_name, sep="\t")

    df_raw_data = df.copy()

    # Store values into dict()
    for i in range(len(default_header)):
        xlsx_header[default_header[i]] = df.columns.values[i]

    # Turn str into float currency
    _unit_price = [float(s.replace(",", "")) for s in df[xlsx_header["Unit price"]]]
    _total_invoice_taxNotIncluded = [
        float(s.replace(",", "")) for s in df[xlsx_header["Total (excl. tax)"]]
    ]

    df = df.drop(columns=[xlsx_header["Unit price"], xlsx_header["Total (excl. tax)"]])

    df[xlsx_header["Unit price"]] = pd.DataFrame(_unit_price)
    df[xlsx_header["Total (excl. tax)"]] = pd.DataFrame(_total_invoice_taxNotIncluded)

    # Filter, get all invoices where status == "Not paid"
    if xlsx_header["Status"] == "Status":
        df = df[df[xlsx_header["Status"]] == "Not paid"]
        df_raw_data = df_raw_data[df_raw_data[xlsx_header["Status"]] == "Not paid"]

        lang = "en"
    else:
        df = df[df[xlsx_header["Status"]] == "Chưa trả"]
        df_raw_data = df_raw_data[df_raw_data[xlsx_header["Status"]] == "Chưa trả"]
        lang = "vi"

    # print(df[xlsx_header["Date"]].values)
    unique_dates = df[xlsx_header["Date"]].unique()

    # print(df_raw_data)

    for datetime in unique_dates:
        df_by_date = df[df[xlsx_header["Date"]] == datetime]
        df_table_view = df_raw_data[df_raw_data[xlsx_header["Date"]] == datetime]

        # print(f"datetime:\t{datetime}")
        # print(df_raw_data[df_raw_data[xlsx_header["Date"]] == datetime])

        total_invoice = df_by_date[xlsx_header["Total (excl. tax)"]].sum()

        mons_diff = (
            month_diff(str(datetime), _date_now, "%Y-%m-%d %H:%M:%S")
            if lang == "en"
            else month_diff(str(datetime), _date_now, "%d/%m/%Y")
        )
        # print(f"Hóa đơn ngày:\t{datetime}")
        md_string += f"## Hóa đơn ngày:\t{datetime}"
        md_string += "\n\n"

        if INTERSTE_CALC:
            # Months differences
            md_string += f" - Số tháng thiếu: {mons_diff}"
            md_string += "\n\n"

            # Debt = total_invoice * mons_diff * interest_rate
            formatted_num = "{:,.0f}".format(total_invoice * mons_diff * interest_rate)
            md_string += f" - Tiền lãi suất: {formatted_num} VND"
            md_string += "\n\n"

        # Invoice total
        # formatted_num = "{:,.0f}".format(total_invoice)
        # md_string += f" - Giá trị hóa đơn: {formatted_num} VND"
        # md_string += "\n\n"

        md_string += "### Hóa đơn chi tiết\n"

        md_string += (
            df_table_view[
                [
                    xlsx_header["Product"],
                    xlsx_header["Quantity"],
                    xlsx_header["Unit price"],
                    xlsx_header["Total (excl. tax)"],
                ]
            ].to_markdown(index=False, colalign=("left", "left", "right", "right"))
            + "\n"
        )
        md_string += f"|Tổng cộng|||**{int(total_invoice):,}**|\n"
        total_of_all_invoice += total_invoice
        total_of_all_invoice_debt += total_invoice * mons_diff * interest_rate

    md_string += f"### Tổng Gốc: {int(total_of_all_invoice):,} VND\n"

    if INTERSTE_CALC:
        md_string += f"### Tổng Lãi: {int(total_of_all_invoice_debt):,} VND\n"
        md_string += f"### Tổng tiền: {total_of_all_invoice+int(total_of_all_invoice_debt):,} VND"

    return md_string


def toPdf(md_string: str):
    css = "<link rel='stylesheet' href='pdf-styles.css'>\n"

    html_string = markdown.markdown(md_string)
    html_string = css + html_string

    with open(f"html.html", "w", encoding="utf-8") as f:
        f.write(html_string)

    pdfkit.from_string(
        html_string,
        "test.pdf",
        configuration=config,
        options={"enable-local-file-access": ""},
        css="pdf-styles.css",
    )
    # pdfkit.from_string(
    #     html_string, "test.pdf", options={"enable-local-file-access": ""}
    # )


if __name__ == "__main__":
    # Init setup
    config = pdfkit.configuration(wkhtmltopdf="./wkhtmltox/bin/wkhtmltopdf.exe")
    xlsx_header = dict()
    default_header = [
        "Ref.",
        "Date",
        "Status",
        "Product",
        "Quantity",
        "Total (excl. tax)",
        "Unit price",
    ]
    lang = ""
    cus_name = ""

    # Create the parser
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument("--interest_rate", "-ir", type=float, default=0.03)
    parser.add_argument("--interest_calc", "-ic", type=int, default=True)
    parser.add_argument(
        "--date_calc", "-dc", type=str, default=datetime.now().strftime("%d/%m/%Y")
    )

    # Parse the arguments
    args = parser.parse_args()

    # Now you can use these arguments in your script
    interest_rate = args.interest_rate
    INTERSTE_CALC = args.interest_calc
    _date_now = args.date_calc

    for file_name in os.listdir("./"):
        total_of_all_invoice = 0  # Đây là tổng tiền các hóa đơn

        # Đây là tổng tiền từng (hóa đơn * lãi xuất hàng háng)
        total_of_all_invoice_debt = 0
        md_string = ""

        if file_name.endswith(".csv"):
            cus_name, _ = file_name.split(".")
            md_string += "**Cửa hàng thuốc bảo vệ thực vật Nam Khang**\n\n"
            md_string += "**Địa chỉ:** 755 Nguyễn Văn Linh, Năm Trại, Tây Ninh.\n\n"
            md_string += "**Số điện thoại:** 0947381573 - Bùi Văn Tư\n\n"
            md_string += f"Ngày đáo hạn thanh toán: **{_date_now}**\n\n"

            if INTERSTE_CALC:
                md_string += f"Lãi suất hàng tháng: **{interest_rate*100}%/tháng**\n\n"

            md_string += f"# Công nợ khách hàng **{cus_name}**\n"

            md_string += debt_cal(
                file_name, total_of_all_invoice, total_of_all_invoice_debt, _date_now
            )

            # toPdf(md_string)

            filename_md = cus_name.replace(" ", "-")
            with open(f"md/{filename_md}_input.md", "w", encoding="utf-8") as f:
                f.write(md_string)

    # # Get a list of all files in the current directory
    # files = os.listdir(".")

    # # Filter the list to include only .xlsx files
    # xlsx_files = [file for file in files if file.endswith(".csv")]

    # # Move each .xlsx file to the /done/ directory
    # for file in xlsx_files:
    #     shutil.move(file, "./done/" + file)
