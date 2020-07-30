from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from forms.ui_create_project_dialog import Ui_CreateProjectDialog

class CreateProjectDialog(QDialog):

    def __init__(self, project_types, default_path: str):
        super().__init__()

        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)

        self.project_types = project_types
        self.default_path = default_path

        self.ui.ProjectTypeComboBox.addItems(project_types)
        self.ui.LocationToolButton.setDefaultAction(self.ui.actionChooseFolder)
        self.ui.LocationLineEdit.setText(self.default_path + "/Untitled")

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.title = ""
        self.authors = ""
        self.project_type = ""
        self.path = ""

    @pyqtSlot()
    def on_actionChooseFolder_triggered(self):
        path = QFileDialog.getExistingDirectory(caption="Choose project folder", directory=self.default_path)
        if path:
            self.ui.LocationLineEdit.setText(path)

    def accept(self) -> None:
        directory = QDir(self.ui.LocationLineEdit.text())
        if directory.exists():
            if not directory.isEmpty():
                dialog = QMessageBox()
                reply = QMessageBox.question(self, "Create project?", "The directory you specified is not empty. Are you" +
                                     "sure that you want to create the project there?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return

        self.path = self.ui.LocationLineEdit.text()
        self.authors = self.ui.AuthoursLineEdit.text()
        self.project_type = self.ui.ProjectTypeComboBox.currentText()
        self.title = self.ui.TitleLineEdit.text()
        super().accept()

