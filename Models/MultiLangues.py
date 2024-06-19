import json
from Models.Global import ErrorHandler
from Models.ProgramConfig import ProgramConfig
import os


class MultiLanguages:
    def __init__(self) -> None:
        self.language = ProgramConfig().read("DEFAULT", "language")

        self.load()

    def get_locale(self) -> str:
        return self.language

    def load(self) -> ErrorHandler:
        """
        Load data translate from folder translate with name is `self.language`

        Returns:
            ErrorHandler: _description_
        """
        # TODO: Find if there self.language file in translate folder, if not return FILE_NOT_FOUND
        language_file = f"translate/{self.language}.json"
        with open(language_file, "r", encoding="utf8") as jsonfile:
            self.trans_data = json.load(jsonfile)

        ErrorHandler.OK

    def trans(self, text: str) -> str:
        # TODO: check condition if there no corect text
        return self.trans_data[text]
