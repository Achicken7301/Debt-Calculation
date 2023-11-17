echo "This process will take time!!! Please be patient and wait."
echo "unzip python folder"
unzip -q .\Python310.zip

echo "Installing packages"
.\Python310\python.exe -m pip install -r requirements.txt --no-warn-script-location


# Check if pandoc.exe exist
if (!(Test-Path -Path "./pandoc.exe")) {
    Expand-Archive -Path pandoc.zip -DestinationPath . -Force
}

echo "Create template folders"
New-Item -ItemType Directory -Force -Path md, pdf, done

