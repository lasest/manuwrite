import collections
import copy

from PyQt5.QtCore import QDate, QSize, QPoint, QStandardPaths, Qt
from PyQt5.QtGui import QColor

import components.extractors


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

# Patterns used by MarkdownHighlighter class to identify expressions in the text
highlighter_patterns = collections.OrderedDict({
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
                     r"^()(~[^~][^~]*~)()$",
        "footnote": r"\[\^..*\]",
        "table": r"\{#tbl:..*\}"
    })

# Default project settings
project_settings = collections.OrderedDict({
        "Title": {"type": "str", "value": ""},
        "Date created": {"type": "mapping/int", "value": [QDate.currentDate().year(), QDate.currentDate().month(),
                                                          QDate.currentDate().day()]},
        "Authors": {"type": "str", "value": ""},
        "Project type": {"type": "enum", "value": "Notes", "allowed values": ["Notes", "Article", "Book"]},
        "Absolute path": {"type": "str", "value": ""},
        "Description": {"type": "str", "value": ""},
        "Additional meta information": {"type": "str", "value": ""},
        "Files to render": {"type": "mapping/str", "value": []},
        "Style": {"type": "str", "value": "Manubot classic"},
        "Render to": {"type": "str", "value": "Html"},
        "Pandoc command (auto)": {"type": "str", "value": ""},
        "Pandoc command (manual)": {"type": "str", "value": ""},
        "Project structure combined": {"type": "dict", "value": copy.deepcopy(document_info_template)},
        "Project structure raw": {"type": "dict", "value": dict()}
    })

# Default application settings
application_settings = {
            # Main window
            "MainWindow/size/value": QSize(640, 480),
            "MainWindow/size/type": "None",

            "MainWindow/pos/value": QPoint(100, 100),
            "MainWindow/pos/type": "None",

            "MainWindow/splitter_sizes/value": [150, 294, 196],
            "MainWindow/splitter_sizes/type": "map/int",

            "MainWindow/project_widget_width/value": 150,
            "MainWindow/project_widget_width/type": "int",

            "MainWindow/preview_width/value": 196,
            "MainWindow/preview_width/type": "int",

            "MainWindow/last_project/value": "",
            "MainWindow/last_project/type": "str",

            # Settings dialog
            "SettingsDialog/size/value": QSize(400, 600),
            "SettingsDialog/size/type": "None",

            "SettingsDialog/pos/value": QPoint(100, 100),
            "SettingsDialog/pos/type": "None",

            "SettingsDialog/current tab index/value": 0,
            "SettingsDialog/current tab index/type": "int",

            # Project settings dialog
            "ProjectSettingsDialog/size/value": QSize(400, 600),
            "ProjectSettingsDialog/size/type": "None",

            "ProjectSettingsDialog/pos/value": QPoint(100, 100),
            "ProjectSettingsDialog/pos/type": "None",

            "ProjectSettingsDialog/current tab index/value": 0,
            "ProjectSettingsDialog/current tab index/type": "int",

            # Add heading dialog
            "AddHeadingDialog/autonumber/value": 2,
            "AddHeadingDialog/autonumber/type": "int",

            "AddHeadingDialog/autogen identifier/value": 0,
            "AddHeadingDialog/autogen identifier/type": "int",

            # Add image dialog
            "AddImageDialog/autogen identifier/value": 2,
            "AddImageDialog/autogen identifier/type": "int",

            "AddImageDialog/autonumber/value": 2,
            "AddImageDialog/autonumber/type": "int",

            # Add table dialog
            "AddTableDialog/autogen identifier/value": 2,
            "AddTableDialog/autogen identifier/type": "int",

            "AddTableDialog/autonumber/value": 2,
            "AddTableDialog/autonumber/type": "int",

            # Add footnote dialog
            "AddFootnoteDialog/autogen identifier/value": 2,
            "AddFootnoteDialog/autogen identifier/type": "int",

            # Application
            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Application/Project folder/type": "str",

            # Editor
            "Editor/Font name/value": "Hack",
            "Editor/Font name/type": "str",

            "Editor/Font size/value": 14,
            "Editor/Font size/type": "int",

            "Editor/Default image width/value": 500,
            "Editor/Default image width/type": "int",

            "Editor/Default image height/value": 500,
            "Editor/Default image height/type": "int",

            "Editor/Image tooltip height/value": 250,
            "Editor/Image tooltip height/type": "int",

            "Editor/Image tooltip width/value": 250,
            "Editor/Image tooltip width/type": "int",

            "Editor/Show image tooltips/value": True,
            "Editor/Show image tooltips/type": "bool",

            "Editor/Show citation tooltips/value": True,
            "Editor/Show citation tooltips/type": "bool",

            "Editor/Current color schema/value": "System colors",
            "Editor/Current color schema/type": "str",

            # Render
            "Render/Autorender/value": True,
            "Render/Autorender/type": "bool",

            "Render/Autorender delay/value": 1000,
            "Render/Autorender delay/type": "int",

            "Render/Formats/value": [{"name": "Html", "pandoc name": "html", "file extension": "html"},
                                     {"name": "Pdf", "pandoc name": "pdf", "file extension": "pdf"},
                                     {"name": "Doc", "pandoc name": "doc", "file extension": "doc"}],
            "Render/Formats/type": "list",

            "Render/Styles/value": [{"name": "Manuwrite strict", "folder": "manuwrite_classic"},
                                    {"name": "Manuwrite modern", "folder": "manuwrite_modern"},
                                    {"name": "Manubot classic", "folder": "manubot_classic"}],
            "Render/Styles/type": "list",

            # Projects
            "Projects/Project types/value": ["Article", "Book", "Notes", "Other"],
            "Projects/Project types/type": "list"
        }

