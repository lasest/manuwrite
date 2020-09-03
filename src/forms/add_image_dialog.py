from PyQt5.QtWidgets import QDialog, QAbstractButton, QFileDialog, QShortcut, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence

from ui_forms.ui_add_image_dialog import Ui_AddImageDialog
import common


class AddImageDialog(QDialog):

    def __init__(self, project_manager, settings_manager, used_identifiers: dict, parent):

        super().__init__(parent=parent)
        self.ui = Ui_AddImageDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.SettingsManager = settings_manager
        self.ProjectManager = project_manager
        self.image_text: str = ""
        self.image_path: str = ""
        self.image_width: int = 0
        self.image_height: int = 0
        if self.ProjectManager:
            self.default_dir = self.ProjectManager.get_setting_value("Absolute path")
        else:
            self.default_dir = self.SettingsManager.get_setting_value("Application/Project folder")
        self.identifier: str = ""
        self.used_identifiers: dict = used_identifiers
        self.has_additional_attributes = False
        self.AcceptShortcut = QShortcut(QKeySequence("Ctrl+Return"), self)

        # Read settings
        self.read_settings()

        # Prepare ui elements
        if self.ui.AutogenIdentifierCheckbox.isChecked():
            self.ui.IdentifierLineEdit.setEnabled(False)
            self.ui.ImageTextLineEdit.setFocus()
        else:
            self.ui.IdentifierLineEdit.setEnabled(True)
            self.ui.IdentifierLineEdit.setFocus()

        # Connect slots and signals
        self.AcceptShortcut.activated.connect(self.on_AcceptShortcut_activated)

    def read_settings(self) -> None:
        self.ui.AutogenIdentifierCheckbox.setChecked(self.SettingsManager.get_setting_value("AddImageDialog/autogen identifier"))
        self.ui.AutonumberCheckbox.setChecked(self.SettingsManager.get_setting_value("AddImageDialog/autonumber"))
        self.ui.WidthLineEdit.setText(str(self.SettingsManager.get_setting_value("Editor/Default image width")))
        self.ui.HeightLineEdit.setText(str(self.SettingsManager.get_setting_value("Editor/Default image height")))

    def write_settigns(self) -> None:
        self.SettingsManager.set_setting_value("AddImageDialog/autogen identifier",
                                               self.ui.AutogenIdentifierCheckbox.isChecked())
        self.SettingsManager.set_setting_value("AddImageDialog/autonumber", self.ui.AutonumberCheckbox.isChecked())

    def generate_identifier(self, identifier: str) -> str:
        index = 1
        while identifier + str(index) in self.used_identifiers:
            index += 1

        return identifier + str(index)

    def accept(self) -> None:
        """Saves values from ui elements to objects attributes"""

        self.image_text = self.ui.ImageTextLineEdit.text()
        self.image_path = self.ui.ImagePathLineEdit.text()
        if self.ui.HeightLineEdit.text():
            self.image_height = int(self.ui.HeightLineEdit.text())
        if self.ui.WidthLineEdit.text():
            self.image_width = int(self.ui.WidthLineEdit.text())

        identifier = ""
        prefix = ""
        # Add prefix to include figure in numbering
        if self.ui.AutonumberCheckbox.isChecked():
            prefix += "fig:"

        # Generate identifier or use one provided by the user
        if self.ui.AutogenIdentifierCheckbox.isChecked():
            identifier = common.generate_identifier(self.ui.ImageTextLineEdit.text(), prefix, self.used_identifiers,
                                                    placeholder="figure")
        else:
            identifier += prefix + self.ui.IdentifierLineEdit.text().strip()

        # Check if identifier is valid and unused
        if not common.is_valid_identifier(identifier, allow_empty=True):
            QMessageBox.warning(self, "Identifier invalid", "Identifier cannot contain spaces or tabulation characters")
            return

        if identifier in self.used_identifiers:
            QMessageBox.warning(self, "Identifier already used", "The identifier you specified is already used in " +
                                "the current document or project. Please specify a unique identifier")
            return

        self.identifier = identifier
        
        # If not has_additional_attribues, the main window will skip the part of the image tag which is in curly braces
        if self.identifier or self.image_width or self.image_height:
            self.has_additional_attributes = True

        self.write_settigns()
        super(AddImageDialog, self).accept()

    @pyqtSlot()
    def on_OpenFileButton_clicked(self) -> None:
        """Calls open file dialog for the user to choose image"""

        path = QFileDialog.getOpenFileName(self, "Choose image", self.default_dir,
                                           "JPEG image (*.jpg *.jpeg *.jpe *.jfif);; PNG image (*.png);;" +
                                           "SVG image (*.svg);;GIF image (*.gif);;All files (*.*)")
        if path:
            self.ui.ImagePathLineEdit.setText(path[0])

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
