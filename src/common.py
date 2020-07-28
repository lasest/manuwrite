from enum import Enum


class Result(Enum):
    CANCEL = 0
    SAVE = 1
    DISCARD = 2

class ProjectError(Exception):

    def __init__(self, message: str = ""):
        self.message = message
