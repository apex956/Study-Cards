import os
from enum import Enum, unique


class Const:
    f_separator = ";"  # field separator in import file and in work file
    filepath = os.path.join('..', 'data', '')  # a relative path in any OS
    FRONT_CARD_COLOR = "lightgrey"
    BACK_CARD_COLOR = "lavender"


@unique
class PopUpType(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class LnIdx:
    """ Index to data within lines of the work file and the term list data structure """
    TERM1_IDX = 0
    TERM2_IDX = 1
    TERM1_TAG_IDX = 2
    TERM2_TAG_IDX = 3
