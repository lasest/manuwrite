import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from forms import mainwindow
from resources import icons_rc


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_icons()
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)

        self.ui.EditorTabLabel.clicked.connect(self.on_EditorTabLabel_clicked)
        self.ui.GitTabLabel.clicked.connect(self.on_GitTabLabel_clicked)
        self.ui.ProjectTabLabel.clicked.connect(self.on_ProjectTabLabel_clicked)

        self.show()

    def on_EditorTabLabel_clicked(self):
        self.set_active_tab(self.ui.EditorTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(1)

    def on_GitTabLabel_clicked(self):
        self.set_active_tab(self.ui.GitTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(2)

    def on_ProjectTabLabel_clicked(self):
        self.set_active_tab(self.ui.ProjectTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(3)

    def set_icons(self):
        self.ui.EditorTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/document-papirus.svg")))
        self.ui.GitTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/git-branch.svg")))
        self.ui.ProjectTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/project-management.svg")))

    def set_active_tab(self, label: QLabel):

        for tab in self.tabs:
            tab.setStyleSheet("QLabel { background-color: black}")

        label.setAutoFillBackground(True)
        label.setStyleSheet("QLabel { background-color : blue; }")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
