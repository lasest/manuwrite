from collections import OrderedDict
from typing import Tuple, Dict, List

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument
from PyQt5.QtCore import QRegExp, Qt


class Rule():

    def __init__(self, name: str, pattern: str, text_format: QTextCharFormat):
        self.name = name
        self.expression = QRegExp(pattern)
        self.format = text_format


class MarkdownHighlighter(QSyntaxHighlighter):

    # TODO: implement alternate heading 1 and heading 2 syntax (requires working with previous line)

    # Patterns to be detected
    patterns = OrderedDict({
        "heading-1": r"^\s*#$|^\s*#[^#].*",
        "heading-2": r"^\s*##$|^\s*##[^#].*",
        "heading-3": r"^\s*###$|^\s*###[^#].*",
        "heading-4": r"^\s*####$|^\s*####[^#].*",
        "heading-5": r"^\s*#####$|^\s*#####[^#].*",
        "heading-6": r"^\s*######.*",
        "line-break": r"\s\s$",
        "horizontal-rule": r"^\*\*\*\**$|^----*$|^____*$",
        "italic": r"()(^[*_][^*][^*]*[*_]$)()|" +
                  r"([^*_])([*_][^*][^*]*[*_]$)()|" +
                  r"()(^[*_][^*][^*]*[*_])([^*_])|" +
                  r"([^*_])([*_][^*][^*]*[*_])([^*_])",
        "bold": r"()(^[*_][*_][^*][^*]*[*_][*_]$)()|" +
                r"([^*_])([*_][*_][^*][^*]*[*_][*_]$)()|" +
                r"()(^[*_][*_][^*][^*]*[*_][*_])([^*_])|" +
                r"([^*_])([*_][*_][^*][^*]*[*_][*_])([^*_])",
        "bold-and-italic": r"[*_][*_][*_][^*][^*]*[*_][*_][*_]",
        "blockquote-1": r"^\s*>$|^\s*>[^>].*",
        "blockquote-2": r"^\s*>>$|^\s*>>[^>].*",
        "blockquote-3": r"^\s*>>>$|^\s*>>>[^>].*",
        "blockquote-n": r"^\s*>>>>$|^\s*>>>>[^>].*",
        "ordered-list": r"^\s*\d\.",
        "unordered-list": r"^\s*[-+*]\s",
        "code": r"`..*`",
        "link": r"()(^\[..*\]\(..*\))|" +
                r"([^!])(\[..*\]\(..*\))",
        "image": r"!\[.*\]\(..*\)",
        "citation": r"\[@[\S][\S]*:[\S][\S]*\]"
    })

    def __init__(self, document: QTextDocument):
        super().__init__(document)

        # Create formats
        self.formats: Dict[str, QTextCharFormat] = {key: QTextCharFormat() for key in self.patterns.keys()}
        self.set_formats()

        # Create rules
        self.rules: List[Rule] = []
        for pattern in self.patterns.items():
            self.rules.append(Rule(pattern[0], pattern[1], self.formats[pattern[0]]))

    def set_formats(self) -> None:
        """Sets formats which will be applied to the text by highlighter"""

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
        self.formats["citation"].setForeground(Qt.red)
        self.formats["citation"].setToolTip("Some random text")

    def highlightBlock(self, text: str) -> None:
        """Finds and highlights tags in the text. Automatically called when document changes"""
        tags = self.get_tags(text)

        for tag in tags:
            self.setFormat(tag[0], tag[1], self.formats[tag[2]])

    def get_tags(self, text: str) -> List[Tuple[int, int, str]]:
        """Returns a list of tags, which were found in given text. Information about each tag is in format
        [first symbol of tag, length of tag, name of tag]"""

        tags = []

        for rule in self.rules:
            index = rule.expression.indexIn(text)
            while index >= 0:
                # Have to use offset for certain tags because some perl features are not available in qt (i. e.
                # lookahead and lookbehind
                loffset = 0
                roffset = 0

                if rule.name in ("italic", "bold"):
                    group_n = 0
                    for i in (2, 5, 8, 11):
                        if rule.expression.cap(i):
                            group_n = i
                            break
                    loffset = len(rule.expression.cap(group_n - 1))
                    roffset = len(rule.expression.cap(group_n + 1))
                elif rule.name == "link":
                    group_n = 0
                    for i in (2, 4):
                        if rule.expression.cap(i):
                            group_n = i
                            break
                    loffset = len(rule.expression.cap(group_n - 1))

                length = rule.expression.matchedLength() - loffset - roffset
                tags.append((index + loffset, length, rule.name))
                index = rule.expression.indexIn(text, index + length + roffset)

        return tags
