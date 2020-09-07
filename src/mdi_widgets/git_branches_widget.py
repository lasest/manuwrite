from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_branches_widget import Ui_GitBranchesWidget


class GitBranchesWidget(QWidget):

    def __init__(self, parent):
        super(GitBranchesWidget, self).__init__(parent)

        self.ui = Ui_GitBranchesWidget()
        self.ui.setupUi(self)
