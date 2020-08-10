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
