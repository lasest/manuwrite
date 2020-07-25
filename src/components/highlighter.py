from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QRegExp, Qt


class Rule():

    def __init__(self, name: str, pattern: str, text_format: QTextCharFormat):
        self.name = name
        self.expression = QRegExp(pattern)
        self.format = text_format


class MarkdownHighlighter(QSyntaxHighlighter):

    structures = (
        "heading-1", "heading-1-alt", "heading-2-alt", "heading-2", "heading-3", "heading-4", "heading-5", "heading-6",
        "line-break", "horizontal-rule",
        "bold", "bold-alt", "italic", "italic-alt", "bold-and-italic",
        "blockquote-1", "blockquote-2", "blockquote-3", "blockquote-n",
        "ordered-list", "unordered-list",
        "code", "link", "image"
    )

    # TODO: implement alternate heading 1 and heading 2 syntax (requires working with previous line)
    # TODO: implement recognizing titles and other elements when they are not at the beginning of the line but are tabbed
    # TODO: make it so that the inner asterikses are not considered part of another construct, e.g. in ***text*** 2 inner \
    # are recognized as part of a bold statement

    patterns = {
        "heading-1": r"^#$|^#[^#].*",
        "heading-2": r"^##$|^##[^#].*",
        "heading-3": r"^###$|^###[^#].*",
        "heading-4": r"^####$|^####[^#].*",
        "heading-5": r"^#####$|^#####[^#].*",
        "heading-6": r"^######.*",
        "line-break": r"\s\s$",
        "horizontal-rule": r"^\*\*\*\**$|^----*$|^____*$",
        "bold": r"[*_][*_]..*[*_][*_]",
        "italic": r"[^*_][^*_][*_]..*[*_][^*_][^*_]",
        "bold-and-italic": r"[*_][*_][*_]..*[*_][*_][*_]",
        "blockquote-1": r"^>$|^>[^>].*",
        "blockquote-2": r"^>>$|^>>[^>].*",
        "blockquote-3": r"^>>>$|^>>>[^>].*",
        "blockquote-n": r"^>>>>$|^>>>>[^>].*",
        "ordered-list": r"^\d\.",
        "unordered-list": r"^[-+*]\s",
        "code": r"`..*`",
        "link": r"^\[..*\]\(..*\)|[^!]\[..*\]\(..*\)",
        "image": r"!\[..*\]\(..*\)"
    }

    def __init__(self, document):
        super().__init__(document)

        self.formats = {key: QTextCharFormat() for key in self.patterns.keys()}
        self.set_formats()

        self.rules = []
        for pattern in self.patterns.items():
            self.rules.append(Rule(pattern[0], pattern[1], self.formats[pattern[0]]))

    def set_formats(self):
        self.formats["heading-1"].setForeground(Qt.yellow)
        self.formats["heading-2"].setForeground(Qt.magenta)
        self.formats["heading-3"].setForeground(Qt.green)
        self.formats["heading-4"].setForeground(Qt.cyan)
        self.formats["heading-5"].setForeground(Qt.red)
        self.formats["heading-6"].setForeground(Qt.blue)
        self.formats["line-break"].setBackground(Qt.red)
        self.formats["horizontal-rule"].setBackground(Qt.white)
        self.formats["bold"].setFontWeight(75)
        self.formats["italic"].setFontItalic(True)
        self.formats["bold-and-italic"].setFontItalic(True)
        self.formats["bold-and-italic"].setFontWeight(75)
        self.formats["blockquote-1"].setForeground(Qt.darkGreen)
        self.formats["blockquote-2"].setForeground(Qt.darkMagenta)
        self.formats["blockquote-3"].setForeground(Qt.darkYellow)
        self.formats["blockquote-n"].setForeground(Qt.darkCyan)
        self.formats["ordered-list"].setForeground(Qt.darkBlue)
        self.formats["unordered-list"].setForeground(Qt.darkRed)
        self.formats["code"].setFontFamily("fantasy")
        self.formats["link"].setFontUnderline(True)
        self.formats["image"].setFontStrikeOut(True)

    def highlightBlock(self, text):

        for rule in self.rules:
            index = rule.expression.indexIn(text)
            while index >= 0:
                length = rule.expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = rule.expression.indexIn(text, index + length)
