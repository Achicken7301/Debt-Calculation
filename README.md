# Debt Calculation

This script will take customer debt table from dolibarr software, calculate with some interest rate and export to pdf file

Default interest rate is 3% per month

`Debt = total_invoice * mons_diff * interest_rate`

Where `mons_diff` is the difference between invoice created date and pay date.


## How to use

Save customer debt table to .xlsx file.

Examples:

Customer's name is: `This is customer name`

Customer `.xlsx` file's name is: `This is customer name.xlsx`

Run 1 time script `Init_Setup.sh`. Then run script `run.sh`.

Pdf files will store into `pdf` folder which name is `This-is-customer-name.pdf.`

`.xlsx` files will move to `done` folder after calculated.
