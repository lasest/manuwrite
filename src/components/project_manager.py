import toml
import copy
from collections import OrderedDict

from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import QModelIndex, QDir, QFile, pyqtSlot, pyqtSignal, QObject

from common import ProjectError
import defaults
from components.thread_manager import ThreadManager
import components.managers


class Communicator(QObject):
    """Used to send signals"""

    ProjectStructureUpdated = pyqtSignal()

    def __init__(self):
        super().__init__()


class ProjectManager():

    def __init__(self, thread_manager):

        # Set attributes
        self.defaults = copy.deepcopy(defaults.project_settings)
        self.project_info = dict()
        self.FsModel = QFileSystemModel()
        self.ThreadManager = thread_manager
        self.Communicator = Communicator()
        self.root_path = ""
        self.project_loaded = False

    def close_project(self):
        self.root_path = ""
        self.project_loaded = False
        self.project_info = dict()

    def load_project(self, directory_path: str):
        self.root_path = directory_path
        self.FsModel.setRootPath(directory_path)
        self.read_project_info()
        self.project_loaded = True

    def is_project_loaded(self) -> bool:
        return self.project_loaded

    def read_project_info(self) -> None:
        """Reads project configuration data from default storage location"""
        if QFile.exists(self.root_path + "/.manuwrite/project.toml"):
            try:
                file = QFile()
                file.setFileName(self.root_path + "/.manuwrite/project.toml")
                file.open(QFile.ReadOnly)
                data = OrderedDict(toml.loads(file.readAll().data().decode()))
            except OSError:
                raise ProjectError("An error occured while reading project file")
            finally:
                file.close()
            self.project_info = data

            for key in self.defaults.keys():
                if key not in self.project_info:
                    self.project_info[key] = self.defaults[key]

            # Update project structure
            filenames = []
            for filename in self.get_setting_value("Files to render"):
                filenames.append(self.get_setting_value("Absolute path") + "/" + filename)

            self.ThreadManager.perform_operation("parse_project", self.on_MarkdownProjectParserThread_finished,
                                                 filepaths=filenames)
            self.set_setting_value("Absolute path", self.root_path)

        else:
            raise ProjectError("Project file doesn't exits")

    def save_project_data(self) -> None:
        """Saves project configuration data to permanent storage"""
        try:
            file = QFile()
            file.setFileName(self.root_path + "/.manuwrite/project.toml")
            file.open(QFile.WriteOnly)
            file.write(toml.dumps(self.project_info).encode())
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
            file.setFileName(directory_path + "/.manuwrite/project.toml")
            file.open(QFile.ReadWrite)

            project_settings = copy.deepcopy(defaults.project_settings)
            project_settings["Absolute path"] = {"type": "str", "value": directory_path}

            file.write(toml.dumps(project_settings).encode())
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
        return copy.deepcopy(self.project_info[setting]["value"])

    def set_setting_value(self, setting: str, value) -> None:
        """Sets the value of a given setting"""

        self.project_info[setting]["value"] = value

    def update_project_structure(self, file_structure: dict) -> None:
        """Updates filestructure of a file in raw project structure. Then generates a new combined project structure
        (from new raw structure) and updates corresponding project settings entry. Before all checks if the file
        structure belongs to a file that is to be rendered according to the current project settings"""

        filepath = file_structure["filepath"]
        del file_structure["filepath"]

        # Check if filepath is to be rendered, otherwise do not include it in project structure
        if not self.is_file_to_be_rendered(filepath):
            return

        # Get raw project structure from settings (in format {filepath: document_info}
        raw_project_structure = self.get_setting_value("Project structure raw")
        raw_project_structure[filepath] = file_structure

        combined_project_structure = self.get_combined_project_structure(raw_project_structure)

        self.set_setting_value("Project structure raw", raw_project_structure)
        self.set_setting_value("Project structure combined", combined_project_structure)

        # Send signal to main window to update project structure tree, if necessary
        self.Communicator.ProjectStructureUpdated.emit()

    def get_combined_project_structure(self, raw_project_structure: dict) -> dict:
        """Convert raw project structure ({filepath: document_info}) to combined document structure (document_info)"""
        combined = copy.deepcopy(defaults.document_info_template)
        del combined["filepath"]

        for key1, value1 in raw_project_structure.items():
            for key2, value2 in value1.items():
                combined[key2].update(value2)

        return combined

    def is_file_to_be_rendered(self, filepath: str) -> bool:
        files_to_render = self.get_setting_value("Files to render").copy()
        for i in range(len(files_to_render)):
            files_to_render[i] = self.get_setting_value("Absolute path") + "/" + files_to_render[i]

        # Check if filepath is to be rendered, otherwise do not include it in project structure
        if filepath in files_to_render:
            return True
        else:
            return False

    # Doesn't work as a slot for some reason
    #@pyqtSlot(dict)
    def on_MarkdownProjectParserThread_finished(self, project_structure: dict) -> None:
        """Update project structure with data received from MarkdownProjectParserThread"""

        self.set_setting_value("Project structure raw", project_structure)

        combined_project_structure = self.get_combined_project_structure(project_structure)
        self.set_setting_value("Project structure combined", combined_project_structure)

        self.Communicator.ProjectStructureUpdated.emit()
