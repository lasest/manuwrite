from PyQt5.QtCore import QObject, QSettings, QSize, QPoint, QStandardPaths


class SettingsManager(QObject):

    def __init__(self, parent):
        super().__init__(parent)

        # Default settings. Type "None" means that Settings manager shouldn't try to perform type converstion
        self.settings: QSettings = QSettings("Manuwrite", "Manuwrite Editor")
        self.defaults = {
            "MainWindow/size/value": QSize(640, 480),
            "MainWindow/size/type": "None",

            "MainWindow/pos/value": QPoint(100, 100),
            "MainWindow/pos/type": "None",

            "MainWindow/splitter_sizes/value": [150, 294, 196],
            "MainWindow/splitter_sizes/type": "map/int",

            "MainWindow/project_widget_width/value": 150,
            "MainWindow/project_widget_width/type": "int",

            "MainWindow/preview_width/value": 196,
            "MainWindow/preview_width/type": "int",

            "MainWindow/last_project/value": "",
            "MainWindow/last_project/type": "str",

            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Application/Project folder/type": "str",

            "Editor/Font name/value": "Hack",
            "Editor/Font name/type": "str",

            "Editor/Font size/value": 14,
            "Editor/Font size/type": "int",

            "Projects/Project types/value": ["Article", "Book", "Notes", "Other"],
            "Projects/Project types/type": "list"
        }

        # Maps datatype names read from config to functions
        self.datatypes = {
            "int": int,
            "str": str,
            "None": None,
            "list": list,
            "map/int": "mapping"
        }

        # Set settings to defaults if some keys are missing
        for key, value in self.defaults.items():
            if key not in self.settings.allKeys():
                self.set_setting(key, value)

    def get_setting_value(self, setting: str):
        """Returns the value of the specified setting, performing the necessary type conversion"""

        # Check for misspelled keys
        if setting + "/value" not in self.defaults:
            raise KeyError

        value = self.settings.value(setting + "/value", self.defaults[setting + "/value"])
        type = self.settings.value(setting + "/type", "None")
        converter = self.datatypes[type]

        # Convert to data type if it is given
        if type != "None":
            if type.startswith("map"):
                converter = type[type.find("/") + 1:]
                converter = self.datatypes[converter]
                value = map(converter, value)
            else:
                value = converter(value)

        return value

    def set_setting_value(self, setting: str, value) -> None:
        """Sets the value of a setting"""

        setting = setting + "/value"
        if setting not in self.defaults:
            raise KeyError

        self.settings.setValue(setting, value)
