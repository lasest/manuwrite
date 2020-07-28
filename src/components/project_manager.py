import json

from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import QModelIndex, QDir, QFile

from common import ProjectError


class ProjectManager():

    def __init__(self, directory_path: str):

        self.root_path = directory_path
        self.FsModel = QFileSystemModel()
        #self.FsModel.setReadOnly(True)
        self.FsModel.setRootPath(directory_path)
        self.project_info = dict()
        self.ModelIndex = self.FsModel.index(directory_path)
        self.read_project_info()

    def read_project_info(self):
        print("Reading Project info")
        if QFile.exists(self.root_path + "/.manuwrite/project.json"):
            file = QFile()
            file.setFileName(self.root_path + "/.manuwrite/project.json")
            file.open(QFile.ReadOnly)
            data = json.loads(file.readAll().data().decode())
            self.project_info = data
        else:
            print("Cannot read project info. File \"{}\" doesn't exist.".format(self.root_path + "/.manuwrite/project.json"))
            raise ProjectError("Project file doesn't exits")

    def uptade_project_info(self, info: dict):
        pass


    def save_project_data(self) -> bool:
        pass

    @staticmethod
    def create_project(directory_path):
        directory = QDir(directory_path)

        directory.mkdir(".manuwrite")
        directory.mkdir("images")
        directory.mkdir("notes")
        directory.mkdir("data")

        directory.mkpath(".manuwrite/render")
        file = QFile()
        file.setFileName(directory_path + "/.manuwrite/project.json")
        file.open(QFile.ReadWrite)

        project_info = {
            "title": "Untitled",
            "date_created:": "2020-07-28",
            "author": "Sergey Lazarev",
            "project_type": "notes",
            "absolute_path": directory_path
        }

        file.write(json.dumps(project_info, indent=4).encode())
        file.close()

    def create_folder(self, path: str):
        directory = QDir(self.root_path)
        directory.mkdir(path)

    def delete_file(self, item: QModelIndex):
        path = self.FsModel.filePath(item)
        # Check if path is dir or file
        if self.FsModel.isDir(item):
            directory = QDir(path)
            directory.removeRecursively()
        else:
            file = QFile(path)
            file.moveToTrash()

    def rename(self, item: QModelIndex, name: str):
        directory = QDir(self.root_path)
        old_path = self.FsModel.filePath(item)
        new_path = old_path[:old_path.rfind(directory.separator())] + "/" + name
        directory.rename(old_path, new_path)

    def create_file(self, path: str):
        file = QFile()
        file.setFileName(path)
        file.open(QFile.ReadWrite)
        file.close()
