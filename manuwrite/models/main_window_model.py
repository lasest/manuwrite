from PyQt5.QtCore import QObject


class MainWindowModel(QObject):

    def __init__(self, parent=None):
        super(MainWindowModel, self).__init__(parent)

        self.editorPageFullyInitiated = False
        self.gitPageFullyInitiated = False
