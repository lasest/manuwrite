import toml
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QObject, QSettings, QStandardPaths, QDir, QFile
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
        self.set_setting_value("Render/Css_styles", self.scan_for_css_styles())
        self.set_setting_value("Render/Csl_styles", self.scan_for_csl_styles())
        self.set_setting_value("Colors/Color_schemas", self.scan_for_color_schemas())

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

    def get_appdata_path(self) -> str:
        """Returns path to the directory, where app specific data is stored (i.e. styles, colors, templates etc). If the
        directory doesn't exist, creates it"""
        # TODO: exception possible here
        path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        dir = QDir(path)
        if not dir.exists(path):
            dir.mkpath(path)

        return QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

    def scan_for_css_styles(self) -> dict:
        """Scans <app data>/css_styles subdirectories for css styles. Returns a dictionary with information about the
         styles that were found"""
        # TODO: hadnle exceptions
        # Get the list of all subdirectories
        path = self.get_appdata_path() + "/css_styles"
        directory = QDir(path)
        subdirectories = directory.entryList(QDir.Dirs | QDir.NoDotAndDotDot)

        styles = dict()
        # Iterate over subdirectories to check if they contain styles
        for subdirectory in subdirectories:
            directory.cd(subdirectory)
            entries = directory.entryList(QDir.Files)

            # Check if necessary files are present
            if "description.toml" in entries and "style.css" in entries:
                # Parse description
                style_info = toml.load(path + "/" + subdirectory + "/" + "description.toml")
                style_info["path"] = path + "/" + subdirectory + "/" + "style.css"
                styles[style_info["identifier"]] = style_info

        return styles

    def scan_for_csl_styles(self) -> dict:
        """Scans <app data>/csl_styles subdirectories for csl styles. Returns a dictionary with information about the
        styles that were found"""

        def get_namespace(elem) -> str:
            """Extracts namespace from element tag"""
            if elem[0] == "{":
                namespace = elem[:elem.find("}") + 1]
            else:
                namespace = ""
            return namespace

        # TODO: hadnle exceptions
        # Get all files in the csl_styles directory
        path = self.get_appdata_path() + "/csl_styles"
        directory = QDir(path)
        entries = directory.entryList(QDir.Files)

        # Iterate over files
        styles = dict()
        for entry in entries:
            if entry.endswith(".csl"):
                # Get root node
                tree = ET.parse(path + "/" + entry)
                root = tree.getroot()

                # Check if there is a namespace
                namespace = get_namespace(root.tag)

                # Get style name
                title = root.find(namespace + "info").find(namespace + "title").text
                styles[title] = {"name": title, "path": path + "/" + entry}

        return styles

    def scan_for_color_schemas(self) -> dict:
        """Scans <app data>/color_schemes subdirectories for color schemas. Returns a dictionary with information about
        the color schemes that were found"""

        # TODO: handle exceptions
        # Get the list of all subdirectories
        path = self.get_appdata_path() + "/color_schemas"
        directory = QDir(path)
        subdirectories = directory.entryList(QDir.Dirs | QDir.NoDotAndDotDot)

        schemas = dict()
        # Iterate over subdirectories to check if they contain color schemas
        for subdirectory in subdirectories:
            directory.cd(subdirectory)
            entries = directory.entryList(QDir.Files)

            # Check if schema file is present
            if "schema.toml" in entries:
                schema_info = dict()

                filepath = path + "/" + subdirectory + "/" + "schema.toml"
                schema = toml.load(filepath)
                name = schema["Schema name"]

                schema_info["name"] = name
                schema_info["path"] = filepath

                schemas[name] = schema_info

        return schemas

    def get_color_schema(self, schema_identifier: str) -> dict:
        color_schemas = self.get_setting_value("Colors/Color_schemas")
        schema_filepath = color_schemas[schema_identifier]["path"]
        schema = toml.load(schema_filepath)

        return schema

    def get_current_color_schema(self) -> dict:
        """Return current color schema or the default color schema, if failed to get the current one"""
        schema_identifier = self.get_setting_value("Editor/Current color schema")
        if schema_identifier != "System colors":
            try:
                schema = self.get_color_schema(schema_identifier)
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

    def save_color_schema(self, color_schema: dict) -> None:
        """Saves given color schema to file"""
        # TODO: exception possible here
        schema_identifier = color_schema["Schema name"]
        schema_info = self.get_setting_value("Colors/Color_schemas")[schema_identifier]
        filepath = schema_info["path"]

        file_handle = open(filepath, "w+")
        toml.dump(color_schema, file_handle)
        file_handle.close()

    def import_color_schema_from_dict(self, schema_name: str, color_schema: dict) -> None:
        """Imports color schema from a dictionary"""
        # Set schema name
        color_schema["Schema name"] = schema_name

        # Create directory for new schema file
        directory = QDir(self.get_appdata_path() + "/color_schemas")
        directory.mkdir(schema_name)

        # Add information about schema to settings manager
        schemas = self.get_setting_value("Colors/Color_schemas")
        filepath = self.get_appdata_path() + "/color_schemas/" + schema_name + "/schema.toml"
        schema_info = {"name": schema_name, "path": filepath}

        schemas[schema_name] = schema_info

        # Save schema
        self.set_setting_value("Colors/Color_schemas", schemas)
        self.save_color_schema(color_schema)

    def import_color_schema_from_file(self, filepath: str) -> None:
        """Imports color schema from a file"""
        # TODO: add exception handling. Can check by "Data type" == "Manuwrite color schema"
        # Parse schema
        schema = toml.load(filepath)
        schema_name = schema["Schema name"]
        new_path = self.get_appdata_path() + "/color_schemas/" + schema_name + "/schema.toml"

        # Create schema dir
        directory = QDir(self.get_appdata_path() + "/color_schemas")
        directory.mkdir(schema_name)

        # Copy schema to its dir and add to SettingsManager
        schemas = self.get_setting_value("Colors/Color_schemas")
        schemas[schema_name] = {"name": schema_name, "path": new_path}
        self.set_setting_value("Colors/Color_schemas", schemas)

        QFile.copy(filepath, new_path)

    def delete_color_scheme(self, scheme_identifier: str) -> None:
        """Deletes a color scheme files and removes it from SettingsManager"""
        # Get scheme info
        scheme_info = self.get_setting_value("Colors/Color_schemas")[scheme_identifier]
        filepath = scheme_info["path"]
        directory_path = filepath[:filepath.rfind("/")]

        # Remove scheme directory
        directory = QDir(directory_path)
        directory.removeRecursively()

        # Remove scheme from settings manager
        schemas = self.get_setting_value("Colors/Color_schemas")
        schemas.pop(scheme_identifier)
        self.set_setting_value("Colors/Color_schemas", schemas)

    def export_color_scheme_to_file(self, scheme_identifier: str, filepath: str) -> None:
        """Exports a color scheme to file"""
        # Get filepath of a scheme
        schemes = self.get_setting_value("Colors/Color_schemas")
        scheme_path = schemes[scheme_identifier]["path"]

        # Copy file
        QFile.copy(scheme_path, filepath)
