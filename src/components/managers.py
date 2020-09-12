from PyQt5.QtWidgets import QApplication

import components.project_manager
import components.settings_manager
import components.thread_manager
import components.git_manager

# Define all managers that will be used throughout the program. Manager objects are persistent, i.e will not be
# recreated

ThreadManager = components.thread_manager.ThreadManager()
ProjectManager = components.project_manager.ProjectManager(ThreadManager)
SettingsManager = components.settings_manager.SettingsManager()
GitManager = components.git_manager.GitManager()
