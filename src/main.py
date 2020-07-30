import sys
#import os

from PyQt5.QtWidgets import QApplication

from gui_components.main_window import MainWindow


def main():
    #args = ["--blink-settings=darkMode=4", "darkModeImagePolicy=2"]
    #os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
    #args = ["--qt-flag", "ignore-gpu-blacklist", "--qt-flag", "enable-gpu-rasterization", "--qt-flag", "enable-native-gpu-memory-buffers", "--qt-flag", "num-raster-threads=4"]
    app = QApplication(sys.argv)
    window = MainWindow()
    #print(app.arguments())
    window.show()
    sys.exit(app.exec_())


main()
