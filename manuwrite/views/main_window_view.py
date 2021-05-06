from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QStatusBar, QToolBar, QLabel, QAction, QActionGroup,
                             QTabWidget, QToolButton, QTextEdit, QWidget, QGridLayout, QPushButton, QScrollArea,
                             QVBoxLayout)

from manuwrite.views.console_dock_view import ConsoleDockView
from manuwrite.views.project_dock_view import ProjectDockView
from manuwrite.views.document_preview_dock_view import DocumentPreviewDockView
from manuwrite.views.git_dock_view import GitDockView
from manuwrite.views.welcome_page_info_block import WelcomePageInfoBlock
from manuwrite.models.managers import settingsManager


class MainWindowView(QMainWindow): 

    def __init__(self, parent=None):
        """MainWindowView constructor"""
        super().__init__(parent)

        # Create UI
        self._createActions()
        self._createMenu()
        self._createSidebar()
        self._createStatusBar()
        self._createCentralWidget()
        self._createConsoleDock()

        # Set some initial states
        self.setWindowTitle('Manuwrite')
        self._apply_settings()

    def _createMenu(self):
        """Create main menu"""
        # Create file menu
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.actionNewDocument)
        file_menu.addAction(self.actionNewProject)
        file_menu.addAction(self.actionOpenDocument)
        file_menu.addAction(self.actionOpenProject)
        file_menu.addAction(self.actionSaveDocument)
        file_menu.addAction(self.actionSaveDocumentAs)
        file_menu.addAction(self.actionCloseDocument)
        file_menu.addAction(self.actionCloseProject)

        file_menu.addSeparator()

        file_menu.addAction(self.actionSettings)
        file_menu.addAction(self.actionProjectSettings)

        file_menu.addSeparator()

        file_menu.addAction(self.actionExit)

        # Create edit menu
        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(self.actionUndo)
        edit_menu.addAction(self.actionRedo)

        edit_menu.addSeparator()

        edit_menu.addAction(self.actionCut)
        edit_menu.addAction(self.actionCopy)
        edit_menu.addAction(self.actionPaste)
        edit_menu.addAction(self.actionDelete)

        edit_menu.addSeparator()

        edit_menu.addAction(self.actionSelectAll)

        edit_menu.addSeparator()

        edit_menu.addAction(self.actionFind)
        edit_menu.addAction(self.actionFindReplace)

        # Create view menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.actionToggleProjectTab)
        view_menu.addAction(self.actionToggleDocumentPreview)
        view_menu.addAction(self.actionToggleGitDock)
        view_menu.addAction(self.actionToggleConsoleDock)

        # Create insert menu
        insert_menu = self.menuBar().addMenu("&Insert")
        insert_menu.addAction(self.actionCitation)
        insert_menu.addAction(self.actionAddTable)
        insert_menu.addAction(self.actionInsertFootnote)
        insert_menu.addAction(self.actionLink)
        insert_menu.addAction(self.actionCrossRef)
        insert_menu.addAction(self.actionImage)
        insert_menu.addAction(self.actionHorizontalRule)

        # Create format menu
        format_menu = self.menuBar().addMenu("&Format")
        format_menu.addAction(self.actionItalic)
        format_menu.addAction(self.actionBold)
        format_menu.addAction(self.actionBoldItalic)
        format_menu.addAction(self.actionStrikethrough)

        format_menu.addSeparator()

        format_menu.addAction(self.actionSuperscript)
        format_menu.addAction(self.actionSubscript)
        format_menu.addAction(self.actionCode)
        format_menu.addAction(self.actionBlockquote)

        format_menu.addSeparator()

        heading_menu = format_menu.addMenu("Heading")
        heading_menu.addAction(self.actionHeading1)
        heading_menu.addAction(self.actionHeading2)
        heading_menu.addAction(self.actionHeading3)
        heading_menu.addAction(self.actionHeading4)
        heading_menu.addAction(self.actionHeading5)
        heading_menu.addAction(self.actionHeading6)

        format_menu.addSeparator()

        format_menu.addAction(self.actionOrderedList)
        format_menu.addAction(self.actionUnorderedList)

        # Create render menu
        rendering_menu = self.menuBar().addMenu("&Render")
        rendering_menu.addAction(self.actionToggleAutorenderDocument)
        rendering_menu.addAction(self.actionRenderDocument)
        rendering_menu.addAction(self.actionRenderProject)

        # Create help menu
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.actionAbout)

    def _createSidebar(self):
        """Create sidebar"""
        sidebar = QToolBar()
        sidebar.setContextMenuPolicy(Qt.PreventContextMenu)
        sidebar.setObjectName("MainWindow_SideBar")
        sidebar.setFloatable(False)
        sidebar.setMovable(False)
        sidebar.setIconSize(QSize(64, 64))

        sidebar.addAction(self.actionOpenHomePage)
        sidebar.addAction(self.actionOpenEditorPage)
        sidebar.addAction(self.actionOpenGitPage)

        self.addToolBar(Qt.LeftToolBarArea, sidebar)

    def _createStatusBar(self):
        """Create status bar"""
        status_bar = QStatusBar()
        status_bar.setObjectName("MainWindow_StatusBar")

        git_status_label = QLabel("GIT STATUS", status_bar)
        self.gitStatusWidget = git_status_label
        status_bar.addPermanentWidget(self.gitStatusWidget, 1)
        self.gitStatusWidget.hide()

        line_and_col_label = QLabel("LN, COL", status_bar)
        self.cursorPositionStatusWidget = line_and_col_label
        status_bar.addPermanentWidget(self.cursorPositionStatusWidget, 0)
        self.cursorPositionStatusWidget.hide()

        file_format_label = QLabel("FORMAT", status_bar)
        self.fileFormatStatusWidget = file_format_label
        status_bar.addPermanentWidget(self.fileFormatStatusWidget, 0)
        self.fileFormatStatusWidget.hide()

        file_lang_label = QLabel("LANGUAGE", status_bar)
        self.fileLanguageStatusWidget = file_lang_label
        status_bar.addPermanentWidget(self.fileLanguageStatusWidget, 0)
        self.fileLanguageStatusWidget.hide()

        self.setStatusBar(status_bar)

    def _createActions(self):
        """Create all actions and set them as attributes of this view"""

        icon_prefix = settingsManager.get_icon_prefix()

        # SIDEBAR ACTIONS
        #####################
        pages_action_group = QActionGroup(self)

        action = QAction(QIcon(f"icons_common:home.svg"), "Home page", self)
        action.setCheckable(True)
        pages_action_group.addAction(action)
        self.actionOpenHomePage = action

        action = QAction(QIcon(f"icons_common:document-papirus.svg"), "Editor page", self)
        action.setCheckable(True)
        pages_action_group.addAction(action)
        self.actionOpenEditorPage = action

        action = QAction(QIcon(f"icons_common:git-branch.svg"), "Git page", self)
        action.setCheckable(True)
        pages_action_group.addAction(action)
        self.actionOpenGitPage = action

        # FILE MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:document-new.svg"), "&New", self)
        action.setShortcut(QKeySequence.StandardKey.New)
        action.setStatusTip("Create a new document")
        # Connect
        self.actionNewDocument = action

        action = QAction("New project...", self)
        action.setStatusTip("Create a new project")
        # Connect
        self.actionNewProject = action

        action = QAction(QIcon(f"{icon_prefix}:document-open.svg"), "&Open", self)
        action.setShortcut(QKeySequence.StandardKey.Open)
        action.setStatusTip("Open a file")
        # Connect
        self.actionOpenDocument = action

        action = QAction("Open project", self)
        action.setStatusTip("Open a project")
        # Connect
        self.actionOpenProject = action

        action = QAction("Close project", self)
        action.setStatusTip("Close current project")
        # Connect
        self.actionCloseProject = action

        action = QAction(QIcon(f"{icon_prefix}:document-save.svg"), "&Save", self)
        action.setShortcut(QKeySequence.StandardKey.Save)
        action.setStatusTip("Save current document")
        # Connect
        self.actionSaveDocument = action

        action = QAction(QIcon(f"{icon_prefix}:document-save-as.svg"), "Save as...", self)
        action.setShortcut(QKeySequence.StandardKey.SaveAs)
        action.setStatusTip("Save current document as a new document")
        # Connect
        self.actionSaveDocumentAs = action

        action = QAction(QIcon(f"{icon_prefix}:configure.svg"), "Settings", self)
        action.setShortcut(QKeySequence.StandardKey.Preferences)
        action.setStatusTip("Configure settings")
        # Connect
        self.actionSettings = action

        action = QAction("&Exit", self)
        action.setStatusTip("Exit application")
        # Connect
        self.actionExit = action

        action = QAction("&Close document", self)
        action.setShortcut(QKeySequence.StandardKey.Close)
        action.setStatusTip("Close current document")
        # Connect
        self.actionCloseDocument = action

        action = QAction("Project settings", self)
        action.setStatusTip("Current project settings")
        # Connect
        self.actionProjectSettings = action

        # EDIT MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:edit-undo.svg"), "&Undo", self)
        action.setShortcut(QKeySequence.StandardKey.Undo)
        action.setStatusTip("Undo last action")
        # Connect
        self.actionUndo = action

        action = QAction(QIcon(f"{icon_prefix}:edit-redo.svg"), "&Redo", self)
        action.setShortcut(QKeySequence.StandardKey.Redo)
        action.setStatusTip("Redo last undid action")
        # Connect
        self.actionRedo = action

        action = QAction(QIcon(f"{icon_prefix}:edit-cut.svg"), "&Cut", self)
        action.setShortcut(QKeySequence.StandardKey.Cut)
        action.setStatusTip("Cut selection")
        # Connect
        self.actionCut = action

        action = QAction(QIcon(f"{icon_prefix}:edit-copy.svg"), "&Copy", self)
        action.setShortcut(QKeySequence.StandardKey.Copy)
        action.setStatusTip("Copy selection")
        # Connect
        self.actionCopy = action

        action = QAction(QIcon(f"{icon_prefix}:edit-paste.svg"), "&Paste", self)
        action.setShortcut(QKeySequence.StandardKey.Paste)
        action.setStatusTip("Paste from clipboard")
        # Connect
        self.actionPaste = action

        action = QAction(QIcon(f"{icon_prefix}:edit-delete.svg"), "&Delete", self)
        action.setShortcut(QKeySequence.StandardKey.Delete)
        action.setStatusTip("Delete selection")
        # Connect
        self.actionDelete = action

        action = QAction(QIcon(f"{icon_prefix}:edit-select-all.svg"), "&Select all", self)
        action.setShortcut(QKeySequence.StandardKey.SelectAll)
        action.setStatusTip("Select entire document")
        # Connect
        self.actionSelectAll = action

        action = QAction(QIcon(f"{icon_prefix}:edit-find.svg"), "&Find", self)
        action.setShortcut(QKeySequence.StandardKey.Find)
        action.setStatusTip("Find text")
        # Connect
        self.actionFind = action

        action = QAction(QIcon(f"{icon_prefix}:edit-find-replace.svg"), "&Replace", self)
        action.setShortcut(QKeySequence.StandardKey.Replace)
        action.setStatusTip("Find and replace text")
        # Connect
        self.actionFindReplace = action

        # INSERT MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:horizontal-rule.svg"), "Horizontal rule", self)
        action.setStatusTip("Insert a horizontal line")
        # Connect
        self.actionHorizontalRule = action

        action = QAction(QIcon(f"{icon_prefix}:insert-footnote.svg"), "Footnote...", self)
        action.setStatusTip("Insert a footnote")
        # Connect
        self.actionInsertFootnote = action

        action = QAction(QIcon(f"{icon_prefix}:table.svg"), "Table...", self)
        action.setStatusTip("Insert a table")
        # Connect
        self.actionAddTable = action

        action = QAction(QIcon(f"{icon_prefix}:link.svg"), "Link...", self)
        action.setStatusTip("Insert a link")
        # Connect
        self.actionLink = action

        action = QAction(QIcon(f"{icon_prefix}:text-frame-link.svg"), "Cross-reference...", self)
        action.setStatusTip("Insert a cross-reference")
        # Connect
        self.actionCrossRef = action

        action = QAction(QIcon(f"{icon_prefix}:insert-image.svg"), "Image...", self)
        action.setStatusTip("Insert an image")
        # Connect
        self.actionImage = action

        action = QAction("Citation...", self)
        action.setStatusTip("Insert a citation")
        # Connect
        self.actionCitation = action

        # FORMAT MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:format-text-italic.svg"), "&Italic", self)
        action.setShortcut(QKeySequence.StandardKey.Italic)
        action.setStatusTip("Make selected text italic")
        # Connect
        self.actionItalic = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-bold.svg"), "&Bold", self)
        action.setShortcut(QKeySequence.StandardKey.Bold)
        action.setStatusTip("Make selected text bold")
        # Connect
        self.actionBold = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-bold-italic.svg"), "&Bold and Italic", self)
        action.setStatusTip("Make selected text bold and italic")
        # Connect
        self.actionBoldItalic = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-strikethrough.svg"), "Strikethrough", self)
        action.setStatusTip("Make selected text strikethrough")
        # Connect
        self.actionStrikethrough = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-subscript.svg"), "Subscript", self)
        action.setStatusTip("Insert a subscript")
        # Connect
        self.actionSubscript = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-superscript.svg"), "Superscript", self)
        action.setStatusTip("Insert a superscript")
        # Connect
        self.actionSuperscript = action

        action = QAction(QIcon(f"{icon_prefix}:heading1.svg"), "Heading 1", self)
        action.setShortcut(QKeySequence.fromString("CTRL+1"))
        action.setStatusTip("Insert level 1 heading")
        # Connect
        self.actionHeading1 = action

        action = QAction(QIcon(f"{icon_prefix}:heading2.svg"), "Heading 2", self)
        action.setShortcut(QKeySequence.fromString("CTRL+2"))
        action.setStatusTip("Insert level 2 heading")
        # Connect
        self.actionHeading2 = action

        action = QAction(QIcon(f"{icon_prefix}:heading3.svg"), "Heading 3", self)
        action.setShortcut(QKeySequence.fromString("CTRL+3"))
        action.setStatusTip("Insert level 3 heading")
        # Connect
        self.actionHeading3 = action

        action = QAction(QIcon(f"{icon_prefix}:heading4.svg"), "Heading 4", self)
        action.setShortcut(QKeySequence.fromString("CTRL+4"))
        action.setStatusTip("Insert level 4 heading")
        # Connect
        self.actionHeading4 = action

        action = QAction(QIcon(f"{icon_prefix}:heading5.svg"), "Heading 5", self)
        action.setShortcut(QKeySequence.fromString("CTRL+5"))
        action.setStatusTip("Insert level 5 heading")
        # Connect
        self.actionHeading5 = action

        action = QAction(QIcon(f"{icon_prefix}:heading6.svg"), "Heading 6", self)
        action.setShortcut(QKeySequence.fromString("CTRL+6"))
        action.setStatusTip("Insert level 6 heading")
        # Connect
        self.actionHeading6 = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-blockquote.svg"), "Blockquote", self)
        action.setStatusTip("Insert a blockquote")
        # Connect
        self.actionBlockquote = action

        action = QAction(QIcon(f"{icon_prefix}:ord-list.svg"), "Ordered list", self)
        action.setStatusTip("Start an ordered list")
        # Connect
        self.actionOrderedList = action

        action = QAction(QIcon(f"{icon_prefix}:unord-list.svg"), "Unordered list", self)
        action.setStatusTip("Start an unordered list")
        # Connect
        self.actionUnorderedList = action

        action = QAction(QIcon(f"{icon_prefix}:format-text-code.svg"), "Code", self)
        action.setStatusTip("Format text as code")
        # Connect
        self.actionCode = action

        # RENDER MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:checkbox_off.svg"), "Autorender document", self)
        action.setStatusTip("Toggle document autorendering")
        action.setCheckable(True)
        # Connect
        self.actionToggleAutorenderDocument = action

        action = QAction("Render document", self)
        action.setStatusTip("Render current document")
        # Connect
        self.actionRenderDocument = action

        action = QAction("Render project", self)
        action.setStatusTip("Render current project")
        # Connect
        self.actionRenderProject = action

        # VIEW MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:checkbox_off.svg"), "Project tab", self)
        action.setStatusTip("Show/hide project tab")
        action.setCheckable(True)
        self.actionToggleProjectTab = action

        action = QAction(QIcon(f"{icon_prefix}:checkbox_off.svg"), "Document preview", self)
        action.setStatusTip("Show/hide document preview")
        action.setCheckable(True)
        self.actionToggleDocumentPreview = action

        action = QAction(QIcon(f"{icon_prefix}:checkbox_off.svg"), "Git dock", self)
        action.setStatusTip("Show/hide Git dock")
        action.setCheckable(True)
        self.actionToggleGitDock = action

        action = QAction(QIcon(f"{icon_prefix}:checkbox_off.svg"), "Console dock", self)
        action.setStatusTip("Show/hide console preview")
        action.setCheckable(True)
        self.actionToggleConsoleDock = action

        # HELP MENU ACTIONS
        #####################
        action = QAction(QIcon(f"{icon_prefix}:help-about.svg"), "&About", self)
        action.setStatusTip("Show about message")
        # Connect
        self.actionAbout = action

    def _createCentralWidget(self):
        """Create central widget of the window"""
        self.mainStackedWidget = QStackedWidget(self)

        self.welcomePage = QScrollArea(self)
        #self.welcomePage = QWidget(self)
        self.editorPage = QMainWindow(self)
        self.gitPage = QMainWindow(self)

        self.mainStackedWidget.addWidget(self.welcomePage)
        self.mainStackedWidget.addWidget(self.editorPage)
        self.mainStackedWidget.addWidget(self.gitPage)

        self.setCentralWidget(self.mainStackedWidget)

        self._createWelcomePage()
        self._createEditorPage()
        self._createGitPage()

    def _createEditorPage(self):
        self._createEditorPageToolbar()

        project_structure_dock = ProjectDockView(self.editorPage)
        self.editorPage.addDockWidget(Qt.LeftDockWidgetArea, project_structure_dock)
        project_structure_dock.hide()

        document_preview_dock = DocumentPreviewDockView(self)
        self.editorPage.addDockWidget(Qt.RightDockWidgetArea, document_preview_dock)
        document_preview_dock.hide()

        editors_tab_widget = QTabWidget(self)
        editors_tab_widget.setObjectName("MainWindow_EditorsTabWidget")
        self.editorPage.setCentralWidget(editors_tab_widget)

        # Set attributes
        self.editorsTabWidget = editors_tab_widget
        self.projectDock = project_structure_dock
        self.documentPreviewDock = document_preview_dock

    def _createEditorPageToolbar(self):
        """Creates the toolbar for Editor page"""
        toolbar = QToolBar(self)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        toolbar.addAction(self.actionItalic)
        toolbar.addAction(self.actionBold)
        toolbar.addAction(self.actionBoldItalic)
        toolbar.addAction(self.actionStrikethrough)
        toolbar.addSeparator()

        toolbar.addAction(self.actionSuperscript)
        toolbar.addAction(self.actionSubscript)
        toolbar.addAction(self.actionCode)
        toolbar.addAction(self.actionBlockquote)
        toolbar.addSeparator()

        toolbar.addAction(self.actionHeading1)
        heading_action_button = toolbar.widgetForAction(self.actionHeading1)
        heading_action_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        heading_action_button.addAction(self.actionHeading2)
        heading_action_button.addAction(self.actionHeading3)
        heading_action_button.addAction(self.actionHeading4)
        heading_action_button.addAction(self.actionHeading5)
        heading_action_button.addAction(self.actionHeading6)

        toolbar.addAction(self.actionOrderedList)
        toolbar.addAction(self.actionUnorderedList)
        toolbar.addSeparator()

        toolbar.addAction(self.actionHorizontalRule)
        toolbar.addAction(self.actionInsertFootnote)
        toolbar.addAction(self.actionAddTable)
        toolbar.addAction(self.actionLink)
        toolbar.addAction(self.actionCrossRef)
        toolbar.addAction(self.actionImage)
        toolbar.addAction(self.actionCitation)
        toolbar.addSeparator()

        toolbar.addAction(self.actionRenderDocument)
        toolbar.addAction(self.actionRenderProject)

        self.editorPage.addToolBar(toolbar)

    def _createGitPage(self):
        # Create git dock
        git_dock = GitDockView(self.gitPage)
        self.gitPage.addDockWidget(Qt.LeftDockWidgetArea, git_dock)
        git_dock.hide()
        self.gitDock = git_dock

        # Create git output display widget
        text_edit = QTextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.hide()

        # Create git placeholder widget
        self._createGitPlaceholderWidget()

        self.gitPage.setCentralWidget(self.gitPlaceholderWidget)

        # Set attributes
        self.MainGitTextEdit = text_edit

    def _createGitPlaceholderWidget(self):

        git_placeholder_widget = QWidget(self)

        layout = QGridLayout(git_placeholder_widget)
        layout.setAlignment(Qt.AlignCenter)

        info_label = QLabel("Not Git repository has been loaded. Use buttons below to create a new repository or use " +
                            "an existing one", git_placeholder_widget)
        info_label.setWordWrap(True)
        layout.addWidget(info_label, 0, 0, 1, 2)

        create_new_repository_label = QLabel("Create a new repository in project folder", git_placeholder_widget)
        layout.addWidget(create_new_repository_label, 1, 0, 1, 1)

        create_new_repository_button = QPushButton("Create", git_placeholder_widget)
        layout.addWidget(create_new_repository_button, 1, 1, 1, 1)

        connect_remote_label = QLabel("Connect existing remote repository", git_placeholder_widget)
        layout.addWidget(connect_remote_label, 2, 0, 1, 1)

        connect_remote_button = QPushButton("Connect...", git_placeholder_widget)
        layout.addWidget(connect_remote_button, 2, 1, 1, 1)

        # Set attributes
        self.gitPlaceholderWidget = git_placeholder_widget
        self.gitPlaceholderCreateRepoButton = create_new_repository_button
        self.gitPlaceholderConnectRemoteButton = connect_remote_button

    def _createWelcomePage(self):

        def create_h2_label(text: str, parent):
            label = QLabel(text, parent)
            label.setObjectName("WelcomePage_Heading2")
            return label

        def create_ext_link_label(text: str, parent):
            label = QLabel(text, parent)
            label.setOpenExternalLinks(True)
            return label

        widget = QWidget(self.welcomePage)
        widget.setObjectName("WelcomePage_ContainerWidget")
        layout = QGridLayout(widget)
        layout.setColumnMinimumWidth(0, 400)
        layout.setColumnMinimumWidth(1, 400)

        # Title
        title_label = QLabel("Manuwrite", widget)
        title_label.setObjectName("WelcomePage_Title")
        layout.addWidget(title_label, 0, 0, 1, 2)

        # Subtitle
        subtitle_label = QLabel("Next generation of scholarly writing", widget)
        subtitle_label.setObjectName("WelcomePage_Subtitle")
        layout.addWidget(subtitle_label, 1, 0, 1, 2)

        # "Start" block
        start_layout = QVBoxLayout()

        start_label = create_h2_label("Start", widget)
        start_layout.addWidget(start_label)

        new_file_label = QLabel(widget)
        new_file_label.setText('Create a <a href="#new-file">New file</a> or a <a href="#new-project">New project</a>')
        start_layout.addWidget(new_file_label)

        clone_repo_label = QLabel('<a href="#clone">Clone</a> a remote repository', widget)
        start_layout.addWidget(clone_repo_label)

        layout.addLayout(start_layout, 2, 0, 1, 1)

        # "Recent" block
        recent_layout = QVBoxLayout()

        recent_label = create_h2_label("Recent", widget)
        recent_layout.addWidget(recent_label)

        no_recent_label = QLabel("No recent files or projects")
        recent_layout.addWidget(no_recent_label)

        layout.addLayout(recent_layout, 3, 0, 1, 1)

        # "Help" block
        help_layout = QVBoxLayout()

        help_label = create_h2_label("Help", widget)
        help_layout.addWidget(help_label)

        help_layout.addWidget(create_ext_link_label('<a href="https://www.TMP.com">Manuwrite tutorial</a>', widget))

        label = create_ext_link_label('<a href="https://www.markdownguide.org/basic-syntax">Markdown reference</a>', widget)
        help_layout.addWidget(label)

        label = create_ext_link_label('<a href="https://pandoc.org/MANUAL.html">Pandoc user\'s guide</a>', widget)
        help_layout.addWidget(label)

        help_layout.addWidget(create_ext_link_label('<a href="https://training.github.com/downloads/github-git-' +
                                                    'cheat-sheet/">Git cheatsheet</a> and a <a href="https://git-scm' +
                                                    '.com/docs">complete reference</a>', widget))

        label = create_ext_link_label('<a href="https://github.com/lasest/manuwrite">Manuwrite repository</a>', widget)
        help_layout.addWidget(label)

        layout.addLayout(help_layout, 4, 0, 1, 1)

        # Archive block
        archive_layout = QVBoxLayout()

        archive_label = create_h2_label("Archive", widget)
        archive_layout.addWidget(archive_label)

        view_projects_widget = WelcomePageInfoBlock(widget)
        view_projects_widget.set_title("View projects")
        view_projects_widget.set_description("Show information about your manuwrite projects")
        archive_layout.addWidget(view_projects_widget)

        layout.addLayout(archive_layout, 2, 1, 1, 1)

        # Customize block
        customize_layout = QVBoxLayout()

        customize_label = create_h2_label("Customize", widget)
        customize_layout.addWidget(customize_label)

        csl_styles_widget = WelcomePageInfoBlock(widget)
        csl_styles_widget.set_title("CSL styles")
        csl_styles_widget.set_description("Install additional CSL styles")
        customize_layout.addWidget(csl_styles_widget)

        render_styles_widget = WelcomePageInfoBlock(widget)
        render_styles_widget.set_title("Rendering styles")
        render_styles_widget.set_description("Install additional manuscript rendering styles")
        customize_layout.addWidget(render_styles_widget)

        templates_widget = WelcomePageInfoBlock(widget)
        templates_widget.set_title("Project templates")
        templates_widget.set_description("Install additional project templates")
        customize_layout.addWidget(templates_widget)

        layout.addLayout(customize_layout, 3, 1, 2, 1)

        self.welcomePage.setWidget(widget)
        self.welcomePage.setAlignment(Qt.AlignCenter)

    def _createConsoleDock(self):
        self.consoleDock = ConsoleDockView(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.consoleDock)
        self.consoleDock.hide()

    def _apply_settings(self):
        settings = settingsManager.appSettings

        self.move(settings.mainWindow.posX, settings.mainWindow.posY)
        self.resize(settings.mainWindow.width, settings.mainWindow.height)
