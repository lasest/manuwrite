from PyQt5.QtWidgets import QTabWidget
from gui_components.qtabbar_custom import QTabBarCustom


class QTabWidgetCustom(QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setTabBar(QTabBarCustom(self))
