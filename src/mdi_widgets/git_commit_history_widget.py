from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_commit_history_widget import Ui_GitCommitHistoryWidget


class GitCommitHistoryWidget(QWidget):

    def __init__(self, parent):
        super(GitCommitHistoryWidget, self).__init__(parent)

        self.ui = Ui_GitCommitHistoryWidget()
        self.ui.setupUi(self)
