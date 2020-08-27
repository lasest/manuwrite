from collections import OrderedDict
import copy

from PyQt5.QtWidgets import QTreeWidgetItem

from resources import icons_rc
import defaults


class ProjectError(Exception):

    def __init__(self, message: str = ""):
        self.message = message


def is_valid_identifier(identifier: str, allow_empty: bool = False) -> bool:
    result = True

    if identifier.find(" ") >= 0 or identifier.find("\t") >= 0:
        result = False

    if identifier == "" and not allow_empty:
        result = False

    return result


def generate_identifier(text: str, prefix: str = "", used_identifiers=None) -> str:
    """Generates a valid pandoc identifier from given text and adds a specified prefix to it. Then checks if the
    generated identifier is in used_identifiers. If it is, creates a unique identifier by adding a number at the end"""

    if used_identifiers is None:
        used_identifiers = set()

    text = text.strip()

    # Convert all to lowercase
    text = text.lower()

    # Replace all spaces with hyphens
    text = text.replace(" ", "-")

    # Remove everything up to the first letter
    index = -1
    for i in range(len(text)):
        if text[i].isalpha():
            index = i
            break

    if index == -1:
        text = ""
    else:
        text = text[index:]

    # Remove all non-alphanumeric characters, except underscores, hyphens, and periods
    clear_text = ""
    for index in range(len(text)):
        if text[index].isalnum() or text[index] in {'_', '-', '.'}:
            clear_text += text[index]

    identifier = prefix + clear_text

    # Check if identifier is not already used
    if identifier in used_identifiers:
        i = 1
        while identifier + "-" + str(i) in used_identifiers:
            i += 1
        identifier = identifier + "-" + str(i)

    return identifier


def load_project_structure(project_structure: dict, tree_widget, exclude_categories: list = None) -> None:
    """Populates the tree widget with given project structure"""
    top_level_items = []

    if exclude_categories is None:
        exclude_categories = list()

    item_categories = copy.deepcopy(defaults.identifier_categories)
    for item in exclude_categories:
        item_categories.remove(item)
    item_categories.remove("headings")

    def get_entry_info(entry) -> list:
        """Returns a list of value, each for the corresponding column of the tree"""
        info = [
            entry[0],
            entry[1]["text"],
            str(entry[1]["block_number"]),
            entry[1]["project_filepath"]
        ]

        if "level" in entry[1]:
            info.append(str(entry[1]["level"]))
        else:
            info.append("")

        return info

    def create_item_from_entry(entry, entry_category):
        """Creates a QWidgetItem from a given entry if project_structure sub dictionaries. Sets its parent based on
        header index. If header index is -1, adds it to top level items list"""
        header_index = entry[1]["current_header_index"]
        if header_index >= 0:
            parent = headings[header_index]
            item = QTreeWidgetItem(parent, get_entry_info(entry))
        else:
            item = QTreeWidgetItem(get_entry_info(entry))
            top_level_items.append(item)

        item.setIcon(0, defaults.ProjectStructureIcons[entry_category]["icon"])

    tree_widget.clear()

    # Form a list of all the headings in the structure
    headings = []
    for heading in project_structure["headings"].items():
        level = int(heading[1]["level"])

        # Find header's parent heading or create it w/o a parent, if it is a top level heading
        parent = None
        for item in reversed(headings):
            if int(item.text(4)) < level:
                parent = item
                break
        if parent:
            item = QTreeWidgetItem(parent, get_entry_info(heading))
        else:
            item = QTreeWidgetItem(get_entry_info(heading))

        item.setIcon(0, defaults.ProjectStructureIcons["headings"]["icon"])
        headings.append(item)

    # Add all other elements of the tree
    for category in item_categories:
        for item in project_structure[category].items():
            create_item_from_entry(item, category)

    # Add top level items and headings. All child items seem to be added automatically after this step
    tree_widget.insertTopLevelItems(0, top_level_items)
    tree_widget.insertTopLevelItems(0, headings)

    tree_widget.expandAll()
    tree_widget.resizeColumnToContents(0)
