from PyQt5.QtWidgets import QPushButton, QColorDialog
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtCore import Qt


class ColorButton(QPushButton):

    def __init__(self, parent, color: QColor):

        super().__init__(parent)

        self.color = color
        self.setStyleSheet(f"QPushButton {{background-color: {self.color.name()}}}")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # self.color, self, "Choose color"
        if event.button() == Qt.LeftButton:
            self.color = QColorDialog.getColor(self.color)
            self.setStyleSheet(f"QPushButton {{background-color: {self.color.name()}}}")

        super(ColorButton, self).mousePressEvent(event)