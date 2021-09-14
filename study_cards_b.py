"""
Description: This is the base module of the Study Cards application for studying languages or
memorizing facts.
Created: August 2021
Authors: Amir Bar-Sever
Programming language: Python 3
Status: work in progress
"""
# ==============================================================
# This file includes: Configuration variables, enums and types as well as global variables
# Note: export from Quizlet with a ";" separator between the sides of the card
#
#===============================================================

import random
import tkinter as tk
import tkinter.messagebox
import pathlib
import sys
import os
from fileinput import FileInput
from collections import namedtuple
from enum import Enum
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

PROJINFO = config_object["PROJINFO"]
language1 = PROJINFO["language1"]
language2 = PROJINFO["language2"]
number_of_sets = PROJINFO["number_of_sets"]
import_file_name = PROJINFO["import_file_name"]
set_title = PROJINFO["set_title"]  # The title of the study set

filepath = os.path.join('.', 'data', '')  # a relative path in any OS
import_word_file = True  # import a file per user demand.
f_separator = ";"  # field separator in import file and in work file
w_file = import_file_name.removesuffix(".txt")+"_dat"+".txt"

term_list = []  # list of terms and answers taken from the work file
ab_sort_lst = []  # list of indexes of the alphabetically sorted term list
shuffled_list = []  # list of indexes of the shuffled term list
front_side = 0  # The term side of the card
back_side = 1  # The answer side of the card
mode = "alphabetical"  # Terms are arranged alphabetically based on the 1st side only
line_number = 0  # The running index of the lines in the file and in the list of terms
act_ln = 0  # The index of the displayed line
card_side = front_side
card_text = []  # The text of both sides of the current card
filtered_ab_sort_lst = []
filtered_shuffled_list = []
filtered_term_list = []
filtered_list_size = 0


# structure of data in work file and in RAM
lang1_idx = 0
lang2_idx = 1
lang1_tag_idx = 2
lang2_tag_idx = 3

# from language index to language and vice versa
languages = [language1, language2]
l_dir = {language1: 0,
         language2: 1}

# The filter does not change with 1st language
VAL = 0  # index for value
TXT = 1  # index for radio button text
NO_FILTER = [0, "Show all"]
LOW_FILTER = [1, "Show low"]  # level of knowledge of studied terms
MED_FILTER = [2, "Show medium"]
HIGH_FILTER = [3, "Show high"]
GEN_FILTER = [4, "Show generic"]  # for example: spelling problems
UNTAGGED_FILTER = [5, "Show untagged"]


TagInfo = namedtuple("TagInfo", ["d_txt", "val", "rb_txt"])
NoTag = TagInfo("not tagged", 0, "No tags")
LowTag = TagInfo("tagged low", 1, "Low")
MedTag = TagInfo("tagged med", 2, "Med")
HighTag = TagInfo("tagged high", 3, "High")
GenTag = TagInfo("tagged gen", 4, "Generic")

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

class PopUpType:
    Info = 0
    Warning = 1
    Error = 2
