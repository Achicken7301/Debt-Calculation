from PyQt5 import QtWidgets
from Models.ProgramConfig import ProgramConfig
from ui.edit_store_infos_ui import Ui_EditStoreDialog


class EditStoreInfos(QtWidgets.QDialog):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.ui = Ui_EditStoreDialog()
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
        section = "STORE"
        conf = ProgramConfig()
        opt_list = conf.get_all_opt_in(section)

        # Load each member of list to Qline
        for i in range(len(self.store_Qline_edit_list)):
            self.store_Qline_edit_list[i].setText(conf.read(section, opt_list[i]))

    def save_all_conf_data(self):
        section = "STORE"
        conf = ProgramConfig()
        opt_list = conf.get_all_opt_in(section)
        # Get qline text and store info .conf file
        for i in range(len(self.store_Qline_edit_list)):
            conf.create_update(
                section, opt_list[i], self.store_Qline_edit_list[i].text()
            )

        conf.save()

    def dialogOK(self):
        edited_store_name = self.ui.store_name.text()
        self.save_all_conf_data()
        self.accept()

    def dialogCancle(self):
        self.close()
