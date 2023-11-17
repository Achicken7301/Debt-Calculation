# Run the Python script
.\Python310\python.exe .\cal_debt.py

# Get all Markdown files in the md directory
$files = Get-ChildItem -Path .\md\ -Filter *_input.md

# Iterate over the files
foreach ($file in $files) {
    # Print the name of the file
    Write-Output $file.Name

    # Get the base name of the file
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    Write-Output "$baseName.pdf"

    # Convert the Markdown file to a PDF
    .\pandoc.exe --pdf-engine='wkhtmltox\bin\wkhtmltopdf.exe' --css=pdf-styles.css -o ".\pdf\$baseName.pdf" $file.FullName
}


