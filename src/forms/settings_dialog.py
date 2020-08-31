from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QFont, QColor

from components.settings_manager import SettingsManager
from ui_forms.ui_settings_dialog import Ui_SettingsDialog
from widgets.color_button import ColorButton


class SettingsDialog(QDialog):

    def __init__(self, settings_manager: SettingsManager, parent):
        super().__init__(parent=parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setPalette(parent.palette())

        # Set attributes
        self.SettingsManager = settings_manager
        self.is_populating_ColorSchemaCombobox = False

        # Prepare ui elements
        self.read_window_settings()
        self.read_general_settings()
        self.read_editor_settings()
        self.read_render_settings()
        self.read_color_settings()

    def load_editor_color_schema(self) -> None:
        """Populates ColorTable on Editor tab with information about the color schema, currently selected in the
        ColorSchemaComboBox"""

        def load_section(section: str, section_title: str, schema: dict):
            """Appends all key-value pairs of the dictionary "section" (from dictionary "schema") to the table. Adds a
            section header before the items"""
            offset = self.ui.ColorsTable.rowCount()
            items = list(schema[section].items())

            self.ui.ColorsTable.setRowCount(offset + len(items) + 1)

            self.ui.ColorsTable.setSpan(offset, 0, 1, 2)
            item = QTableWidgetItem(section_title)
            self.ui.ColorsTable.setItem(offset, 0, item)

            for i in range(0, len(items)):
                item = items[i]

                table_item = QTableWidgetItem(item[0])
                self.ui.ColorsTable.setItem(offset + i + 1, 0, table_item)

                table_item = QTableWidgetItem(item[1]['name'])
                table_item.setFlags(table_item.flags() ^ Qt.ItemIsEditable)
                self.ui.ColorsTable.setItem(offset + i + 1, 1, table_item)

                button = ColorButton(self, QColor(item[1]["color"]))
                button.setMaximumWidth(50)
                self.ui.ColorsTable.setCellWidget(offset + i + 1, 2, button)

        allow_editing = True
        self.ui.ColorsTable.clear()
        self.ui.ColorsTable.setRowCount(0)

        schema_name = self.ui.ColorSchemaComboBox.currentText()
        if schema_name == "System colors":
            allow_editing = False

        schema = self.get_selected_color_schema()

        if allow_editing:
            self.ui.ColorsTable.setEnabled(True)
        else:
            self.ui.ColorsTable.setEnabled(False)

        load_section("Application_colors", "Application colors", schema)
        load_section("Editor_colors", "Editor colors", schema)
        load_section("Markdown_colors", "Markdown colors", schema)

    def read_window_settings(self) -> None:
        """Reads settings regarding widnow size and position"""
        self.resize(self.SettingsManager.get_setting_value("SettingsDialog/size"))
        self.move(self.SettingsManager.get_setting_value("SettingsDialog/pos"))
        tab_index = self.SettingsManager.get_setting_value("SettingsDialog/current tab index")
        self.ui.MainTabWidget.setCurrentIndex(tab_index)

    def read_general_settings(self) -> None:
        """Reads settings for the General settings tab"""
        pass

    def read_editor_settings(self) -> None:
        """Reads settings for the Editor settings tab"""
        self.ui.FontComboBox.setCurrentFont(QFont(self.SettingsManager.get_setting_value("Editor/Font name")))
        self.ui.FontSizeSpinBox.setValue(self.SettingsManager.get_setting_value("Editor/Font size"))

        width = self.SettingsManager.get_setting_value("Editor/Default image width")
        height = self.SettingsManager.get_setting_value("Editor/Default image height")
        self.ui.DefImageSizeWidthLineEdit.setText(str(width))
        self.ui.DefImageSizeHeightLineEdit.setText(str(height))

        width = self.SettingsManager.get_setting_value("Editor/Image tooltip width")
        height = self.SettingsManager.get_setting_value("Editor/Image tooltip height")
        self.ui.ImageToolTipWidthLineEdit.setText(str(width))
        self.ui.ImageToolTipHeightLineEdit.setText(str(height))

        self.ui.ShowImageTooltipsCheckBox.setChecked(self.SettingsManager.get_setting_value("Editor/Show image tooltips"))
        self.ui.ShowCitationTooltipsCheckBox.setChecked(self.SettingsManager.get_setting_value("Editor/Show citation tooltips"))

        if not self.ui.ShowImageTooltipsCheckBox.checkState():
            self.ui.ImageToolTipWidthLineEdit.setEnabled(False)
            self.ui.ImageToolTipHeightLineEdit.setEnabled(False)

    def read_color_settings(self) -> None:
        # ColorTable is populated automatically when ColorSchemaCombobox value changes
        # Adjust color table
        self.ui.ColorsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.ColorsTable.setColumnHidden(0, True)

        # Populate ColorSchemaCombobox
        self.populate_ColorSchemaCombobox()

        # Populate IconsCombobox
        self.ui.IconsCombobox.addItems(["Dark", "Light"])
        icon_theme = self.SettingsManager.get_setting_value("Colors/Icons")
        index = self.ui.IconsCombobox.findText(icon_theme)
        self.ui.IconsCombobox.setCurrentIndex(index)

    def populate_ColorSchemaCombobox(self):
        """Populates ColorSchemaCombobox with color schemas"""
        self.is_populating_ColorSchemaCombobox = True
        self.ui.ColorSchemaComboBox.clear()

        self.ui.ColorSchemaComboBox.addItem("System colors")
        schemas = self.SettingsManager.get_setting_value("Colors/Color_schemas")
        for identifier, schema_info in schemas.items():
            self.ui.ColorSchemaComboBox.addItem(schema_info["name"])

        index = self.ui.ColorSchemaComboBox.findText(
            self.SettingsManager.get_setting_value("Editor/Current color schema"))
        if index == -1:
            index = 0

        self.ui.ColorSchemaComboBox.setCurrentIndex(index)
        self.is_populating_ColorSchemaCombobox = False
        self.on_ColorSchemaComboBox_currentIndexChanged(index)

    def get_selected_color_schema(self) -> dict:
        """Returns the color schema currently selected in ColorSchemaCombobox"""
        schemas = self.SettingsManager.get_setting_value("Colors/Color_schemas")
        schema_identifier = self.ui.ColorSchemaComboBox.currentText()

        # TODO: change to index based detection rather than text (can be translated)
        if schema_identifier == "System colors":
            schema = self.SettingsManager.get_default_color_schema()
        elif schema_identifier in schemas:
            schema = self.SettingsManager.get_color_schema(schema_identifier)
        else:
            schema = self.SettingsManager.get_default_color_schema()
            self.ui.ColorSchemaComboBox.setCurrentIndex(0)
            QMessageBox.warning(self, "Error", f'Color schema "{schema_identifier}" was not found!')

        return schema

    def read_render_settings(self) -> None:
        """Read settings for the Render settings tab"""
        self.ui.AllowAutoRenderCheckbox.setChecked(self.SettingsManager.get_setting_value("Render/Autorender"))
        self.ui.AutorenderDelayLineEdit.setText(str(self.SettingsManager.get_setting_value("Render/Autorender delay")))

    def update_window_settings(self) -> None:
        """Update settings regarding window size and position (autosaved)"""
        self.SettingsManager.set_setting_value("SettingsDialog/size", self.size())
        self.SettingsManager.set_setting_value("SettingsDialog/pos", self.pos())
        tab_index = self.ui.MainTabWidget.currentIndex()
        self.SettingsManager.set_setting_value("SettingsDialog/current tab index", tab_index)

    def update_general_settings(self) -> None:
        """Save settings for the General settings tab"""
        pass

    def update_editor_settings(self) -> None:
        """Save settings for the Editor settings tab"""
        self.SettingsManager.set_setting_value("Editor/Font name", self.ui.FontComboBox.currentText())
        self.SettingsManager.set_setting_value("Editor/Font size", self.ui.FontSizeSpinBox.value())

        width = self.ui.DefImageSizeWidthLineEdit.text()
        height = self.ui.DefImageSizeHeightLineEdit.text()
        self.SettingsManager.set_setting_value("Editor/Default image width", width)
        self.SettingsManager.set_setting_value("Editor/Default image height", height)

        width = self.ui.ImageToolTipWidthLineEdit.text()
        height = self.ui.ImageToolTipHeightLineEdit.text()
        self.SettingsManager.set_setting_value("Editor/Image tooltip width", width)
        self.SettingsManager.set_setting_value("Editor/Image tooltip height", height)

        self.SettingsManager.set_setting_value("Editor/Show citation tooltips", self.ui.ShowCitationTooltipsCheckBox.checkState())
        self.SettingsManager.set_setting_value("Editor/Show image tooltips", self.ui.ShowImageTooltipsCheckBox.checkState())

    def update_render_settings(self) -> None:
        """Save settings for the Render settings tab"""
        self.SettingsManager.set_setting_value("Render/Autorender", self.ui.AllowAutoRenderCheckbox.checkState())
        self.SettingsManager.set_setting_value("Render/Autorender delay", self.ui.AutorenderDelayLineEdit.text())

    def update_color_settings(self) -> None:
        """Saves settings from Colors tab"""
        # Save schema name
        self.SettingsManager.set_setting_value("Editor/Current color schema", self.ui.ColorSchemaComboBox.currentText())

        # Save colors from ColorsTable
        if self.ui.ColorSchemaComboBox.currentText() != "System colors":
            color_schema_name = self.ui.ColorSchemaComboBox.currentText()
            color_schema = self.SettingsManager.get_color_schema(color_schema_name)

            for i in range(self.ui.ColorsTable.rowCount()):

                color_name = self.ui.ColorsTable.item(i, 0).text()
                if color_name in color_schema["Application_colors"]:
                    color_schema["Application_colors"][color_name]["color"] = self.ui.ColorsTable.cellWidget(i, 2).color.name()
                elif color_name in color_schema["Editor_colors"]:
                    color_schema["Editor_colors"][color_name]["color"] = self.ui.ColorsTable.cellWidget(i, 2).color.name()
                elif color_name in color_schema["Markdown_colors"]:
                    color_schema["Markdown_colors"][color_name]["color"] = self.ui.ColorsTable.cellWidget(i, 2).color.name()

            self.SettingsManager.save_color_schema(color_schema)

        # Save Icons theme
        icons_theme = self.ui.IconsCombobox.currentText()
        self.SettingsManager.set_setting_value("Colors/Icons", icons_theme)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Saves window settings when the window closes"""
        self.update_window_settings()

    def reject(self) -> None:
        """Saves window settings when the window closes"""
        self.update_window_settings()
        super().reject()

    def accept(self) -> None:
        """Saves all settings to permanent storage"""

        self.update_window_settings()
        self.update_general_settings()
        self.update_editor_settings()
        self.update_render_settings()
        self.update_color_settings()

        super().accept()

    @pyqtSlot(int)
    def on_ShowImageTooltipsCheckBox_stateChanged(self, state: int) -> None:
        """Disables corresponding gui controls if Image tooltips are disabled"""
        if state:
            self.ui.ImageToolTipWidthLineEdit.setEnabled(True)
            self.ui.ImageToolTipHeightLineEdit.setEnabled(True)
        else:
            self.ui.ImageToolTipWidthLineEdit.setEnabled(False)
            self.ui.ImageToolTipHeightLineEdit.setEnabled(False)

    @pyqtSlot(int)
    def on_ColorSchemaComboBox_currentIndexChanged(self, index: int) -> None:
        """Loads color schema to ColorTable when the value of ColorSchemaComboBox changes"""
        if not self.is_populating_ColorSchemaCombobox:
            self.ui.ColorsTable.clear()
            self.load_editor_color_schema()

    @pyqtSlot()
    def on_NewColorSchemaButton_clicked(self) -> None:
        """Creates a new color schema based on the currently selected one"""

        # Get name for new schema
        result = QInputDialog.getText(self, "Create color schema - Manuwrite", "New schema name:")
        # Check if user accepted
        if not result[1]:
            return

        schema_name = result[0]
        # Check if schema name is valid
        if schema_name == "":
            QMessageBox.warning(self, "Error", "Schema name cannot be empty.")
            return

        # Create schema directory and file based on the currently selected schema colors
        self.SettingsManager.import_color_schema_from_dict(schema_name, self.get_selected_color_schema())

        # Repopulate ColorSchemasCombobox
        self.populate_ColorSchemaCombobox()

        # Select newly created schema
        index = self.ui.ColorSchemaComboBox.findText(schema_name)
        self.ui.ColorSchemaComboBox.setCurrentIndex(index)

    @pyqtSlot()
    def on_DeleteColorSchemaButton_clicked(self) -> None:
        """Deletes color schema currently selected in ColorSchemaCombobox"""
        # TODO: disable delete button on item change instead
        # If system colors are currently selected as a color scheme, do nothing
        if self.ui.ColorSchemaComboBox.currentIndex() == 0:
            return

        # Remove scheme
        scheme_identifier = self.ui.ColorSchemaComboBox.currentText()
        self.SettingsManager.delete_color_scheme(scheme_identifier)

        # Update ColorSchemeCombobox
        self.populate_ColorSchemaCombobox()

    @pyqtSlot()
    def on_ImportColorSchemaButton_clicked(self) -> None:
        """Imports a new color scheme from file"""
        # Get filepath
        filepath = QFileDialog.getOpenFileName(self, "Import color scheme")[0]
        if not filepath:
            return

        # Import from file
        self.SettingsManager.import_color_schema_from_file(filepath)

        # Repopulate ColorSchemasCombobox
        self.populate_ColorSchemaCombobox()

    @pyqtSlot()
    def on_ExportColorSchemaButton_clicked(self) -> None:
        """Exports a color theme to a file"""
        # Do not export, if default scheme is selected (there is no file to copy)
        if self.ui.ColorSchemaComboBox.currentIndex() == 0:
            return

        # Get filepath
        filepath = QFileDialog.getSaveFileName(self, "Export color scheme")[0]
        if not filepath:
            return

        # Export to file
        selected_scheme_identifier = self.ui.ColorSchemaComboBox.currentText()
        self.SettingsManager.export_color_scheme_to_file(selected_scheme_identifier, filepath)
