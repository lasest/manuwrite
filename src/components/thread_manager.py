import subprocess
import copy
from typing import List

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QTextDocument

import defaults
from components.document_parsing import parse_document


class MarkdownProjectParserThread(QThread):
    """Parses every file in list that is provided to it one by one. Saves raw project structure in 'project_structure'
    field in the form of a dictionary {filepath: document_info} where 'document_info' is a dictionary provided by
    parse_document() function"""

    def __init__(self, parent, filepaths: List[str]):
        super().__init__(parent)

        self.filepaths = filepaths
        self.project_structure = dict()
        self.result = dict()

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

        self.result = self.project_structure


class MarkdownDocumentParserThread(QThread):
    """Parses a QTextDocument using a parse_document() function. Stores parsed data in self.document_info field"""

    def __init__(self, parent, document: QTextDocument):
        super().__init__(parent)

        self.document = document
        self.document_info = copy.deepcopy(defaults.document_info_template)
        self.document_info["filepath"] = self.document.baseUrl().toLocalFile()
        self.result = dict()

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
        self.result = self.document_info


class ManubotCiteThread(QThread):
    """Generates a citation for given citekey using manubot. Citation is stored in self.citation field"""

    def __init__(self, parent, citekey: str):
        super().__init__(parent)
        self.citekey = citekey
        self.result = dict()

    def run(self) -> None:
        manubot = subprocess.run(["manubot", "cite", "--render", self.citekey], capture_output=True)
        manubot.check_returncode()

        self.result["citekey"] = self.citekey
        self.result["citation"] = manubot.stdout.decode()


class ProjectRenderer(QThread):

    def __init__(self, project_manager):
        super().__init__()
        self.ProjectManager = project_manager
        self.result = ""

    def run(self) -> None:
        command = self.ProjectManager.get_setting_value("Full_pandoc_command")
        subprocess.run(command.split(), cwd=self.ProjectManager.get_setting_value("Absolute path"))


class PandocThread(QThread):
    """Renders given markdown document to some format using Pandoc"""

    def __init__(self, parent, markdown: str):
        super().__init__(parent)
        self.markdown = markdown
        self.result = ""

    def run(self) -> None:
        pandoc = subprocess.run(["pandoc", "--to", "html", "--filter", "pandoc-manubot-cite", "--filter", "pandoc-citeproc", "--filter", "pandoc-fignos", "--filter", "pandoc-tablenos", "--filter", "pandoc-secnos", "--css", "style.css", "--standalone"], input=self.markdown.encode(), capture_output=True)
        try:
            pandoc.check_returncode()
        except subprocess.CalledProcessError as e:
            print(str(e))

        self.result = pandoc.stdout.decode()


class ThreadWrapper(QObject):
    """Stores the thread together with the function, which should be called when the thread is finished
    (handler_function). Handler function is passed self.thread.result as an argument, hence all thread classes must
    have a result field"""

    thread_finished = pyqtSignal(QObject)

    def __init__(self, thread, handler_function, thread_type=None):
        super().__init__()
        self.thread = thread
        self.handler_function = handler_function
        self.thread_type = thread_type

        self.thread.finished.connect(self.handle)

    def start_thread(self):
        self.thread.start()

    def handle(self):
        self.handler_function(self.thread.result)
        self.thread_finished.emit(self)


class ThreadManager(QObject):
    """Manages threads. Makes sure that the number of threads running at the same time is not too high. Keeps track of
    what threads are currently running and which are waiting in the queue"""

    def __init__(self, max_threads: int = None):

        super().__init__()

        self.running_threads: List[ThreadWrapper] = []
        self.pending_threads: List[ThreadWrapper] = []
        self.running_thread_count = 0

        if max_threads is None:
            self.max_threads = QThread.idealThreadCount()
        else:
            self.max_threads = max_threads

        if self.max_threads < 1:
            self.max_threads = 1

    # House hold methods
    def run_thread(self, thread_wrapper: ThreadWrapper, disobey_thread_limit: bool = False) -> None:
        """Runs a thread if it will not violate the thread count limit. Otherwise puts the thread in the queue"""

        if (self.running_thread_count < self.max_threads) or disobey_thread_limit:
            self.running_threads.append(thread_wrapper)
            self.running_thread_count += 1
            thread_wrapper.start_thread()
        else:
            self.pending_threads.append(thread_wrapper)

    def run_next_thread(self, finished_thread_wrapper: ThreadWrapper) -> None:
        """Runs the next thread from the pending_threads list. Last come first served logic is used here to receive the
        results quicker when the user is typing"""
        self.running_threads.remove(finished_thread_wrapper)
        self.running_thread_count -= 1

        if self.pending_threads:
            self.running_threads.append(self.pending_threads[-1])
            self.running_thread_count += 1
            self.pending_threads[-1].start_thread()
            self.pending_threads.remove(self.pending_threads[-1])

    # Thread-starting methods
    def get_citation(self, citekey: str, handler_function) -> None:
        """Starts manubot thread to get citation info for a given citekey."""

        thread_wrapper = ThreadWrapper(ManubotCiteThread(self, citekey), handler_function)
        thread_wrapper.thread_finished.connect(self.run_next_thread)

        self.run_thread(thread_wrapper)

    def markdown_to_html(self, markdown: str, handler_function) -> None:
        """Starts pandoc thread to convert given string from markdown to html."""

        thread_wrapper = ThreadWrapper(PandocThread(self, markdown), handler_function)
        thread_wrapper.thread_finished.connect(self.run_next_thread)

        self.run_thread(thread_wrapper)

    def parse_markdown_document(self, document: QTextDocument, handler_function) -> None:
        """Starts a MarkdownDocumentParserThread to parse a given markdown document for document structure."""

        thread_wrapper = ThreadWrapper(MarkdownDocumentParserThread(self, document), handler_function,
                                       thread_type="document_parser")
        thread_wrapper.thread_finished.connect(self.run_next_thread)

        self.run_thread(thread_wrapper, disobey_thread_limit=True)

    def parse_project(self, filenames: List[str], handler_function) -> None:
        """Starts MarkdownProjectParser thread to parse a given list of files"""

        thread_wrapper = ThreadWrapper(MarkdownProjectParserThread(self, filenames), handler_function)
        thread_wrapper.thread_finished.connect(self.run_next_thread)

        self.run_thread(thread_wrapper)

    def render_project(self, project_manager, handler_function):
        thread_wrapper = ThreadWrapper(ProjectRenderer(project_manager), handler_function)
        thread_wrapper.thread_finished.connect(self.run_next_thread)

        self.run_thread(thread_wrapper)