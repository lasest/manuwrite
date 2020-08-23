from typing import List

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextDocument

import defaults


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


# Create a list of IdentifierParser objects
patterns = defaults.parser_patterns
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
