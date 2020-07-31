from collections import namedtuple

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QWidget, QVBoxLayout, QLabel, QMessageBox,
                            QMenu, QInputDialog, QTableWidgetItem, QHeaderView, QComboBox)
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QUrl, QPoint, QVariant, QObject, QModelIndex)
from PyQt5.QtGui import *

from forms.ui_main_window import Ui_MainWindow
from gui_components.text_editor import TextEditor
from gui_components.add_link_dialog import AddLinkDialog
from gui_components.add_image_dialog import AddImageDialog
from gui_components.add_citation_dialog import AddCitationDialog
from gui_components.create_project_dialog import CreateProjectDialog
from gui_components.settings_dialog import SettingsDialog
from resources import icons_rc
from common import ProjectError
from components.project_manager import ProjectManager
from components.settings_manager import SettingsManager


class MainWindow(QMainWindow):

    OpenedEditor = namedtuple("OpenedEditor", ["filepath", "in_current_project"])

    def __init__(self) -> None:
        super().__init__()

        # Prepare Ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EditorTabWidget.clear()
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)

        # Call convenience functions to setup Ui
        self.set_icons()
        self.set_toolbar_actions()

        # Set additional class attributes
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)
        self.ProjectManager = None
        self.loading_project = False
        self.OpenedEditors = []
        self.SettingsManager = SettingsManager(self)

        # Read settings
        self.read_settings()

        self.show()

    # Utility functions
    def set_toolbar_actions(self) -> None:
        # Assign actions to toolbar buttons
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

        self.ui.RenderFileToolButton.setDefaultAction(self.ui.actionRenderFile)

    def set_icons(self) -> None:
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

    def set_active_tab(self, label: QLabel) -> None:
        """Makes specified label in MainTabsFrame appear selected and deselects all other labels. Switches tab in
        MainStackedWidget to the appropriate value."""

        for tab in self.tabs:
            background_color = self.palette().color(self.palette().Background)
            tab.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

        background_color = self.palette().color(self.palette().Highlight)
        label.setStyleSheet("QLabel {{ background-color : {}; }}".format(background_color.name()))

    def get_editor(self, tab_index: int = None) -> TextEditor:
        """Returns the TextEditor object of the currently active tab in EditorTabWidget (or the editor of the tab at
        the specified index"""

        if self.ui.EditorTabWidget.count() == 0:
            return None

        if tab_index is None:
            tab_index = self.ui.EditorTabWidget.currentIndex()

        return self.ui.EditorTabWidget.widget(tab_index).findChild(TextEditor)

    def load_project(self, path: str) -> None:
        """Attempts to load project at specified path (path to project root directory)."""

        self.loading_project = True

        # Create project manager for current project
        try:
            self.ProjectManager = ProjectManager(path)
        except ProjectError as e:
            self.ProjectManager = None
            QMessageBox.critical(self, "Error", "Failed to load project: " + e.message.lower())
            return

        # Populate ProjectWidget with information about project file structure
        self.ui.ProjectTreeView.setModel(self.ProjectManager.FsModel)
        self.ui.ProjectTreeView.setRootIndex(self.ProjectManager.FsModel.index(path))
        self.ui.ProjectTreeView.hideColumn(1)
        self.ui.ProjectTreeView.hideColumn(2)
        self.ui.ProjectTreeView.hideColumn(3)
        self.ui.ProjectTreeView.header().setVisible(False)
        self.on_EditorTabLabel_clicked()
        self.ProjectManager.FsModel.directoryLoaded.connect(self.on_ProjectManager_ProjectDirectoryLoaded)
        self.ui.ProjectSettingsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.ProjectSettingsTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate project settings
        # TODO: remove this section and create proper widgets for project settings
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

        self.loading_project = False

    def read_settings(self) -> None:
        """Get settings from SettignsManager and adjust the ui accordingly"""

        self.ui.ProjectLabel.setStyleSheet("QLabel {background-color: SlateGrey; }")
        self.resize(self.SettingsManager.get_setting_value("MainWindow/size"))
        self.move(self.SettingsManager.get_setting_value("MainWindow/pos"))
        self.ui.splitter.setSizes(self.SettingsManager.get_setting_value("MainWindow/splitter_sizes"))

        if self.SettingsManager.get_setting_value("MainWindow/last_project"):
            self.load_project(self.SettingsManager.get_setting_value("MainWindow/last_project"))

    def write_settings(self) -> None:
        """Write settings to permanent storage"""

        self.SettingsManager.set_setting_value("MainWindow/size", self.size())
        self.SettingsManager.set_setting_value("MainWindow/pos", self.pos())
        self.SettingsManager.set_setting_value("MainWindow/splitter_sizes", self.ui.splitter.sizes())
        if self.ProjectManager is not None:
            self.SettingsManager.set_setting_value("MainWindow/last_project", self.ProjectManager.root_path)
        else:
            self.SettingsManager.set_setting_value("MainWindow/last_project", "")

    # Event handling
    def closeEvent(self, event: QCloseEvent) -> None:
        """Checks whether any editors have unsaved changes before closing the main window. Asks whether to save or
        discard them if there are. Writes settings before closing"""

        unsaved_editors = []
        detailed_text = "Modified documents:\n"

        # Create a list of editors with unsaved changes
        for index in range(len(self.OpenedEditors)):
            editor = self.get_editor(index)
            if editor.text_changed:
                unsaved_editors.append((index, self.ui.EditorTabWidget.tabBar().tabText(index)))
                detailed_text += self.ui.EditorTabWidget.tabBar().tabText(index) + "\n"

        if len(unsaved_editors) != 0:
            # Create dialog
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Save documents - Manuwrite")
            dialog.setText("Some documents have been modified. Do you want to save them before closing?")
            dialog.addButton(QMessageBox.SaveAll)
            dialog.addButton(QMessageBox.Discard)
            dialog.addButton(QMessageBox.Cancel)
            dialog.setDetailedText(detailed_text)
            dialog.show()

            answer = dialog.exec_()
            # Ignore event if any of the save operations failed and return
            if answer == QMessageBox.SaveAll:
                for item in unsaved_editors:
                    if not self.on_actionSave_triggered(item[0]):
                        event.ignore()
                        return
                self.write_settings()
            elif answer == QMessageBox.Cancel:
                event.ignore()
        else:
            self.write_settings()

    # Signal handling
    @pyqtSlot()
    def on_EditorTabLabel_clicked(self) -> None:
        """Switch to editor tab"""
        self.set_active_tab(self.ui.EditorTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_GitTabLabel_clicked(self) -> None:
        """Switch to git tab"""
        self.set_active_tab(self.ui.GitTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def on_ProjectTabLabel_clicked(self) -> None:
        """Switch to project tab"""
        self.set_active_tab(self.ui.ProjectTabLabel)
        self.ui.MainStackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def on_actionNew_triggered(self) -> None:
        """Creates a new tab in EditorTabWidget, puts a TextEditor in that tab, sets editor settings and switches to the
         created tab"""

        # Create main widget of the tab
        widget = QWidget(self)
        widget.setLayout(QVBoxLayout())
        widget.layout().setContentsMargins(0, 2, 0, 0)

        # Create editor and set its settings
        editor = TextEditor(widget, self.ui.webEngineView)

        font = editor.font()
        font.setPointSize(self.SettingsManager.get_setting_value("Editor/Font size"))
        font.setRawName(self.SettingsManager.get_setting_value("Editor/Font name"))
        editor.setFont(font)

        self.OpenedEditors.append(self.OpenedEditor(filepath=None, in_current_project=False))
        widget.layout().addWidget(editor)

        # Create new tab
        self.ui.EditorTabWidget.untitled_docs_counter += 1
        index = self.ui.EditorTabWidget.addTab(widget, f"Untitled {self.ui.EditorTabWidget.untitled_docs_counter}")
        self.ui.EditorTabWidget.setCurrentIndex(index)

        editor.setFocus()
        self.on_EditorTabLabel_clicked()

    @pyqtSlot()
    def on_actionOpen_triggered(self, path: str = None):
        """Open file at given path, or get path from user with QFileDialog if path is not given"""

        if path is None:
            path = QFileDialog.getOpenFileName()[0]

        if path:
            # Read file
            try:
                file_handle = open(path, mode="r")
                text = file_handle.read()
            except OSError:
                QMessageBox.critical(self, "Error", "Failed to open file. Some error occurred")
                return
            finally:
                file_handle.close()

            # Create new tab and load text into editor
            self.on_actionNew_triggered()
            editor = self.get_editor()
            editor.appendPlainText(text)
            editor.document().setBaseUrl(QUrl.fromLocalFile(path))
            editor.text_changed = False

            # Configure new tab
            current_tab_index = self.ui.EditorTabWidget.currentIndex()
            filename = path[path.rfind("/") + 1:]

            self.OpenedEditors[current_tab_index] = self.OpenedEditor(filepath=path, in_current_project=False)
            self.ui.EditorTabWidget.setTabToolTip(current_tab_index, path)
            self.ui.EditorTabWidget.setTabText(current_tab_index, filename)

    @pyqtSlot()
    def on_actionSave_triggered(self, index: int = None) -> bool:
        """Save contents of editor at the currently open tab or the tab at index, if index is specified. Saves to file
        specified by the baseUrl of the editor's document. If baseUrl is empty, calls on_actionSaveAs_triggered()"""

        if self.ui.EditorTabWidget.count() == 0:
            return True

        if index is None:
            index = self.ui.EditorTabWidget.currentIndex()

        result = False
        editor = self.get_editor(index)

        if editor.document().baseUrl().url():
            try:
                file_handle = open(editor.document().baseUrl().url(QUrl.PreferLocalFile), mode="w")
                file_handle.write(editor.toPlainText())
                result = True
                editor.text_changed = False
            except OSError:
                filename = self.ui.EditorTabWidget.tabText(index)
                QMessageBox.critical(self, "Error", f"Failed to save file \"{filename}\"")
            finally:
                file_handle.close()
        else:
            result = self.on_actionSave_As_triggered(index)

        return result

    @pyqtSlot()
    def on_actionSave_As_triggered(self, index: int = None) -> bool:
        """Save contents of editor at the currently open tab (or tab at index, if index is given) to the file specified
        by the user through QFileDialog"""

        if self.ui.EditorTabWidget.count() == 0:
            return True

        if index is None:
            index = self.ui.EditorTabWidget.currentIndex()

        result = False
        editor = self.get_editor(index)

        current_path = editor.document().baseUrl().url(QUrl.PreferLocalFile)
        if not current_path:
            current_path = self.SettingsManager.get_setting_value("Application/Project folder")

        path = QFileDialog.getSaveFileName(directory=current_path)[0]

        if path:
            try:
                file_handle = open(path, mode="w+")
                file_handle.write(editor.toPlainText())
                result = True
                editor.text_changed = False
            except OSError:
                filename = self.ui.EditorTabWidget.tabText(index)
                QMessageBox.critical(self, "Error", f"Failed to save file \"{filename}\"")
            finally:
                file_handle.close()

            tabname = path[path.rfind("/") + 1:]

            editor.document().setBaseUrl(QUrl.fromLocalFile(path))
            self.OpenedEditors[index] = self.OpenedEditor(filepath=path, in_current_project=False)
            self.ui.EditorTabWidget.setTabToolTip(index, path)
            self.ui.EditorTabWidget.setTabText(index, tabname)

        return result

    @pyqtSlot(int)
    def on_EditorTabWidget_tabCloseRequested(self, index: int) -> None:
        """Close EditorTabWidget's tab at index. If there are unsaved changes in that tab's editor, ask whether to save
        them"""

        remove = True
        if self.get_editor(index).text_changed:
            filename = self.ui.EditorTabWidget.tabText(index)
            answer = QMessageBox.warning(self, "Close document - Manuwrite", f"The document \"{filename}\" has been" +
                                         " modified. Do you want to save your changes or discard them?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if answer == QMessageBox.Save:
                if not self.on_actionSave_triggered(index):
                    remove = False
            elif answer == QMessageBox.Cancel:
                remove = False

        if remove:
            self.ui.EditorTabWidget.removeTab(index)
            del self.OpenedEditors[index]

    # TOOLBAR ACTIONS
    # Insert markdown tags for text formatting at cursor or at selection
    @pyqtSlot()
    def on_actionItalic_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("*")

    @pyqtSlot()
    def on_actionBold_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("**")

    @pyqtSlot()
    def on_actionBoldItalic_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("***")

    @pyqtSlot()
    def on_actionHeading1_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("# ")

    @pyqtSlot()
    def on_actionHeading2_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("## ")

    @pyqtSlot()
    def on_actionHeading3_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("### ")

    @pyqtSlot()
    def on_actionHeading4_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("#### ")

    @pyqtSlot()
    def on_actionHeading5_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("##### ")

    @pyqtSlot()
    def on_actionHeading6_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("###### ")

    @pyqtSlot()
    def on_actionHorizontalRule_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_empty_line("---")

    @pyqtSlot()
    def on_actionBlockquote_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("> ")

    @pyqtSlot()
    def on_actionOrdList_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("1. ")

    @pyqtSlot()
    def on_actionUnordList_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_line_beginning("- ")

    @pyqtSlot()
    def on_actionLink_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() == 0:
            return

        dialog = AddLinkDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("[{}]({})".format(dialog.link_text, dialog.link_address))

    @pyqtSlot()
    def on_actionImage_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() == 0:
            return

        dialog = AddImageDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("![{}]({})".format(dialog.image_text, dialog.image_path))

    @pyqtSlot()
    def on_actionCode_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("`")

    @pyqtSlot()
    def on_actionAddCitation_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() == 0:
            return

        dialog = AddCitationDialog()
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("[@{}]".format(dialog.citation_identifier))

    @pyqtSlot()
    def on_actionRenderFile_triggered(self) -> None:
        """Render the contents of the editor at the currently active tab to markdown"""

        self.get_editor().render_to_html()

    # End of TOOLBAR ACTIONS
    @pyqtSlot(bool)
    def on_actionProjectTab_triggered(self, checked: bool) -> None:
        """Collaplse/open ProjectWidget"""

        if checked:
            width = self.SettingsManager.get_setting_value("MainWindow/project_widget_width")
            self.ui.splitter.setSizes([width, self.ui.EditorTabWidget.width() - width, self.ui.webEngineView.width()])
        else:
            self.SettingsManager.set_setting_value("MainWindow/project_widget_width", self.ui.ProjectWidget.width())
            self.ui.splitter.setSizes([0, self.ui.ProjectWidget.width() + self.ui.EditorTabWidget.width(),
                                       self.ui.webEngineView.width()])

    @pyqtSlot()
    def on_actionOpenProject_triggered(self) -> None:
        """Ask user for path to project. Attempt to open project if user provides the path"""
        path = QFileDialog.getExistingDirectory(caption="Open project", directory=self.SettingsManager.get_setting_value("Application/Project folder"))
        if path:
            self.load_project(path)

    @pyqtSlot()
    def on_actionNewProject_triggered(self) -> None:
        """Attempts to create a new project at a directory given by the user"""

        dialog = CreateProjectDialog(self.SettingsManager.get_setting_value("Projects/Project types"),
                                     self.SettingsManager.get_setting_value("Application/Project folder"))
        dialog.show()
        if dialog.exec_():
            ProjectManager.create_project(dialog.path)
            self.load_project(dialog.path)
            self.ProjectManager.uptade_project_info(("Title", dialog.title))
            self.ProjectManager.uptade_project_info(("Author", dialog.authors))
            self.ProjectManager.uptade_project_info(("Project type", dialog.project_type))
            self.ProjectManager.save_project_data()

    @pyqtSlot(QPoint)
    def on_ProjectTreeView_customContextMenuRequested(self, point: QPoint) -> None:
        """Displays context menu for the ProjectWidget to create/delete/rename files in the project tree"""

        if self.ProjectManager is None:
            return

        menu = QMenu()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        # Actions in order: CreateFile, CreateFolder, Rename, Delete
        allow_actions = []
        menu_actions = [self.ui.actionCreateFolder, self.ui.actionCreateFile, self.ui.actionRename,
                        self.ui.actionDelete]

        # Make action available based on what item was clicked on
        if clicked_item.data() is None:
            allow_actions += (True, True, False, False)
        elif self.ProjectManager.FsModel.isDir(clicked_item):
            allow_actions += [True, True, True, True]
        else:
            allow_actions += [False, False, True, True]

        for i in range(len(menu_actions)):
            menu_actions[i].setEnabled(allow_actions[i])
            menu_actions[i].setData(QVariant(point))

        menu.addActions(menu_actions)
        menu.exec_(self.ui.ProjectTreeView.mapToGlobal(point))

    @pyqtSlot()
    def on_actionCreateFolder_triggered(self) -> None:
        """Creates a folder in project structure under the element, on which the user clicked when calling the context
        menu"""

        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()

        path = self.ProjectManager.FsModel.filePath(clicked_item)
        name = QInputDialog.getText(self, "Create folder", "Folder name:")

        if name:
            self.ProjectManager.create_folder(path + "/" + name[0])

    @pyqtSlot()
    def on_actionCreateFile_triggered(self) -> None:
        """Creates a file in project structure under the element, on which the user clicked when calling the context
        menu"""

        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()

        path = self.ProjectManager.FsModel.filePath(clicked_item)
        name = QInputDialog.getText(self, "Create file", "File name:")

        if name:
            self.ProjectManager.create_file(path + "/" + name[0])

    @pyqtSlot()
    def on_actionDelete_triggered(self) -> None:
        """Deletes a file or a folder in project structure, which corresponds to the element, on which the user clicked
        when calling the context menu"""

        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()

        self.ProjectManager.delete_file(clicked_item)

    @pyqtSlot()
    def on_actionRename_triggered(self) -> None:
        """Renames a file or a folder in project structure, which corresponds to the element, on which the user clicked
        when calling the context menu"""

        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            return

        name = QInputDialog.getText(self, "Rename", "New name:")

        if name:
            self.ProjectManager.rename(clicked_item, name[0])

    @pyqtSlot(str)
    def on_ProjectManager_ProjectDirectoryLoaded(self) -> None:
        """Expands the project tree in the ProjectWidget, when the project directory is loaded. Can't do it before it
        is loaded (i.e. in load_project()"""

        self.ui.ProjectTreeView.expandToDepth(4)

    @pyqtSlot(int, int)
    def on_ProjectSettingsTableWidget_cellChanged(self, row: int, column: int):
        # TODO: remove this function and create a proper project configuration screen
        if self.loading_project:
            pass
        else:
            key = self.ui.ProjectSettingsTableWidget.item(row, 0).text()
            value = self.ui.ProjectSettingsTableWidget.item(row, 1).text()
            self.ProjectManager.uptade_project_info((key, value))

    @pyqtSlot()
    def on_SaveProjectSettingsButton_clicked(self) -> None:
        """Attempt to save project settings which are currently in memory to permanent storage"""

        if self.ProjectManager is not None:
            self.ProjectManager.save_project_data()

    @pyqtSlot(int)
    def on_SettingComboBox_valueChanged(self, current_index: int):
        # TODO: Remove this fuction
        sender = QObject.sender(self)
        row = sender.row
        key = self.ui.ProjectSettingsTableWidget.item(row, 0).text()
        value = sender.itemText(current_index)
        self.ProjectManager.uptade_project_info((key, value))

    @pyqtSlot(QModelIndex)
    def on_ProjectTreeView_clicked(self, index: QModelIndex) -> None:
        """Open the file, which the user clicked on in the project tree"""

        if not self.ProjectManager.FsModel.isDir(index):
            filepath = self.ProjectManager.FsModel.filePath(index)

            for i in range(len(self.OpenedEditors)):

                if filepath == self.OpenedEditors[i].filepath:
                    self.ui.EditorTabWidget.setCurrentIndex(i)
                    return

            self.on_actionOpen_triggered(filepath)

    @pyqtSlot(bool)
    def on_actionShowPreview_triggered(self, checked: bool) -> None:
        """Collapse/show WebEngineView, in which rendered markdown is displayed"""

        if checked:
            width = self.SettingsManager.get_setting_value("MainWindow/preview_width")
            self.ui.splitter.setSizes([self.ui.ProjectWidget.width(), self.ui.EditorTabWidget.width() -
                                       width, width])
        else:
            self.SettingsManager.set_setting_value("MainWindow/preview_width", self.ui.webEngineView.width())
            self.ui.splitter.setSizes([self.ui.ProjectWidget.width(), self.ui.EditorTabWidget.width() +
                                       self.ui.webEngineView.width(), 0])

    @pyqtSlot()
    def on_actionSettings_triggered(self) -> None:
        """Show settings dialog"""

        dialog = SettingsDialog(self.SettingsManager)
        dialog.show()
        dialog.exec_()
