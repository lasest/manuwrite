import copy

from PyQt5.QtWidgets import QDialog, QCompleter, QTreeWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot

from ui_forms.ui_add_crossref_dialog import Ui_AddCrossRefDialog
import common
import defaults


class AddCrossRefDialog(QDialog):

    def __init__(self, project_structure: dict, is_cursor_in_sentence: bool, parent):

        super().__init__(parent=parent)
        self.ui = Ui_AddCrossRefDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.tag = ""
        self.project_structure = project_structure

        self.identifier_list = self.get_identifier_list()
        self.IdentifierCompleter = QCompleter(self.identifier_list, self)
        self.IdentifierCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.IdentiferLineEdit.setCompleter(self.IdentifierCompleter)

        # Prepare ui
        common.load_project_structure(self.project_structure, self.ui.StructureTreeWidget, ["footnotes", "citations"])
        self.ui.StructureTreeWidget.setHeaderLabels(("Text", "Identifier"))

        if is_cursor_in_sentence:
            self.ui.LCCleverRefRadioButton.setChecked(True)
        else:
            self.ui.TCCleverRefRadioButton.setChecked(True)

    def get_identifier_list(self) -> list:
        """Returns a list of all identifiers in project structure"""

        #del self.project_structure["filepath"]
        identifiers = list()

        for item1 in self.project_structure.items():
            for item2 in item1[1].items():
                identifiers.append(item2[0])

        return identifiers

    def accept(self) -> None:
        """Forms a tag based on the ui contents before closing the form"""
        identifier = self.ui.IdentiferLineEdit.text()

        # Check if identifier exists
        if identifier not in self.identifier_list:
            QMessageBox.warning(self, "Identifier invalid",
                                "Identifier you specified has not been found. Please specify an identifier defined " +
                                "in the current namespace (files to be rendered if current file is to be rendered or " +
                                "only the current file if it is not.")
            return

        # Determine reference type
        identifier_categories = copy.deepcopy(defaults.identifier_categories)
        identifier_categories.remove("footnotes")
        identifier_categories.remove("citations")

        identifier_category = ""
        for category in identifier_categories:
            if identifier in self.project_structure[category]:
                identifier_category = category
                break

        # Form tag
        tag = "@"
        prefix = defaults.identifier_prefixes[identifier_category]

        if not identifier.startswith(prefix + ":"):
            tag += prefix + ":"

        tag += identifier

        # Handle clever references
        clever_ref_symbol = ""
        if self.ui.LCCleverRefRadioButton.isChecked():
            clever_ref_symbol = "+"
        elif self.ui.TCCleverRefRadioButton.isChecked():
            clever_ref_symbol = "*"
        elif self.ui.NoCleverRefRadioButton.isChecked():
            clever_ref_symbol = "!"

        tag = clever_ref_symbol + tag

        self.tag = tag

        super().accept()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_StructureTreeWidget_itemClicked(self, item, column_number) -> None:
        """Fills IdentifierLineEdit with identifier, which was clicked on in the StructureTreeWidget"""
        self.ui.IdentiferLineEdit.setText(item.text(1))
