from PyQt5.QtWidgets import QVBoxLayout, QLabel

from manuwrite.views.dock_view import DockView, TitleWidgetTypes


class ConsoleDockView(DockView):

    def __init__(self, parent=None):
        super(ConsoleDockView, self).__init__(title_widget_type=TitleWidgetTypes.LABEL, parent=parent)

        self.set_title("Console dock")

        self.widget().setLayout(QVBoxLayout())
        self.widget().layout().addWidget(QLabel("Console window", self))
