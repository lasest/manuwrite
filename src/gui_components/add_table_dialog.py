from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QShortcut, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QKeySequence

from forms.ui_add_table_dialog import Ui_AddTableDialog

import common


class AddTableDialog(QDialog):

    def __init__(self, used_identifiers: dict, settings_manager):
        super().__init__()

        self.ui = Ui_AddTableDialog()
        self.ui.setupUi(self)

        # Set attributes
        self.used_identifiers = used_identifiers
        self.AcceptShortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.table_tag = ""  # The resulting table will be stored here
        self.SettingsManager = settings_manager

        # Read settings
        self.read_settings()

        # Prepare ui
        if self.ui.AutogenIdentifierCheckbox.checkState():
            self.ui.IdentifierLineEdit.setEnabled(False)
            self.ui.CaptionLineEdit.setFocus()
        else:
            self.ui.IdentifierLineEdit.setEnabled(True)
            self.ui.IdentifierLineEdit.setFocus()

        # Connect signals and slots
        self.AcceptShortcut.activated.connect(self.on_AcceptShortcut_activated)

    def read_settings(self) -> None:
        self.ui.AutogenIdentifierCheckbox.setCheckState(self.SettingsManager.get_setting_value("AddImageDialog/autogen identifier"))
        self.ui.AutonumberCheckbox.setCheckState(self.SettingsManager.get_setting_value("AddImageDialog/autonumber"))

    def write_settings(self) -> None:
        self.SettingsManager.set_setting_value("AddImageDialog/autogen identifier",
                                               self.ui.AutogenIdentifierCheckbox.checkState())
        self.SettingsManager.set_setting_value("AddImageDialog/autonumber", self.ui.AutonumberCheckbox.checkState())

    def generate_identifier(self, identifier: str) -> str:
        index = 1
        while identifier + str(index) in self.used_identifiers:
            index += 1

        return identifier + str(index)

    def generate_simple_table(self) -> str:
        text = ""
        row_count = self.ui.TablePreviewWidget.rowCount()
        col_count = self.ui.TablePreviewWidget.columnCount()

        # get maximal column widths
        spacer_width = 2
        column_widths = []
        for column in range(col_count):
            max_width = 1
            for row in range(row_count):
                current_width = len(self.ui.TablePreviewWidget.item(row, column).text())
                if current_width > max_width:
                    max_width = current_width
            column_widths.append(max_width)

        # add header row
        for column in range(col_count):
            text += "{text:<{width}}".format(text=self.ui.TablePreviewWidget.item(0, column).text(),
                                             width=column_widths[column])
            if column + 1 != col_count:
                text += " " * spacer_width
        text += "\n"

        for column in range(col_count):
            text += "{text:<{width}}".format(text="-" * column_widths[column],
                                             width=column_widths[column])
            if column + 1 != col_count:
                text += " " * spacer_width
        text += "\n"

        for row in range(1, row_count):
            for column in range(col_count):
                text += "{text:<{width}}".format(text=self.ui.TablePreviewWidget.item(row, column).text(), width=column_widths[column])
                if column + 1 != col_count:
                    text += " " * spacer_width
            text += "\n"

        return text

    def fill_empty_items(self):
        for row in range(self.ui.TablePreviewWidget.rowCount()):
            for column in range(self.ui.TablePreviewWidget.columnCount()):
                if self.ui.TablePreviewWidget.item(row, column) is None:
                    self.ui.TablePreviewWidget.setItem(row, column, QTableWidgetItem())

    def accept(self) -> None:
        # Handle identifier
        identifier = ""

        # Add prefix to include table in numbering
        if self.ui.AutonumberCheckbox.checkState():
            identifier += "tbl:"

        # Generate identifier or use one provided by the user
        if self.ui.AutogenIdentifierCheckbox.checkState():
            identifier = self.generate_identifier(identifier)
        else:
            identifier += self.ui.IdentifierLineEdit.text().strip()

        # Check if identifier is valid and unused
        if not common.is_valid_identifier(identifier, allow_empty=True):
            QMessageBox.warning(self, "Identifier invalid",
                                "Identifier cannot contain spaces or tabulation characters")
            return

        if identifier in self.used_identifiers:
            QMessageBox.warning(self, "Identifier already used",
                                "The identifier you specified is already used in " +
                                "the current document or project. Please specify a unique identifier")
            return

        # Generate table text
        self.fill_empty_items()
        table_body = self.generate_simple_table()

        # Store table to attribute
        caption_text = f"Table: {self.ui.CaptionLineEdit.text()} {{#{identifier}}}"

        self.table_tag = table_body + "\n" + caption_text

        self.write_settings()
        super().accept()

    @pyqtSlot(int)
    def on_AutogenIdentifierCheckbox_stateChanged(self, state: int) -> None:
        """Disables or enables IdentifierLineEdit based on whether the user wants the identifier to be autogenerated"""
        if state:
            self.ui.IdentifierLineEdit.setEnabled(False)
            self.ui.IdentifierLineEdit.clear()
        else:
            self.ui.IdentifierLineEdit.setEnabled(True)

    @pyqtSlot()
    def on_AcceptShortcut_activated(self) -> None:
        """Accepts the dialog when Ctrl+Enter is pressed"""
        self.accept()

    @pyqtSlot(int)
    def on_RowsSpinBox_valueChanged(self, value: int):
        self.ui.TablePreviewWidget.setRowCount(value)

    @pyqtSlot(int)
    def on_ColumnsSpinBox_valueChanged(self, value: int):
        self.ui.TablePreviewWidget.setColumnCount(value)
