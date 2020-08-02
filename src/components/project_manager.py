import json
from collections import OrderedDict

from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import QModelIndex, QDir, QFile, QDate

from common import ProjectError


class ProjectManager():

    defaults = OrderedDict({
        "Title": {"type": "str", "value": ""},
        "Date created": {"type": "mapping/int", "value": [QDate.currentDate().year(), QDate.currentDate().month(),
                                                          QDate.currentDate().day()]},
        "Authors": {"type": "str", "value": ""},
        "Project type": {"type": "enum", "value": "Notes", "allowed values": ["Notes", "Article", "Book"]},
        "Absolute path": {"type": "str", "value": ""},
        "Description": {"type": "str", "value": ""},
        "Additional meta information": {"type": "str", "value": ""},
        "Files to render": {"type": "mapping/str", "value": []},
        "Style": {"type": "str", "value": "Manubot classic"},
        "Render to": {"type": "str", "value": "Html"},
        "Pandoc command (auto)": {"type": "str", "value": ""},
        "Pandoc command (manual)": {"type": "str", "value": ""}
    })

    def __init__(self, directory_path: str):

        # Set attributes
        self.root_path = directory_path
        self.project_info = dict()
        self.FsModel = QFileSystemModel()

        self.FsModel.setRootPath(directory_path)
        self.read_project_info()

    def read_project_info(self) -> None:
        """Reads project configuration data from default storage location"""
        if QFile.exists(self.root_path + "/.manuwrite/project.json"):
            try:
                file = QFile()
                file.setFileName(self.root_path + "/.manuwrite/project.json")
                file.open(QFile.ReadOnly)
                data = OrderedDict(json.loads(file.readAll().data().decode()))
            except OSError:
                raise ProjectError("An error occured while reading project file")
            finally:
                file.close()
            self.project_info = data

            for key in self.defaults.keys():
                if key not in self.project_info:
                    self.project_info[key] = self.defaults[key]

        else:
            raise ProjectError("Project file doesn't exits")

    def uptade_project_info(self, info: dict) -> None:
        """Updates self.project_info with data from given dictionary"""

        self.project_info[info[0]]["value"] = info[1]

    def save_project_data(self) -> None:
        """Saves project configuration data to permanent storage"""
        try:
            file = QFile()
            file.setFileName(self.root_path + "/.manuwrite/project.json")
            file.open(QFile.WriteOnly)
            file.write(json.dumps(self.project_info, indent=4).encode())
        except OSError:
            raise ProjectError("Failed to write project configuration data")
        finally:
            file.close()

    @staticmethod
    def create_project(directory_path: str) -> None:
        """Creates a new project at given path"""

        try:
            directory = QDir(directory_path)

            directory.mkdir(".manuwrite")
            directory.mkdir("images")
            directory.mkdir("notes")
            directory.mkdir("data")

            directory.mkpath(".manuwrite/render")
            file = QFile()
            file.setFileName(directory_path + "/.manuwrite/project.json")
            file.open(QFile.ReadWrite)

            project_settings = ProjectManager.defaults
            project_settings["Absolute path"] = directory_path

            file.write(json.dumps(project_settings, indent=4).encode())
            file.close()
        except OSError:
            raise ProjectError("Error creating project files")

    def create_folder(self, path: str) -> None:
        """Creates an empty directory at given path"""
        directory = QDir(self.root_path)
        directory.mkdir(path)

    def delete_file(self, item: QModelIndex) -> None:
        """Deletes a file or a directory by given ModelIndex"""

        path = self.FsModel.filePath(item)
        try:
            # Check if path is dir or file
            if self.FsModel.isDir(item):
                directory = QDir(path)
                directory.removeRecursively()
            else:
                file = QFile(path)
                file.moveToTrash()
        except OSError:
            raise ProjectError("Error deleting file or directory")

    def rename(self, item: QModelIndex, name: str) -> None:
        """Renames a file or a directory at a given ModelIndex to given name"""

        directory = QDir(self.root_path)
        old_path = self.FsModel.filePath(item)
        new_path = old_path[:old_path.rfind(directory.separator())] + "/" + name
        try:
            directory.rename(old_path, new_path)
        except OSError:
            raise ProjectError("Error renaming file or directory")

    def create_file(self, path: str) -> None:
        """Creates a file at a given path"""

        try:
            file = QFile()
            file.setFileName(path)
            file.open(QFile.ReadWrite)
        except OSError:
            raise ProjectError
        finally:
            file.close()

    def get_setting_value(self, setting: str):
        """Return the value of a given setting"""

        return self.project_info[setting]["value"]

    def set_setting_value(self, setting: str, value) -> None:
        """Sets the value of a given setting"""

        self.project_info[setting]["value"] = value
