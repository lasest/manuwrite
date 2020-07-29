from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QToolTip
from PyQt5.QtCore import QSize, QRect, Qt, QObject, pyqtSignal, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QTextFormat, QTextCursor

from components.highlighter import MarkdownHighlighter
from components.thread_manager import ThreadManager


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
        self.citations = dict()
        self.ThreadManager = ThreadManager(max_threads=4)
        self.ThreadManager.manubotCiteThreadFinished.connect(self.on_manubot_thread_finished)


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
        point = self.viewport().mapToGlobal(self.cursorRect().topLeft())
        QToolTip.showText(point, "")

        cursor = self.textCursor()

        current_line_text = cursor.block().text()
        current_line_tags = self.highlighter.get_tags(current_line_text)
        for tag in current_line_tags:
            tag_text = current_line_text[tag[0]:tag[0] + tag[1]]
            tag_text = tag_text[2:-1]
            if tag[2] == "citation":
                if tag_text not in self.citations:
                    self.citations[tag_text] = ""
                    self.ThreadManager.get_citation(tag_text)
                    QToolTip.showText(point, "Fetching citation info...")
                elif self.citations[tag_text] == "" and cursor.position() >= tag[0] and cursor.position() <= (tag[1] + tag[0]):
                    QToolTip.showText(point, "Fetching citation info...")
                else:
                    QToolTip.showText(point, self.citations[tag_text])

        extraSelections = []

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

    def on_TextEditor_textChanged(self) -> None:
        self.text_changed = True

    def insert_text_at_cursor(self, text: str, move_center=False) -> None:
        initial_pos = self.textCursor().position()
        self.textCursor().insertText(text)

        if move_center:
            cursor = self.textCursor()
            cursor.setPosition(initial_pos + int(len(text) / 2))
            self.setTextCursor(cursor)

    def insert_text_at_line_beginning(self, text: str) -> None:
        init_pos = self.textCursor().position()
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        self.setTextCursor(cursor)
        cursor.insertText(text)

        cursor.setPosition(init_pos + len(text))
        self.setTextCursor(cursor)

    def insert_text_at_selection_bound(self, text: str) -> None:
        start = self.textCursor().selectionStart()
        end = self.textCursor().selectionEnd()
        self.textCursor().clearSelection()

        cursor = self.textCursor()
        cursor.setPosition(end)
        self.setTextCursor(cursor)
        cursor.insertText(text)

        cursor = self.textCursor()
        cursor.setPosition(start)
        self.setTextCursor(cursor)
        cursor.insertText(text)

    def insert_text_at_empty_line(self, text: str) -> None:
        if self.textCursor().block().text() == "":
            self.textCursor().insertText(text)
        else:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.EndOfLine)
            cursor.insertText("\n{}".format(text))

    def insert_double_tag(self, tag: str) -> None:
        if len(self.textCursor().selection().toPlainText()) == 0:
            self.insert_text_at_cursor(tag * 2, move_center=True)
        else:
            self.insert_text_at_selection_bound(tag)

    def get_citation_for_key(self, citekey: str):
        thread = ManubotThread(self, citekey)
        self.manubot_threads.append(thread)
        thread.finished.connect(self.on_manubot_thread_finished)
        print("Starting thread")
        thread.start()

    @pyqtSlot(str, str)
    def on_manubot_thread_finished(self, citekey: str, citation: str):
        self.citations[citekey] = citation
