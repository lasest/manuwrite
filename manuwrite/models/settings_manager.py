from dataclasses import dataclass
from enum import Enum


class ThemeColor(Enum):
    Dark = 0
    Light = 1


@dataclass()
class MainWindowSettings:
    posX: int = 0
    posY: int = 0
    width: int = 1920
    height: int = 1080

    consoleDockHeight: int = 250
    consoleDockToggle: bool = False

    projectDockWidth: int = 300
    projectDockToggle: bool = True

    documentPreviewDockWidth: int = 450
    documentPreviewDockToggle: int = True

    gitDockWidth: int = 300
    gitDockToggle: bool = True


@dataclass()
class StyleSettings:
    themeColor: ThemeColor = ThemeColor.Dark


@dataclass()
class AppSettings:
    mainWindow: MainWindowSettings = MainWindowSettings()
    styleSettings: StyleSettings = StyleSettings()


class SettingsManager:

    def __init__(self):
        self.appSettings = AppSettings()

    def get_icon_prefix(self):
        if self.appSettings.styleSettings.themeColor == ThemeColor.Dark:
            return "icons_dark"
        else:
            return "icons_light"
