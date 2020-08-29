import toml

from PyQt5.QtCore import QObject, QSettings, QStandardPaths, QDir, QDirIterator
from PyQt5.QtGui import QPalette

import defaults


class SettingsManager(QObject):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Maps datatype names read from config to functions
        self.datatypes = {
            "int": int,
            "str": str,
            "bool": bool,
            "None": None,
            "list": list,
            "dict": dict,
            "map/int": "mapping"
        }

        # Default settings. Type "None" means that Settings manager shouldn't try to perform type converstion
        self.defaults = defaults.application_settings

        # Load settigns
        self.settings: QSettings = QSettings("Manuwrite", "Manuwrite Editor")
        self.color_schema = self.get_current_color_schema()

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

    def set_setting(self, setting: str, value) -> None:
        """Sets the value of the setting. This method performs no safe checks and should not be used outside the
        SettingsManager class"""

        self.settings.setValue(setting, value)

    def get_appdata_path(self) -> None:
        """Returns path to the directory, where app specific data is stored (i.e. styles, colors, templates etc). If the
        directory doesn't exist, creates it"""
        # TODO: exception possible here
        path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        dir = QDir(path)
        if not dir.exists(path):
            dir.mkpath(path)

        return QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

    def get_color_schemas(self) -> dict:
        """Return a dict of all color schemes found in the /color_schemas subdirectory of the app data directory"""
        # TODO: exception possible here
        path = self.get_appdata_path() + "/color_schemas"
        dir_iter = QDirIterator(path, QDirIterator.Subdirectories)
        color_schemas = dict()
        schema_names = []

        while dir_iter.hasNext():
            filepath = dir_iter.next()

            if filepath.endswith(".toml"):
                data = toml.load(filepath)
                if "Data type" in data and data["Data type"] == "Manuwrite color schema":
                    color_schemas[data["Schema name"]] = data
                    schema_names.append(data["Schema name"])

            color_schemas["Schema names"] = schema_names

        return color_schemas

    def get_current_color_schema(self) -> dict:
        """Return current color schema or the default color schema, if failed to get the current one"""
        schema_name = self.get_setting_value("Editor/Current color schema")
        if schema_name != "System colors":
            try:
                schema = self.get_color_schemas()[schema_name]
            except (KeyError, OSError):
                schema = None
        else:
            schema = None

        if schema is None:
            schema = self.get_default_color_schema()

        return schema

    def get_default_color_schema(self) -> dict:
        """Return the color scheme based on the system colors"""
        palette = QPalette(self.parent.palette())

        return defaults.get_default_color_schema(palette)

    def save_color_schema(self, color_schema):
        # TODO: exception possible here
        path = self.get_appdata_path() + "/color_schemas"
        dir_iter = QDirIterator(path, QDirIterator.Subdirectories)

        while dir_iter.hasNext():
            filepath = dir_iter.next()

            if filepath.endswith(".toml"):
                data = toml.load(filepath)
                if "Schema name" in data and data["Schema name"] == color_schema["Schema name"]:
                    file_handle = open(filepath, "w")
                    toml.dump(color_schema, file_handle)
                    file_handle.close()
                    break
