from PyQt5.QtWidgets import QDialog, QAbstractButton, QFileDialog
from PyQt5.QtCore import pyqtSlot

from forms.ui_add_image_dialog import Ui_AddImageDialog


class AddImageDialog(QDialog):

    def __init__(self, default_width: int, default_height: int, default_dir: str):

        super().__init__()
        self.ui = Ui_AddImageDialog()
        self.ui.setupUi(self)

        # Set attributes
        self.image_text: str = ""
        self.image_path: str = ""
        self.image_width: int = 0
        self.image_height: int = 0
        self.default_dir: str = default_dir

        # Prepare ui elements
        self.ui.WidthLineEdit.setText(str(default_width))
        self.ui.HeightLineEdit.setText(str(default_height))

        self.ui.ImageTextLineEdit.setFocus()

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button) -> None:
        """Saves values from ui elements to objects attributes"""

        self.image_text = self.ui.ImageTextLineEdit.text()
        self.image_path = self.ui.ImagePathLineEdit.text()
        if self.ui.HeightLineEdit.text():
            self.image_height = int(self.ui.HeightLineEdit.text())
        if self.ui.WidthLineEdit.text():
            self.image_width = int(self.ui.WidthLineEdit.text())

    @pyqtSlot()
    def on_OpenFileButton_clicked(self) -> None:
        """Calls open file dialog for the user to choose image"""

        # TODO: add filters to the dialog
        path = QFileDialog.getOpenFileName(self, "Choose image", self.default_dir,
                                           "JPEG image (*.jpg *.jpeg *.jpe *jfif);; PNG image (*.png);;" +
                                           "SVG image (*.svg);;GIF image (*.gif);;All files (*.*)")
        if path:
            self.ui.ImagePathLineEdit.setText(path[0])
