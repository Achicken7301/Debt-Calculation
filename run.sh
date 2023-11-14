#!/bin/bash
. ./env/Scripts/activate

python ./cal_debt.py

for file in md/*_input.md; do
    echo $file
    echo $(basename ${file%.md}.pdf)

    ./pandoc.exe --pdf-engine='wkhtmltox/bin/wkhtmltopdf.exe' --css=pdf-styles.css -o pdf/$(basename ${file%.md}.pdf) $file
done

. deactivate
