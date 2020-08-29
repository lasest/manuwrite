from PyQt5.QtWidgets import QDialog, QListWidgetItem, QListWidget
from PyQt5.QtCore import QDate, QDirIterator, QDir, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QCloseEvent

from ui_forms.ui_project_settings_dialog import Ui_ProjectSettingsDialog
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

        self.pandoc_filters = self.ProjectManager.get_setting_value("Pandoc_filters")
        self.yaml_metablock = self.ProjectManager.get_setting_value("YAML_metablock")
        self.pandoc_args = self.ProjectManager.get_setting_value("Pandoc_args")
        self.pandoc_kargs = self.ProjectManager.get_setting_value("Pandoc_kargs")

        # Prepare ui elements
        self.set_toolbuttons_actions()
        self.load_icons()

        # Read settings
        self.read_window_settings()
        self.read_meta_information_settings()
        self.read_render_settings()
        self.read_pandoc_settings()
        self.read_xnos_settings()

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

    # Reading settings
    def read_pandoc_settings(self) -> None:
        self.ui.PandocXnosCheckbox.setChecked(self.pandoc_filters["pandoc-xnos"])
        self.ui.PandocSecnosCheckbox.setChecked(self.pandoc_filters["pandoc-secnos"])
        self.ui.PandocFignosCheckbox.setChecked(self.pandoc_filters["pandoc-fignos"])
        self.ui.PandocTablenosCheckbox.setChecked(self.pandoc_filters["pandoc-tablenos"])
        self.ui.PandocEqnosCheckbox.setChecked(self.pandoc_filters["pandoc-eqnos"])
        self.ui.PandocCiteProcCheckbox.setChecked(self.pandoc_filters["pandoc-citeproc"])
        self.ui.ManubotCiteCheckbox.setChecked(self.pandoc_filters["pandoc-manubot-cite"])

        self.ui.NumberSectionsCheckbox.setChecked(self.pandoc_args["number-sections"])
        self.ui.StandaloneCheckbox.setChecked(self.pandoc_args["standalone"])

        self.ui.ManualBibLineEdit.setText(self.yaml_metablock["bibliography"])

    def read_xnos_settings(self) -> None:
        self.ui.SecnosCleverCheckbox.setChecked(self.yaml_metablock["secnos-cleveref"])
        self.ui.SecnosPlusNameLineEdit.setText(self.yaml_metablock["secnos-plus-name"])
        self.ui.SecnosStarNameLineEdit.setText(self.yaml_metablock["secnos-star-name"])

        self.ui.FignosCleverCheckbox.setChecked(self.yaml_metablock["fignos-cleveref"])
        self.ui.FignosNumberBySecCheckbox.setChecked(self.yaml_metablock["fignos-number-by-section"])
        self.ui.FignosPlusNameLineEdit.setText(self.yaml_metablock["fignos-plus-name"])
        self.ui.FignosStarNameLineEdit.setText(self.yaml_metablock["fignos-star-name"])
        self.ui.FignosCaptionNameLineEdit.setText(self.yaml_metablock["fignos-caption-name"])
        index = self.ui.FignosCaptionSepCombobox.findText(self.yaml_metablock["fignos-caption-separator"])
        if index == -1:
            index = 0
        self.ui.FignosCaptionSepCombobox.setCurrentIndex(index)

        self.ui.TablenosCleverCheckbox.setChecked(self.yaml_metablock["tablenos-cleveref"])
        self.ui.TablenosNumberBySecCheckbox.setChecked(self.yaml_metablock["tablenos-number-by-section"])
        self.ui.TablenosPlusNameLineEdit.setText(self.yaml_metablock["tablenos-plus-name"])
        self.ui.TablenosStarNameLineEdit.setText(self.yaml_metablock["tablenos-star-name"])
        self.ui.TablenosCaptionNameLineEdit.setText(self.yaml_metablock["tablenos-caption-name"])
        index = self.ui.TablenosCaptionSepCombobox.findText(self.yaml_metablock["tablenos-caption-separator"])
        if index == -1:
            index = 0
        self.ui.TablenosCaptionSepCombobox.setCurrentIndex(index)

        self.ui.EqnosCleverCheckbox.setChecked(self.yaml_metablock["eqnos-cleveref"])
        self.ui.EqnosNumberBySecCheckbox.setChecked(self.yaml_metablock["eqnos-number-by-section"])
        self.ui.EqnosPlusNameLineEdit.setText(self.yaml_metablock["eqnos-plus-name"])
        self.ui.EqnosStarNameLineEdit.setText(self.yaml_metablock["eqnos-star-name"])
        self.ui.EqnosEqrefCheckbox.setChecked(self.yaml_metablock["eqnos-eqref"])

    def read_window_settings(self) -> None:
        """Read window settings (i.e. position, size, etc)"""
        self.resize(self.SettingsManager.get_setting_value("ProjectSettingsDialog/size"))
        self.move(self.SettingsManager.get_setting_value("ProjectSettingsDialog/pos"))
        tab_index = self.SettingsManager.get_setting_value("ProjectSettingsDialog/current tab index")
        self.ui.MainTabWidget.setCurrentIndex(tab_index)

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
        self.ui.MetaInfoCheckbox.setChecked(self.ProjectManager.get_setting_value("Include_metainfo"))

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
        for identifier, style_info in styles.items():
            self.ui.StyleCombobox.addItem(style_info["name"], userData=identifier)

        current_style_identifier = self.ProjectManager.get_setting_value("Style")
        index = self.ui.StyleCombobox.findData(current_style_identifier)
        self.ui.StyleCombobox.setCurrentIndex(index)

        # Populate formats combobox
        formats = self.SettingsManager.get_setting_value("Render/Formats")
        for identifier, format_info in formats.items():
            self.ui.RenderToCombobox.addItem(format_info["name"], userData=identifier)

        current_output_format_identifier = self.ProjectManager.get_setting_value("Render to")
        index = self.ui.RenderToCombobox.findData(current_output_format_identifier)
        self.ui.RenderToCombobox.setCurrentIndex(index)

        # Populate PandocCommandLineEdit
        self.ui.PandocCommandLineEdit.setText(self.ProjectManager.get_setting_value("Pandoc command (auto)"))
        self.ui.PandocCommandManualLineEdit.setText(self.ProjectManager.get_setting_value("Pandoc command (manual)"))

    # Writing settings
    def update_window_settings(self) -> None:
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/size", self.size())
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/pos", self.pos())
        tab_index = self.ui.MainTabWidget.currentIndex()
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/current tab index", tab_index)

    def update_meta_information_settings(self) -> None:
        """Update meta information settings in Project manager with info from gui"""
        self.ui.PandocCommandLineEdit.setText(self.get_pandoc_command())

        self.ProjectManager.set_setting_value("Title", self.ui.TitleLineEdit.text())

        date = self.ui.dateEdit.date()
        self.ProjectManager.set_setting_value("Date created", [date.year(), date.month(), date.day()])

        self.ProjectManager.set_setting_value("Authors", self.ui.AuthorsLineEdit.text())
        self.ProjectManager.set_setting_value("Description", self.ui.DescriptionPlainTextEdit.toPlainText())
        self.ProjectManager.set_setting_value("Additional meta information", self.ui.AdditionalMetaInfoPlainTextEdit.toPlainText())
        self.ProjectManager.set_setting_value("Include_metainfo", self.ui.MetaInfoCheckbox.isChecked())

    def update_render_settings(self) -> None:
        """Update render information settings in Project manager with info from gui"""
        # Update files to render
        files_to_render = []
        for i in range(self.ui.FilesToRenderListWidget.count()):
            if not self.ui.FilesToRenderListWidget.item(i).text().endswith("(File not found!)"):
                files_to_render.append(self.ui.FilesToRenderListWidget.item(i).text())
        self.ProjectManager.set_setting_value("Files to render", files_to_render)

        # Update style info
        style_identifier = self.ui.StyleCombobox.currentData()
        self.ProjectManager.set_setting_value("Style", style_identifier)
        styles = self.SettingsManager.get_setting_value("Render/Styles")
        style_filepath = styles[style_identifier]["path"]
        self.pandoc_kargs["css"] = style_filepath

        # Update output format and filename
        format_identifier = self.ui.RenderToCombobox.currentData()
        self.ProjectManager.set_setting_value("Render to", format_identifier)
        formats = self.SettingsManager.get_setting_value("Render/Formats")
        current_format = formats[format_identifier]

        self.pandoc_kargs["to"] = current_format["pandoc_option"]
        self.pandoc_kargs["output"] = f"output.{current_format['file_extension']}"

        # Update pandoc command
        self.ProjectManager.set_setting_value("Pandoc command (auto)", self.get_pandoc_command())
        self.ProjectManager.set_setting_value("Pandoc command (manual)", self.ui.PandocCommandManualLineEdit.text())

        full_pandoc_command = self.ProjectManager.get_setting_value("Pandoc command (auto)") + " " + self.ProjectManager.get_setting_value("Pandoc command (manual)")
        self.ProjectManager.set_setting_value("Full_pandoc_command", full_pandoc_command)

    def update_pandoc_settings(self) -> None:
        self.pandoc_filters["pandoc-xnos"] = self.ui.PandocXnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-secnos"] = self.ui.PandocSecnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-fignos"] = self.ui.PandocFignosCheckbox.isChecked()
        self.pandoc_filters["pandoc-tablenos"] = self.ui.PandocTablenosCheckbox.isChecked()
        self.pandoc_filters["pandoc-eqnos"] = self.ui.PandocEqnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-citeproc"] = self.ui.PandocCiteProcCheckbox.isChecked()
        self.pandoc_filters["pandoc-manubot-cite"] = self.ui.ManubotCiteCheckbox.isChecked()

        self.pandoc_args["number-sections"] = self.ui.NumberSectionsCheckbox.isChecked()
        self.pandoc_args["standalone"] = self.ui.StandaloneCheckbox.isChecked()

        self.yaml_metablock["bibliography"] = self.ui.ManualBibLineEdit.text()

    def update_xnos_settings(self) -> None:
        self.yaml_metablock["secnos-cleveref"] = self.ui.SecnosCleverCheckbox.isChecked()
        self.yaml_metablock["secnos-plus-name"] = self.ui.SecnosPlusNameLineEdit.text()
        self.yaml_metablock["secnos-star-name"] = self.ui.SecnosStarNameLineEdit.text()

        self.yaml_metablock["fignos-cleveref"] = self.ui.FignosCleverCheckbox.isChecked()
        self.yaml_metablock["fignos-number-by-section"] = self.ui.FignosNumberBySecCheckbox.isChecked()
        self.yaml_metablock["fignos-plus-name"] = self.ui.FignosPlusNameLineEdit.text()
        self.yaml_metablock["fignos-star-name"] = self.ui.FignosStarNameLineEdit.text()
        self.yaml_metablock["fignos-caption-name"] = self.ui.FignosCaptionNameLineEdit.text()

        if self.ui.FignosCaptionSepCombobox.currentIndex() != 0:
            self.yaml_metablock["fignos-caption-separator"] = self.ui.FignosCaptionSepCombobox.currentText()
        else:
            self.yaml_metablock["fignos-caption-separator"] = ""

        self.yaml_metablock["tablenos-cleveref"] = self.ui.TablenosCleverCheckbox.isChecked()
        self.yaml_metablock["tablenos-number-by-section"] = self.ui.TablenosNumberBySecCheckbox.isChecked()
        self.yaml_metablock["tablenos-plus-name"] = self.ui.TablenosPlusNameLineEdit.text()
        self.yaml_metablock["tablenos-star-name"] = self.ui.TablenosStarNameLineEdit.text()
        self.yaml_metablock["tablenos-caption-name"] = self.ui.TablenosCaptionNameLineEdit.text()

        if self.ui.TablenosCaptionSepCombobox.currentIndex() != 0:
            self.yaml_metablock["tablenos-caption-separator"] = self.ui.TablenosCaptionSepCombobox.currentText()
        else:
            self.yaml_metablock["tablenos-caption-separator"] = ""

        self.yaml_metablock["eqnos-cleveref"] = self.ui.EqnosCleverCheckbox.isChecked()
        self.yaml_metablock["eqnos-number-by-section"] = self.ui.EqnosNumberBySecCheckbox.isChecked()
        self.yaml_metablock["eqnos-plus-name"] = self.ui.EqnosPlusNameLineEdit.text()
        self.yaml_metablock["eqnos-star-name"] = self.ui.EqnosStarNameLineEdit.text()
        self.yaml_metablock["eqnos-eqref"] = self.ui.EqnosEqrefCheckbox.isChecked()

    # End of writing settings
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
        """Forms a pandoc command based on the info from gui"""

        command = ""

        def add_arg(arg: str, option=True) -> None:
            nonlocal command
            prefix = ""
            if option:
                prefix += "--"

            command += f"{prefix}{arg} "

        add_arg("pandoc", option=False)

        # Add pandoc args
        for key, value in self.pandoc_args.items():
            if value:
                add_arg(key)

        # Add pandoc filters
        for key, value in self.pandoc_filters.items():
            if value:
                add_arg(f"filter={key}")

        # Add pandoc kargs
        for key, value in self.pandoc_kargs.items():
            if not (type(value) == str and value == ""):
                add_arg(f"{key}={value}")

        # Add files to be rendered
        files_to_render = list(self.ProjectManager.get_setting_value("Files to render"))
        for file in files_to_render:
            add_arg(file, option=False)

        # Remove trailing space
        command = command[:-1]

        return command

    def accept(self) -> None:
        """Update project settings in Project manager and save them if the dialog is accepted"""

        self.update_window_settings()
        self.update_meta_information_settings()
        self.update_render_settings()
        self.update_pandoc_settings()
        self.update_xnos_settings()

        self.ProjectManager.set_setting_value("YAML_metablock", self.yaml_metablock)
        self.ProjectManager.set_setting_value("Pandoc_filters", self.pandoc_filters)
        self.ProjectManager.set_setting_value("Pandoc_kargs", self.pandoc_kargs)
        self.ProjectManager.set_setting_value("Pandoc_args", self.pandoc_args)

        self.ProjectManager.save_project_data()

        super().accept()

    def reject(self) -> None:
        self.update_window_settings()
        super().reject()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Save window related settings before closing"""
        self.update_window_settings()

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
