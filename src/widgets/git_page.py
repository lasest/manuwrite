from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMdiSubWindow
from PyQt5.QtGui import QIcon, QPixmap

from ui_widgets.ui_git_page_widget import Ui_GitPageWidget
from mdi_widgets.git_mdi_area_placeholder_widget import GitMdiAreaPlaceholderWidget

from widgets.mdisubwindow_custom import MdiSubWindow_custom
import components.managers


class GitPage(QWidget):

    def __init__(self):
        super(GitPage, self).__init__()
        self.ui = Ui_GitPageWidget()
        self.ui.setupUi(self)

        self.ProjectManager = components.managers.ProjectManager
        self.SettingsManager = components.managers.SettingsManager
        self.ThreadManager = components.managers.ThreadManager
        self.GitManager = components.managers.GitManager

        self.is_tiling_windows = False

        self.windows = dict()

        # Prepare GitMdiAreaPlaceholder
        window = MdiSubWindow_custom(self, Qt.FramelessWindowHint)
        window.setWindowState(Qt.WindowMaximized)
        widget = GitMdiAreaPlaceholderWidget(parent=window, project_manager=self.ProjectManager,
                                             git_manager=self.GitManager, handler_function=self.on_GitSingal)
        window.setWidget(widget)

        self.ui.GitMdiArea.addSubWindow(window)

        window.show()

    def create_windows(self) -> None:
        """Creates all mdi windows for the GitMdiArea"""

        self.is_tiling_windows = True

        from mdi_widgets.git_branches_widget import GitBranchesWidget
        from mdi_widgets.git_commit_history_widget import GitCommitHistoryWidget
        from mdi_widgets.git_commit_widget import GitCommitWidget
        from mdi_widgets.git_diff_widget import GitDiffWidget
        from mdi_widgets.git_status_widget import GitStatusWidget

        widget_classes = {"branches_window": GitBranchesWidget,
                           "commit_history_window": GitCommitHistoryWidget,
                           "commit_window": GitCommitWidget,
                           "diff_window": GitDiffWidget,
                           "status_window": GitStatusWidget
                           }

        # Create an empty icon for the subwindows
        no_icon = QPixmap(8, 8)
        no_icon.fill(Qt.transparent)
        no_icon = QIcon(no_icon)

        def create_window(window_name: str) -> None:
            """Creates a single Mdi subwindow"""
            window = MdiSubWindow_custom(self, Qt.WindowTitleHint | Qt.WindowCloseButtonHint |Qt.CustomizeWindowHint)
            window.setWindowIcon(no_icon)
            window.setOption(QMdiSubWindow.RubberBandMove)
            window.setOption(QMdiSubWindow.RubberBandResize)
            widget_class = widget_classes[window_name]
            widget = widget_class(parent=window, project_manager=self.ProjectManager,
                                  git_manager=self.GitManager, handler_function=self.on_GitSingal)
            window.setWidget(widget)

            self.ui.GitMdiArea.addSubWindow(window)
            window.show()
            window.MdiSubwindowSignal.connect(self.on_MdiSubwindowSignal)

        for window_name in widget_classes.keys():
            create_window(window_name)

        self.ui.GitMdiArea.tileSubWindows()
        self.is_tiling_windows = False

    def on_GitSingal(self):
        """Handles signals emitted by mdi subwindows of the GitMdiArea"""
        self.ui.GitMdiArea.closeAllSubWindows()

        self.create_windows()

    def on_MdiSubwindowSignal(self):
        if not self.is_tiling_windows:
            self.is_tiling_windows = True
            self.ui.GitMdiArea.tileSubWindows()
            self.is_tiling_windows = False

