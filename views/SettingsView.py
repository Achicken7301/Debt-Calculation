from PyQt5 import QtWidgets
from Models.Global import ExportFormat, Option, Section
from Models.ProgramConfigModel import ProgramConfig
from ui.settings_ui import Ui_SettingsDialog


class Settings(QtWidgets.QDialog):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        # order is matter here cuz it need to be fixed with .conf file
        self.store_Qline_edit_list = [
            self.ui.store_name,
            self.ui.store_addr,
            self.ui.store_street,
            self.ui.store_dist,
            self.ui.store_province,
            self.ui.store_city,
            self.ui.store_phone,
        ]

        # Read from .conf file
        self.load_all_conf_data()

        # Combine buttons
        self.ui.dialogButtonBox.accepted.connect(self.dialogOK)
        self.ui.dialogButtonBox.rejected.connect(self.dialogCancle)

    def load_all_conf_data(self):
        conf = ProgramConfig()
        opt_list = conf.get_all_opt_in(Section.STORE.value)

        # Load each member of list to Qline
        for i in range(len(self.store_Qline_edit_list)):
            self.store_Qline_edit_list[i].setText(
                conf.read(Section.STORE.value, opt_list[i])
            )

        # Get export_format from .conf file
        # conf.read("GENERAL", "export_format")
        # self.ui.export_format.setEditText(
        #     conf.read(Section.GENERAL.value, Option.export_format.value)
        # )
        self.ui.export_format_comboBox.setCurrentText(
            conf.read(Section.GENERAL.value, Option.export_format.value)
        )

    def save_all_conf_data(self):
        conf = ProgramConfig()
        opt_list = conf.get_all_opt_in(Section.STORE.value)
        # Get qline text and store info .conf file
        for i in range(len(self.store_Qline_edit_list)):
            conf.create_update(
                Section.STORE.value, opt_list[i], self.store_Qline_edit_list[i].text()
            )

        conf.create_update(
            Section.GENERAL.value,
            Option.export_format.value,
            self.ui.export_format_comboBox.currentText(),
        )

        conf.save()

    def dialogOK(self):
        self.save_all_conf_data()
        self.accept()

    def dialogCancle(self):
        self.close()
