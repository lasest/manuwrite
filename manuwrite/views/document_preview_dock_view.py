from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtWebEngineWidgets


from manuwrite.views.dock_view import DockView, TitleWidgetTypes


class DocumentPreviewDockView(DockView):

    def __init__(self, parent=None):
        super(DocumentPreviewDockView, self).__init__(title_widget_type=TitleWidgetTypes.LABEL, parent=parent)

        self.set_title("Preview")

        layout = QVBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        self.widget().setLayout(layout)

        web_view_widget = QtWebEngineWidgets.QWebEngineView(self)
        self.widget().layout().addWidget(web_view_widget)

        self.webViewWidget = web_view_widget


