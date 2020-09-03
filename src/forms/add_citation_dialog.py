from typing import Tuple

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QRegExp, Qt
from manubot.cite.handlers import prefix_to_handler

from ui_forms.ui_add_citation_dialog import Ui_AddCitationDialog


class AddCitationDialog(QDialog):

    def __init__(self, thread_manager, parent):
        super().__init__(parent=parent)

        self.ui = Ui_AddCitationDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.citation_identifier = ""
        self.allow_close = True
        self.ThreadManager = thread_manager

        # Get a list of prefixes, supported by manubot
        self.prefixes = list(prefix_to_handler.keys())
        for i in range(len(self.prefixes)):
            self.prefixes[i] += ":"

        # The prefixes that the program will attempt to recognize if no prefix if provided by the user
        self.common_prefixes = {
            "doi": r"10.\d{4,9}/[-._;()/:A-Z0-9]+",
            "short-doi": r"^10/\w{5}$",
            "isbn": r"^((978[\--– ])?[0-9][0-9\--– ]{10}[\--– ][0-9xX])|((978)?[0-9]{9}[0-9Xx])$",
            "pmid": r"^\d{7,8}$",
            "arxiv": r"^\w\w*/\d{7}$|" +
                     r"\d{4}\.\d{4}|" +
                     r"\d{4}\.\d{5}",
            "url": r"^http[s]{0,1}://\w\w*|" +
                   r"^www.\w\w*|" +
                   r"^\w\w*\.\w\w\w*"
        }

    def log(self, text: str) -> None:
        """Logs the message to the ui element"""
        self.ui.InfoTextEdit.appendPlainText(text)

    def check_identifier(self, identifier: str) -> Tuple[str, str]:
        """Tries to determine the identifier type from given citekey. Adds manubot-compatible citation prefix to the
        identifier if no prefix is present and the identifier type can be guessed.
        Returns (identifier type, identifier) -> str, str"""

        ident_type = None

        for tag in self.prefixes:
            if identifier.lower().startswith(tag):
                ident_type = tag[:-1]

        if not ident_type:
            for prefix, regexp in self.common_prefixes.items():
                exp = QRegExp(regexp, Qt.CaseInsensitive)
                index = exp.indexIn(identifier)
                if index >= 0:
                    identifier = prefix + ":" + identifier
                    ident_type = prefix
        if not ident_type:
            self.log("Identifier type cannot be determined. Please check the identifier or add the type manually as" +
                     "in \"doi:identifier\"")

        return ident_type, identifier

    def accept(self) -> None:
        """If check identifier checkbox is checked, make sure that the provided identifier can be identifier by manubot.
        Only checks the format of the identifier (i.e. @doi:10..*), not whether the citation data will be available"""

        if self.ui.CheckIdentifierCheckbox.isChecked():

            identifier_type, identifier = self.check_identifier(self.ui.IdentifierLineEdit.text())
            if identifier_type:
                self.citation_identifier = identifier
                super().accept()
        else:
            self.citation_identifier = self.ui.IdentifierLineEdit.text()
            super().accept()

    @pyqtSlot(dict)
    def on_thread_finished(self, citation_info: dict) -> None:
        """Prints citation info received from pandoc thread to the ui"""

        self.log(citation_info["citation"])

    @pyqtSlot()
    def on_ShowInfoPushButton_clicked(self) -> None:

        # Determine identifier type
        self.log("Checking identifier...")
        identifier_type, identifier = self.check_identifier(self.ui.IdentifierLineEdit.text().strip())

        if identifier_type:
            self.log(f"Type: {identifier_type}")
            self.log(f"Identifier: {identifier}")
            self.log("Retrieving info...\n")
            self.ThreadManager.perform_operation("get_citation", self.on_thread_finished, citekey=identifier)
