from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_commit_widget import Ui_GitCommitWidget


class GitCommitWidget(QWidget):

    def __init__(self, parent):
        super(GitCommitWidget, self).__init__(parent)

        self.ui = Ui_GitCommitWidget()
        self.ui.setupUi(self)
