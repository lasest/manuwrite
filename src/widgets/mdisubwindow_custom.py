from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtGui import QMoveEvent, QCloseEvent

import common


class MdiSubWindow_custom(QMdiSubWindow):

    def __init__(self, parent, flags):
        super(MdiSubWindow_custom, self).__init__(parent, flags)

        self.MdiSubwindowSignal = common.communicator.MdiSubwindowSignal

    def moveEvent(self, moveEvent: QMoveEvent) -> None:
        super(MdiSubWindow_custom, self).moveEvent(moveEvent)
        self.lower()

        self.MdiSubwindowSignal.emit()
