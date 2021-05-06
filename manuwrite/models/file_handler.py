from PyQt5.QtCore import QObject, QDir, QFile, QIODevice


class FileHandler(QObject):

    def __init__(self, parent=None):

        super(FileHandler, self).__init__(parent)

    def write_file_contents(self, filepath: str, data):
        fh = QFile(filepath, self)
        fh.open(QIODevice.WriteOnly)
        fh.write(data.encode())
        fh.close()

    def read_file_contents(self, filepath: str):
        fh = QFile(filepath, self)
        fh.open(QIODevice.ReadOnly)
        file_contents = fh.readAll()
        fh.close()
        data = file_contents.data().decode()
        return data

