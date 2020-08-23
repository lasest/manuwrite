import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

from forms.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName("Manuwrite")
    QCoreApplication.setOrganizationName("Manuwrite")
    QCoreApplication.setOrganizationDomain("manuwrite.org")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
