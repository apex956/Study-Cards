import os
from enum import Enum, unique
from collections import namedtuple


class Const:
    F_SEPARATOR = ";"  # field separator in import file and in work file
    FILE_PATH = os.path.join('..', 'data', '')  # a relative path in any OS
    FRONT_CARD_COLOR = "lightgrey"
    BACK_CARD_COLOR = "lavender"


class GuiTc:
    MW_WIDTH = 1100  # The width of the main window in pixels
    BUTTON_FONT = "Helvetica 16"
    R_B_FONT = "Helvetica 14"  # RADIO_BUTTON_FONT
    RB_BG = "white smoke"  # Radio Button Background color
    L2_FRAME_BG = "white smoke"  # The background color of level 2 frames


class CrdOrdr:
    CardOrder = namedtuple("CardOrder", ["val", "txt"])
    Alphabetical = CardOrder(11, "Alphabetical")
    Random = CardOrder(22, "Random")
    Original = CardOrder(33, "Original")


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
