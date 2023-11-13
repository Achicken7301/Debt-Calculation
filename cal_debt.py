import sys
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

# import markdown
# import pypandoc
# import codecs
# import pdfkit


interest_rate = 0.03
input = ["Date", "Status", "Quantity", "Unit price", "Total (excl. tax)"]

# Đây là tổng tiền các hóa đơn
total_of_all_invoice = 0

# Đây là tổng tiền từng (hóa đơn * lãi xuất hàng háng)
total_of_all_invoice_debt = 0


def month_diff(_date):
    # Given date
    given_date = datetime.strptime(_date, "%Y-%m-%d %H:%M:%S")

    # Current date
    now = datetime.now()

    # Calculate the difference in months
    diff = relativedelta(now, given_date)
    months_diff = diff.years * 12 + diff.months
    return months_diff


def debt_cal(cus_name: str):
    global md_string, total_of_all_invoice, total_of_all_invoice_debt
    df = pd.read_excel(f"{cus_name}.xlsx")

    #
    df = df[df["Status"] == "Not paid"]

    #
    unique_date = df["Date"].unique()

    for datetime in unique_date:
        df_by_date = df[df["Date"] == datetime]

        total_invoice = df_by_date["Total (excl. tax)"].sum()

        mons_diff = month_diff(str(datetime))
        # print(f"Hóa đơn ngày:\t{datetime}")
        md_string += f"## Hóa đơn ngày:\t{datetime}"
        md_string += "\n\n"

        # Months differences
        md_string += f" - Số tháng thiếu: {mons_diff}"
        md_string += "\n\n"

        # Invoice total
        formatted_num = "{:,}".format(total_invoice)
        md_string += f" - Giá trị hóa đơn: {formatted_num} VND"
        md_string += "\n\n"

        # Debt = total_invoice * mons_diff * interest_rate
        formatted_num = "{:,.0f}".format(total_invoice * mons_diff * interest_rate)
        md_string += f" - Tiền lãi suất: {formatted_num} VND"
        md_string += "\n\n"

        # Invoice detail
        # Format table before printout ERROR but works
        df_by_date[["Total (excl. tax)", "Unit price"]] = df_by_date[
            ["Total (excl. tax)", "Unit price"]
        ].map("{:,}".format)
        print(df_by_date[["Product", "Quantity", "Unit price", "Total (excl. tax)"]])

        md_string += "### Hóa đơn chi tiết\n"
        md_string += (
            df_by_date[
                ["Product", "Quantity", "Unit price", "Total (excl. tax)"]
            ].to_markdown()
            + "\n"
        )

        total_of_all_invoice += total_invoice
        total_of_all_invoice_debt += total_invoice * mons_diff * interest_rate

    md_string += f"### Tổng Gốc: {total_of_all_invoice:,} VND\n"
    md_string += f"### Tổng Lãi: {int(total_of_all_invoice_debt):,} VND\n"
    md_string += (
        f"### Tổng tiền: {total_of_all_invoice+int(total_of_all_invoice_debt):,} VND"
    )


if __name__ == "__main__":
    cus_name = ""
    for file_name in os.listdir("./"):
        md_string = ""
        if file_name.endswith(".xlsx"):
            cus_name, _ = file_name.split(".")

            md_string += "**Công ty thuốc bảo vệ thực vật Nam Khang**\n\n"
            md_string += "**Địa chỉ:** 755 Nguyễn Văn Linh, Năm Trại, Tây Ninh.\n\n"
            md_string += "**Số điện thoại:** 0947381573 - Bùi Văn Tư\n\n"

            md_string += f"# Công nợ khách hàng **{cus_name}**\n"

            debt_cal(cus_name)

            # toPdf()
            # print(md_string)
            filename_md = cus_name.replace(" ", "-")
            with open(f"md/{filename_md}_input.md", "w", encoding="utf-8") as f:
                f.write(md_string)
