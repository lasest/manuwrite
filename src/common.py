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
