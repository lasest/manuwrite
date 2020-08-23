import subprocess
import copy
from typing import List

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QTextDocument

import defaults
from document_parsing import parse_document


class MarkdownProjectParserThread(QThread):
    """Parses every file in list that is provided to it one by one. Saves raw project structure in 'project_structure'
    field in the form of a dictionary {filepath: document_info} where 'document_info' is a dictionary provided by
    parse_document() function"""

    def __init__(self, parent, filepaths: List[str]):
        super().__init__(parent)

        self.filepaths = filepaths
        self.project_structure = dict()
        for filepath in filepaths:
            self.project_structure[filepath] = dict()

    def run(self) -> None:

        for filepath in self.filepaths:
            with open(filepath) as f:
                file_contents = f.read()

            document = QTextDocument(file_contents, self)
            # TODO: set base url of a document to filepath here
            document_info = copy.deepcopy(defaults.document_info_template)
            parse_document(document, document_info)
            self.project_structure[filepath] = document_info

            # Removing filepath key so that the dictionary could be used assuming every value in it is a dictionary
            del self.project_structure[filepath]["filepath"]


class MarkdownDocumentParserThread(QThread):
    """Parses a QTextDocument using a parse_document() function. Stores parsed data in self.document_info field"""

    def __init__(self, parent, document: QTextDocument):
        super().__init__(parent)

        self.document = document
        self.document_info = copy.deepcopy(defaults.document_info_template)
        self.document_info["filepath"] = self.document.baseUrl().toLocalFile()

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
        parse_document(self.document, self.document_info)


class ManubotCiteThread(QThread):
    """Generates a citation for given citekey using manubot. Citation is stored in self.citation field"""

    def __init__(self, parent, citekey: str):
        super().__init__(parent)
        self.citekey = citekey
        self.citation = ""

    def run(self) -> None:
        manubot = subprocess.run(["manubot", "cite", "--render", self.citekey], capture_output=True)
        manubot.check_returncode()
        self.citation = manubot.stdout.decode()


class PandocThread(QThread):
    """Renders given markdown document to some format using Pandoc"""

    def __init__(self, parent, markdown: str):
        super().__init__(parent)
        self.markdown = markdown
        self.html = ""

    def run(self) -> None:
        pandoc = subprocess.run(["pandoc", "--to", "html", "--filter", "pandoc-manubot-cite", "--filter", "pandoc-citeproc", "--filter", "pandoc-fignos", "--filter", "pandoc-tablenos", "--css", "style.css", "--standalone"], input=self.markdown.encode(), capture_output=True)
        pandoc.check_returncode()
        self.html = pandoc.stdout.decode()


class ThreadManager(QObject):
    """Manages threads. Makes sure that the number of threads running at the same time is not too high. Keeps track of
    what threads are currently running and which are waiting in the queue"""

    # Signals that will be emitted when a thread finishes
    manubotCiteThreadFinished = pyqtSignal(str, str)
    pandocThreadFinished = pyqtSignal(str)
    MarkdownDocumentParserThreadFinished = pyqtSignal(dict)
    MarkdownProjectParserThreadFinished = pyqtSignal(dict)

    def __init__(self, max_threads: int = 4):

        super().__init__()

        self.running_threads = []
        self.pending_threads = []
        self.running_thread_count = 0
        self.max_threads = max_threads
        self.is_parsing_document = False

    # House hold methods
    def run_thread(self, thread, disobey_thread_limit=False) -> None:
        """Runs a thread if it will not violate the thread count limit. Otherwise puts the thread in the queue"""

        if (self.running_thread_count < self.max_threads) or disobey_thread_limit:
            self.running_threads.append(thread)
            self.running_thread_count += 1
            thread.start()
        else:
            self.pending_threads.append(thread)

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

    # Thread-starting methods
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

    def parse_markdown_document(self, document: QTextDocument) -> None:
        """Starts a MarkdownDocumentParserThread to parse a given markdown document for document structure. Does not
        obey the thread limit, but checks to make sure that only one such thread is running at a time"""

        if not self.is_parsing_document:
            thread = MarkdownDocumentParserThread(self, document)
            thread.finished.connect(self.on_parse_markdown_document_finished)

            self.run_thread(thread, disobey_thread_limit=True)
            self.is_parsing_document = True

    def parse_project(self, filenames: List[str]) -> None:
        """Starts MarkdownProjectParser thread to parse a given list of files"""

        thread = MarkdownProjectParserThread(self, filenames)
        thread.finished.connect(self.on_parse_project_thread_finished)

        self.run_thread(thread)

    # Thread.finished handlers
    # TODO: write what functions receive these signals
    def on_manubot_cite_thread_finished(self) -> None:
        """Performes thread management and emits manubotCiteThreadFinished to inform that the thread has finished"""

        sender = QObject.sender(self)
        self.run_next_thread(sender)

        citekey = sender.citekey
        citation = sender.citation

        self.manubotCiteThreadFinished.emit(citekey, citation)

    def on_pandoc_thread_finished(self) -> None:
        """Performs thread management and emits pandocThreadFinished to inform that the thread has finished"""
        sender = QObject.sender(self)
        self.run_next_thread(sender)

        html = sender.html
        self.pandocThreadFinished.emit(html)

    def on_parse_markdown_document_finished(self) -> None:
        """Performs thread management and emits MarkdownDocumentParserThreadFinished to inform that the thread has
        finished"""

        self.is_parsing_document = False
        sender = QObject.sender(self)
        self.run_next_thread(sender)

        self.MarkdownDocumentParserThreadFinished.emit(sender.document_info)

    def on_parse_project_thread_finished(self) -> None:
        """Performs thread management and emits MarkdownProjectParserThreadFinished to inform that the thread has
        finished"""

        sender = QObject.sender(self)
        self.run_next_thread(sender)

        self.MarkdownProjectParserThreadFinished.emit(sender.project_structure)
