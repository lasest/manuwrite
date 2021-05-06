from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import QEvent, Qt


class WelcomePageInfoBlock(QFrame):

    def __init__(self, parent):

        super(WelcomePageInfoBlock, self).__init__(parent)
        self.setObjectName("WelcomePage_InfoBlock")

        self.titleLabel = QLabel(self)
        self.descriptionLabel = QLabel(self)

        self.setLayout(QVBoxLayout())

        self.layout().addWidget(self.titleLabel)
        self.layout().addWidget(self.descriptionLabel)

    def set_title(self, text: str):
        self.titleLabel.setText(text)

    def set_description(self, text: str):
        self.descriptionLabel.setText(text)

    def enterEvent(self, event: QEvent):
        self.setCursor(Qt.PointingHandCursor)
        super(WelcomePageInfoBlock, self).enterEvent(event)