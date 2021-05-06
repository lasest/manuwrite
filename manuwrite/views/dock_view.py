from enum import Enum

from PyQt5.QtWidgets import (QDockWidget, QFrame, QHBoxLayout, QLabel, QWidget, QSizePolicy, QPushButton, QComboBox)
from PyQt5.QtCore import Qt


class TitleWidgetTypes(Enum):
    LABEL = 0
    COMBOBOX = 1


class DockView(QDockWidget):

    def __init__(self, title_widget_type: TitleWidgetTypes = TitleWidgetTypes.LABEL, parent=None):

        super(DockView, self).__init__(parent)
        self.title_widget_type = title_widget_type

        self._create_title_bar()
        self._create_main_widget()

        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setContextMenuPolicy(Qt.PreventContextMenu)

    def _create_title_bar(self):
        title_bar = QFrame(self)
        title_bar.setObjectName("DockTitleBar")

        # Set title bar geometry
        title_bar.setFixedHeight(title_bar.fontMetrics().height() * 1.5)

        # Create layout for the title bar
        layout = QHBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setAlignment(Qt.AlignVCenter)
        title_bar.setLayout(layout)

        # Create title label and close button
        title_widget = None
        if self.title_widget_type == TitleWidgetTypes.LABEL:
            title_widget = QLabel(title_bar)
        else:
            title_widget = QComboBox(title_bar)
        title_widget.setObjectName("DockTitleBar_TitleWidget")
        title_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        spacer = QWidget(title_bar)
        spacer.setObjectName("Spacer")
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        close_button = QPushButton("x", title_bar)
        close_button.setObjectName("DockTitleBar_CloseButton")

        close_button.setFixedWidth(close_button.fontMetrics().height())
        close_button.setFixedHeight(close_button.fontMetrics().height())

        # Set attributes and add widgets to the layout
        title_bar.layout().addWidget(title_widget)
        title_bar.layout().addWidget(spacer)
        title_bar.layout().addWidget(close_button)

        self.setTitleBarWidget(title_bar)

        self.closeButton = close_button
        self.titleWidget = title_widget

    def _create_main_widget(self):
        widget = QWidget(self)
        widget.setObjectName("DockMainWidget")
        self.setWidget(widget)

    def insert_widget_right(self, widget: QWidget):
        pass

    def set_title(self, title: str):
        if self.title_widget_type == TitleWidgetTypes.LABEL:
            self.titleWidget.setText(title)
        else:
            self.titleWidget.setCurrentText(title)

    def add_title_option(self, text: str):
        if self.title_widget_type == TitleWidgetTypes.COMBOBOX:
            self.titleWidget.addItem(text)
        else:
            raise ValueError("Attempting to add title option to Dock titleWidget, which is not a QComboBox")
