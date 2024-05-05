import configparser


class ProgramConfig:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(".conf")  # Replace 'settings.conf' with your file name

    def create_update(self, section: str, opt: str, opt_data: str):
        self.config[section][opt] = opt_data

    def read(self, section: str, opt: str) -> str:
        return self.config[section][opt]

    def save(self):
        with open(".conf", "w") as configfile:
            self.config.write(configfile)
