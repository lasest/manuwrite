import subprocess
import collections
from typing import List

from PyQt5.QtCore import QThread, QObject, pyqtSignal, QRegExp
from PyQt5.QtGui import QTextDocument


def heading_extractor(heading: str):

    identifier_regexp = QRegExp(r"{#\w\w*")
    loffset = 2

    # Determine heading level
    heading = heading.strip()
    length = len(heading)
    heading = heading.lstrip("#")
    heading_level = length - len(heading)
    if heading_level > 6:
        heading_level = 6

    # Save heading text
    heading_text = heading.strip(" #")

    # Check if heading has explicit identifier
    # TODO: fully mimic pandoc's identifier generation

    index = identifier_regexp.indexIn(heading_text)
    if index >= 0:
        identifier = heading_text[index + loffset:index + identifier_regexp.matchedLength()]

    # Generate an implicit identifier if there is no explicit one
    if index == -1:
        identifier = heading_text.lower().replace(" ", "-")

    # Return resulting dictionary
    return {identifier: {"text": heading_text,
                         "level": heading_level}}


def figure_extractor(image_tag: str):

    identifier_regexp = QRegExp(r"{#fig:\w\w*")
    loffset = 2

    # get identifier
    index = identifier_regexp.indexIn(image_tag)
    if index >= 0:
        identifier = image_tag[index + loffset: index + identifier_regexp.matchedLength()]
    else:
        identifier = "No identifier found"

    # get caption
    start = image_tag.index("[")
    end = image_tag.index("]")
    caption = image_tag[start + 1: end]

    # get filepath
    start = image_tag.index("(")
    end = image_tag.index(")")
    filepath = image_tag[start + 1: end]

    return {identifier: {"text": caption,
                         "filepath": filepath}}


def citation_extractor(citation_tag: str):
    identifier = citation_tag[2:-1]
    return {identifier: {"text": identifier}}


def footnote_extractor(footnote_tag: str):
    identifier = footnote_tag[2:-1]
    return {identifier: {"text": identifier}}


def table_extractor(table_tab: str):
    identifier = table_tab[2:-1]
    return {identifier: {"text": identifier}}


class IdentifierParser():

    def __init__(self, pattern, extractor, category):
        self.regexp = QRegExp(pattern)
        self.extractor = extractor
        self.category = category

    def extract(self):
        return self.extractor(self.regexp.cap(0))


class MarkdownDocumentParserThread(QThread):

    patterns = {
        r"^\s*#$|^\s*#[^#].*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"^\s*##$|^\s*##[^#].*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"^\s*###$|^\s*###[^#].*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"^\s*####$|^\s*####[^#].*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"^\s*#####$|^\s*#####[^#].*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"^\s*######.*": {
            "category": "headings",
            "extractor": heading_extractor
        },
        r"!\[.*\]\(..*\)|!\[.*\]\(..*\)\{.*\}": {
            "category": "figures",
            "extractor": figure_extractor
        },
        r"\[@[\S][\S]*:[\S][\S]*\]": {
            "category": "citations",
            "extractor": citation_extractor
        },
        r"\[\^..*\]": {
            "category": "footnotes",
            "extractor": footnote_extractor
        },
        r"\{#tbl:..*\}": {
            "category": "tables",
            "extractor": table_extractor
        }
    }

    def __init__(self, parent, document: QTextDocument):
        super().__init__(parent)
        self.document = document
        self.document_info = {
            "citations": collections.OrderedDict(),
            "figures": collections.OrderedDict(),
            "tables": collections.OrderedDict(),
            "footnotes": collections.OrderedDict(),
            "headings": collections.OrderedDict()
        }

        self.identifier_parsers: List[IdentifierParser] = []
        for key, value in self.patterns.items():
            parser = IdentifierParser(key, value["extractor"], value["category"])
            self.identifier_parsers.append(parser)

    def is_setext_heading(self, line_number: int, heading_sybmol: str):
        current_line = self.document.findBlockByNumber(line_number).text()

        if heading_sybmol == "=":
            index = self.setext_heading_1.indexIn(current_line)
        else:
            index = self.setext_heading_2.indexIn(current_line)
        if index >= 0:
            prev_line = ""
            prevprev_line = ""
            if line_number == 0:
                prev_line = ""
                prevprev_line = ""
            elif line_number == 1:
                prev_line = self.document.findBlockByNumber(line_number - 1).text()
                prevprev_line = ""
            else:
                prev_line = self.document.findBlockByNumber(line_number - 1).text()
                prevprev_line = self.document.findBlockByNumber(line_number - 2).text()

            if prev_line and not prevprev_line:
                return True
            else:
                return False

    def run(self) -> None:
        line_count = self.document.blockCount()
        header_index = -1
        for i in range(line_count):
            line = self.document.findBlockByNumber(i).text()
            for parser in self.identifier_parsers:
                index = parser.regexp.indexIn(line)
                while index >= 0:
                    # TODO: check if identifier has already been used
                    info = parser.extract()
                    identifier = list(info.keys())[0]
                    print(info)
                    info[identifier]["block_number"] = i
                    info[identifier]["current_header_index"] = header_index
                    info[identifier]["project_filepath"] = self.document.baseUrl().toString()
                    print(info)
                    if parser.category == "headings":
                        header_index += 1

                    self.document_info[parser.category].update(info)
                    length = parser.regexp.matchedLength()
                    index = parser.regexp.indexIn(line, index + length)


