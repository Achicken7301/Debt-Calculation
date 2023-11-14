#!/bin/sh
if [ -d "./env" ]; then
	echo "The 'env' directory exists in the current folder."
else
	echo "The 'env' directory does not exist in the current folder."
	echo "Start create env for python"
	python -m venv env
fi



echo "Init use env"
# NOTE: Check if this is window or linux
# Actiavte python env
. ./env/Scripts/activate

echo "Install from requirements"
pip install -r requirements.txt

# Deactivate env
echo "De-activate python env"
. deactivate


mkdir md pdf done

