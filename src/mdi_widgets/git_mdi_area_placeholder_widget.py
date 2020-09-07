from PyQt5.QtWidgets import QWidget

from ui_mdi_widgets.ui_git_mdi_area_placeholder_widget import Ui_GitMdiAreaPlaceholderWidget


class GitMdiAreaPlaceholderWidget(QWidget):

    def __init__(self, parent):
        super(GitMdiAreaPlaceholderWidget, self).__init__(parent)

        self.ui = Ui_GitMdiAreaPlaceholderWidget()
        self.ui.setupUi(self)