class ManubotCiteThread(QThread):

    def __init__(self, parent, citekey: str):
        super().__init__(parent)
        self.citekey = citekey
        self.citation = ""

    def run(self):
        manubot = subprocess.run(["manubot", "cite", "--render", self.citekey], capture_output=True)
        manubot.check_returncode()
        self.citation = manubot.stdout.decode()


class PandocThread(QThread):

    def __init__(self, parent, markdown: str):
        super().__init__(parent)
        self.markdown = markdown
        self.html = ""

    def run(self):
        pandoc = subprocess.run(["pandoc", "--to", "html", "--filter", "pandoc-manubot-cite", "--filter", "pandoc-citeproc", "--filter", "pandoc-fignos", "--css", "style.css", "--standalone"], input=self.markdown.encode(), capture_output=True)
        pandoc.check_returncode()
        self.html = pandoc.stdout.decode()


class ThreadManager(QObject):

    manubotCiteThreadFinished = pyqtSignal(str, str)
    pandocThreadFinished = pyqtSignal(str)
    MarkdownDocumentParserThreadFinished = pyqtSignal(dict)

    def __init__(self, max_threads: int = 4):

        super().__init__()

        self.running_threads = []
        self.pending_threads = []
        self.running_thread_count = 0
        self.max_threads = max_threads
        self.is_parsing_document = False

    def get_citation(self, citekey: str) -> None:
        """Starts manubot thread to get citation info for a given citekey. When thread is finished
        manubotCiteThreadFinished signal is emitted and should be caught by the caller"""

        thread = ManubotCiteThread(self, citekey)
        thread.finished.connect(self.on_manubot_cite_thread_finished)

        self.run_thread(thread)

    def markdown_to_html(self, markdown: str) -> None:
        """Starts pandoc thread to convert given string from markdown to html. When the thread is finished
        pandocThreadFinished signal is emitted and should be caught by the caller"""

        thread = PandocThread(self, markdown)
        thread.finished.connect(self.on_pandoc_thread_finished)

        self.run_thread(thread)

    def on_manubot_cite_thread_finished(self) -> None:
        """Performes thread management and emits manubotCiteThreadFinished to inform that the thread has finished"""

        sender = QObject.sender(self)
        self.run_next_thread(sender)

        citekey = sender.citekey
        citation = sender.citation

        self.manubotCiteThreadFinished.emit(citekey, citation)

    def run_next_thread(self, finished_thread) -> None:
        """Runs the next thread from the pending_threads list. Last come first served logic is used here to receive the
        results quicker when the user is typing"""
        self.running_threads.remove(finished_thread)
        self.running_thread_count -= 1

        if self.pending_threads:
            self.running_threads.append(self.pending_threads[-1])
            self.running_thread_count += 1
            self.pending_threads[-1].start()
            self.pending_threads.remove(self.pending_threads[-1])

    def on_pandoc_thread_finished(self) -> None:
        """Performs thread management and emits pandocThreadFinished to inform that the thread has finished"""
        sender = QObject.sender(self)
        self.run_next_thread(sender)

        html = sender.html
        self.pandocThreadFinished.emit(html)

    def parse_markdown_document(self, document):
        if not self.is_parsing_document:
            thread = MarkdownDocumentParserThread(self, document)
            thread.finished.connect(self.on_parse_markdown_document_finished)
            self.running_threads.append(thread)
            self.running_thread_count += 1
            self.is_parsing_document = True
            thread.start()

    def on_parse_markdown_document_finished(self):
        self.is_parsing_document = False
        sender = QObject.sender(self)
        self.run_next_thread(sender)

        self.MarkdownDocumentParserThreadFinished.emit(sender.document_info)

    def run_thread(self, thread):
        if self.running_thread_count < self.max_threads:
            self.running_threads.append(thread)
            self.running_thread_count += 1
            thread.start()
        else:
            self.pending_threads.append(thread)
