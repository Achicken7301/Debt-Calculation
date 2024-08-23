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

        # Read from .conf file
        self.conf_file = ProgramConfig()
        # Store all options into list
        # Load each member of list to Qline
        self.ui.store_name.setText(self.conf_file.read("STORE", "name"))

        # Combine buttons
        self.ui.dialogButtonBox.accepted.connect(self.dialogOK)
        self.ui.dialogButtonBox.rejected.connect(self.dialogCancle)

    def dialogOK(self):
        edited_store_name = self.ui.store_name.text()
        # Get data str from Qline and update to .conf file
        self.conf_file.create_update("STORE", "name", edited_store_name)
        self.conf_file.save()
        self.accept()

    def dialogCancle(self):
        self.close()
