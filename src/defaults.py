import collections
import copy

from PyQt5.QtCore import QDate, QSize, QPoint, QStandardPaths, Qt
from PyQt5.QtGui import QColor, QIcon, QPalette

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
                r"([^!])(\[..*\]\(..*\))()|" +
                r"()(<https://.*>)()|" +
                r"()(<http://.*>)()|" +
                r"()(<ftp://.*>)()|" +
                r"()(<ftps://.*>)()",
        "image": r"!\[.*\]\(..*\)|!\[.*\]\(..*\)\{.*\}",
        "citation": r"\[@[\S][\S]*:[\S][\S]*\]",
        "strikeout": r"~~[^~][^~]*~~",
        "superscript": r"\^..*\^",
        "subscript": r"([^~])(~[^~][^~]*~)([^~])|" +
                     r"^()(~[^~][^~]*~)([^~])|" +
                     r"([^~])(~[^~][^~]*~)()$|" +
                     r"^()(~[^~][^~]*~)()$",
        "footnote": r"\[\^..*\]",
        "table": r"\{#tbl:..*\}",
        "cross-reference": r"^()([+!*]?@\S\S*)()|" +
                           r"([^\[])([+!*]?@\S\S*)()"
    })

# Default project settings
project_settings = collections.OrderedDict({
        # General project info (autogenerated)
        "Absolute path": {"type": "str", "value": ""},
        "Output_path": {"type": "str", "value": ""},
        "Project structure combined": {"type": "dict", "value": copy.deepcopy(document_info_template)},
        "Project structure raw": {"type": "dict", "value": dict()},

        # Meta information section
        "Date created": {"type": "mapping/int", "value": [QDate.currentDate().year(), QDate.currentDate().month(),
                                                          QDate.currentDate().day()]},
        "Project type": {"type": "enum", "value": "Notes", "allowed values": ["Notes", "Article", "Book"]},
        "Additional meta information": {"type": "str", "value": ""},
        "Include_metainfo": {"type": "bool", "value": True},

        # Render section
        "Files to render": {"type": "mapping/str", "value": []},
        "Css_style": {"type": "str", "value": "manuwrite_strict"},
        "Csl_style": {"type": "str", "value": ""},
        "Render to": {"type": "str", "value": "html"},
        "Pandoc_command_manual": {"type": "str", "value": ""},
        "Pandoc_command_full": {"type": "str", "value": ""},

        # Pandoc section
        # Pandoc filters. Added to the command as --filter=key if the value is True
        "Pandoc_filters": {"type": "dict", "value": {
            "pandoc-xnos": True,
            "pandoc-secnos": True,
            "pandoc-fignos": True,
            "pandoc-tablenos": True,
            "pandoc-eqnos": True,
            "pandoc-citeproc": True,
            "pandoc-manubot-cite": True
        }},

        # YAML Metablock key-value pairs. Added to yaml metablock file if the value is not an empty string
        "YAML_metablock": {"type": "dict", "value": {
            # Meta information
            "title": "",
            "author": "",
            # TODO: add keywords to meta information in gui
            "keywords": "",
            "abstract": "",

            # Pandoc-xnos section
            "xnos-number-offset": "",
            "xnos-capitalise": False,
            # Pandoc-secnos section
            "secnos-cleveref": True,
            "secnos-plus-name": "",
            "secnos-star-name": "",
            # Pandoc-fignos section
            "fignos-cleveref": True,
            "fignos-number-by-section": True,
            "fignos-plus-name": "",
            "fignos-star-name": "",
            "fignos-caption-name": "",
            "fignos-caption-separator": "",
            # Pandoc-tablenos section
            "tablenos-cleveref": True,
            "tablenos-number-by-section": True,
            "tablenos-plus-name": "",
            "tablenos-star-name": "",
            "tablenos-caption-name": "",
            "tablenos-caption-separator": "",
            # Pandoc-eqnos section
            "eqnos-cleveref": True,
            "eqnos-number-by-section": True,
            "eqnos-eqref": False,
            "eqnos-plus-name": "",
            "eqnos-star-name": "",

            # Pandoc-citeproc
            "bibliography": ""
        }},

        # Pandoc keyword arguments (i.e. --key=value). Added to the command if the value is not an empty string.
        "Pandoc_kwargs": {"type": "dict", "value": {
            "to": "html",
            "css": "",
            "output": "",
            "number-offset": "",
            "metadata-file": ""
        }},

        # Pandoc non-keyword arguments (i.e. --arg). Added to the comman if the value is True
        "Pandoc_args": {"type": "dict", "value": {
            "number-sections": True,
            "standalone": True
        }},
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

            "MainWindow/ProjectTabWidget_currentTab/value": 0,
            "MainWindow/ProjectTabWidget_currentTab/type": "int",

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
            "AddHeadingDialog/autonumber/value": True,
            "AddHeadingDialog/autonumber/type": "bool",

            # TODO: Do we really need 3 radio button in that dialog??
            "AddHeadingDialog/autogen identifier/value": 0,
            "AddHeadingDialog/autogen identifier/type": "int",

            # Add image dialog
            "AddImageDialog/autogen identifier/value": True,
            "AddImageDialog/autogen identifier/type": "bool",

            "AddImageDialog/autonumber/value": True,
            "AddImageDialog/autonumber/type": "bool",

            # Add table dialog
            "AddTableDialog/autogen identifier/value": True,
            "AddTableDialog/autogen identifier/type": "bool",

            "AddTableDialog/autonumber/value": True,
            "AddTableDialog/autonumber/type": "bool",

            # Add footnote dialog
            "AddFootnoteDialog/autogen identifier/value": True,
            "AddFootnoteDialog/autogen identifier/type": "bool",

            # Application
            "Application/Project folder/value": QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Application/Project folder/type": "str",

            # General
            "General/Document_parsing_interval/value": 2000,
            "General/Document_parsing_interval/type": "int",

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

            "Render/Formats/value": {
                "html": {"name": "Html", "pandoc_option": "html", "file_extension": "html"},
                "pdf": {"name": "Pdf", "pandoc_option": "pdf", "file_extension": "pdf"},
                "docx": {"name": "Docx", "pandoc_option": "docx", "file_extension": "docx"}
            },
            "Render/Formats/type": "dict",

            "Render/Css_styles/value": {
                "style_identifier": {
                    "name": "style_name",
                    "path": "style_path"
                }
            },
            "Render/Css_styles/type": "dict",

            "Render/Csl_styles/value": {
                "style_identifier": {
                    "name": "style_name",
                    "path": "style_path"
                }
            },
            "Render/Csl_styles/type": "dict",

            "Colors/Color_schemas/value": {
                "schema_identifier": {
                    "name": "schema_name",
                    "path": "schema_path"
                }
            },
            "Colors/Color_schemas/type": "dict",

            "Colors/Icons/value": "Light",
            "Colors/Icons/type": "str",

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

ProjectStructureIcons = {
    "citations": {"icon": QIcon(":/icons_common/icons_common/citation-yellow.svg")},
    "figures": {"icon": QIcon(":/icons_common/icons_common/image-jpeg.svg")},
    "tables": {"icon": QIcon(":/icons_common/icons_common/table-red.svg")},
    "footnotes": {"icon": QIcon(":/icons_common/icons_common/footnote-blue.svg")},
    "headings": {"icon": QIcon(":/icons_common/icons_common/heading-purple.svg")}
}

identifier_categories = ["headings", "figures", "citations", "footnotes", "tables"]

identifier_prefixes = {
    "headings": "sec",
    "figures": "fig",
    "tables": "tbl"
}


def get_default_color_schema(palette: QPalette) -> dict:
    """Returns a default color schema based on a given palette"""
    default_color_schema = {
        "Data type": "Manuwrite color schema",
        "Schema name": "System colors",
        "Application_colors": {
            "window": {
                "name": "Window background",
                "color": palette.color(palette.Window).name()
            },
            "window_text": {
                "name": "Window text",
                "color": palette.color(palette.WindowText).name()
            },
            "base": {
                "name": "Base",
                "color": palette.color(palette.Base).name()
            },
            "alternate_base": {
                "name": "Alternate base",
                "color": palette.color(palette.AlternateBase).name()
            },
            "tooltip_base": {
                "name": "Tooltip base",
                "color": palette.color(palette.ToolTipBase).name()
            },
            "tooltip_text": {
                "name": "Tooltip text",
                "color": palette.color(palette.ToolTipText).name()
            },
            "placeholder_text": {
                "name": "Placeholder text",
                "color": palette.color(palette.PlaceholderText).name()
            },
            "text": {
                "name": "Text",
                "color": palette.color(palette.Text).name()
            },
            "button": {
                "name": "Button base",
                "color": palette.color(palette.Button).name()
            },
            "button_text": {
                "name": "Button text",
                "color": palette.color(palette.ButtonText).name()
            },
            "bright_text": {
                "name": "Bright text",
                "color": palette.color(palette.BrightText).name()
            },
        },
        "Editor_colors": {"background": {"name": "Editor background",
                                         "color": palette.color(palette.Base).name()},
                          "text": {"name": "Text",
                                   "color": palette.color(palette.Text).name()},
                          "current_line": {"name": "Current line",
                                           "color": palette.color(palette.AlternateBase).name()},
                          "linenumber_area": {"name": "Line number area",
                                              "color": palette.color(palette.AlternateBase).darker(150).name()},
                          "linenumber_text": {"name": "Line number area text",
                                              "color": palette.color(palette.Text).name()}
                          },
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
                            "superscript": {"name": "Superscript",
                                            "color": "#4081d1"},
                            "subscript": {"name": "Subscript",
                                          "color": "#4081d1"},
                            "footnote": {"name": "Footnote",
                                         "color": "#ff0000"},
                            "table": {"name": "Table",
                                      "color": "#0000ff"},
                            "cross-reference": {"name": "Cross reference",
                                                "color": "#00ff00"}
                            }
    }

    return default_color_schema
