from PyQt5.QtWidgets import (QStackedWidget, QWidget, QGridLayout, QListView, QPushButton, QPlainTextEdit, QVBoxLayout,
                             QTreeView)

from manuwrite.views.dock_view import DockView, TitleWidgetTypes


class GitDockView(DockView):

    def __init__(self, parent=None):

        super(GitDockView, self).__init__(title_widget_type=TitleWidgetTypes.COMBOBOX, parent=parent)

        self.add_title_option("Commit")
        self.add_title_option("Repository files")
        self.add_title_option("Branches")
        self.add_title_option("Remotes")

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        self.widget().setLayout(layout)

        stacked_widget = QStackedWidget(self)
        self.widget().layout().addWidget(stacked_widget)
        self.stackedWidget = stacked_widget

        self._create_commit_tab()
        self._create_repository_files_tab()
        self._create_branches_tab()
        self._create_remote_tab()

    def _create_commit_tab(self):
        widget = QWidget(self)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)

        changed_files_list_view = QListView(self.stackedWidget)
        container_layout.addWidget(changed_files_list_view)

        controls_layout = QGridLayout()
        controls_layout.setContentsMargins(5, 5, 5, 5)

        stage_button = QPushButton("Stage", self.stackedWidget)
        controls_layout.addWidget(stage_button, 0, 0, 1, 1)

        unstage_button = QPushButton("Unstage", self.stackedWidget)
        controls_layout.addWidget(unstage_button, 0, 1, 1, 1)

        stage_all_button = QPushButton("Stage all", self.stackedWidget)
        controls_layout.addWidget(stage_all_button, 1, 0, 1, 1)

        unstage_all_button = QPushButton("Unstage all", self.stackedWidget)
        controls_layout.addWidget(unstage_all_button, 1, 1, 1, 1)

        # Create commit message text edit
        commit_text_edit = QPlainTextEdit(self.stackedWidget)
        document = commit_text_edit.document()
        line_height = document.documentLayout().blockBoundingRect(document.begin()).height()
        commit_text_edit.setFixedHeight(line_height * 3)
        commit_text_edit.setPlaceholderText("Commit message...")
        controls_layout.addWidget(commit_text_edit, 2, 0, 1, 2)

        commit_button = QPushButton("Commit", self.stackedWidget)
        controls_layout.addWidget(commit_button, 3, 0, 1, 2)

        container_layout.addLayout(controls_layout)

        widget.setLayout(container_layout)
        self.stackedWidget.addWidget(widget)

        # Set attributes
        self.changesFilesListView = changed_files_list_view
        self.stageButton = stage_button
        self.unstageButton = unstage_button
        self.stageAllButton = stage_all_button
        self.unstageAllButton = unstage_all_button
        self.commitTextEdit = commit_text_edit
        self.commitButton = commit_button

    def _create_repository_files_tab(self):
        repository_files_tree_view = QTreeView(self.stackedWidget)
        self.stackedWidget.addWidget(repository_files_tree_view)

        # Set attributes
        self.repositoryFilesTreeView = repository_files_tree_view

    def _create_branches_tab(self):
        branches_list_view = QListView(self.stackedWidget)
        self.stackedWidget.addWidget(branches_list_view)

        # Set attributes
        self.branchesListView = branches_list_view

    def _create_remote_tab(self):
        remotes_list_view = QListView(self.stackedWidget)
        self.stackedWidget.addWidget(remotes_list_view)

        # Set attributes
        self.remotesListView = remotes_list_view
