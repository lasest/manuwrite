import toml

from PyQt5.QtCore import QObject, QSettings, QSize, QPoint, QStandardPaths, QDir, QDirIterator, Qt
from PyQt5.QtGui import QPalette, QColor


class SettingsManager(QObject):

    def __init__(self, parent):
        super().__init__(parent)

        # Default settings. Type "None" means that Settings manager shouldn't try to perform type converstion
        self.parent = parent
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

            "SettingsDialog/size/value": QSize(400, 600),
            "SettingsDialog/size/type": "None",

            "SettingsDialog/pos/value": QPoint(100, 100),
            "SettingsDialog/pos/type": "None",

            "SettingsDialog/current tab index/value": 0,
            "SettingsDialog/current tab index/type": "int",

            "ProjectSettingsDialog/size/value": QSize(400, 600),
            "ProjectSettingsDialog/size/type": "None",

            "ProjectSettingsDialog/pos/value": QPoint(100, 100),
            "ProjectSettingsDialog/pos/type": "None",

            "ProjectSettingsDialog/current tab index/value": 0,
            "ProjectSettingsDialog/current tab index/type": "int",

            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Application/Project folder/type": "str",

            "Editor/Font name/value": "Hack",
            "Editor/Font name/type": "str",

            "Editor/Font size/value": 14,
            "Editor/Font size/type": "int",

            "Editor/Default image width/value": 500,
            "Editor/Default image width/type": "int",

            "Editor/Default image height/value": 500,
            "Editor/Default image height/type": "int",

            "Editor/Image tooltip height/value": 250,
            "Editor/Image tooltip height/type": "int",

            "Editor/Image tooltip width/value": 250,
            "Editor/Image tooltip width/type": "int",

            "Editor/Show image tooltips/value": True,
            "Editor/Show image tooltips/type": "bool",

            "Editor/Show citation tooltips/value": True,
            "Editor/Show citation tooltips/type": "bool",

            "Editor/Current color schema/value": "System colors",
            "Editor/Current color schema/type": "str",

            "Render/Autorender/value": True,
            "Render/Autorender/type": "bool",

            "Render/Autorender delay/value": 1000,
            "Render/Autorender delay/type": "int",

            "Projects/Project types/value": ["Article", "Book", "Notes", "Other"],
            "Projects/Project types/type": "list",

            "Render/Formats/value": [{"name": "Html", "pandoc name": "html", "file extension": "html"},
                                     {"name": "Pdf", "pandoc name": "pdf", "file extension": "pdf"},
                                     {"name": "Doc", "pandoc name": "doc", "file extension": "doc"}],
            "Render/Formats/type": "list",

            "Render/Styles/value": [{"name": "Manuwrite strict", "folder": "manuwrite_classic"},
                                    {"name": "Manuwrite modern", "folder": "manuwrite_modern"},
                                    {"name": "Manubot classic", "folder": "manubot_classic"}],
            "Render/Styles/type": "list"
        }

        # Maps datatype names read from config to functions
        self.datatypes = {
            "int": int,
            "str": str,
            "bool": bool,
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

    def get_color_schemas(self):
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

    def get_current_color_schema(self):
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
        palette = QPalette(self.parent.palette())

        schema = {
            "Data type": "Manuwrite color schema",
            "Schema name": "System colors",
            "Editor_colors": {"background": {"color": palette.color(palette.Base).name()},
                              "text": {"color": palette.color(palette.Text).name()},
                              "current_line": {"color": palette.color(palette.AlternateBase).name()},
                              "linenumber_area": {"color": palette.color(palette.AlternateBase).darker(150).name()},
                              "linenumber_text": {"color": palette.color(palette.Text).name()}},
            "Markdown_colors": {"heading-1": {"color": QColor(Qt.red).name()},
                                "heading-2": {"color": QColor(Qt.red).name()},
                                "heading-3": {"color": QColor(Qt.red).name()},
                                "heading-4": {"color": QColor(Qt.red).name()},
                                "heading-5": {"color": QColor(Qt.red).name()},
                                "heading-6": {"color": QColor(Qt.red).name()},
                                "line-break": {"color": "#ff8080"},
                                "horizontal-rule": {"color": "#ff8080"},
                                "italic": {"color": QColor(Qt.yellow).name()},
                                "bold": {"color": QColor(Qt.yellow).name()},
                                "bold-and-italic": {"color": QColor(Qt.yellow).name()},
                                "blockquote-1": {"color": QColor(Qt.cyan).name()},
                                "blockquote-2": {"color": QColor(Qt.cyan).name()},
                                "blockquote-3": {"color": QColor(Qt.cyan).name()},
                                "blockquote-n": {"color": QColor(Qt.cyan).name()},
                                "ordered-list": {"color": QColor(Qt.red).name()},
                                "unordered-list": {"color": QColor(Qt.red).name()},
                                "code": {"color": QColor(Qt.green).name()},
                                "link": {"color": "#3e95ff"},
                                "image": {"color": "#3e95ff"},
                                "citation": {"color": "#3e95ff"}}
        }

        return schema

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




