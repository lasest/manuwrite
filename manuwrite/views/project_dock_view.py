from PyQt5.QtWidgets import QTreeView, QComboBox, QWidget, QVBoxLayout, QStackedWidget

from manuwrite.views.dock_view import DockView, TitleWidgetTypes


class ProjectDockView(DockView):
    
    def __init__(self, parent=None):
        
        super(ProjectDockView, self).__init__(title_widget_type=TitleWidgetTypes.COMBOBOX, parent=parent)

        self.set_title("Project dock")

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        self.widget().setLayout(layout)

        self.stackedWidget = QStackedWidget(self)
        self.widget().layout().addWidget(self.stackedWidget)

        self.add_title_option("Project files")
        self.add_title_option("File structure")
        self.add_title_option("Project structure")

        self._create_project_files_tab()
        self._create_file_structure_tab()
        self._create_project_structure_tab()

    def _create_project_files_tab(self):
        files_tree_view = QTreeView()
        self.stackedWidget.addWidget(files_tree_view)

        self.FilesTreeView = files_tree_view

    def _create_file_structure_tab(self):
        file_structure_tree_view = QTreeView()
        self.stackedWidget.addWidget(file_structure_tree_view)

        self.FileStructureTreeView = file_structure_tree_view

    def _create_project_structure_tab(self):
        project_structure_tree_view = QTreeView()
        self.stackedWidget.addWidget(project_structure_tree_view)

        self.ProjectStructureTreeView = project_structure_tree_view
