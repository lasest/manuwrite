from PyQt5.QtWidgets import QDialog, QAbstractButton, QMessageBox
from PyQt5.QtCore import pyqtSlot

from ui_forms.ui_add_link_dialog import Ui_AddLinkDialog


class AddLinkDialog(QDialog):

    def __init__(self, parent):

        super().__init__(parent=parent)
        self.ui = Ui_AddLinkDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.link: str = ""

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button: QAbstractButton) -> None:
        """Saves inputs from ui elements to class attributes. Performs basic checks that the link info is correct"""

        # Incomplete list of prefixes that pandoc recognizes as links in <prefix link>
        prefixes = (
            "https://", "http://", "ftp://", "ftps://", "ssh://", "file://", "mailto:", "magnet:"
        )

        address = self.ui.LinkAddressLineEdit.text()
        text = self.ui.LinkTextLineEdit.text()

        # If text is given use usual markdown link syntax, otherwise try to use <link> syntax
        if text:
            self.link = f"[{text}]({address})"
        else:
            if address.startswith(prefixes):
                self.link = f"<{address}>"
            else:
                self.link = f"<https://{address}>"
