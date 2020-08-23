from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtGui import QMouseEvent


class QTabBarCustom(QTabBar):

    def __init__(self, parent):
        super().__init__(parent)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Closes the tab is the user clicks it with middle mouse button"""

        if event.button() == Qt.MidButton:
            self.tabCloseRequested.emit(self.tabAt(event.pos()))

        super(QTabBar, self).mouseReleaseEvent(event)
