from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QUrl)
from PyQt5.QtGui import *

from forms.ui_main_window import Ui_MainWindow
from resources import icons_rc
from gui_components.text_editor import TextEditor
from gui_components.save_changes_single_dialog import (SaveChangesSingleDialog, Result)
from gui_components.qtabbar_custom import QTabBarCustom


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_icons()
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)

        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EditorTabWidget.setTabsClosable(True)
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
            background_color = self.palette().color(self.palette().Background)
            tab.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

        label.setAutoFillBackground(True)
        background_color = self.palette().color(self.palette().Highlight)
        label.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

    def get_editor(self, tab_index: int = None) -> TextEditor:
        if tab_index is None:
            tab_index = self.ui.EditorTabWidget.currentIndex()

        return self.ui.EditorTabWidget.widget(tab_index).findChild(TextEditor)

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
        new_widget.layout().setContentsMargins(0,2,0,0)

        self.on_EditorTabLabel_clicked()
        index = self.ui.EditorTabWidget.addTab(new_widget, "New tab")
        self.ui.EditorTabWidget.setCurrentIndex(index)
        self.ui.EditorTabWidget.setTabText(index, "Untitled")
        self.get_editor().setFocus()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0]:
            file_handle = open(filename[0], mode="r")
            text = file_handle.read()
            file_handle.close()

            self.on_actionNew_triggered()
            self.get_editor().appendPlainText(text)
            self.get_editor().document().setBaseUrl(QUrl.fromLocalFile(filename[0]))

            index = filename[0].rfind("/")
            self.ui.EditorTabWidget.setTabText(self.ui.EditorTabWidget.currentIndex(), filename[0][index+1:])

    @pyqtSlot()
    def on_actionSave_triggered(self, index=None) -> bool:
        if index is None:
            index = self.ui.EditorTabWidget.currentIndex()

        if self.get_editor(index).document().baseUrl().url():
            file_handle = open(self.get_editor(index).document().baseUrl().url(QUrl.PreferLocalFile), mode="w")
            file_handle.write(self.get_editor(index).toPlainText())
            file_handle.close()
            self.get_editor(index).textChanged = False
            result = True
        else:
            result = self.on_actionSave_As_triggered(index)

        return result

    @pyqtSlot()
    def on_actionSave_As_triggered(self, index=None) -> bool:
        if index is None:
            index = self.ui.EditorTabWidget.currentIndex()

        result = False

        filename = QFileDialog.getSaveFileName()
        if filename[0]:
            file_handle = open(filename[0], mode="w+")
            file_handle.write(self.get_editor(index).toPlainText())
            file_handle.close()
            self.get_editor(index).textChanged = False

            self.get_editor(index).document().setBaseUrl(QUrl.fromLocalFile(filename[0]))

            index = filename[0].rfind("/")
            self.ui.EditorTabWidget.setTabText(index, filename[0][index + 1:])

            result = True

        return result

    @pyqtSlot(int)
    def on_EditorTabWidget_tabCloseRequested(self, index):
        if self.get_editor(index).text_changed:
            dialog = SaveChangesSingleDialog(self.ui.EditorTabWidget.tabBar().tabText(index))
            dialog.show()
            dialog.setFixedSize(dialog.size())
            dialog.exec_()

            if dialog.result == Result.CANCEL:
                return
            elif dialog.result == Result.SAVE:
                if not self.on_actionSave_triggered(index):
                    return

        self.ui.EditorTabWidget.removeTab(index)
