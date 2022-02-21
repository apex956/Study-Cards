import os
from enum import Enum, unique
from collections import namedtuple
from configparser import ConfigParser
import logging


class Const:
    LOG_LEVEL = logging.DEBUG  # For production version change the level from DEBUG to INFO
    F_SEPARATOR = ";"  # field separator in import file and in work file
    FILE_PATH = os.path.join('..', 'data', '')  # a relative path in any OS
    JSON_F_NAME = "sets_config.json"  # Name of study sets JSON configuration file
    CNF_INI_F_NAME = "config.ini"  # Name of the main configuration file


class GuiTc:
    MW_WIDTH = 1100  # The width of the main window in pixels
    BUTTON_FONT = "Helvetica 16"
    R_B_FONT = "Helvetica 14"  # RADIO_BUTTON_FONT
    RB_BG = "white smoke"  # Radio Button Background color
    L2_FRAME_BG = "white smoke"  # The background color of level 2 frames
    FRONT_CARD_COLOR = "lightgrey"
    BACK_CARD_COLOR = "lavender"


class CrdOrdr:
    CardOrder = namedtuple("CardOrder", ["val", "txt"])
    Alphabetical = CardOrder(11, "Alphabetical")
    Random = CardOrder(22, "Random")
    Original = CardOrder(33, "Original")


class PopUpType:
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    QUESTION = "Question"


class LnIdx:
    """ Index to data within lines of the work file and the term list data structure """
    TERM1_IDX = 0
    TERM2_IDX = 1
    TERM1_TAG_IDX = 2
    TERM2_TAG_IDX = 3


class Fltr:
    VAL = 0  # index for value in the tuples below
    TXT = 1  # index for radio button text in the tuples below
    NO_FLTR = (0, "All tags")
    LOW_FLTR = (1, "Poor")  # level of knowledge of studied terms
    MED_FLTR = (2, "Moderate")
    HIGH_FLTR = (3, "Good")
    GEN_FLTR = (4, "Fairly good")  # for example: spelling problems
    UNTAGGED_FLTR = (5, "Untagged")

    @classmethod
    def filter_val_to_txt(cls, filter_val):
        if filter_val == cls.UNTAGGED_FLTR[cls.VAL]:
            return cls.UNTAGGED_FLTR[cls.TXT]
        elif filter_val == cls.LOW_FLTR[cls.VAL]:
            return cls.LOW_FLTR[cls.TXT]
        elif filter_val == cls.MED_FLTR[cls.VAL]:
            return cls.MED_FLTR[cls.TXT]
        elif filter_val == cls.HIGH_FLTR[cls.VAL]:
            return cls.HIGH_FLTR[cls.TXT]
        elif filter_val == cls.GEN_FLTR[cls.VAL]:
            return cls.GEN_FLTR[cls.TXT]
        elif filter_val == cls.NO_FLTR[cls.VAL]:
            return cls.NO_FLTR[cls.TXT]
        else:
            print("Filter not found!")
            raise ValueError


class Tag:
    TagInfo = namedtuple("TagInfo", ["d_txt", "val", "rb_txt"])
    NoTag = TagInfo("not tagged", 0, "No tag")
    LowTag = TagInfo("tagged low", 1, "Poor (P)")
    MedTag = TagInfo("tagged med", 2, "Moderate (M)")
    HighTag = TagInfo("tagged high", 3, "Good (G)")
    GenTag = TagInfo("tagged minor", 4, "Fairly good")

    # value to data text dictionary
    tvdt_dir = {NoTag.val: NoTag.d_txt,
                LowTag.val: LowTag.d_txt,
                MedTag.val: MedTag.d_txt,
                HighTag.val: HighTag.d_txt,
                GenTag.val: GenTag.d_txt}

    # data text to value dictionary
    tdtv_dir = {NoTag.d_txt: NoTag.val,
                LowTag.d_txt: LowTag.val,
                MedTag.d_txt: MedTag.val,
                HighTag.d_txt: HighTag.val,
                GenTag.d_txt: GenTag.val}
