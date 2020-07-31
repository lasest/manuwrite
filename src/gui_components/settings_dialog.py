from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import Qt

from forms.ui_settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog):

    def __init__(self, SettingsManager):
        super().__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.SettingsManager = SettingsManager

        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.setColumnCount(2)

        self.SettingsManager.settings.beginGroup("Application")
        items = self.SettingsManager.settings.allKeys()
        self.SettingsManager.settings.endGroup()

        print(self.SettingsManager.settings.allKeys())

        for i in range(len(items)):
            print("Iterating at index ", i)
            print(items[i])
            item = items[i]
            key = "Application/" + item[:item.find("/")]
            value = self.SettingsManager.get_setting_value(key)
            print("key:", key)
            print(value)

            table_item = QTableWidgetItem(key)
            table_item.setFlags(table_item.flags() ^ Qt.ItemIsEditable)
            self.ui.tableWidget.setItem(i, 0, table_item)

            table_item = QTableWidgetItem(value)
            self.ui.tableWidget.setItem(i, 1, table_item)
