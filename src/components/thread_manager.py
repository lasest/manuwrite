import subprocess
import collections
import copy
from typing import List, Tuple

from PyQt5.QtCore import QThread, QObject, pyqtSignal, QRegExp, QFile
from PyQt5.QtGui import QTextDocument


class IdentifierParser():
    """Used to parse a tag for information. For example get image caption and image filepath from image tag. Call
    extract() to get the parsed information. The tag to be parsed is stored in regexp field after calling
    regexp.indexIn() on the text to be parsed. Field 'extractor' stores the function which should be used on the tag
    to parse it. Field 'category' stores the key of the 'document_info_template' dictionary, which should be updated
    with the parsed information"""

    def __init__(self, pattern, extractor, category):
        self.regexp = QRegExp(pattern)
        self.extractor = extractor
        self.category = category

    def extract(self) -> dict:
        """Returns the dictionary with information parsed by the extractor function"""
        return self.extractor(self.regexp.cap(0))

# Extractor functions
# Extractor function takes one string to be parsed and returns a tuple of parsed identifier and a dictionary in the
# form of {identifier: {text: [name], ...}}. 'text' field must be present. This value will be displayed in project
# structure tree as the name of the entry. Other optional field may be added


def heading_extractor(heading: str) -> Tuple[str, dict]:
    """Extracts information about a heading from the heading tag"""

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
    return identifier, {identifier: {"text": heading_text,
                                     "level": heading_level}}


def figure_extractor(image_tag: str) -> Tuple[str, dict]:
    """Extracts information about an image from image tag"""

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

    return identifier, {identifier: {"text": caption,
                                     "filepath": filepath}}


def citation_extractor(citation_tag: str) -> Tuple[str, dict]:
    """Extracts information about a citation from citation tag"""
    identifier = citation_tag[2:-1]
    return identifier, {identifier: {"text": identifier}}


def footnote_extractor(footnote_tag: str) -> Tuple[str, dict]:
    """Extracts information about a footnote from footnote tag"""
    identifier = footnote_tag[2:-1]
    return identifier, {identifier: {"text": identifier}}


def table_extractor(table_tag: str) -> Tuple[str, dict]:
    """Extracts information about a table from table tag"""
    identifier = table_tag[2:-1]
    return identifier, {identifier: {"text": identifier}}


# From this dictionary a list of IdentifierParser objects will be created. Keys are patterns used to generate QRegExp
# for each object. 'category' value corresponds to the keys in 'document_info_template'. 'extractor' value is the
# extractor function to be used

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


# The template of document_info dictionary. Each key except for filepath contains a dictionary in the form of
# {identifier: {text: [name], ...}. 'text' key is mandatory

document_info_template = {
            "filepath": "",
            "citations": collections.OrderedDict(),
            "figures": collections.OrderedDict(),
            "tables": collections.OrderedDict(),
            "footnotes": collections.OrderedDict(),
            "headings": collections.OrderedDict()
        }

# Create a list of IdentifierParser objects
identifier_parsers: List[IdentifierParser] = []
for key, value in patterns.items():
    parser = IdentifierParser(key, value["extractor"], value["category"])
    identifier_parsers.append(parser)


def parse_document(document: QTextDocument, document_info: dict):
    """Parses the document line by line for tags matching regexp of objects in identifier_parsers. Updates the
    provided document_info dictionary with the parsed information"""

    line_count = document.blockCount()
    header_index = -1

    for i in range(line_count):
        current_line = document.findBlockByNumber(i).text()

        for parser in identifier_parsers:
            index = parser.regexp.indexIn(current_line)

            while index >= 0:
                # TODO: check if identifier has already been used
                identifier, parsed_info = parser.extract()

                # Add additional fields
                parsed_info[identifier]["block_number"] = i
                parsed_info[identifier]["current_header_index"] = header_index
                parsed_info[identifier]["project_filepath"] = document.baseUrl().toLocalFile()

                if parser.category == "headings":
                    header_index += 1

                document_info[parser.category].update(parsed_info)
                length = parser.regexp.matchedLength()
                index = parser.regexp.indexIn(current_line, index + length)


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
            document_info = copy.deepcopy(document_info_template)
            parse_document(document, document_info)
            self.project_structure[filepath] = document_info

            # Removing filepath key so that the dictionary could be used assuming every value in it is a dictionary
            del self.project_structure[filepath]["filepath"]


class MarkdownDocumentParserThread(QThread):
    """Parses a QTextDocument using a parse_document() function. Stores parsed data in self.document_info field"""

    def __init__(self, parent, document: QTextDocument):
        super().__init__(parent)

        self.document = document
        self.document_info = copy.deepcopy(document_info_template)
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
        pandoc = subprocess.run(["pandoc", "--to", "html", "--filter", "pandoc-manubot-cite", "--filter", "pandoc-citeproc", "--filter", "pandoc-fignos", "--css", "style.css", "--standalone"], input=self.markdown.encode(), capture_output=True)
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
