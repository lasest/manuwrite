from PyQt5.QtCore import pyqtSlot, QObject, Qt
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from manuwrite.views.main_window_view import MainWindowView
from manuwrite.controllers.project_dock_controller import ProjectDockController
from manuwrite.controllers.git_dock_controller import GitDockController
from manuwrite.models.managers import settingsManager
from manuwrite.models.main_window_model import MainWindowModel


class MainWindowController(QObject):

    def __init__(self, view: MainWindowView, model: MainWindowModel, parent=None):
        super(MainWindowController, self).__init__(parent)
        
        self.view = view
        self.model = model
        self._connect_signals_to_slots()
        self._create_other_controllers()

        # Set some initial states
        self._toggle_docks_according_to_settings()
        self._resize_console_dock()
        self.view.actionOpenHomePage.toggle()

    def _connect_signals_to_slots(self):
        # Sidebar signals
        ###################
        self.view.actionOpenEditorPage.toggled.connect(self.on_actionOpenEditorPage_triggered)
        self.view.actionOpenGitPage.toggled.connect(self.on_actionOpenGitPage_triggered)
        self.view.actionOpenHomePage.toggled.connect(self.on_actionOpenHomePage_triggered)

        # Dock toggle/close signals
        ###################
        self.view.actionToggleProjectTab.toggled.connect(self.on_actionToggleProjectTab_toggled)
        self.view.projectDock.closeButton.clicked.connect(self.on_projectTabCloseButton_clicked)

        self.view.actionToggleConsoleDock.toggled.connect(self.on_actionToggleConsoleDock_toggled)
        self.view.consoleDock.closeButton.clicked.connect(self.on_consoleDockCloseButton_clicked)

        self.view.actionToggleGitDock.toggled.connect(self.on_actionToggleGitDock_toggled)
        self.view.gitDock.closeButton.clicked.connect(self.on_gitDockCloseButton_clicked)

        self.view.actionToggleDocumentPreview.toggled.connect(self.on_actionToggleDocumentPreview_toggled)
        self.view.documentPreviewDock.closeButton.clicked.connect(self.on_documentPreviewCloseButton_clicked)

    def _create_other_controllers(self):
        self.projectDockController = ProjectDockController(self.view.projectDock, self)
        self.gitDockController = GitDockController(self.view.gitDock, self)

    def _resize_console_dock(self):
        console_dock_height = settingsManager.appSettings.mainWindow.consoleDockHeight

        self.view.resizeDocks([self.view.consoleDock], [console_dock_height], Qt.Vertical)

    def _update_check_icon(self, action: QAction, state: bool):
        icon_prefix = settingsManager.get_icon_prefix()

        if state:
            action.setIcon(QIcon(f"{icon_prefix}:checkbox_on.svg"))
        else:
            action.setIcon(QIcon(f"{icon_prefix}:checkbox_off.svg"))

    def _toggle_docks_according_to_settings(self):
        self.view.actionToggleProjectTab.setChecked(settingsManager.appSettings.mainWindow.projectDockToggle)
        self.view.actionToggleDocumentPreview.setChecked(
            settingsManager.appSettings.mainWindow.documentPreviewDockToggle)
        self.view.actionToggleGitDock.setChecked(settingsManager.appSettings.mainWindow.gitDockToggle)
        self.view.actionToggleConsoleDock.setChecked(settingsManager.appSettings.mainWindow.consoleDockToggle)


    # Sidebar Slots
    ###################
    @pyqtSlot(bool)
    def on_actionOpenHomePage_triggered(self, checked: bool):
        if checked:
            self.view.mainStackedWidget.setCurrentIndex(0)

    @pyqtSlot(bool)
    def on_actionOpenEditorPage_triggered(self, checked: bool):
        if checked:
            self.view.mainStackedWidget.setCurrentIndex(1)

            if not self.model.editorPageFullyInitiated:
                project_dock_width = settingsManager.appSettings.mainWindow.projectDockWidth
                preview_dock_width = settingsManager.appSettings.mainWindow.documentPreviewDockWidth

                self.view.editorPage.resizeDocks([self.view.projectDock], [project_dock_width], Qt.Horizontal)
                self.view.editorPage.resizeDocks([self.view.documentPreviewDock], [preview_dock_width], Qt.Horizontal)

                self.model.editorPageFullyInitiated = True

    @pyqtSlot(bool)
    def on_actionOpenGitPage_triggered(self, checked: bool):
        if checked:
            self.view.mainStackedWidget.setCurrentIndex(2)

            if not self.model.gitPageFullyInitiated:
                git_dock_width = settingsManager.appSettings.mainWindow.gitDockWidth

                self.view.gitPage.resizeDocks([self.view.gitDock], [git_dock_width], Qt.Horizontal)

                self.model.gitPageFullyInitiated = True

    # Dock toggle/close slots
    ###################
    @pyqtSlot(bool)
    def on_actionToggleProjectTab_toggled(self, checked: bool):
        self.view.projectDock.setVisible(checked)
        self._update_check_icon(self.view.actionToggleProjectTab, checked)

    @pyqtSlot()
    def on_projectTabCloseButton_clicked(self):
        self.view.actionToggleProjectTab.setChecked(False)

    @pyqtSlot(bool)
    def on_actionToggleConsoleDock_toggled(self, checked: bool):
        self.view.consoleDock.setVisible(checked)
        self._update_check_icon(self.view.actionToggleConsoleDock, checked)

    @pyqtSlot()
    def on_consoleDockCloseButton_clicked(self):
        self.view.actionToggleConsoleDock.setChecked(False)

    @pyqtSlot(bool)
    def on_actionToggleGitDock_toggled(self, checked: bool):
        self.view.gitDock.setVisible(checked)
        self._update_check_icon(self.view.actionToggleGitDock, checked)

    @pyqtSlot()
    def on_gitDockCloseButton_clicked(self):
        self.view.actionToggleGitDock.setChecked(False)

    @pyqtSlot(bool)
    def on_actionToggleDocumentPreview_toggled(self, checked: bool):
        self.view.documentPreviewDock.setVisible(checked)
        self._update_check_icon(self.view.actionToggleDocumentPreview, checked)

    @pyqtSlot()
    def on_documentPreviewCloseButton_clicked(self):
        self.view.actionToggleDocumentPreview.setChecked(False)
