from typing import Tuple, Dict, List

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument, QColor
from PyQt5.QtCore import QRegExp

import defaults


class Rule():

    def __init__(self, name: str, pattern: str, text_format: QTextCharFormat):
        self.name = name
        self.expression = QRegExp(pattern)
        self.format = text_format


class MarkdownHighlighter(QSyntaxHighlighter):

    def __init__(self, document: QTextDocument, settings_manager):
        super().__init__(document)

        self.SettingsManager = settings_manager
        self.patterns = defaults.highlighter_patterns
        self.allow_highlighting = True

        # Create formats
        self.formats: Dict[str, QTextCharFormat] = {key: QTextCharFormat() for key in self.patterns.keys()}
        self.set_formats()

        # Create rules
        self.rules: List[Rule] = []
        for pattern in self.patterns.items():
            self.rules.append(Rule(pattern[0], pattern[1], self.formats[pattern[0]]))

    def prevent_highlighting(self, prevent: bool):
        """Stops or resumes highlighting of the current document"""
        self.allow_highlighting = not prevent
        self.rehighlight()

    def set_formats(self) -> None:
        """Sets formats which will be applied to the text by highlighter"""

        color_schema = self.SettingsManager.color_schema

        for key in self.formats.keys():
            self.formats[key].setForeground(QColor(color_schema["Markdown_colors"][key]["color"]))

        for s in "link", "image", "citation":
            self.formats[s].setFontUnderline(True)

        self.formats["horizontal-rule"].setBackground(QColor(color_schema["Markdown_colors"]["horizontal-rule"]["color"]))
        # for s in "line-break",  "horizontal-rule":
        #     self.formats[s].setBackground(QColor(color_schema["Markdown_colors"][s]["color"]))

        for s in "heading-1", "heading-2", "heading-3", "heading-4", "heading-5", "heading-6", "bold", "italic", "bold-and-italic":
            self.formats[s].setFontWeight(75)

        self.formats["code"].setFontFamily("Monospace")

    def highlightBlock(self, text: str) -> None:
        """Finds and highlights tags in the text. Automatically called when document changes"""
        if self.allow_highlighting:
            tags = self.get_tags(text)
        else:
            tags = []

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
