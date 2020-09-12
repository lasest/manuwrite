from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_diff_widget import Ui_GitDiffWidget


class GitDiffWidget(QWidget):

    def __init__(self, parent, project_manager, git_manager, handler_function):
        super(GitDiffWidget, self).__init__(parent)

        self.ui = Ui_GitDiffWidget()
        self.ui.setupUi(self)
