from typing import List

from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from ui_forms.ui_create_project_dialog import Ui_CreateProjectDialog


class CreateProjectDialog(QDialog):

    def __init__(self, project_types: List[str], default_path: str):
        super().__init__()

        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)

        # Set attributes
        self.project_types: List[str] = project_types
        self.default_path: str = default_path
        self.title: str = ""
        self.authors: str = ""
        self.project_type: str = ""
        self.path: str = ""

        # Prepare ui
        self.ui.ProjectTypeComboBox.addItems(project_types)
        self.ui.LocationToolButton.setDefaultAction(self.ui.actionChooseFolder)
        self.ui.LocationLineEdit.setText(self.default_path + "/Untitled")

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    @pyqtSlot()
    def on_actionChooseFolder_triggered(self):
        """Creates file dialog for the user to choose project folder"""

        path = QFileDialog.getExistingDirectory(caption="Choose project folder", directory=self.default_path)
        if path:
            self.ui.LocationLineEdit.setText(path)

    def accept(self) -> None:
        """Checks if a specified directory is empty. If it isn't warns the user. If the directory doesn't exist attempts
        to create it"""

        accept = True
        path = self.ui.LocationLineEdit.text()
        directory = QDir(path)

        if directory.exists():
            if not directory.isEmpty():
                reply = QMessageBox.question(self, "Create project?", "The directory you specified is not empty." +
                                             "Are you sure that you want to create the project there?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    accept = False
        else:
            try:
                directory.mkpath(self.ui.LocationLineEdit.text())
            except OSError as e:
                accept = False
                QMessageBox.critical(self, "Error", f"Failed to create project folder: {str(e)}")

        self.path = self.ui.LocationLineEdit.text()
        self.authors = self.ui.AuthoursLineEdit.text()
        self.project_type = self.ui.ProjectTypeComboBox.currentText()
        self.title = self.ui.TitleLineEdit.text()
        if accept:
            super().accept()

