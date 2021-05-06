from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QFontMetrics

from manuwrite.views.git_dock_view import GitDockView


class GitDockController(QObject):

    def __init__(self, view: GitDockView, parent=None):

        super(GitDockController, self).__init__(parent)
        self.view = view

        self._connect_signals_to_slots()
        self.on_titleWidgetComboBox_indexChanged(0)

    def _connect_signals_to_slots(self):
        self.view.titleWidget.currentIndexChanged.connect(self.on_titleWidgetComboBox_indexChanged)

    @pyqtSlot(int)
    def on_titleWidgetComboBox_indexChanged(self, index: int):
        self.view.stackedWidget.setCurrentIndex(index)

        font = self.view.titleWidget.font()
        font_metrics = QFontMetrics(font)
        width = font_metrics.horizontalAdvance(self.view.titleWidget.currentText()) + 32
        self.view.titleWidget.setFixedWidth(width)
