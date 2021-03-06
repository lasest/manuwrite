import copy
import yaml

from PyQt5.QtWidgets import QDialog, QListWidgetItem, QListWidget, QMessageBox, QFileDialog, QAbstractButton
from PyQt5.QtCore import QDate, QDirIterator, QDir, Qt, pyqtSlot, QFile, QIODevice
from PyQt5.QtGui import QCloseEvent

from ui_forms.ui_project_settings_dialog import Ui_ProjectSettingsDialog
from components.project_manager import ProjectManager
from components.settings_manager import SettingsManager
import common


class ProjectSettingsDialog(QDialog):

    def __init__(self, parent, project_manager: ProjectManager, settings_manager: SettingsManager):

        super().__init__(parent=parent)
        self.ui = Ui_ProjectSettingsDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.ProjectManager = project_manager
        self.SettingsManager = settings_manager

        self.pandoc_filters = self.ProjectManager.get_setting_value("Pandoc_filters")
        self.yaml_metablock = self.ProjectManager.get_setting_value("YAML_metablock")
        self.pandoc_args = self.ProjectManager.get_setting_value("Pandoc_args")
        self.pandoc_kwargs = self.ProjectManager.get_setting_value("Pandoc_kwargs")

        # Read settings
        self.read_window_settings()
        self.read_meta_information_settings()
        self.read_render_settings()
        self.read_pandoc_settings()
        self.read_xnos_settings()

        # Prepare ui elements
        self.set_toolbuttons_actions()
        self.load_icons()

        self.on_NumberSectionsCheckbox_stateChanged(self.ui.NumberSectionsCheckbox.isChecked())
        self.on_PandocXnosCheckbox_stateChanged(self.ui.PandocXnosCheckbox.isChecked())

    def load_icons(self) -> None:
        icon_type = self.SettingsManager.get_setting_value("Colors/Icons")
        prefix = f"icons_{icon_type.lower()}"

        common.load_icon("go-up-skip.svg", prefix, self.ui.actionMoveToTheTop)
        common.load_icon("go-up.svg", prefix, self.ui.actionMoveUp)
        common.load_icon("go-previous.svg", prefix, self.ui.actionMoveLeft)
        common.load_icon("go-next.svg", prefix, self.ui.actionMoveRight)
        common.load_icon("go-down.svg", prefix, self.ui.actionMoveDown)
        common.load_icon("go-down-skip.svg", prefix, self.ui.actionMoveToTheBottom)

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

        number_offset = self.pandoc_kwargs["number-offset"]
        if number_offset:
            self.ui.NumberOffsetSpinBox.setValue(int(number_offset))
        else:
            self.ui.NumberOffsetSpinBox.setValue(0)

        self.ui.NumberSectionsCheckbox.setChecked(self.pandoc_args["number-sections"])
        self.ui.StandaloneCheckbox.setChecked(self.pandoc_args["standalone"])

        self.ui.ManualBibLineEdit.setText(self.yaml_metablock["bibliography"])

    def read_xnos_settings(self) -> None:
        self.ui.XnosCapitaliseCheckbox.setChecked(self.yaml_metablock["xnos-capitalise"])
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
        self.ui.TitleLineEdit.setText(self.yaml_metablock["title"])

        date = list(map(int, self.ProjectManager.get_setting_value("Date created")))
        date = QDate(date[0], date[1], date[2])
        self.ui.dateEdit.setDate(date)

        self.ui.AuthorsLineEdit.setText(self.yaml_metablock["author"])
        self.ui.ProjectTypeValueLabel.setText(self.ProjectManager.get_setting_value("Project type"))
        self.ui.DescriptionPlainTextEdit.setPlainText(self.yaml_metablock["abstract"])
        self.ui.ManualYamlPlainTextEdit.setPlainText(self.ProjectManager.get_setting_value("Additional meta " +
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
                filepath = filepath[len(self.ProjectManager.root_path) + 1:]
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

        # Populate CssStyleCombobox
        self.ui.CssStyleCombobox.addItem("None")
        styles = self.SettingsManager.get_setting_value("Render/Css_styles")
        for identifier, style_info in styles.items():
            self.ui.CssStyleCombobox.addItem(style_info["name"], userData=identifier)

        current_style_identifier = self.ProjectManager.get_setting_value("Css_style")
        index = self.ui.CssStyleCombobox.findData(current_style_identifier)
        if index == -1:
            index = 0

        self.ui.CssStyleCombobox.setCurrentIndex(index)

        # Populate CslStyleCombobox
        self.ui.CslStyleCombobox.addItem("Default")
        styles = self.SettingsManager.get_setting_value("Render/Csl_styles")
        for identifier, style_info in styles.items():
            self.ui.CslStyleCombobox.addItem(style_info["name"], userData=identifier)

        current_csl_identifier = self.ProjectManager.get_setting_value("Csl_style")
        index = self.ui.CslStyleCombobox.findData(current_csl_identifier)
        if index == -1:
            index = 0

        self.ui.CslStyleCombobox.setCurrentIndex(index)

        # Populate formats combobox
        formats = self.SettingsManager.get_setting_value("Render/Formats")
        for identifier, format_info in formats.items():
            self.ui.OutputFormatCombobox.addItem(format_info["name"], userData=identifier)

        current_output_format_identifier = self.ProjectManager.get_setting_value("Render to")
        index = self.ui.OutputFormatCombobox.findData(current_output_format_identifier)
        self.ui.OutputFormatCombobox.setCurrentIndex(index)

        # Populate PandocCommandLineEdit
        self.ui.PandocCommandTextBrowser.setText(self.ProjectManager.get_setting_value("Pandoc_command_full"))
        self.ui.ManualPandocArgsLineEdit.setText(self.ProjectManager.get_setting_value("Pandoc_command_manual"))

    # Writing settings
    def update_window_settings(self) -> None:
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/size", self.size())
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/pos", self.pos())
        tab_index = self.ui.MainTabWidget.currentIndex()
        self.SettingsManager.set_setting_value("ProjectSettingsDialog/current tab index", tab_index)

    def update_meta_information_settings(self) -> None:
        """Update meta information settings in Project manager with info from gui"""

        self.yaml_metablock["title"] = self.ui.TitleLineEdit.text()

        date = self.ui.dateEdit.date()
        self.ProjectManager.set_setting_value("Date created", [date.year(), date.month(), date.day()])
        self.yaml_metablock["author"] = self.ui.AuthorsLineEdit.text()
        self.yaml_metablock["abstract"] = self.ui.DescriptionPlainTextEdit.toPlainText()
        self.ProjectManager.set_setting_value("Additional meta information", self.ui.ManualYamlPlainTextEdit.toPlainText())
        self.ProjectManager.set_setting_value("Include_metainfo", self.ui.MetaInfoCheckbox.isChecked())

    def update_render_settings(self) -> None:
        """Update render information settings in Project manager with info from gui"""
        # Update files to render
        files_to_render = []
        for i in range(self.ui.FilesToRenderListWidget.count()):
            if not self.ui.FilesToRenderListWidget.item(i).text().endswith("(File not found!)"):
                files_to_render.append(self.ui.FilesToRenderListWidget.item(i).text())
        self.ProjectManager.set_setting_value("Files to render", files_to_render)

        # Update css style info
        if self.ui.CssStyleCombobox.currentIndex() == 0:
            self.ProjectManager.set_setting_value("Css_style", "")
            self.pandoc_kwargs["css"] = ""
        else:
            style_identifier = self.ui.CssStyleCombobox.currentData()
            self.ProjectManager.set_setting_value("Css_style", style_identifier)

            # Copy css style to project folder
            styles = self.SettingsManager.get_setting_value("Render/Css_styles")
            old_path = styles[style_identifier]["path"]
            new_path = self.ProjectManager.get_setting_value("Absolute path") + "/style.css"
            QFile.copy(old_path, new_path)
            self.pandoc_kwargs["css"] = "style.css"

        # Update csl style info
        if self.ui.CslStyleCombobox.currentIndex() == 0:
            self.ProjectManager.set_setting_value("Csl_style", "")
            self.pandoc_kwargs["csl"] = ""
        else:
            style_identifier = self.ui.CslStyleCombobox.currentData()
            self.ProjectManager.set_setting_value("Csl_style", style_identifier)

            # Copy csl style to project folder
            styles = self.SettingsManager.get_setting_value("Render/Csl_styles")
            old_path = styles[style_identifier]["path"]
            new_path = self.ProjectManager.get_setting_value("Absolute path") + "/csl_style.csl"
            QFile.copy(old_path, new_path)
            self.pandoc_kwargs["csl"] = "csl_style.csl"

        # Update output format and filename
        format_identifier = self.ui.OutputFormatCombobox.currentData()
        self.ProjectManager.set_setting_value("Render to", format_identifier)
        formats = self.SettingsManager.get_setting_value("Render/Formats")
        current_format = formats[format_identifier]

        self.pandoc_kwargs["to"] = current_format["pandoc_option"]
        self.pandoc_kwargs["output"] = f"output.{current_format['file_extension']}"
        output_path = self.ProjectManager.get_setting_value("Absolute path") + "/" + self.pandoc_kwargs["output"]
        self.ProjectManager.set_setting_value("Output_path", output_path)

    def update_pandoc_settings(self) -> None:
        self.pandoc_filters["pandoc-xnos"] = self.ui.PandocXnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-secnos"] = self.ui.PandocSecnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-fignos"] = self.ui.PandocFignosCheckbox.isChecked()
        self.pandoc_filters["pandoc-tablenos"] = self.ui.PandocTablenosCheckbox.isChecked()
        self.pandoc_filters["pandoc-eqnos"] = self.ui.PandocEqnosCheckbox.isChecked()
        self.pandoc_filters["pandoc-citeproc"] = self.ui.PandocCiteProcCheckbox.isChecked()
        self.pandoc_filters["pandoc-manubot-cite"] = self.ui.ManubotCiteCheckbox.isChecked()

        number_offset = self.ui.NumberOffsetSpinBox.value()
        if number_offset:
            self.pandoc_kwargs["number-offset"] = number_offset
            self.yaml_metablock["xnos-number-offset"] = number_offset
        else:
            self.pandoc_kwargs["number-offset"] = ""
            self.yaml_metablock["xnos-number-offset"] = ""

        self.pandoc_args["number-sections"] = self.ui.NumberSectionsCheckbox.isChecked()
        self.pandoc_args["standalone"] = self.ui.StandaloneCheckbox.isChecked()

        self.yaml_metablock["bibliography"] = self.ui.ManualBibLineEdit.text()

    def update_xnos_settings(self) -> None:
        self.yaml_metablock["xnos-capitalise"] = self.ui.XnosCapitaliseCheckbox.isChecked()
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

        # Add pandoc kwargs
        for key, value in self.pandoc_kwargs.items():
            if not (type(value) == str and value == ""):
                add_arg(f"{key}={value}")

        # Add manual arguments
        manual_part = self.ProjectManager.get_setting_value("Pandoc_command_manual")
        if manual_part:
            command += " " + manual_part.strip() + " "

        # Add files to be rendered
        files_to_render = list(self.ProjectManager.get_setting_value("Files to render"))
        for file in files_to_render:
            add_arg(file, option=False)

        # Remove trailing space
        command = command[:-1]

        return command

    def generate_yaml_metablock(self) -> str:
        """Generates a yaml string from self.yaml_metablock dictionary"""

        # Remove entries w/o values (i.e. empty strings)
        yaml_metablock = copy.deepcopy(self.yaml_metablock)
        keys_to_remove = []
        for key in yaml_metablock:
            if type(yaml_metablock[key]) == str and yaml_metablock[key] == "":
                keys_to_remove.append(key)

        for key in keys_to_remove:
            yaml_metablock.pop(key)

        # Generate the yaml output
        yaml_text = yaml.dump(yaml_metablock)

        return yaml_text

    def apply_settings(self) -> None:
        """Updates settings and writes them to file"""
        self.update_meta_information_settings()
        self.update_render_settings()
        self.update_pandoc_settings()
        self.update_xnos_settings()

        # Save YAML metablock to file
        yaml_text = self.generate_yaml_metablock()

        filepath = self.ProjectManager.get_setting_value("Absolute path") + "/yaml_metablock.yaml"
        try:
            file_handle = QFile(filepath)
            if file_handle.open(QIODevice.WriteOnly | QIODevice.Text):
                line = "-" * 3 + "\n"
                file_handle.write(line.encode())
                file_handle.write(yaml_text.encode())

                manual_yaml = "\n" + self.ui.ManualYamlPlainTextEdit.toPlainText()
                file_handle.write(manual_yaml.encode())

                line = "\n" + "." * 3
                file_handle.write(line.encode())
                file_handle.close()

                # Add argument to pandoc command
                self.pandoc_kwargs["metadata-file"] = "yaml_metablock.yaml"

        except Exception as e:
            QMessageBox.critical(self, "Error saving settings",
                                 f"Some error occured when trying to save the settings. ({str(e)})")
            return
        finally:
            file_handle.close()

        # Set certain settings
        self.ProjectManager.set_setting_value("YAML_metablock", self.yaml_metablock)
        self.ProjectManager.set_setting_value("Pandoc_filters", self.pandoc_filters)
        self.ProjectManager.set_setting_value("Pandoc_kwargs", self.pandoc_kwargs)
        self.ProjectManager.set_setting_value("Pandoc_args", self.pandoc_args)

        # Update pandoc command
        # Do not change order, pandoc_command_manual is should be saved before generating full command
        self.ProjectManager.set_setting_value("Pandoc_command_manual", self.ui.ManualPandocArgsLineEdit.text())
        full_pandoc_command = self.get_pandoc_command()
        self.ProjectManager.set_setting_value("Pandoc_command_full", full_pandoc_command)

        # Save pandoc command to build.sh
        filepath = self.ProjectManager.get_setting_value("Absolute path") + "/build.sh"
        try:
            file_handle = QFile(filepath)
            if file_handle.open(QIODevice.WriteOnly | QIODevice.Text):
                file_handle.write(full_pandoc_command.encode())
        except Exception as e:
            QMessageBox.critical(self, "Error saving settings",
                                 f"Some error occured when trying to save the settings. ({str(e)})")
            return

        finally:
            file_handle.close()

        # Write settings to file
        self.ProjectManager.save_project_data()

    def accept(self) -> None:
        """Applies settings when dialog is accepted"""
        # Update settings
        self.update_window_settings()
        self.apply_settings()

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

    # Ui consistency slots - enable/disable some elements of the form depending on the state of other elements
    @pyqtSlot(int)
    def on_NumberSectionsCheckbox_stateChanged(self, state: int) -> None:
        self.ui.NumberOffsetSpinBox.setEnabled(state)
        if not state:
            self.ui.NumberOffsetSpinBox.setValue(0)

    @pyqtSlot(int)
    def on_PandocXnosCheckbox_stateChanged(self, state: int) -> None:
        self.ui.PandocXnosFrame.setEnabled(not state)

        if state:
            self.ui.PandocSecnosCheckbox.setChecked(False)
            self.ui.PandocFignosCheckbox.setChecked(False)
            self.ui.PandocTablenosCheckbox.setChecked(False)
            self.ui.PandocEqnosCheckbox.setChecked(False)

    @pyqtSlot(int)
    def on_PandocCiteProcCheckbox_stateChanged(self, state: int) -> None:
        self.ui.PandocCiteProcFrame.setEnabled(state)

        if not state:
            self.ui.ManualBibLineEdit.setText("")
            self.ui.ManubotCiteCheckbox.setChecked(False)

    @pyqtSlot()
    def on_ManualBibToolButton_clicked(self) -> None:
        """Choose bibliography file"""
        filepath = QFileDialog.getOpenFileName(self, "Choose bibliography file",
                                               self.ProjectManager.get_setting_value("Absolute path"),
                                               filter="BibLaTeX (*.bib);;BibTeX (*.bibtex);;Copac (*.copac);;" +
                                                      "CSL JSON (*.json);;CSL YAML (*.yaml);;EndNote (*.enl);;" +
                                                      "EndNote XML (*.xml);;ISI (*.wos);;MEDLINE (*.medline);;" +
                                                      "MODS (*.mods);;NBIB (*.nbib);;RIS (*.ris);;All files (*.*)")
        if filepath[0]:
            self.ui.ManualBibLineEdit.setText(filepath[0])

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button: QAbstractButton) -> None:
        """Applies settings when Apply button is clicked"""
        standard_button = self.ui.buttonBox.standardButton(button)
        if standard_button == self.ui.buttonBox.Apply:
            self.apply_settings()

            # Update pandoc command output
            self.ui.PandocCommandTextBrowser.setText(self.ProjectManager.get_setting_value("Pandoc_command_full"))
