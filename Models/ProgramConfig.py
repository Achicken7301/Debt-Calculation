import configparser
import os
import shutil


class ProgramConfig:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        # Check there is .conf file, if not, copy from example from example.conf file to .conf
        if self.ensure_conf_file():
            print("Create .conf file")

        self.config.read(".conf")  # Replace 'settings.conf' with your file name

    def ensure_conf_file(
        self, conf_file=".conf", example_conf_file="example.conf"
    ) -> bool:
        if not os.path.isfile(conf_file):
            shutil.copyfile(example_conf_file, conf_file)
            return True
        else:
            return False

    def create_update(self, section: str, opt: str, opt_data: str):
        self.config[section][opt] = opt_data

    def read(self, section: str, opt: str) -> str:
        print(f"[{section}][{opt}]")
        return self.config[section][opt]

    def save(self):
        with open(".conf", "w") as configfile:
            self.config.write(configfile)
