import sys

from PyQt5.QtWidgets import QApplication

from gui_components.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
