from PyQt5.QtCore import QObject, QSettings, QSize, QPoint, QStandardPaths


class SettingsManager(QObject):

    def __init__(self, parent):
        super().__init__(parent)

        self.settings: QSettings = QSettings("Manuwrite", "Manuwrite Editor")
        self.defaults = {
            "MainWindow/size/value": QSize(640, 480),
            "MainWindow/pos/value": QPoint(100, 100),
            "MainWindow/splitter_sizes/value": [150, 294, 196],
            "MainWindow/last_project/value": "",
            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        }

        for key, value in self.defaults.items():
            if key not in self.settings.allKeys():
                self.set_setting(key, value)

    def get_setting_value(self, setting: str, force_types=None):
        setting = setting + "/value"
        if setting not in self.defaults:
            raise KeyError

        return self.settings.value(setting, self.defaults[setting])

    def set_setting_value(self, setting: str, value):
        setting = setting + "/value"
        if setting not in self.defaults:
            raise KeyError

        self.settings.setValue(setting, value)

    def set_setting(self, setting: str, value):
        self.settings.setValue(setting, value)

    def get_setting(self, setting: str):
        return self.settings.value(setting)
