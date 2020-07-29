import subprocess

from PyQt5.QtWidgets import QDialog, QAbstractButton
from PyQt5.QtCore import pyqtSlot, QRegExp, Qt, QThread
from manubot.cite.handlers import prefix_to_handler

from forms.ui_add_citation_dialog import Ui_AddCitationDialog
from components.thread_manager import ThreadManager


class AddCitationDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_AddCitationDialog()
        self.ui.setupUi(self)

        self.prefixes = tuple(prefix_to_handler.keys())
        self.prefixes_with_colon = []
        for prefix in self.prefixes:
            self.prefixes_with_colon.append(prefix + ":")
        self.prefixes = tuple(self.prefixes_with_colon)
        self.citation_identifier = ""
        self.allow_close = True
        self.ThreadManager = ThreadManager()
        self.ThreadManager.manubotCiteThreadFinished.connect(self.on_thread_finished)
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
        self.ui.InfoTextEdit.appendPlainText(text)

    @pyqtSlot()
    def on_ShowInfoPushButton_clicked(self) -> bool:
        text = ""
        # Determine identifier type
        self.log("Checking identifier...")
        data = self.check_identifier(self.ui.IdentifierLineEdit.text().strip())
        if data[0]:
            self.log("Type: {}".format(data[0]))
            self.log("Identifier: {}".format(data[1]))
            self.log("Retrieving info...\n")
            self.ThreadManager.get_citation(data[1])


    def accept(self) -> None:
        if self.ui.CheckIdentifierCheckbox.isChecked():
            data = self.check_identifier(self.ui.IdentifierLineEdit.text())
            if data[0]:
                self.citation_identifier = data[1]
                super().accept()
        else:
            self.citation_identifier = self.ui.IdentifierLineEdit.text()
            super().accept()

    def check_identifier(self, identifier: str):
        ident_type = None

        for tag in self.prefixes:
            if identifier.lower().startswith(tag):
                ident_type = tag[:-1]

        if not ident_type:
            for item in self.common_prefixes.items():
                exp = QRegExp(item[1], Qt.CaseInsensitive)
                index = exp.indexIn(identifier)
                if index >= 0:
                    identifier = item[0] + ":" + identifier
                    ident_type = item[0]
        if not ident_type:
            self.log("Identifier type cannot be determined. Please check the identifier or add the type manually as in \"doi:identifier\"")

        return (ident_type, identifier)

    @pyqtSlot(str, str)
    def on_thread_finished(self, citekey: str, citation: str):
        self.ui.InfoTextEdit.appendPlainText(citation)
