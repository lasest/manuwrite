from PyQt5.QtWidgets import QDialog, QAbstractButton
from PyQt5.QtCore import pyqtSlot

from forms.ui_add_link_dialog import Ui_AddLinkDialog

class AddLinkDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_AddLinkDialog()
        self.ui.setupUi(self)
        self.link_text = ""
        self.link_address = ""

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        self.link_text = self.ui.LinkTextLineEdit.text()
        self.link_address = self.ui.LinkAddressLineEdit.text()
