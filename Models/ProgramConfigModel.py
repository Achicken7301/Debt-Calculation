from configparser import ConfigParser
import os.path
from shutil import copyfile
from Models.Global import ExportFormat, Option, Section


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class ProgramConfig(SingletonClass):

    def __init__(self) -> None:
        self.config =ConfigParser()
        # Check there is .conf file, if not, copy from example from example.conf file to .conf
        if self.ensure_conf_file():
            print("Create .conf file")

        self.config.read(
            ".conf", encoding="utf-8"
        )  # Replace 'settings.conf' with your file name

        # Will optimize this later
        self.section = dict()
        self.option = dict()
        self.section[Section.GENERAL] = Section.GENERAL.value
        self.option[Option.export_format] = Option.export_format.value

    def get_all_opt_in(self, sec_target: str) -> list:
        """Return as a list of all opt in section

        Args:
            section (str): section in file

        Returns:
            list: list of all opts
        """
        temp_opt = list()
        for opt in self.config.options(section=sec_target):
            temp_opt.append(opt)

        return temp_opt

    def ensure_conf_file(
        self, conf_file=".conf", example_conf_file="example.conf"
    ) -> bool:
        if not os.path.isfile(conf_file):
            copyfile(example_conf_file, conf_file)
            return True
        else:
            return False

    def create_update(self, section: str, opt: str, opt_data: str):
        """Create AND Update
        But remember to self.config.save() to store data to file

        Args:
            section (str): CAPS
            opt (str): options
            opt_data (str): updated data
        """
        self.config[section][opt] = opt_data

    def read(self, section: str, opt: str):
        if section == Section.GENERAL and opt == Option.export_format:
            value_export_format = self.config[self.section[Section.GENERAL]][
                self.option[Option.export_format]
            ]
            if value_export_format == ExportFormat.DOCX.value:
                return ExportFormat.DOCX
            elif value_export_format == ExportFormat.EXCEL.value:
                return ExportFormat.EXCEL
            else:
                return ExportFormat.PDF

        return str(self.config[section][opt])

    def save(self):
        with open(".conf", "w", encoding="utf-8") as configfile:
            self.config.write(configfile)
