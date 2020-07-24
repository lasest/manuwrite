from PyQt5.QtWidgets import QDialog, QAbstractButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import (pyqtSlot)

from forms.ui_save_changes_multiple_dialog import Ui_SaveChangesMultipleDialog
from common import Result


class SaveChangesMultipleDialog(QDialog):

    def __init__(self, filenames: [str]):
        super().__init__()
        self.ui = Ui_SaveChangesMultipleDialog()
        self.ui.setupUi(self)
        self.load_icons()
        self.result = Result.CANCEL

        self.ui.listWidget.addItems(filenames)

    def load_icons(self):
        self.ui.IconLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/warning.svg")))

    # Slots
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        if self.ui.buttonBox.buttonRole(button) == self.ui.buttonBox.AcceptRole:
            self.result = Result.SAVE
        elif self.ui.buttonBox.buttonRole(button) == self.ui.buttonBox.DestructiveRole:
            self.result = Result.DISCARD

        self.close()
