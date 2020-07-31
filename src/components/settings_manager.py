from PyQt5.QtCore import QObject, QSettings, QSize, QPoint, QStandardPaths


class SettingsManager(QObject):

    def __init__(self, parent):
        super().__init__(parent)

        self.settings: QSettings = QSettings("Manuwrite", "Manuwrite Editor")
        self.defaults = {
            "MainWindow/size/value": QSize(640, 480),
            "MainWindow/pos/value": QPoint(100, 100),
            "MainWindow/splitter_sizes/value": [150, 294, 196],
            "MainWindow/splitter_sizes/type": "map/int",
            "MainWindow/project_widget_width/value": 150,
            "MainWindow/project_widget_width/type": "int",
            "MainWindow/preview_width/value": 196,
            "MainWindow/preview_width/type": "int",
            "MainWindow/last_project/value": "",
            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Editor/Font name/value": "Hack",
            "Editor/Font size/value": 14,
            "Editor/Font size/type": "int",
            "Projects/Project types/value": ["Article", "Book", "Notes", "Other"],
            "Projects/Project types/type": "list"
        }

        self.datatypes = {
            "int": int,
            "str": str,
            "None": None,
            "list": list,
            "map/int": "map/int"
        }

        for key, value in self.defaults.items():
            if key not in self.settings.allKeys():
                self.set_setting(key, value)

    def get_setting_value(self, setting: str, force_types=None):

        if setting + "/value" not in self.defaults:
            raise KeyError

        value = self.settings.value(setting + "/value", self.defaults[setting + "/value"])
        type = self.datatypes[self.settings.value(setting + "/type", "None")]

        if type is not None:
            if type.startswith("map"):
                mapping_type = type[type.find("/") + 1:]
                mapping_type = self.datatypes[mapping_type]
                value = map(mapping_type, value)
            else:
                value = type(value)

        return value

    def set_setting_value(self, setting: str, value):
        setting = setting + "/value"
        if setting not in self.defaults:
            raise KeyError

        self.settings.setValue(setting, value)

    def set_setting(self, setting: str, value):
        self.settings.setValue(setting, value)

    def get_setting(self, setting: str):
        return self.settings.value(setting)
