import copy

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QToolTip
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal, QPoint, pyqtSlot, QTimer, QUrl
from PyQt5.QtGui import QPainter, QTextFormat, QTextCursor, QMouseEvent, QFont, QColor, QTextCharFormat
from PyQt5.QtWebEngineWidgets import QWebEngineView

from components.highlighter import MarkdownHighlighter
from components.thread_manager import ThreadManager
import defaults


class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event) -> None:
        """Calls editor to draw line number area"""
        self.editor.lineNumberAreaPaintEvent(event)


class TextEditor(QPlainTextEdit):

    FileStrucutreUpdated = pyqtSignal(dict)

    def __init__(self, parent, display_widget: QWebEngineView, settings_manager, thread_manager: ThreadManager):

        super().__init__(parent)

        # Set attributes
        self.lineNumberArea = LineNumberArea(self)
        self.display_widget = display_widget
        self.highlighter = MarkdownHighlighter(self.document(), settings_manager)
        self.text_changed = False
        self.ThreadManager = thread_manager
        self.setMouseTracking(True)
        self.InputTimer = QTimer(self)
        self.DocumentParsingTimer = QTimer(self)
        self.SettingsManager = settings_manager
        self.is_current_editor = False
        self.is_parsing_document = False
        self.char_format = QTextCharFormat(self.currentCharFormat())
        self.document_structure: dict = copy.deepcopy(defaults.document_info_template)

        self.ColorSchema = self.SettingsManager.color_schema

        # Connect signals to slots
        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.on_TextEditor_CursorMoved)
        self.textChanged.connect(self.on_TextEditor_textChanged)
        self.selectionChanged.connect(self.on_TextEditor_CursorMoved)
        self.InputTimer.timeout.connect(self.on_InputTimer_timeout)
        self.DocumentParsingTimer.timeout.connect(self.on_DocumentParsingTimer_timeout)

        self.updateLineNumberAreaWidth(0)
        self.InputTimer.setSingleShot(True)
        self.DocumentParsingTimer.setSingleShot(True)
        self.read_settings()

        # Trigger it to highlight current line, when the editor is first opened
        self.on_TextEditor_CursorMoved()

    def lineNumberAreaWidth(self) -> int:
        """Returns the width of the line number area depending on the number of digits that need to be displayed"""

        digits = 1
        line_count = max(1, self.document().blockCount())
        while line_count >= 10:
            line_count /= 10
            digits += 1

        if digits < 4:
            digits = 4

        space = 10 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _) -> None:
        """Updates the width of line number area when the number of lines in the document changes"""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy) -> None:
        """Updates line number are when the user scrolls or something else happens (not sure how it works)"""

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event) -> None:
        """Updates line numbers area when the editor is resized"""

        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                        self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event) -> None:
        """Paints the line number area of the editor"""

        painter = QPainter(self.lineNumberArea)
        color = QColor(self.ColorSchema["Editor_colors"]["linenumber_area"]["color"])
        painter.fillRect(event.rect(), color)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                color = QColor(self.ColorSchema["Editor_colors"]["linenumber_text"]["color"])
                painter.setPen(color)
                painter.drawText(5, top, self.lineNumberArea.width(), height,
                                 Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def on_TextEditor_CursorMoved(self) -> None:
        """Highlights the current line and shows a tooltip if a citation or an image is under text cursor"""

        # Display tool tip for image or citation
        point = self.viewport().mapToGlobal(self.cursorRect().topLeft())
        cursor = self.textCursor()
        self.display_tooltips_for_cursor(cursor, point)

        # Don't highlight if multiple lines are selected
        extraSelections = []

        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        cursor.setPosition(selection_start)
        start_line_number = cursor.blockNumber()
        cursor.setPosition(selection_end)
        end_line_number = cursor.blockNumber()

        if start_line_number != end_line_number:
            self.setExtraSelections([QTextEdit.ExtraSelection()])
            return

        # Highlight current line
        selection = QTextEdit.ExtraSelection()

        lineColor = QColor(self.ColorSchema["Editor_colors"]["current_line"]["color"])

        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def on_TextEditor_textChanged(self) -> None:
        """Set text_changed property to True and start InputTimer. When the timer finishes, the document will be
        rendered, if the settings do not say otherwise (disable autorender)"""

        self.text_changed = True
        if self.SettingsManager.get_setting_value("Render/Autorender"):
            self.InputTimer.start(self.SettingsManager.get_setting_value("Render/Autorender delay"))

    def insert_text_at_cursor(self, text: str, move_center=False) -> None:
        """Inserts text at current cursor position. If move_center is set to True, moves cursor to the center of
        inserted string after insertion"""

        initial_pos = self.textCursor().position()
        self.textCursor().insertText(text)

        if move_center:
            cursor = self.textCursor()
            cursor.setPosition(initial_pos + int(len(text) / 2))
            self.setTextCursor(cursor)

    def insert_text_at_line_beginning(self, text: str) -> None:
        """Inserts text at the beginning of the current line. Tries to keep the cursor position in the string the
        same"""

        init_pos = self.textCursor().position()
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        self.setTextCursor(cursor)
        cursor.insertText(text)

        cursor.setPosition(init_pos + len(text))
        self.setTextCursor(cursor)

    def insert_text_at_selection_bound(self, text: str) -> None:
        """Inserts given text at the beginning and at the end of the current selection"""

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

    def insert_text_at_empty_paragraph(self, text: str) -> None:
        """Inserts text in an empty paragraph"""

        line_number = self.textCursor().blockNumber()
        if line_number:
            previous_line = self.document().findBlockByNumber(line_number - 1).text()
        else:
            previous_line = ""

        if self.textCursor().block().text() == "" and previous_line == "":
            self.textCursor().insertText(text)
        elif self.textCursor().block().text() == "" and previous_line != "":
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.EndOfLine)
            cursor.insertText("\n{}".format(text))
        else:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.EndOfLine)
            cursor.insertText("\n\n{}".format(text))

    def insert_double_tag(self, tag: str) -> None:
        """Inserts a double tag in the text (i.e. italic, bold, etc). Inserts at cursor if no text is selected, or at
        the selection boundaries if there is a selection"""

        if len(self.textCursor().selection().toPlainText()) == 0:
            self.insert_text_at_cursor(tag * 2, move_center=True)
        else:
            self.insert_text_at_selection_bound(tag)

    def display_tooltips_for_cursor(self, cursor: QTextCursor, display_point: QPoint) -> None:
        """Displays a tooltip at current cursor position if a citation tag or an image tag is under cursor. Hides
        the tooltip if no tags are under cursor"""

        def is_inside_tag(tag, cursor_pos) -> bool:
            """Returns True if given cursor position is inside tag boundaries"""
            return tag[0] <= cursor_pos < (tag[1] + tag[0])

        show_citation_tooltips = self.SettingsManager.get_setting_value("Editor/Show citation tooltips")
        show_image_tooltips = self.SettingsManager.get_setting_value("Editor/Show image tooltips")
        hide_tooltip = True
        current_line_text = cursor.block().text()
        current_line_tags = self.highlighter.get_tags(current_line_text)
        cursor_pos = cursor.positionInBlock()

        for tag in current_line_tags:
            tag_text = current_line_text[tag[0]:tag[0] + tag[1]]

            if show_citation_tooltips and tag[2] == "citation" and is_inside_tag(tag, cursor_pos):
                # Remove brackets and @ symbol from the tag text
                tag_text = tag_text[2:-1]

                # TODO: use an extractor here?
                # If the citekey is not in self.document_info["citations"] or doesn't have a citation text yet, show
                # placeholder
                if tag_text not in self.document_structure["citations"]:
                    QToolTip.showText(display_point, "Fetching citation info...", self, QRect(), 5000)
                    hide_tooltip = False

                elif tag_text in self.document_structure["citations"] and self.document_structure["citations"][tag_text]["citation"] == "":
                    QToolTip.showText(display_point, "Fetching citation info...", self, QRect(), 5000)
                    hide_tooltip = False

                # If the citekey is in self.document_info["citations"] and citation show citation info
                else:
                    QToolTip.showText(display_point, self.document_structure["citations"][tag_text]["citation"], self, QRect(), 5000)
                    hide_tooltip = False

            elif show_image_tooltips and tag[2] == "image" and is_inside_tag(tag, cursor_pos):
                # Do nothing
                if not self.SettingsManager.get_setting_value("Editor/Show citation tooltips"):
                    return

                path = tag_text[tag_text.find("(") + 1:tag_text.find(")")]
                width = self.SettingsManager.get_setting_value("Editor/Image tooltip width")
                height = self.SettingsManager.get_setting_value("Editor/Image tooltip height")
                QToolTip.showText(display_point, f"<img src='{path}' width='{width}' height='{height}'>",
                                  self, QRect(), 5000)
                hide_tooltip = False

        # Hide tooltip if no image or citation is under cursor
        if hide_tooltip:
            QToolTip.hideText()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Displays tooltips if citation or image tags are under mouse cursor"""

        pos = event.pos()
        pos.setX(pos.x() - self.viewportMargins().left())
        pos.setY(pos.y() - self.viewportMargins().top())
        cursor = self.cursorForPosition(pos)

        self.display_tooltips_for_cursor(cursor, event.globalPos())
        super(TextEditor, self).mouseMoveEvent(event)

    def render_to_html(self) -> None:
        """Asks thread manager to render document contents to html"""

        self.ThreadManager.markdown_to_html(self.toPlainText(), self.on_pandoc_thread_finished)

    def read_settings(self) -> None:
        """Read settings and apply them"""

        font = QFont(self.SettingsManager.get_setting_value("Editor/Font name"))
        font.setPointSize(self.SettingsManager.get_setting_value("Editor/Font size"))
        self.setFont(font)

        if self.ColorSchema:
            bg_color = self.ColorSchema['Editor_colors']['background']['color']
            text_color = self.ColorSchema['Editor_colors']['text']['color']

            self.setStyleSheet(f"QPlainTextEdit {{background-color: {bg_color}; color: {text_color}}}")
            self.char_format.setForeground(QColor(self.ColorSchema['Editor_colors']['text']['color']))

    # NOT CURRENTLY USED
    def apply_format_to_line(self, line_number: int, format: QTextCharFormat, block_state: int = None) -> None:
        """Applies given format and block state to the line at given block number"""
        cursor = self.textCursor()
        cursor.setPosition(self.document().findBlockByNumber(line_number).position())
        cursor.select(QTextCursor.LineUnderCursor)
        self.setTextCursor(cursor)

        cursor.mergeCharFormat(format)

        if block_state is not None:
            self.document().findBlockByNumber(line_number).setUserState(block_state)

    def parse_document(self) -> None:
        """Asks ThreadManager to parse the document for structure if the document isn't already being parsed"""
        if not self.is_parsing_document:
            self.ThreadManager.parse_markdown_document(self.document(), self.on_parsing_document_finished)
            self.is_parsing_document = True

    def is_cursor_in_sentence(self) -> bool:
        """Determines if the cursor is inside a sentence. For example to determine if next word should be
        title-cased."""
        line_number = self.textCursor().blockNumber()
        current_line = self.document().findBlockByNumber(line_number).text()
        cursor_pos = self.textCursor().positionInBlock()

        if not current_line:
            return False

        in_sentence = True
        for index in range(cursor_pos - 1, -1, -1):
            current_symbol = current_line[index]

            if current_symbol in (" ", "\t"):
                continue
            if current_symbol in {".", "!", "?"}:
                in_sentence = False

            break

        return in_sentence

    @pyqtSlot(str)
    def on_pandoc_thread_finished(self, html: str) -> None:
        """Updates document preview when pandoc thread finishes"""
        # TODO: Change to use value from settings
        self.display_widget.setHtml(html, QUrl("file:///home/lasest/Working folder/manuwrite/style.css"))

    @pyqtSlot()
    def on_InputTimer_timeout(self) -> None:
        """Renders document to html when the user stops typing if settings allow this"""

        self.render_to_html()

    @pyqtSlot(str, str)
    def on_manubot_thread_finished(self, citation_info: dict) -> None:
        """Adds the citation returned by manubot thread to the self.citations dictionary when the thread is finished"""
        citekey = citation_info["citekey"]
        citation = citation_info["citation"]

        self.document_structure["citations"][citekey]["citation"] = citation

    @pyqtSlot(dict)
    def on_parsing_document_finished(self, data: dict) -> None:
        """Updates self.document_structure with newly parsed data and emits FileStrucutreUpdated so that the main
        window could update the ProjectManager's information about current project structure or display the structure"""
        # TODO: add time configuration
        self.is_parsing_document = False
        self.DocumentParsingTimer.start(5000)

        for citation in self.document_structure["citations"].items():
            if citation[0] in data["citations"]:
                data["citations"][citation[0]]["citation"] = citation[1]["citation"]

        for citation in data["citations"].items():
            if citation[1]["citation"] == "":
                self.ThreadManager.get_citation(citation[0], self.on_manubot_thread_finished)

        self.document_structure = data

        self.FileStrucutreUpdated.emit(data)

    @pyqtSlot()
    def on_DocumentParsingTimer_timeout(self) -> None:
        """Starts parsing the document structure is this is the currently selected editor"""

        if self.is_current_editor:
            self.parse_document()
