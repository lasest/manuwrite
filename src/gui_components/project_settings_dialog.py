from PyQt5.QtWidgets import QDialog, QListWidgetItem, QListWidget
from PyQt5.QtCore import QDate, QDirIterator, QDir, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QCloseEvent

from forms.ui_project_settings_dialog import Ui_ProjectSettingsDialog
from components.project_manager import ProjectManager
from components.settings_manager import SettingsManager


class ProjectSettingsDialog(QDialog):

    def __init__(self, parent, project_manager: ProjectManager, settings_manager: SettingsManager):

        super().__init__(parent)
        self.ui = Ui_ProjectSettingsDialog()
        self.ui.setupUi(self)

        # Set attributes
        self.ProjectManager = project_manager
        self.SettingsManager = settings_manager

        # Prepare ui elements
        self.set_toolbuttons_actions()
        self.load_icons()
        self.read_window_settings()
        self.read_meta_information_settings()
        self.read_render_settings()

    def load_icons(self) -> None:
        self.ui.actionMoveToTheTop.setIcon(QIcon(":/icons_dark/icons_dark/go-up-skip.svg"))
        self.ui.actionMoveUp.setIcon(QIcon(":/icons_dark/icons_dark/go-up.svg"))
        self.ui.actionMoveLeft.setIcon(QIcon(":/icons_dark/icons_dark/go-previous.svg"))
        self.ui.actionMoveRight.setIcon(QIcon(":/icons_dark/icons_dark/go-next.svg"))
        self.ui.actionMoveDown.setIcon(QIcon(":/icons_dark/icons_dark/go-down.svg"))
        self.ui.actionMoveToTheBottom.setIcon(QIcon(":/icons_dark/icons_dark/go-down-skip.svg"))

    def set_toolbuttons_actions(self) -> None:
        """Set defalult actions for tool buttons"""
        self.ui.MoveAllUpToolButton.setDefaultAction(self.ui.actionMoveToTheTop)
        self.ui.MoveUpToolButton.setDefaultAction(self.ui.actionMoveUp)
        self.ui.MoveLeftToolButton.setDefaultAction(self.ui.actionMoveLeft)
        self.ui.MoveRightToolButton.setDefaultAction(self.ui.actionMoveRight)
        self.ui.MoveDownToolButton.setDefaultAction(self.ui.actionMoveDown)
        self.ui.MoveAllDownToolButton.setDefaultAction(self.ui.actionMoveToTheBottom)

    def read_window_settings(self) -> None:
        """Read window settings (i.e. position, size, etc)"""
        self.resize(self.SettingsManager.get_setting_value("SettingsDialog/size"))
        self.move(self.SettingsManager.get_setting_value("SettingsDialog/pos"))

    def read_meta_information_settings(self) -> None:
        """Read meta information settings and update gui elements on Meta information tab"""
        self.ui.TitleLineEdit.setText(self.ProjectManager.get_setting_value("Title"))

        date = list(map(int, self.ProjectManager.get_setting_value("Date created")))
        date = QDate(date[0], date[1], date[2])
        self.ui.dateEdit.setDate(date)

        self.ui.AuthorsLineEdit.setText(self.ProjectManager.get_setting_value("Authors"))
        self.ui.ProjectTypeValueLabel.setText(self.ProjectManager.get_setting_value("Project type"))
        self.ui.DescriptionPlainTextEdit.setPlainText(self.ProjectManager.get_setting_value("Description"))
        self.ui.AdditionalMetaInfoPlainTextEdit.setPlainText(self.ProjectManager.get_setting_value("Additional meta " +
                                                                                                   "information"))

    def read_render_settings(self) -> None:
        """Read render settings and update gui elements on Render tab"""
        # Get the list of all markdown files in the project directory
        dir_iter = QDirIterator(self.ProjectManager.root_path, QDir.Files, QDirIterator.Subdirectories)
        filepaths = []
        while dir_iter.hasNext():
            filepath = dir_iter.next()
            if filepath.endswith(".md"):
                # Get relative path:
                filepath = filepath[len(self.ProjectManager.root_path):]
                filepaths.append(filepath)

        # Get the list of files which should be rendered according to the current project settings
        files_to_render = self.ProjectManager.get_setting_value("Files to render")

        # Populate widgets with filepaths
        for filepath in filepaths:
            if filepath not in files_to_render:
                item = QListWidgetItem(filepath)
                self.ui.AllFilesListWidget.addItem(item)

        for filepath in files_to_render:
            if filepath not in filepaths:
                item = QListWidgetItem(filepath + " (File not found!)")
                item.setForeground(Qt.red)
            else:
                item = QListWidgetItem(filepath)
            self.ui.FilesToRenderListWidget.addItem(item)

        # Populate StylesCombobox
        styles = self.SettingsManager.get_setting_value("Render/Styles")
        for style in styles:
            self.ui.StyleCombobox.addItem(style["name"])

        index = self.ui.StyleCombobox.findText(self.ProjectManager.get_setting_value("Style"))
        self.ui.StyleCombobox.setCurrentIndex(index)

        # Populate formats combobox
        formats = self.SettingsManager.get_setting_value("Render/Formats")
        for format in formats:
            self.ui.RenderToCombobox.addItem(format["name"])

        index = self.ui.RenderToCombobox.findText(self.ProjectManager.get_setting_value("Render to"))
        self.ui.RenderToCombobox.setCurrentIndex(index)

        # Populate PandocCommandLineEdit
        self.ui.PandocCommandLineEdit.setText(self.ProjectManager.get_setting_value("Pandoc command (auto)"))
        self.ui.PandocCommandManualLineEdit.setText(self.ProjectManager.get_setting_value("Pandoc command (manual)"))

    def update_meta_information_settings(self) -> None:
        """Update meta information settings in Project manager with info from gui"""
        self.ui.PandocCommandLineEdit.setText(self.get_pandoc_command())

        self.ProjectManager.set_setting_value("Title", self.ui.TitleLineEdit.text())

        date = self.ui.dateEdit.date()
        self.ProjectManager.set_setting_value("Date created", [date.year(), date.month(), date.day()])

        self.ProjectManager.set_setting_value("Authors", self.ui.AuthorsLineEdit.text())
        self.ProjectManager.set_setting_value("Description", self.ui.DescriptionPlainTextEdit.toPlainText())
        self.ProjectManager.set_setting_value("Additional meta information", self.ui.AdditionalMetaInfoPlainTextEdit.toPlainText())

    def update_render_settings(self) -> None:
        """Update render information settings in Project manager with info from gui"""
        files_to_render = []
        for i in range(self.ui.FilesToRenderListWidget.count()):
            if not self.ui.FilesToRenderListWidget.item(i).text().endswith("(File not found!)"):
                files_to_render.append(self.ui.FilesToRenderListWidget.item(i).text())
        self.ProjectManager.set_setting_value("Files to render", files_to_render)

        self.ProjectManager.set_setting_value("Style", self.ui.StyleCombobox.currentText())
        self.ProjectManager.set_setting_value("Render to", self.ui.RenderToCombobox.currentText())
        self.ProjectManager.set_setting_value("Pandoc command (auto)", self.ui.PandocCommandLineEdit.text())
        self.ProjectManager.set_setting_value("Pandoc command (manual)", self.ui.PandocCommandManualLineEdit.text())
        self.ProjectManager.set_setting_value("Additional meta information",
                                              self.ui.AdditionalMetaInfoPlainTextEdit.toPlainText())

    def get_current_list_widget(self) -> QListWidget:
        """Get QListWidget from Render tab which currently has a selected item in it"""
        if self.ui.FilesToRenderListWidget.selectedItems():
            ListWidget = self.ui.FilesToRenderListWidget
        elif self.ui.AllFilesListWidget.selectedItems():
            ListWidget = self.ui.AllFilesListWidget
        else:
            ListWidget = None

        return ListWidget

    def get_pandoc_command(self) -> str:
        """Form a pandoc command based on the info from gui"""
        # TODO: add filters
        command = "pandoc --standalone "
        for i in range(self.ui.FilesToRenderListWidget.count()):
            item = self.ui.FilesToRenderListWidget.item(i)
            if not item.text().endswith("(File not found!)"):
                command += item.text() + " "

        formats = self.SettingsManager.get_setting_value("Render/Formats")
        current_format = None
        for format in formats:
            if format["name"] == self.ui.RenderToCombobox.currentText():
                current_format = format

        # TODO: update css file in project directory with the corresponding template
        command += "--css .manuwrite/style/style.css "
        command += f"--to {current_format['pandoc name']} "
        command += f"output.{current_format['file extension']}"

        return command

    def accept(self) -> None:
        """Update project settings in Project manager and save them if the dialog is accepted"""

        self.update_meta_information_settings()
        self.update_render_settings()
        self.ProjectManager.save_project_data()

        super().accept()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Save window related settings before closing"""
        self.SettingsManager.set_setting_value("SettingsDialog/size", self.size())
        self.SettingsManager.set_setting_value("SettingsDialog/pos", self.pos())

    @pyqtSlot(QListWidgetItem)
    def on_FilesToRenderListWidget_itemClicked(self, item: QListWidgetItem) -> None:
        """Make sure only one of the QListWidgets on render tab has a selected item in it"""
        self.ui.AllFilesListWidget.clearSelection()
        self.ui.MoveLeftToolButton.setEnabled(False)
        self.ui.MoveRightToolButton.setEnabled(True)

    @pyqtSlot(QListWidgetItem)
    def on_AllFilesListWidget_itemClicked(self, item: QListWidgetItem) -> None:
        """Make sure only one of the QListWidgets on render tab has a selected item in it"""
        self.ui.FilesToRenderListWidget.clearSelection()
        self.ui.MoveLeftToolButton.setEnabled(True)
        self.ui.MoveRightToolButton.setEnabled(False)

    @pyqtSlot()
    def on_actionMoveToTheTop_triggered(self) -> None:
        """Move currently selected item in a QListWidget on render tab to the top of the list"""
        ListWidget = self.get_current_list_widget()
        if ListWidget:
            current_row = ListWidget.currentRow()
            item = ListWidget.takeItem(current_row)
            ListWidget.insertItem(0, item)
            ListWidget.setCurrentRow(0)

    @pyqtSlot()
    def on_actionMoveUp_triggered(self) -> None:
        """Move currently selected item in a QListWidget on render tab one row up"""
        ListWidget = self.get_current_list_widget()
        if ListWidget:
            current_row = ListWidget.currentRow()
            if current_row != 0:
                item = ListWidget.takeItem(current_row)
                ListWidget.insertItem(current_row - 1, item)
                ListWidget.setCurrentRow(current_row - 1)

    @pyqtSlot()
    def on_actionMoveLeft_triggered(self) -> None:
        """Move item from the list of all markdown files to the list of files to be rendered"""
        current_editor, other_editor = self.ui.AllFilesListWidget, self.ui.FilesToRenderListWidget
        if current_editor.selectedItems():
            current_row = current_editor.currentRow()
            item = current_editor.takeItem(current_row)
            other_editor.addItem(item)

    @pyqtSlot()
    def on_actionMoveRight_triggered(self) -> None:
        """Move item from the list of files to be rendered to the list of all markdown files"""
        current_editor, other_editor = self.ui.FilesToRenderListWidget, self.ui.AllFilesListWidget
        if current_editor.selectedItems():
            current_row = current_editor.currentRow()
            item = current_editor.takeItem(current_row)
            if not item.text().endswith("(File not found!)"):
                other_editor.addItem(item)

    @pyqtSlot()
    def on_actionMoveDown_triggered(self) -> None:
        """Move currently selected item in QListWidget on render tab one row down"""
        ListWidget = self.get_current_list_widget()
        if ListWidget:
            current_row = ListWidget.currentRow()
            if current_row != ListWidget.count() - 1:
                item = ListWidget.takeItem(current_row)
                ListWidget.insertItem(current_row + 1, item)
                ListWidget.setCurrentRow(current_row + 1)

    @pyqtSlot()
    def on_actionMoveToTheBottom_triggered(self) -> None:
        """Move currently selected item in QListWidget on render tab to the bottom of the list"""
        ListWidget = self.get_current_list_widget()
        if ListWidget:
            current_row = ListWidget.currentRow()
            item = ListWidget.takeItem(current_row)
            ListWidget.insertItem(ListWidget.count() - 1, item)
            ListWidget.setCurrentRow(ListWidget.count() - 1)

    @pyqtSlot()
    def on_GeneratePandocCommandButton_clicked(self) -> None:
        """Generate the pandoc command based on the current gui inputs and put it to pandoc command line edit"""
        command = self.get_pandoc_command()
        self.ui.PandocCommandLineEdit.setText(command)
