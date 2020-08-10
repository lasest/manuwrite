from PyQt5.QtWidgets import QDialog, QMessageBox, QShortcut
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence

from forms.ui_add_footnote_dialog import Ui_AddFootnoteDialog


class AddFootnoteDialog(QDialog):

    def __init__(self, used_identifiers):

        super().__init__()
        self.ui = Ui_AddFootnoteDialog()
        self.ui.setupUi(self)

        # Set additional attributes
        self.identifier = ""
        self.text = ""
        self.used_identifiers = used_identifiers
        self.AcceptShortcut = QShortcut(QKeySequence("Ctrl+Return"), self)

        # Prepare ui
        if self.ui.AutogenIdentifierCheckbox.checkState():
            self.ui.IdentifierLineEdit.setEnabled(False)
            self.ui.TextPlainTextEdit.setFocus()
        else:
            self.ui.IdentifierLineEdit.setEnabled(True)
            self.ui.IdentifierLineEdit.setFocus()

        # Connect slots and signals
        self.AcceptShortcut.activated.connect(self.on_AcceptShortcut_activated)

    def generate_identifier(self) -> str:
        """Automatically generates a unique identifier for the footnote based on the already used identifiers"""

        identifier = "footnote-"
        index = 1
        while identifier + str(index) in self.used_identifiers:
            index += 1

        return identifier + str(index)

    def accept(self) -> None:
        """Checks if identifier is valid and unique before accepting the dialog"""

        if self.ui.AutogenIdentifierCheckbox.checkState():
            identifier = self.generate_identifier()
        else:
            identifier = self.ui.IdentifierLineEdit.text()

        # Check if identifier is valid and not already used
        identifier = identifier.strip(" ")
        if identifier == "":
            QMessageBox.warning(self, "Identifier invalid", "Identifier field cannot be empty. Please specify a " +
                                "valid identifier or allow to autogenerate it")
            return

        if identifier.find(" ") >= 0 or identifier.find("\t") >= 0:
            QMessageBox.warning(self, "Identifier invalid", "Identifier cannot contain spaces or tabulation characters")
            return

        if identifier in self.used_identifiers:
            QMessageBox.warning(self, "Identifier already used", "The identifier you specified is already used in " +
                                "the current document or project. Please specify a unique identifier")
            return

        self.identifier = identifier
        self.text = self.ui.TextPlainTextEdit.toPlainText()
        super().accept()

    @pyqtSlot(int)
    def on_AutogenIdentifierCheckbox_stateChanged(self, state: int) -> None:
        """Disables or enables IdentifierLineEdit based on whether the user wants the identifier to be autogenerated"""
        if state:
            self.ui.IdentifierLineEdit.setEnabled(False)
        else:
            self.ui.IdentifierLineEdit.setEnabled(True)

    @pyqtSlot()
    def on_AcceptShortcut_activated(self) -> None:
        """Accepts the dialog when Ctrl+Enter is pressed"""
        self.accept()