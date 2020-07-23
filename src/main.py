import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QFile, QIODevice, QUrl)
from PyQt5.QtGui import *

from forms import mainwindow
from resources import icons_rc
from gui_components.text_editor import TextEditor


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_icons()
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)

        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EditorTabWidget.clear()

        self.show()

    # Utility functions
    def set_icons(self):
        self.ui.EditorTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/document-papirus.svg")))
        self.ui.GitTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/git-branch.svg")))
        self.ui.ProjectTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/project-management.svg")))
        self.ui.SettingsLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/settings.svg")))
        self.ui.UserAccounLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_dark/icons_dark/account.svg")))

    def set_active_tab(self, label: QLabel):
        for tab in self.tabs:
            tab.setStyleSheet("QLabel { background-color: black}")

        label.setAutoFillBackground(True)
        label.setStyleSheet("QLabel { background-color : blue; }")

    # Signal handling
    @pyqtSlot()
    def on_EditorTabLabel_clicked(self):
        self.set_active_tab(self.ui.EditorTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_GitTabLabel_clicked(self):
        self.set_active_tab(self.ui.GitTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def on_ProjectTabLabel_clicked(self):
        self.set_active_tab(self.ui.ProjectTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def on_actionNew_triggered(self):
        new_widget = QWidget()
        new_widget.setLayout(QVBoxLayout())
        editor = TextEditor(new_widget)
        new_widget.layout().addWidget(editor)

        self.on_EditorTabLabel_clicked()
        index = self.ui.EditorTabWidget.addTab(new_widget, "New tab")
        self.ui.EditorTabWidget.setCurrentIndex(index)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0]:
            file_handle = open(filename[0], mode="r")
            text = file_handle.read()
            file_handle.close()

            self.on_actionNew_triggered()
            self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).appendPlainText(text)
            self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).document().setBaseUrl(QUrl.fromLocalFile(filename[0]))

    @pyqtSlot()
    def on_actionSave_triggered(self):
        if self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).document().baseUrl().url():
            file_handle = open(self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).document().baseUrl().url(QUrl.PreferLocalFile), mode="w")
            file_handle.write(self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).toPlainText())
            file_handle.close()
        else:
            self.on_actionSave_As_triggered()

    @pyqtSlot()
    def on_actionSave_As_triggered(self):
        filename = QFileDialog.getSaveFileName()
        if filename[0]:
            file_handle = open(filename[0], mode="w+")
            file_handle.write(self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).toPlainText())
            file_handle.close()

            self.ui.EditorTabWidget.currentWidget().findChild(TextEditor).document().setBaseUrl(QUrl.fromLocalFile(filename[0]))

    @pyqtSlot(int)
    def on_EditorTabWidget_tabCloseRequested(self, index):
        self.ui.EditorTabWidget.removeTab(index)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
