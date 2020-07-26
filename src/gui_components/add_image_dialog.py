from PyQt5.QtWidgets import QDialog, QAbstractButton, QFileDialog
from PyQt5.QtCore import pyqtSlot

from forms.ui_add_image_dialog import Ui_AddImageDialog

class AddImageDialog(QDialog):

    def __init__(self):

        super().__init__()
        self.ui = Ui_AddImageDialog()
        self.ui.setupUi(self)
        self.image_text = ""
        self.image_path = ""

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        self.image_text = self.ui.ImageTextLineEdit.text()
        self.image_path = self.ui.ImagePathLineEdit.text()

    @pyqtSlot()
    def on_OpenFileButton_clicked(self):
        path = QFileDialog.getOpenFileName()
        if path:
            self.ui.ImagePathLineEdit.setText(path[0])