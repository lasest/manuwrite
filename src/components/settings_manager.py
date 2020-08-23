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
            # Main window
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

            # Settings dialog
            "SettingsDialog/size/value": QSize(400, 600),
            "SettingsDialog/size/type": "None",

            "SettingsDialog/pos/value": QPoint(100, 100),
            "SettingsDialog/pos/type": "None",

            "SettingsDialog/current tab index/value": 0,
            "SettingsDialog/current tab index/type": "int",

            # Project settings dialog
            "ProjectSettingsDialog/size/value": QSize(400, 600),
            "ProjectSettingsDialog/size/type": "None",

            "ProjectSettingsDialog/pos/value": QPoint(100, 100),
            "ProjectSettingsDialog/pos/type": "None",

            "ProjectSettingsDialog/current tab index/value": 0,
            "ProjectSettingsDialog/current tab index/type": "int",

            # Add heading dialog
            "AddHeadingDialog/autonumber/value": 2,
            "AddHeadingDialog/autonumber/type": "int",

            "AddHeadingDialog/autogen identifier/value": 0,
            "AddHeadingDialog/autogen identifier/type": "int",

            # Add image dialog
            "AddImageDialog/autogen identifier/value": 2,
            "AddImageDialog/autogen identifier/type": "int",

            "AddImageDialog/autonumber/value": 2,
            "AddImageDialog/autonumber/type": "int",

            # Add table dialog
            "AddTableDialog/autogen identifier/value": 2,
            "AddTableDialog/autogen identifier/type": "int",

            "AddTableDialog/autonumber/value": 2,
            "AddTableDialog/autonumber/type": "int",

            # Add footnote dialog
            "AddFootnoteDialog/autogen identifier/value": 2,
            "AddFootnoteDialog/autogen identifier/type": "int",

            # Application
            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Application/Project folder/type": "str",

            # Editor
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

            # Render
            "Render/Autorender/value": True,
            "Render/Autorender/type": "bool",

            "Render/Autorender delay/value": 1000,
            "Render/Autorender delay/type": "int",

            "Render/Formats/value": [{"name": "Html", "pandoc name": "html", "file extension": "html"},
                                     {"name": "Pdf", "pandoc name": "pdf", "file extension": "pdf"},
                                     {"name": "Doc", "pandoc name": "doc", "file extension": "doc"}],
            "Render/Formats/type": "list",

            "Render/Styles/value": [{"name": "Manuwrite strict", "folder": "manuwrite_classic"},
                                    {"name": "Manuwrite modern", "folder": "manuwrite_modern"},
                                    {"name": "Manubot classic", "folder": "manubot_classic"}],
            "Render/Styles/type": "list",

            # Projects
            "Projects/Project types/value": ["Article", "Book", "Notes", "Other"],
            "Projects/Project types/type": "list"
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

        schema = {
            "Data type": "Manuwrite color schema",
            "Schema name": "System colors",
            "Editor_colors": {"background": {"name": "Editor background",
                                             "color": palette.color(palette.Base).name()},
                              "text": {"name": "Text",
                                       "color": palette.color(palette.Text).name()},
                              "current_line": {"name": "Current line",
                                               "color": palette.color(palette.AlternateBase).name()},
                              "linenumber_area": {"name": "Line number area",
                                                  "color": palette.color(palette.AlternateBase).darker(150).name()},
                              "linenumber_text": {"name": "Line number area text",
                                                  "color": palette.color(palette.Text).name()}},
            "Markdown_colors": {"heading-1": {"name": "Heading 1",
                                              "color": QColor(Qt.red).name()},
                                "heading-2": {"name": "Heading 2",
                                              "color": QColor(Qt.red).name()},
                                "heading-3": {"name": "Heading 3",
                                              "color": QColor(Qt.red).name()},
                                "heading-4": {"name": "Heading 4",
                                              "color": QColor(Qt.red).name()},
                                "heading-5": {"name": "Heading 5",
                                              "color": QColor(Qt.red).name()},
                                "heading-6": {"name": "Heading 6",
                                              "color": QColor(Qt.red).name()},
                                "line-break": {"name": "Line break",
                                               "color": "#ff8080"},
                                "horizontal-rule": {"name": "Horizontal rule",
                                                    "color": "#ff8080"},
                                "italic": {"name": "Italic",
                                           "color": QColor(Qt.yellow).name()},
                                "bold": {"name": "Bold",
                                         "color": QColor(Qt.yellow).name()},
                                "bold-and-italic": {"name": "Bold and italic",
                                                    "color": QColor(Qt.yellow).name()},
                                "blockquote-1": {"name": "Blockquote 1",
                                                 "color": QColor(Qt.cyan).name()},
                                "blockquote-2": {"name": "Blockquote 2",
                                                 "color": QColor(Qt.cyan).name()},
                                "blockquote-3": {"name": "Blockquote 3",
                                                 "color": QColor(Qt.cyan).name()},
                                "blockquote-n": {"name": "Blockquote n",
                                                 "color": QColor(Qt.cyan).name()},
                                "ordered-list": {"name": "Ordered list",
                                                 "color": QColor(Qt.red).name()},
                                "unordered-list": {"name": "Unordered list",
                                                   "color": QColor(Qt.red).name()},
                                "code": {"name": "Code",
                                         "color": QColor(Qt.green).name()},
                                "link": {"name": "Link",
                                         "color": "#3e95ff"},
                                "image": {"name": "Image",
                                          "color": "#3e95ff"},
                                "citation": {"name": "Citation",
                                             "color": "#3e95ff"},
                                "strikeout": {"name": "Strikeout",
                                              "color": "#777777"},
                                "superscript": {"name": "Strikeout",
                                              "color": "#4081d1"},
                                "subscript": {"name": "Strikeout",
                                              "color": "#4081d1"},
                                "footnote": {"name": "Footnote",
                                             "color": "#ff0000"},
                                "table": {"name": "Table",
                                          "color": "#0000ff"}
                                }
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




