from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from components.highlighter import MarkdownHighlighter


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor


    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)


    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class TextEditor(QPlainTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.textChanged.connect(self.on_TextEditor_textChanged)
        self.selectionChanged.connect(self.highlightCurrentLine)

        self.highlighter = MarkdownHighlighter(self.document())
        self.updateLineNumberAreaWidth(0)
        self.text_changed = False

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.document().blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        if digits < 4:
            digits = 4
        space = 10 + self.fontMetrics().width('9') * digits
        return space


    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                        self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        color = self.palette().color(self.palette().Dark)
        painter.fillRect(event.rect(), color)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                color = self.palette().color(self.palette().Text)
                painter.setPen(color)
                painter.drawText(5, top, self.lineNumberArea.width(), height,
                                 Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []

        cursor = self.textCursor()
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        cursor.setPosition(selection_start)
        start_line = cursor.blockNumber()
        cursor.setPosition(selection_end)
        end_line = cursor.blockNumber()

        if start_line != end_line:
            self.setExtraSelections([QTextEdit.ExtraSelection()])
            return

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = self.palette().color(self.palette().AlternateBase).darker(70)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def on_TextEditor_textChanged(self):
        self.text_changed = True
