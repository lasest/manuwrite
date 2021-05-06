import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir, QCoreApplication
from PyQt5.QtGui import QColor, QPalette

from manuwrite.models.template_processor import TemplateProcessor
from manuwrite.views.main_window_view import MainWindowView
from manuwrite.controllers.main_window_controller import MainWindowController
from manuwrite.models.file_handler import FileHandler
from manuwrite.models.main_window_model import MainWindowModel


class Application(QApplication):
    
    def __init__(self, args=None):
        
        super(Application, self).__init__(args)

        self._init_app_metadata()
        self._add_search_paths()
        self._create_app_style()
        self._load_app_style()

    def _add_search_paths(self):
        QDir.addSearchPath("templates", "resources/templates/")
        QDir.addSearchPath("styles", "resources/styles/")
        QDir.addSearchPath("icons_dark", "resources/icons_dark")
        QDir.addSearchPath("icons_light", "resources/icons_light")
        QDir.addSearchPath("icons_common", "resources/icons_common")

    def _init_app_metadata(self):
        QCoreApplication.setApplicationName("Manuwrite")
        QCoreApplication.setOrganizationName("Manuwrite")
        QCoreApplication.setOrganizationDomain("manuwrite.org")

    def _create_app_style(self):
        """TMP: shouldn't need to create a style, the app should be districtuted with a style already"""
        style_processor = TemplateProcessor("app.qss", parent=self)
        style_text = style_processor.get_processed_template()

        # TMP: The file has to exist for this to work, otherwise the file prefix won't work!
        fh = FileHandler(parent=self)
        fh.write_file_contents("styles:app.qss", style_text)

    def _load_app_style(self):
        fh = FileHandler()
        style_sheet = fh.read_file_contents("styles:app.qss")
        self.setStyleSheet(style_sheet)

        palette = self.palette()
        palette.setColor(QPalette.Link, QColor("DodgerBlue"))
        self.setPalette(palette)

    def start_app(self):
        view = MainWindowView()
        model = MainWindowModel()
        controller = MainWindowController(view, model, parent=self)

        view.show()
        sys.exit(self.exec())
