from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_status_widget import Ui_GitStatusWidget


class GitStatusWidget(QWidget):

    def __init__(self, parent):
        super(GitStatusWidget, self).__init__(parent)

        self.ui = Ui_GitStatusWidget()
        self.ui.setupUi(self)
