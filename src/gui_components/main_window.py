from typing import Tuple
from collections import namedtuple

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QWidget, QVBoxLayout, QLabel, QAction, QSplitter, QSizePolicy, QMessageBox,
                            QMenu, QInputDialog, QTableWidgetItem, QHeaderView, QComboBox)
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QUrl, QPoint, QVariant, QObject, QModelIndex)
from PyQt5.QtGui import *

from forms.ui_main_window import Ui_MainWindow
from gui_components.text_editor import TextEditor
from gui_components.save_changes_single_dialog import SaveChangesSingleDialog
from gui_components.save_changes_multiple_dialog import SaveChangesMultipleDialog
from gui_components.add_link_dialog import AddLinkDialog
from gui_components.add_image_dialog import AddImageDialog
from gui_components.add_citation_dialog import AddCitationDialog
from resources import icons_rc
from common import Result, ProjectError
from components.project_manager import ProjectManager


class MainWindow(QMainWindow):

    OpenedEditor = namedtuple("OpenedEditor", ["filepath", "in_current_project"])

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_icons()
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)

        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EditorTabWidget.setTabsClosable(True)
        self.ui.EditorTabWidget.clear()

        self.set_toolbar_actions()
        self.ProjectManager = None
        self.ui.splitter.setSizes((150, 450))
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.ProjectLabel.setAutoFillBackground(True)
        self.ui.ProjectLabel.setStyleSheet("QLabel {background-color: SlateGrey; }")
        self.loading_project = False

        self.OpenedEditors = []

        self.show()

    # Utility functions
    def set_toolbar_actions(self):
        self.ui.ItalicToolButton.setDefaultAction(self.ui.actionItalic)
        self.ui.BoldToolButton.setDefaultAction(self.ui.actionBold)
        self.ui.BoldItalicToolButton.setDefaultAction(self.ui.actionBoldItalic)
        self.ui.HorizontalRuleToolButton.setDefaultAction(self.ui.actionHorizontalRule)
        self.ui.OrdListToolButton.setDefaultAction(self.ui.actionOrdList)
        self.ui.UnordListToolButton.setDefaultAction(self.ui.actionUnordList)
        self.ui.LinkToolButton.setDefaultAction(self.ui.actionLink)
        self.ui.ImageToolButton.setDefaultAction(self.ui.actionImage)
        self.ui.CodeToolButton.setDefaultAction(self.ui.actionCode)

        self.ui.HeadingToolButton.addActions([self.ui.actionHeading1, self.ui.actionHeading2, self.ui.actionHeading3,
                                              self.ui.actionHeading4, self.ui.actionHeading5, self.ui.actionHeading6])
        self.ui.HeadingToolButton.setDefaultAction(self.ui.actionHeading1)

        self.ui.BlockquoteToolButton.setDefaultAction(self.ui.actionBlockquote)
        self.ui.AddCitationToolButton.setDefaultAction(self.ui.actionAddCitation)

    def set_icons(self):
        # load common icons
        self.ui.EditorTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/document-papirus.svg")))
        self.ui.GitTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/git-branch.svg")))
        self.ui.ProjectTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/project-management.svg")))
        self.ui.SettingsLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/settings.svg")))
        self.ui.UserAccounLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/account.svg")))

        # load light/dark icons
        self.ui.actionItalic.setIcon(QIcon(":/icons_dark/icons_dark/format-text-italic.svg"))
        self.ui.actionBold.setIcon(QIcon(":/icons_dark/icons_dark/format-text-bold.svg"))
        self.ui.actionBoldItalic.setIcon(QIcon(":/icons_dark/icons_dark/format-text-bold-italic.svg"))
        self.ui.actionHeading1.setIcon(QIcon(":/icons_dark/icons_dark/heading1.svg"))
        self.ui.actionHeading2.setIcon(QIcon(":/icons_dark/icons_dark/heading2.svg"))
        self.ui.actionHeading3.setIcon(QIcon(":/icons_dark/icons_dark/heading3.svg"))
        self.ui.actionHeading4.setIcon(QIcon(":/icons_dark/icons_dark/heading4.svg"))
        self.ui.actionHeading5.setIcon(QIcon(":/icons_dark/icons_dark/heading5.svg"))
        self.ui.actionHeading6.setIcon(QIcon(":/icons_dark/icons_dark/heading6.svg"))
        self.ui.HeadingToolButton.setIcon(QIcon(":/icons_dark/icons_dark/heading1.svg"))

        self.ui.actionHorizontalRule.setIcon(QIcon(":/icons_dark/icons_dark/horizontal-rule.svg"))
        self.ui.actionBlockquote.setIcon(QIcon(":/icons_dark/icons_dark/format-text-blockquote.svg"))
        self.ui.actionOrdList.setIcon(QIcon(":/icons_dark/icons_dark/ord-list.svg"))
        self.ui.actionUnordList.setIcon(QIcon(":/icons_dark/icons_dark/unord-list.svg"))
        self.ui.actionLink.setIcon(QIcon(":/icons_dark/icons_dark/link.svg"))
        self.ui.actionImage.setIcon(QIcon(":/icons_dark/icons_dark/insert-image.svg"))
        self.ui.actionCode.setIcon(QIcon(":/icons_dark/icons_dark/format-text-code.svg"))

    def set_active_tab(self, label: QLabel):
        for tab in self.tabs:
            background_color = self.palette().color(self.palette().Background)
            tab.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

        label.setAutoFillBackground(True)
        background_color = self.palette().color(self.palette().Highlight)
        label.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

    def get_editor(self, tab_index: int = None) -> TextEditor:
        if self.ui.EditorTabWidget.count() == 0:
            return None

        if tab_index is None:
            tab_index = self.ui.EditorTabWidget.currentIndex()

        return self.ui.EditorTabWidget.widget(tab_index).findChild(TextEditor)

    def load_project(self, path: str) -> None:
        self.loading_project = True
        self.ProjectManager = ProjectManager(path)
        self.ui.ProjectTreeView.setModel(self.ProjectManager.FsModel)
        self.ui.ProjectTreeView.setRootIndex(self.ProjectManager.FsModel.index(path))
        self.ui.ProjectTreeView.hideColumn(1)
        self.ui.ProjectTreeView.hideColumn(2)
        self.ui.ProjectTreeView.hideColumn(3)
        self.ui.ProjectTreeView.header().setVisible(False)
        self.ui.ProjectLabel.setAutoFillBackground(True)
        self.on_EditorTabLabel_clicked()
        self.ProjectManager.FsModel.directoryLoaded.connect(self.on_ProjectManager_ProjectDirectoryLoaded)

        # Populate project settings
        rows = len(self.ProjectManager.project_info)
        self.ui.ProjectSettingsTableWidget.setRowCount(rows)
        self.ui.ProjectSettingsTableWidget.setColumnCount(2)

        info = []
        for item in self.ProjectManager.project_info.items():
            info.append(item)

        for i in range(len(info)):
            key = info[i][0]
            table_item = QTableWidgetItem(key)
            table_item.setFlags(table_item.flags() ^ Qt.ItemIsEditable)
            self.ui.ProjectSettingsTableWidget.setItem(i, 0, table_item)

            setting_type = info[i][1]["type"]
            if setting_type != "enum":
                table_item = QTableWidgetItem(info[i][1]["value"])
                self.ui.ProjectSettingsTableWidget.setItem(i, 1, table_item)
            else:
                value = info[i][1]["value"]
                variants = info[i][1]["allowed values"]
                table_item = QComboBox(self.ui.ProjectSettingsTableWidget)
                table_item.addItems(variants)
                index = table_item.findText(value)
                table_item.setCurrentIndex(index)
                table_item.currentIndexChanged.connect(self.on_SettingComboBox_valueChanged)
                table_item.row = i
                self.ui.ProjectSettingsTableWidget.setCellWidget(i, 1, table_item)

        self.ui.ProjectSettingsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.ProjectSettingsTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.loading_project = False

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
        self.ui.EditorTabWidget.untitled_docs_counter += 1
        tabname = "Untitled {}".format(self.ui.EditorTabWidget.untitled_docs_counter)
        self.ui.EditorTabWidget.setTabText(index, tabname)
        self.ui.EditorTabWidget.setTabToolTip(index, tabname)
        font = self.get_editor().font()
        font.setPointSize(14)
        self.get_editor().setFont(font)
        self.get_editor().setFocus()

        self.OpenedEditors.append(self.OpenedEditor(filepath=None, in_current_project=False))

    @pyqtSlot()
    def on_actionOpen_triggered(self, filename: str = None):
        if filename is None:
            filename = QFileDialog.getOpenFileName()
        else:
            filename = (filename, "")
        if filename[0]:
            file_handle = open(filename[0], mode="r")
            text = file_handle.read()
            file_handle.close()

            self.on_actionNew_triggered()
            self.get_editor().appendPlainText(text)
            self.get_editor().document().setBaseUrl(QUrl.fromLocalFile(filename[0]))
            self.OpenedEditors[self.ui.EditorTabWidget.currentIndex()] = self.OpenedEditor(filepath=filename[0], in_current_project=False)

            self.ui.EditorTabWidget.setTabToolTip(self.ui.EditorTabWidget.currentIndex(), filename[0])
            index = filename[0].rfind("/")
            self.ui.EditorTabWidget.setTabText(self.ui.EditorTabWidget.currentIndex(), filename[0][index+1:])
            self.get_editor().text_changed = False

    @pyqtSlot()
    def on_actionSave_triggered(self, index=None) -> bool:
        if self.ui.EditorTabWidget.count() == 0:
            return
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
        if self.ui.EditorTabWidget.count() == 0:
            return

        if index is None:
            index = self.ui.EditorTabWidget.currentIndex()

        result = False

        tabname = self.ui.EditorTabWidget.tabText(index)
        filename = QFileDialog.getSaveFileName(directory=tabname)
        if filename[0]:
            file_handle = open(filename[0], mode="w+")
            file_handle.write(self.get_editor(index).toPlainText())
            file_handle.close()
            self.get_editor(index).textChanged = False

            self.get_editor(index).document().setBaseUrl(QUrl.fromLocalFile(filename[0]))

            self.ui.EditorTabWidget.setTabToolTip(index, filename[0])
            index = filename[0].rfind("/")
            self.ui.EditorTabWidget.setTabText(index, filename[0][index + 1:])
            self.OpenedEditors[index] = self.OpenedEditor(filepath=filename[0], in_current_project=False)

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
        del self.OpenedEditors[index]

    def closeEvent(self, event: QCloseEvent) -> None:
        unsaved_editors = []

        for index in range(self.ui.EditorTabWidget.count()):
            editor = self.get_editor(index)
            if editor.text_changed:
                unsaved_editors.append((index, self.ui.EditorTabWidget.tabBar().tabText(index)))

        if len(unsaved_editors) == 0:
            return
        elif len(unsaved_editors) == 1:
            index = unsaved_editors[0][0]
            dialog = SaveChangesSingleDialog(self.ui.EditorTabWidget.tabBar().tabText(index))
        else:
            dialog = SaveChangesMultipleDialog([item[1] for item in unsaved_editors])

        dialog.show()
        dialog.setFixedSize(dialog.size())
        dialog.exec_()

        if dialog.result == Result.CANCEL:
            event.ignore()
            return
        elif dialog.result == Result.SAVE:
            for item in unsaved_editors:
                if not self.on_actionSave_triggered(item[0]):
                    event.ignore()
                    return

    # TOOLBAR ACTIONS
    @pyqtSlot()
    def on_actionItalic_triggered(self):
        print(self.OpenedEditors)
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("*")

    @pyqtSlot()
    def on_actionBold_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("**")

    @pyqtSlot()
    def on_actionBoldItalic_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("***")

    @pyqtSlot()
    def on_actionHeading1_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("# ")

    @pyqtSlot()
    def on_actionHeading2_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("## ")

    @pyqtSlot()
    def on_actionHeading3_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("### ")

    @pyqtSlot()
    def on_actionHeading4_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("#### ")

    @pyqtSlot()
    def on_actionHeading5_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("##### ")

    @pyqtSlot()
    def on_actionHeading6_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("###### ")

    @pyqtSlot()
    def on_actionHorizontalRule_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_empty_line("---")

    @pyqtSlot()
    def on_actionBlockquote_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("> ")

    @pyqtSlot()
    def on_actionOrdList_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("1. ")

    @pyqtSlot()
    def on_actionUnordList_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("- ")

    @pyqtSlot()
    def on_actionLink_triggered(self):
        if self.ui.EditorTabWidget.count() == 0:
            return
        dialog = AddLinkDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("[{}]({})".format(dialog.link_text, dialog.link_address))

    @pyqtSlot()
    def on_actionImage_triggered(self):
        if self.ui.EditorTabWidget.count() == 0:
            return
        dialog = AddImageDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("![{}]({})".format(dialog.image_text, dialog.image_path))

    @pyqtSlot()
    def on_actionCode_triggered(self):
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("`")

    @pyqtSlot()
    def on_actionAddCitation_triggered(self):
        if self.ui.EditorTabWidget.count() == 0:
            return
        dialog = AddCitationDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("[@{}]".format(dialog.citation_identifier))

    @pyqtSlot(bool)
    def on_actionProjectTab_triggered(self, checked):
        if checked:
            self.ui.splitter.setSizes([1, 5])
        else:
            self.ui.splitter.setSizes([0, 1])

    @pyqtSlot()
    def on_actionOpenProject_triggered(self):
        path = QFileDialog.getExistingDirectory()
        if path:
            try:
                self.load_project(path)
            except ProjectError as e:
                self.ProjectManager = None
                message = QMessageBox()
                message.setText("Failed to load project: " + e.message.lower())
                message.setWindowTitle("Error")
                message.exec_()

    @pyqtSlot()
    def on_actionNewProject_triggered(self):
        path = QFileDialog.getExistingDirectory()
        if path:
            ProjectManager.create_project(path)
            self.load_project(path)

    @pyqtSlot(QPoint)
    def on_ProjectTreeView_customContextMenuRequested(self, point: QPoint):
        if self.ProjectManager is None:
            return

        menu = QMenu()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            self.ui.actionCreateFolder.setEnabled(True)

        if not self.ProjectManager.FsModel.isDir(clicked_item):
            self.ui.actionCreateFolder.setEnabled(False)
        else:
            self.ui.actionCreateFolder.setEnabled(True)

        menu.addActions([self.ui.actionCreateFile, self.ui.actionCreateFolder, self.ui.actionDelete,
                         self.ui.actionRename])

        self.ui.actionCreateFolder.setData(QVariant(point))
        self.ui.actionDelete.setData(QVariant(point))
        self.ui.actionCreateFile.setData(QVariant(point))
        self.ui.actionRename.setData(QVariant(point))

        menu.exec_(self.ui.ProjectTreeView.mapToGlobal(point))

    @pyqtSlot()
    def on_actionCreateFolder_triggered(self):
        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)
        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()
        path = self.ProjectManager.FsModel.filePath(clicked_item)
        name = QInputDialog.getText(self, "Create folder", "Folder name:")
        if name:
            self.ProjectManager.create_folder(path + "/" + name[0])

    @pyqtSlot()
    def on_actionCreateFile_triggered(self):
        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)
        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()
        path = self.ProjectManager.FsModel.filePath(clicked_item)

        name = QInputDialog.getText(self, "Create file", "File name:")
        if name:
            self.ProjectManager.create_file(path + "/" + name[0])

    @pyqtSlot()
    def on_actionDelete_triggered(self):
        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)
        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()
        self.ProjectManager.delete_file(clicked_item)

    @pyqtSlot()
    def on_actionRename_triggered(self):
        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)
        if clicked_item.data() is None:
            return
        name = QInputDialog.getText(self, "Rename", "New name:")
        if name:
            self.ProjectManager.rename(clicked_item, name[0])

    @pyqtSlot(str)
    def on_ProjectManager_ProjectDirectoryLoaded(self, path: str):
        self.ui.ProjectTreeView.expandToDepth(4)

    @pyqtSlot(int, int)
    def on_ProjectSettingsTableWidget_cellChanged(self, row: int, column: int):
        if self.loading_project:
            pass
        else:
            print("Cell changed")
            key = self.ui.ProjectSettingsTableWidget.item(row, 0).text()
            value = self.ui.ProjectSettingsTableWidget.item(row, 1).text()
            self.ProjectManager.uptade_project_info((key, value))

    @pyqtSlot()
    def on_SaveProjectSettingsButton_clicked(self):
        if self.ProjectManager is not None:
            self.ProjectManager.save_project_data()

    @pyqtSlot(int)
    def on_SettingComboBox_valueChanged(self, current_index: int):
        sender = QObject.sender(self)
        row = sender.row
        key = self.ui.ProjectSettingsTableWidget.item(row, 0).text()
        value = sender.itemText(current_index)
        self.ProjectManager.uptade_project_info((key, value))

    @pyqtSlot(QModelIndex)
    def on_ProjectTreeView_clicked(self, index: QModelIndex):
        if not self.ProjectManager.FsModel.isDir(index):
            filepath = self.ProjectManager.FsModel.filePath(index)
            for i in range(len(self.OpenedEditors)):
                if filepath == self.OpenedEditors[i].filepath:
                    self.ui.EditorTabWidget.setCurrentIndex(i)
                    return
            self.on_actionOpen_triggered(filepath)

