from typing import Tuple

from PyQt5.QtCore import QRegExp

import common


# Extractor functions
# Extractor function takes one string to be parsed and returns a tuple of parsed identifier and a dictionary in the
# form of {identifier: {text: [name], ...}}. 'text' field must be present. This value will be displayed in project
# structure tree as the name of the entry. Other optional field may be added


def heading_extractor(heading: str) -> Tuple[str, dict]:
    """Extracts information about a heading from the heading tag"""

    identifier_regexp = QRegExp(r"\{#sec:\w\w*|\{#\w\w*")
    loffset = 2

    # Determine heading level
    heading = heading.strip()
    length = len(heading)
    heading = heading.lstrip("#")
    heading_level = length - len(heading)
    if heading_level > 6:
        heading_level = 6

    # Save heading text
    attributes_index = heading.find("{")
    heading_text = ""
    if attributes_index != -1:
        heading_text = heading[:attributes_index]
    else:
        heading_text = heading

    heading_text = heading_text.strip(" #")

    # Check if heading has explicit identifier
    index = identifier_regexp.indexIn(heading)
    if index >= 0:
        identifier = heading[index + loffset:index + identifier_regexp.matchedLength()]

    # Generate an implicit identifier if there is no explicit one
    if index == -1:
        identifier = common.generate_identifier(heading_text)

    # Return resulting dictionary
    return identifier, {identifier: {"text": heading_text,
                                     "level": heading_level}}


def figure_extractor(image_tag: str) -> Tuple[str, dict]:
    """Extracts information about an image from image tag"""
    identifier_regexp = QRegExp(r"\{#fig:\w\w*")
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
