#!/bin/sh

# Check if env folder not exist
if [ ! -d "./env" ]; then
	echo "The 'env' directory does not exist in the current folder."
	echo "Start create env for python"
	# python -m venv env	
	unzip -q env.zip
fi


# Check if pandoc.exe exist
#!/bin/sh
if [ ! -f ./pandoc.exe ]; then
    unzip -q pandoc.zip
fi



echo "Init use env"
# NOTE: Check if this is window or linux
# Actiavte python env
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
. ./env/Scripts/activate

echo "Install from requirements"
pip install -r requirements.txt

# Deactivate env
echo "De-activate python env"
. deactivate


mkdir md pdf done