# From this dictionary a list of IdentifierParser objects will be created. Keys are patterns used to generate QRegExp
# for each object. 'category' value corresponds to the keys in 'document_info_template'. 'extractor' value is the
# extractor function to be used
parser_patterns = {
        r"^\s*#$|^\s*#[^#].*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"^\s*##$|^\s*##[^#].*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"^\s*###$|^\s*###[^#].*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"^\s*####$|^\s*####[^#].*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"^\s*#####$|^\s*#####[^#].*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"^\s*######.*": {
            "category": "headings",
            "extractor": components.extractors.heading_extractor
        },
        r"!\[.*\]\(..*\)|!\[.*\]\(..*\)\{.*\}": {
            "category": "figures",
            "extractor": components.extractors.figure_extractor
        },
        r"\[@[\S][\S]*:[\S][\S]*\]": {
            "category": "citations",
            "extractor": components.extractors.citation_extractor
        },
        r"\[\^..*\]": {
            "category": "footnotes",
            "extractor": components.extractors.footnote_extractor
        },
        r"\{#tbl:..*\}": {
            "category": "tables",
            "extractor": components.extractors.table_extractor
        }
    }


def get_default_color_schema(palette) -> dict:
    """Returns a default color schema based on a given palette"""
    default_color_schema = {
        "Data type": "Manuwrite color schema",
        "Schema name": "System colors",
        "Editor_colors": {"background": {"name": "Editor background",
                                         "color": palette.color(palette.Base).name()},
                          "text": {"name": "Text",
                                   "color": palette.color(palette.Text).name()},
                          "current_line": {"name": "Current line",
                                           "color": palette.color(palette.AlternateBase).name()},
                          "linenumber_area": {"name": "Line number area",
                                              "color": palette.color(palette.AlternateBase).darker(150).name()},
                          "linenumber_text": {"name": "Line number area text",
                                              "color": palette.color(palette.Text).name()}},
        "Markdown_colors": {"heading-1": {"name": "Heading 1",
                                          "color": QColor(Qt.red).name()},
                            "heading-2": {"name": "Heading 2",
                                          "color": QColor(Qt.red).name()},
                            "heading-3": {"name": "Heading 3",
                                          "color": QColor(Qt.red).name()},
                            "heading-4": {"name": "Heading 4",
                                          "color": QColor(Qt.red).name()},
                            "heading-5": {"name": "Heading 5",
                                          "color": QColor(Qt.red).name()},
                            "heading-6": {"name": "Heading 6",
                                          "color": QColor(Qt.red).name()},
                            "line-break": {"name": "Line break",
                                           "color": "#ff8080"},
                            "horizontal-rule": {"name": "Horizontal rule",
                                                "color": "#ff8080"},
                            "italic": {"name": "Italic",
                                       "color": QColor(Qt.yellow).name()},
                            "bold": {"name": "Bold",
                                     "color": QColor(Qt.yellow).name()},
                            "bold-and-italic": {"name": "Bold and italic",
                                                "color": QColor(Qt.yellow).name()},
                            "blockquote-1": {"name": "Blockquote 1",
                                             "color": QColor(Qt.cyan).name()},
                            "blockquote-2": {"name": "Blockquote 2",
                                             "color": QColor(Qt.cyan).name()},
                            "blockquote-3": {"name": "Blockquote 3",
                                             "color": QColor(Qt.cyan).name()},
                            "blockquote-n": {"name": "Blockquote n",
                                             "color": QColor(Qt.cyan).name()},
                            "ordered-list": {"name": "Ordered list",
                                             "color": QColor(Qt.red).name()},
                            "unordered-list": {"name": "Unordered list",
                                               "color": QColor(Qt.red).name()},
                            "code": {"name": "Code",
                                     "color": QColor(Qt.green).name()},
                            "link": {"name": "Link",
                                     "color": "#3e95ff"},
                            "image": {"name": "Image",
                                      "color": "#3e95ff"},
                            "citation": {"name": "Citation",
                                         "color": "#3e95ff"},
                            "strikeout": {"name": "Strikeout",
                                          "color": "#777777"},
                            "superscript": {"name": "Strikeout",
                                            "color": "#4081d1"},
                            "subscript": {"name": "Strikeout",
                                          "color": "#4081d1"},
                            "footnote": {"name": "Footnote",
                                         "color": "#ff0000"},
                            "table": {"name": "Table",
                                      "color": "#0000ff"}
                            }
    }

    return default_color_schema
