from enum import Enum

from PyQt5.QtWidgets import QDialog, QAbstractButton, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import (pyqtSlot)

from forms.ui_save_changes_single_dialog import Ui_SaveChangesSingleDialog


class Result(Enum):
    CANCEL = 0
    SAVE = 1
    DISCARD = 2


class SaveChangesSingleDialog(QDialog):

    def __init__(self, filename: str):
        super().__init__()
        self.ui = Ui_SaveChangesSingleDialog()
        self.ui.setupUi(self)
        self.set_text(filename)
        self.load_icons()
        self.result = Result.CANCEL


    # Utility functions
    def set_text(self, filename):
        self.ui.MessageLabel.setText("The file {} has been modified.\nDo you want to save changes or discard them?".format(filename))

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
