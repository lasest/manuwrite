from collections import OrderedDict
from typing import Tuple, Dict, List

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument, QColor
from PyQt5.QtCore import QRegExp, Qt


class Rule():

    def __init__(self, name: str, pattern: str, text_format: QTextCharFormat):
        self.name = name
        self.expression = QRegExp(pattern)
        self.format = text_format
        self.loffset = 0
        self.roffset = 0


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
        "link": r"()(^\[..*\]\(..*\))()|" +
                r"([^!])(\[..*\]\(..*\))()",
        "image": r"!\[.*\]\(..*\)|!\[.*\]\(..*\)\{.*\}",
        "citation": r"\[@[\S][\S]*:[\S][\S]*\]",
        "strikeout": r"~~[^~][^~]*~~",
        "superscript": r"\^..*\^",
        "subscript": r"([^~])(~[^~][^~]*~)([^~])|" +
                     r"^()(~[^~][^~]*~)([^~])|" +
                     r"([^~])(~[^~][^~]*~)()$|" +
                     r"^()(~[^~][^~]*~)()$"
    })

    def __init__(self, document: QTextDocument, settings_manager):
        super().__init__(document)

        self.SettingsManager = settings_manager

        # Create formats
        self.formats: Dict[str, QTextCharFormat] = {key: QTextCharFormat() for key in self.patterns.keys()}
        self.set_formats()

        # Create rules
        self.rules: List[Rule] = []
        for pattern in self.patterns.items():
            self.rules.append(Rule(pattern[0], pattern[1], self.formats[pattern[0]]))

    def set_formats(self) -> None:
        """Sets formats which will be applied to the text by highlighter"""

        color_schema = self.SettingsManager.get_current_color_schema()

        for key in self.formats.keys():
            self.formats[key].setForeground(QColor(color_schema["Markdown_colors"][key]["color"]))

        for s in "link", "image", "citation":
            self.formats[s].setFontUnderline(True)

        for s in "line-break",  "horizontal-rule":
            self.formats[s].setBackground(QColor(color_schema["Markdown_colors"][s]["color"]))

        self.formats["code"].setFontFamily("Monospace")

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

                if rule.expression.captureCount() > 1:
                    group_n = 0
                    center_count = int((rule.expression.captureCount()) / 3)
                    for i in range(center_count):
                        current_center = 2 + i * 3
                        if rule.expression.cap(current_center):
                            group_n = current_center
                            break
                    loffset = len(rule.expression.cap(group_n - 1))
                    roffset = len(rule.expression.cap(group_n + 1))

                length = rule.expression.matchedLength() - loffset - roffset
                tags.append((index + loffset, length, rule.name))
                index = rule.expression.indexIn(text, index + length + roffset)

        return tags
