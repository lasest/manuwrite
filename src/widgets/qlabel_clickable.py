from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QLabelClickable(QLabel):

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev) -> None:
        """Emits clicked signal when the user clicks on the label"""

        self.clicked.emit()

