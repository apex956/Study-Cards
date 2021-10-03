import os
from enum import Enum, unique
from collections import namedtuple
from configparser import ConfigParser


class Const:
    F_SEPARATOR = ";"  # field separator in import file and in work file
    FILE_PATH = os.path.join('..', 'data', '')  # a relative path in any OS


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


class Cnf:
    def str_to_bool(s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError

    config_object = ConfigParser()
    config_object.read("config.ini")

    app_info = config_object["APP_INFO"]
    term1 = app_info["term1"]
    term2 = app_info["term2"]

    file_import_info = config_object["FILE_IMPORT_INFO"]
    import_file_request = str_to_bool(file_import_info["import_file_request"])
    import_file_name = file_import_info["import_file_name"]
    set_title = file_import_info["set_title"]  # The title of the study set
    set_id = file_import_info["set_id"]  # The ID of the study set
    w_file = "work_file_" + set_id + ".txt"

