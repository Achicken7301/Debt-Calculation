# Debt Calculation

This script will take customer debt table from dolibarr software, calculate with some interest rate and export to pdf file

Default interest rate is `3%` per month

`Debt = total_invoice * mons_diff * interest_rate`

Where `mons_diff` is the difference between invoice created date and pay date.


## How to use

Right click at `Init_setup.ps1` then `Run with PowerShell`. The setup will take time.

File `.csv` must be seperate by tab `\t`. Open `samples file.csv` with notepad for more details.

File `run.ps1` will run default setting which is: interest rate is `3%/month` and invoice pay date is `now` (the time run the script).

```powershell
Python310\python.exe ./cal_debt.py
./md2pdf.ps1
```

**To set invoice pay date to different one** like `04/10/2023` in `%d/%m/%Y` format.

```powershell
Python310\python.exe ./cal_debt.py -dc 04/10/2023
./md2pdf.ps1
```

To set different **invoice pay date** and **no calculate interest rate**.

```powershell
Python310\python.exe ./cal_debt.py -dc 04/10/2023 -ic 0
./md2pdf.ps1
```

To change **interest rate** to `1%/month`.

```powershell
Python310\python.exe ./cal_debt.py -dc 04/10/2023 -ic 0 -ir 0.01
./md2pdf.ps1
```

For further infomation run

```powershell
Python310\python.exe ./cal_debt.py -h
```