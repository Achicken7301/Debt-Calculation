import json
from Models.Global import ErrorHandler
from Models.ProgramConfig import ProgramConfig
import os
import requests


class MultiLanguages:
    def __init__(self) -> None:
        # Hard coded - Ill fix this
        self.language = ProgramConfig().read("GENERAL", "language")
        # If no translate folder -> create one
        trans_folder = "translate"
        if not os.path.exists(trans_folder):
            os.makedirs(trans_folder)

        # Check languaage .json
        if not os.path.isfile(f"{trans_folder}/{self.language}.json"):
            # Download from git repo
            language_json_url = f"https://raw.githubusercontent.com/Achicken7301/Debt-Calculation/develop/translate/{self.language}.json"
            language_json_reponse = requests.get(language_json_url)
            if language_json_reponse.status_code == 200:
                with open(
                    f"{os.getcwd()}/{trans_folder}/{self.language}.json", "wb"
                ) as file:
                    file.write(language_json_reponse.content)

        self.load(self.language)

    def get_locale(self) -> str:
        return self.language

    def load(self, my_lang) -> ErrorHandler:
        """
        Load data translate from folder translate with name is `self.language`

        Returns:
            ErrorHandler: _description_
        """
        # TODO: Find if there self.language file in translate folder, if not return FILE_NOT_FOUND
        language_file = f"translate/{my_lang}.json"
        with open(language_file, "r", encoding="utf8") as jsonfile:
            self.trans_data = json.load(jsonfile)

        ErrorHandler.OK

    def trans(self, text: str) -> str:
        # TODO: check condition if there no corect text
        return self.trans_data[text]
