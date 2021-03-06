from collections import namedtuple

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QWidget, QVBoxLayout, QLabel, QMessageBox,
                            QMenu, QInputDialog, QTreeWidgetItem, QMdiSubWindow)
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QUrl, QPoint, QVariant, QModelIndex, Qt)
from PyQt5.QtGui import *

import components.managers
import components.project_manager

from ui_forms.ui_main_window import Ui_MainWindow
from widgets.text_editor import TextEditor
from forms.add_link_dialog import AddLinkDialog
from forms.add_image_dialog import AddImageDialog
from forms.add_citation_dialog import AddCitationDialog
from forms.create_project_dialog import CreateProjectDialog
from forms.settings_dialog import SettingsDialog
from forms.project_settings_dialog import ProjectSettingsDialog
from forms.add_footnote_dialog import AddFootnoteDialog
from forms.add_table_dialog import AddTableDialog
from forms.add_heading_dialog import AddHeadingDialog
from forms.add_crossref_dialog import AddCrossRefDialog
from resources import icons_rc
import common


class MainWindow(QMainWindow):

    OpenedEditor = namedtuple("OpenedEditor", ["filepath", "in_current_project", "is_current_editor"])

    def __init__(self) -> None:

        super().__init__()

        # Prepare Ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EditorTabWidget.clear()
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.splitter.setStretchFactor(2, 1)

        self.ui.ProjectStructureTreeWidget.setHeaderLabels(["Text", "Identifier"])
        self.ui.ProjectStructureTreeWidget.setHeaderHidden(False)
        self.ui.ProjectStructureTreeWidget.hideColumn(2)
        self.ui.ProjectStructureTreeWidget.hideColumn(3)

        # Set additional class attributes
        self.tabs = (self.ui.EditorTabLabel, self.ui.GitTabLabel, self.ui.ProjectTabLabel)
        self.ProjectManager = components.managers.ProjectManager
        self.ThreadManager = components.managers.ThreadManager
        self.SettingsManager = components.managers.SettingsManager
        self.SettingsManager.parent = self
        self.GitManager = components.managers.GitManager

        self.OpenedEditors = []
        self.current_editor_index = 0

        # Call convenience functions to setup Ui
        self.load_icons()
        self.set_toolbar_actions()

        # Connect signals and slots
        self.ui.EditorTabWidget.tabBar().currentChanged.connect(self.on_currentEditor_changed)

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
        self.ui.StrikethroughToolButton.setDefaultAction(self.ui.actionStrikethrough)
        self.ui.SuperscriptToolButton.setDefaultAction(self.ui.actionSuperscript)
        self.ui.SubscriptToolButton.setDefaultAction(self.ui.actionSubscript)
        self.ui.FootnoteToolButton.setDefaultAction(self.ui.actionFootnote)
        self.ui.TableToolButton.setDefaultAction(self.ui.actionAddTable)
        self.ui.CrossRefToolButton.setDefaultAction(self.ui.actionCrossRef)
        self.ui.RenderProjectToolButton.setDefaultAction(self.ui.actionRenderProject)

    def load_icons(self) -> None:
        # load common icons
        self.ui.EditorTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/document-papirus.svg")))
        self.ui.GitTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/git-branch.svg")))
        self.ui.ProjectTabLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/project-management.svg")))
        self.ui.SettingsLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/settings.svg")))
        self.ui.UserAccounLabel.setPixmap(QPixmap.fromImage(QImage(":/icons_common/icons_common/account.svg")))

        # load light/dark icons
        icon_type = self.SettingsManager.get_setting_value("Colors/Icons")
        prefix = f"icons_{icon_type.lower()}"

        common.load_icon("format-text-italic.svg", prefix, self.ui.actionItalic)
        common.load_icon("format-text-bold.svg", prefix, self.ui.actionBold)
        common.load_icon("format-text-bold-italic.svg", prefix, self.ui.actionBoldItalic)
        common.load_icon("heading1.svg", prefix, self.ui.actionHeading1)
        common.load_icon("heading2.svg", prefix, self.ui.actionHeading2)
        common.load_icon("heading3.svg", prefix, self.ui.actionHeading3)
        common.load_icon("heading4.svg", prefix, self.ui.actionHeading4)
        common.load_icon("heading5.svg", prefix, self.ui.actionHeading5)
        common.load_icon("heading6.svg", prefix, self.ui.actionHeading6)
        common.load_icon("horizontal-rule.svg", prefix, self.ui.actionHorizontalRule)
        common.load_icon("format-text-blockquote.svg", prefix, self.ui.actionBlockquote)
        common.load_icon("ord-list", prefix, self.ui.actionOrdList)
        common.load_icon("unord-list.svg", prefix, self.ui.actionUnordList)
        common.load_icon("link.svg", prefix, self.ui.actionLink)
        common.load_icon("insert-image.svg", prefix, self.ui.actionImage)
        common.load_icon("format-text-code.svg", prefix, self.ui.actionCode)
        common.load_icon("format-text-strikethrough.svg", prefix, self.ui.actionStrikethrough)
        common.load_icon("format-text-superscript.svg", prefix, self.ui.actionSuperscript)
        common.load_icon("format-text-subscript.svg", prefix, self.ui.actionSubscript)
        common.load_icon("insert-footnote.svg", prefix, self.ui.actionFootnote)
        common.load_icon("table.svg", prefix, self.ui.actionAddTable)
        common.load_icon("text-frame-link.svg", prefix, self.ui.actionCrossRef)

        common.load_icon("heading1.svg", prefix, self.ui.HeadingToolButton)

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

        # Create project manager for current project
        try:
            components.managers.ProjectManager.load_project(path)
        except common.ProjectError as e:
            components.managers.ProjectManager.close_project()
            QMessageBox.critical(self, "Error", "Failed to load project: " + e.message.lower())
            return

        self.ProjectManager.Communicator.ProjectStructureUpdated.connect(self.on_ProjectStructureUpdated)

        # Populate ProjectWidget with information about project file structure
        self.ui.ProjectTreeView.setModel(self.ProjectManager.FsModel)
        self.ui.ProjectTreeView.setRootIndex(self.ProjectManager.FsModel.index(path))
        self.ui.ProjectTreeView.hideColumn(1)
        self.ui.ProjectTreeView.hideColumn(2)
        self.ui.ProjectTreeView.hideColumn(3)
        self.ui.ProjectTreeView.header().setVisible(False)
        self.on_EditorTabLabel_clicked()
        self.ProjectManager.FsModel.directoryLoaded.connect(self.on_ProjectManager_ProjectDirectoryLoaded)

    def read_settings(self) -> None:
        """Get settings from SettignsManager and adjust the ui accordingly"""

        self.resize(self.SettingsManager.get_setting_value("MainWindow/size"))
        self.move(self.SettingsManager.get_setting_value("MainWindow/pos"))
        self.ui.splitter.setSizes(self.SettingsManager.get_setting_value("MainWindow/splitter_sizes"))
        self.ui.ProjectTabWidget.setCurrentIndex(self.SettingsManager.get_setting_value("MainWindow/ProjectTabWidget_currentTab"))

        if self.SettingsManager.get_setting_value("MainWindow/last_project"):
            # Catching all exceptions here, because any unhandled exception at this point would prevent the program
            # from starting again ever
            try:
                self.load_project(self.SettingsManager.get_setting_value("MainWindow/last_project"))
            except Exception as e:
                QMessageBox.critical(self, "Error", "An error occured while attempting to open project. " +
                                     f"Error: {str(type(e)) + ' ' + str(e)}")
                self.ProjectManager.close_project()

        # Read color schema settings for the app
        app_colors = self.SettingsManager.get_current_color_schema()["Application_colors"]
        palette = self.palette()
        palette.setColor(palette.Window, QColor(app_colors["window"]["color"]))
        palette.setColor(palette.WindowText, QColor(app_colors["window_text"]["color"]))
        palette.setColor(palette.Base, QColor(app_colors["base"]["color"]))
        palette.setColor(palette.AlternateBase, QColor(app_colors["alternate_base"]["color"]))
        palette.setColor(palette.ToolTipBase, QColor(app_colors["tooltip_base"]["color"]))
        palette.setColor(palette.ToolTipText, QColor(app_colors["tooltip_text"]["color"]))
        palette.setColor(palette.PlaceholderText, QColor(app_colors["placeholder_text"]["color"]))
        palette.setColor(palette.Text, QColor(app_colors["text"]["color"]))
        palette.setColor(palette.Button, QColor(app_colors["button"]["color"]))
        palette.setColor(palette.ButtonText, QColor(app_colors["button_text"]["color"]))
        palette.setColor(palette.BrightText, QColor(app_colors["bright_text"]["color"]))
        self.setPalette(palette)

    def write_settings(self) -> None:
        """Write settings to permanent storage"""

        self.SettingsManager.set_setting_value("MainWindow/size", self.size())
        self.SettingsManager.set_setting_value("MainWindow/pos", self.pos())

        # Remember splitter sizes if currernt file is not html
        editor = self.get_editor()
        remember_splitter_sizes = True
        if editor:
            if editor.is_html_file():
                remember_splitter_sizes = False
        if remember_splitter_sizes:
            self.SettingsManager.set_setting_value("MainWindow/splitter_sizes", self.ui.splitter.sizes())

        if self.ProjectManager.is_project_loaded():
            self.SettingsManager.set_setting_value("MainWindow/last_project", self.ProjectManager.root_path)
        else:
            self.SettingsManager.set_setting_value("MainWindow/last_project", "")

        self.SettingsManager.set_setting_value("MainWindow/ProjectTabWidget_currentTab", self.ui.ProjectTabWidget.currentIndex())

    def get_current_structure(self, editor: TextEditor) -> dict:
        """Returns a dictionary describing the structure of the currently open document, or the structure of the current
        project if current file is to be rendered"""
        use_project_structure = False
        if self.ProjectManager.is_project_loaded():
            if self.ProjectManager.is_file_to_be_rendered(editor.document().baseUrl().toLocalFile()):
                use_project_structure = True

        identifiers = dict()
        if use_project_structure:
            identifiers = self.ProjectManager.get_setting_value("Project structure combined")
        else:
            identifiers = editor.document_structure

        return identifiers

    def get_used_identifiers(self, identifier_type: str, editor: TextEditor) -> dict:
        """Returns a dictionary of used identifier of a certain type for editor at tab with a given index. Document
        or project structure is used to determine which identifiers are already used."""

        identifiers = self.get_current_structure(editor)

        return identifiers[identifier_type]

    def insert_heading(self, heading_level: int) -> None:
        """Calls AddHeadingDialog and inserts a heading if the user accepted the dialog"""

        editor = self.get_editor()
        if editor:
            dialog = AddHeadingDialog(self.SettingsManager, heading_level, self.get_used_identifiers("headings", editor), parent=self)
            dialog.show()
            if dialog.exec_():
                editor.insert_text_at_empty_paragraph(dialog.heading_tag)

    def maximize_preview(self) -> None:
        """Maximizes webEngineView. Used when opening html files or other files which are not supposed to be edited here
        but can be displayed in preview"""
        sizes = self.ui.splitter.sizes()
        self.ui.splitter.setSizes([sizes[0], 0, sizes[1] + sizes[2]])

    def restore_splitter_sizes(self) -> None:
        """Sets splitter sizes to the values stored in the SettingsManager"""
        sizes = list(self.SettingsManager.get_setting_value("MainWindow/splitter_sizes"))
        self.ui.splitter.setSizes(sizes)

    def resize_splitter(self, filename: str) -> None:
        """Resizes self.ui.splitter based on the file extension of the filename. Maximizes the preview size for certain
        filetypes or restores it to normal values otherwise"""
        if filename.endswith((".html", ".htm")):
            self.maximize_preview()
        else:
            self.restore_splitter_sizes()

    # TODO: maintain the state of the tree before update (i.e. which entry is selected and which entries are expanded
    def update_structure_tree_widget(self, project_structure: dict) -> None:
        """Loads given structure into structure tree widget"""
        common.load_project_structure(project_structure, self.ui.ProjectStructureTreeWidget)

    # Event handling
    def closeEvent(self, event: QCloseEvent) -> None:
        """Checks whether any editors have unsaved changes before closing the main window. Asks whether to save or
        discard them if there are. Writes settings before closing"""

        unsaved_editors = []
        detailed_text = "Modified documents:\n"

        # Create a list of editors with unsaved changes
        for index in range(len(self.OpenedEditors)):
            editor = self.get_editor(index)
            if editor.text_changed_since_save:
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
        """Opens project settings dialog"""
        if self.ProjectManager.is_project_loaded():
            dialog = ProjectSettingsDialog(self, self.ProjectManager, self.SettingsManager)
            dialog.show()
            dialog.exec_()

    @pyqtSlot()
    def on_SettingsLabel_clicked(self) -> None:
        self.on_actionSettings_triggered()

    @pyqtSlot()
    def on_actionNew_triggered(self) -> None:
        """Creates a new tab in EditorTabWidget, puts a TextEditor in that tab, sets editor settings and switches to the
         created tab"""

        # Create main widget of the tab
        widget = QWidget(self)
        widget.setLayout(QVBoxLayout())
        widget.layout().setContentsMargins(0, 2, 0, 0)

        # Create editor
        self.ui.EditorTabWidget.untitled_docs_counter += 1
        filename = f"Untitled {self.ui.EditorTabWidget.untitled_docs_counter}"
        editor = TextEditor(widget, self.ui.webEngineView, self.SettingsManager, self.ThreadManager, filename)
        editor.FileStrucutreUpdated.connect(self.on_fileStructureUpdated)

        self.OpenedEditors.append(self.OpenedEditor(filepath=None, in_current_project=False, is_current_editor=True))
        widget.layout().addWidget(editor)

        # Create new tab
        index = self.ui.EditorTabWidget.addTab(widget, editor.filename)
        self.ui.EditorTabWidget.setCurrentIndex(index)

        editor.setFocus()
        self.on_EditorTabLabel_clicked()

    @pyqtSlot()
    def on_actionOpen_triggered(self, path: str = None):
        """Open file at given path, or get path from user with QFileDialog if path is not given"""

        if path is None:
            path = QFileDialog.getOpenFileName()[0]

        if path:
            # Check if file is already opened in some editor
            for i in range(len(self.OpenedEditors)):

                if path == self.OpenedEditors[i].filepath:
                    self.ui.EditorTabWidget.setCurrentIndex(i)
                    return

            # If it isn't open it in a new editor
            # Read file
            try:
                file_handle = open(path, mode="rb")
                text = file_handle.read()
                text = text.decode(errors="replace")

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

            # Configure new tab
            current_tab_index = self.ui.EditorTabWidget.currentIndex()
            editor.set_filename(path[path.rfind("/") + 1:])

            self.OpenedEditors[current_tab_index] = self.OpenedEditor(filepath=path, in_current_project=False, is_current_editor=True)
            self.ui.EditorTabWidget.setTabToolTip(current_tab_index, path)
            self.ui.EditorTabWidget.setTabText(current_tab_index, editor.filename)

            editor.text_changed_since_save = False
            editor.text_changed_since_render = True

            # Maximize preview tab, if the file is html or set to normal values if it is not
            self.resize_splitter(path)

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
                editor.text_changed_since_save = False
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
                editor.text_changed_since_save = False
            except OSError:
                filename = self.ui.EditorTabWidget.tabText(index)
                QMessageBox.critical(self, "Error", f"Failed to save file \"{filename}\"")
            finally:
                file_handle.close()

            editor.set_filename(path[path.rfind("/") + 1:])

            editor.document().setBaseUrl(QUrl.fromLocalFile(path))
            self.OpenedEditors[index] = self.OpenedEditor(filepath=path, in_current_project=False, is_current_editor=True)
            self.ui.EditorTabWidget.setTabToolTip(index, path)
            self.ui.EditorTabWidget.setTabText(index, editor.filename)

        return result

    @pyqtSlot(int)
    def on_EditorTabWidget_tabCloseRequested(self, index: int) -> None:
        """Close EditorTabWidget's tab at index. If there are unsaved changes in that tab's editor, ask whether to save
        them"""

        remove = True
        if self.get_editor(index).text_changed_since_save:
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
        self.insert_heading(1)

    @pyqtSlot()
    def on_actionHeading2_triggered(self) -> None:
        self.insert_heading(2)

    @pyqtSlot()
    def on_actionHeading3_triggered(self) -> None:
        self.insert_heading(3)

    @pyqtSlot()
    def on_actionHeading4_triggered(self) -> None:
        self.insert_heading(4)

    @pyqtSlot()
    def on_actionHeading5_triggered(self) -> None:
        self.insert_heading(5)

    @pyqtSlot()
    def on_actionHeading6_triggered(self) -> None:
        self.insert_heading(6)

    @pyqtSlot()
    def on_actionHorizontalRule_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_text_at_empty_paragraph("---")

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

        dialog = AddLinkDialog(parent=self)
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor(dialog.link)

    @pyqtSlot()
    def on_actionImage_triggered(self) -> None:
        editor = self.get_editor()

        if editor is None:
            return

        dialog = AddImageDialog(self.ProjectManager, self.SettingsManager, self.get_used_identifiers("figures", editor),
                                parent=self)
        dialog.show()
        if dialog.exec_():

            text = f"![{dialog.image_text}]({dialog.image_path})"

            if dialog.has_additional_attributes:
                text += "{"
                if dialog.identifier:
                    text += f"#{dialog.identifier}"
                if dialog.image_width:
                    text += f" width={dialog.image_width}"
                if dialog.image_height:
                    text += f" height={dialog.image_height}"
                text += "}"

            self.get_editor().insert_text_at_cursor(text)

    @pyqtSlot()
    def on_actionCode_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() != 0:
            self.get_editor().insert_double_tag("`")

    @pyqtSlot()
    def on_actionAddCitation_triggered(self) -> None:
        if self.ui.EditorTabWidget.count() == 0:
            return

        dialog = AddCitationDialog(self.ThreadManager, parent=self)
        dialog.show()
        if dialog.exec_():
            self.get_editor().insert_text_at_cursor("[@{}]".format(dialog.citation_identifier))

    @pyqtSlot()
    def on_actionRenderFile_triggered(self) -> None:
        """Render the contents of the editor at the currently active tab to html"""
        if self.get_editor():
            self.get_editor().render_to_html()

    @pyqtSlot()
    def on_actionStrikethrough_triggered(self) -> None:
        editor = self.get_editor()
        if editor:
            self.get_editor().insert_double_tag("~~")

    @pyqtSlot()
    def on_actionSuperscript_triggered(self) -> None:
        editor = self.get_editor()
        if editor:
            editor.insert_double_tag("^")

    @pyqtSlot()
    def on_actionSubscript_triggered(self) -> None:
        editor = self.get_editor()
        if editor:
            editor.insert_double_tag("~")

    @pyqtSlot()
    def on_actionFootnote_triggered(self) -> None:

        editor = self.get_editor()
        if not editor:
            return

        identifiers = self.get_used_identifiers("footnotes", editor)

        dialog = AddFootnoteDialog(identifiers, self.SettingsManager, parent=self)
        dialog.show()
        if dialog.exec_():
            identifier = dialog.identifier
            text = dialog.text

            editor.insert_text_at_cursor(f"[^{identifier}]")
            editor.insert_text_at_empty_paragraph(f"[^{identifier}]: {text}")

    @pyqtSlot()
    def on_actionCrossRef_triggered(self) -> None:
        editor = self.get_editor()

        if editor:
            dialog = AddCrossRefDialog(self.get_current_structure(editor), editor.is_cursor_in_sentence(), parent=self)
            dialog.show()
            if dialog.exec_():
                editor.insert_text_at_cursor(dialog.tag)

    @pyqtSlot()
    def on_TableToolButton_triggered(self) -> None:

        editor = self.get_editor()
        if not editor:
            return

        dialog = AddTableDialog(self.get_used_identifiers("tables", editor), self.SettingsManager, parent=self)
        dialog.show()
        if dialog.exec_():
            editor.insert_text_at_empty_paragraph(dialog.table_tag)

    @pyqtSlot()
    def on_actionRenderProject_triggered(self) -> None:
        if self.ProjectManager.is_project_loaded():
            self.ThreadManager.perform_operation("render_project", self.on_project_rendered,
                                                 project_manager=self.ProjectManager)

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
                                     self.SettingsManager.get_setting_value("Application/Project folder"), parent=self)
        dialog.show()
        if dialog.exec_():
            ProjectManager.create_project(dialog.path)
            self.load_project(dialog.path)
            yaml_metablock = self.ProjectManager.get_setting_value("YAML_metablock")
            yaml_metablock["title"] = dialog.title
            yaml_metablock["author"] = dialog.authors
            self.ProjectManager.set_setting_value("YAML_metablock", yaml_metablock)
            self.ProjectManager.set_setting_value("Project type", dialog.project_type)
            try:
                self.ProjectManager.save_project_data()
            except common.ProjectError as e:
                QMessageBox.critical(self, "Error", f"Failed to create project: {e.message}")

    @pyqtSlot(QPoint)
    def on_ProjectTreeView_customContextMenuRequested(self, point: QPoint) -> None:
        """Displays context menu for the ProjectWidget to create/delete/rename files in the project tree"""

        if not self.ProjectManager.is_project_loaded():
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
            try:
                self.ProjectManager.create_file(path + "/" + name[0])
            except common.ProjectError as e:
                QMessageBox.critical(self, "Error", f"An error occured: {e.message}")

    @pyqtSlot()
    def on_actionDelete_triggered(self) -> None:
        """Deletes a file or a folder in project structure, which corresponds to the element, on which the user clicked
        when calling the context menu"""

        point = self.ui.actionCreateFolder.data()
        clicked_item = self.ui.ProjectTreeView.indexAt(point)

        if clicked_item.data() is None:
            clicked_item = self.ui.ProjectTreeView.rootIndex()
        try:
            self.ProjectManager.delete_file(clicked_item)
        except common.ProjectError as e:
            QMessageBox.critical(self, "Error", f"An error occured: {e.message}")

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
            try:
                self.ProjectManager.rename(clicked_item, name[0])
            except common.ProjectError as e:
                QMessageBox.critical(self, "Error", f"An error occured: {e.message}")

    @pyqtSlot(str)
    def on_ProjectManager_ProjectDirectoryLoaded(self) -> None:
        """Expands the project tree in the ProjectWidget, when the project directory is loaded. Can't do it before it
        is loaded (i.e. in load_project()"""

        self.ui.ProjectTreeView.expandToDepth(4)

    @pyqtSlot(QModelIndex)
    def on_ProjectTreeView_clicked(self, index: QModelIndex) -> None:
        """Open the file, which the user clicked on in the project tree"""

        if not self.ProjectManager.FsModel.isDir(index):
            filepath = self.ProjectManager.FsModel.filePath(index)
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

        dialog = SettingsDialog(self.SettingsManager, parent=self)
        dialog.show()
        dialog.exec_()

    @pyqtSlot(int)
    def on_currentEditor_changed(self, index: int) -> None:
        # Mark all editors as not-current
        previous_editor = None
        for i in range(self.ui.EditorTabWidget.count()):
            editor = self.get_editor(i)
            if editor.is_current_editor:
                previous_editor = editor
                editor.is_current_editor = False

        # Remember splitter sizes
        if previous_editor:
            sizes = self.ui.splitter.sizes()
            if not previous_editor.is_html_file():
                self.SettingsManager.set_setting_value("MainWindow/splitter_sizes", sizes)

        # Get editor at index and set it current
        editor = self.get_editor(index)
        if editor:
            editor.is_current_editor = True

            # Parse and render new document
            editor.parse_document()
            if self.SettingsManager.get_setting_value("Render/Autorender"):
                editor.render_to_html()

            # Resize splitter
            self.resize_splitter(editor.filename)

    @pyqtSlot(dict)
    def on_fileStructureUpdated(self, file_structure: dict) -> None:
        """Receives signal when the current editor (or the editor that once was current) reports that it's document
        structure has changed. Updates structure tree immediately if it is displaying current file, or sends the
        structure to project manager if it isn't"""

        if self.ui.ProjectStrucutreCombobox.currentIndex() == 0:
            editor = self.get_editor()
            if editor:
                self.update_structure_tree_widget(editor.document_structure)
        else:
            if self.ProjectManager:
                self.ProjectManager.update_project_structure(file_structure)

    @pyqtSlot(int)
    def on_ProjectStrucutreCombobox_currentIndexChanged(self, index: int) -> None:
        """Switches the structure tree between displaying the structure of the current file and the structure of the
        current project"""

        if index == 0:
            editor = self.get_editor()
            if editor:
                self.update_structure_tree_widget(self.get_editor().document_structure)
            else:
                self.ui.ProjectStructureTreeWidget.clear()
        else:
            if self.ProjectManager:
                self.update_structure_tree_widget(self.ProjectManager.get_setting_value("Project structure combined"))
            else:
                self.ui.ProjectStructureTreeWidget.clear()

    @pyqtSlot()
    def on_ProjectStructureUpdated(self) -> None:
        """Receives signal that ProjectManager has updated its project structure. Updates structure tree if the user
        has selected to display project structure"""

        if self.ui.ProjectStrucutreCombobox.currentIndex() == 1:
            self.update_structure_tree_widget(self.ProjectManager.get_setting_value("Project structure combined"))

    @pyqtSlot()
    def on_actionCloseProject_triggered(self) -> None:
        self.ProjectManager = None
        self.ui.ProjectTreeView.setModel(None)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_ProjectStructureTreeWidget_itemDoubleClicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Opens the item clicked by the user in the editor (i.e. opens a file with that item and scrolls to it"""
        filepath = item.text(3)
        block_number = int(item.text(2))

        self.on_actionOpen_triggered(filepath)
        self.get_editor().move_cursor_to_block(block_number)

    def on_project_rendered(self, result) -> None:
        filepath = result

        # Try to display output in preview. Works for html files
        # TODO: for some reason doesn't work with pdfs
        self.ui.webEngineView.load(QUrl.fromLocalFile(filepath))
