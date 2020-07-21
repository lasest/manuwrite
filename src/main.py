import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from forms import mainwindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
