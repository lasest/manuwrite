from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_status_widget import Ui_GitStatusWidget


class GitStatusWidget(QWidget):

    def __init__(self, parent, project_manager, git_manager, handler_function):
        super(GitStatusWidget, self).__init__(parent)

        self.ui = Ui_GitStatusWidget()
        self.ui.setupUi(self)
