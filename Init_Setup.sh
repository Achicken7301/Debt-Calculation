#!/bin/sh

# Check if env folder not exist
if [ ! -d "./env" ]; then
	python -m venv env
	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
	. ./env/Scripts/activate
	pip install -r requirements.txt
	. deactivate
fi


# Check if pandoc.exe exist
#!/bin/sh
if [ ! -f ./pandoc.exe ]; then
    unzip -q pandoc.zip
fi


mkdir md pdf done

