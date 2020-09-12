from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox

from ui_mdi_widgets.ui_git_mdi_area_placeholder_widget import Ui_GitMdiAreaPlaceholderWidget

import common


class GitMdiAreaPlaceholderWidget(QWidget):

    def __init__(self, parent, project_manager, git_manager, handler_function):
        super(GitMdiAreaPlaceholderWidget, self).__init__(parent)

        self.ui = Ui_GitMdiAreaPlaceholderWidget()
        self.ui.setupUi(self)

        self.ProjectManager = project_manager
        self.GitManager = git_manager
        self.GitSignal = common.communicator.GitSignal
        self.GitSignal.connect(handler_function)

    @pyqtSlot()
    def on_CreateRepoPushButton_clicked(self) -> None:
        """Creates a git repository in the current project folder"""
        if not self.ProjectManager.is_project_loaded():
            QMessageBox.warning(self, "No project opened", "Open an existing project or create a new one before " +
                                "initializing a repository.")
        else:
            directory_path = self.ProjectManager.get_setting_value("Absolute path")
            self.GitManager.create_repo_at_path(directory_path)
            self.GitSignal.emit()
