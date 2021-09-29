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
import json
import config_frame
import presnt_frame


class PopUpType:
    Info = "Info"
    Warning = "Warning"
    Error = "Error"


class StudyCardsApp:

    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        app_info = config_object["APP_INFO"]
        self.term1 = app_info["term1"]
        self.term2 = app_info["term2"]
        file_import_info = config_object["FILE_IMPORT_INFO"]
        self.import_file_request = self.str_to_bool(file_import_info["import_file_request"])
        self.import_file_name = file_import_info["import_file_name"]
        self.set_title = file_import_info["set_title"]  # The title of the study set
        self.set_id = file_import_info["set_id"]  # The ID of the study set
        self.filepath = os.path.join('..', 'data', '')  # a relative path in any OS
        self.f_separator = ";"  # field separator in import file and in work file
        self.w_file = "work_file_" + self.set_id + ".txt"
        self.term_list = []  # list of terms and answers taken from the work file
        self.ab_sort_list = []  # list of indexes of the alphabetically sorted term list
        self.shuffled_list = []  # list of indexes of the shuffled term list
        self.front_side = 0  # The term side of the card
        self.back_side = 1  # The answer side of the card
        self.line_number = 0  # The running index of the lines in the file and in the list of terms
        self.act_ln = 0  # The index of the displayed line
        self.card_side = self.front_side
        self.filtered_ab_sort_list = []
        self.filtered_shuffled_list = []
        self.filtered_term_list = []
        self.filtered_list_size = 0
        self.study_set_conf_list = []

        # Index to data in lines of work file and volatile data structure
        self.lang1_idx = 0
        self.lang2_idx = 1
        self.lang1_tag_idx = 2
        self.lang2_tag_idx = 3

        # from language index to language and vice versa
        self.languages = [self.term1, self.term2]
        self.l_dir = {self.term1: 0,
                      self.term2: 1}

        TagInfo = namedtuple("TagInfo", ["d_txt", "val", "rb_txt"])
        self.NoTag = TagInfo("not tagged", 0, "No tags")
        self.LowTag = TagInfo("tagged low", 1, "Low")
        self.MedTag = TagInfo("tagged med", 2, "Med")
        self.HighTag = TagInfo("tagged high", 3, "High")
        self.GenTag = TagInfo("tagged gen", 4, "Generic")

        # value to data text dictionary
        self.tvdt_dir = {self.NoTag.val: self.NoTag.d_txt,
                         self.LowTag.val: self.LowTag.d_txt,
                         self.MedTag.val: self.MedTag.d_txt,
                         self.HighTag.val: self.HighTag.d_txt,
                         self.GenTag.val: self.GenTag.d_txt}

        # data text to value dictionary
        self.tdtv_dir = {self.NoTag.d_txt: self.NoTag.val,
                         self.LowTag.d_txt: self.LowTag.val,
                         self.MedTag.d_txt: self.MedTag.val,
                         self.HighTag.d_txt: self.HighTag.val,
                         self.GenTag.d_txt: self.GenTag.val}

        CardOrder = namedtuple("CardOrder", ["val", "txt"])
        self.Alphabetical = CardOrder(11, "Alphabetical")
        self.Random = CardOrder(22, "Random")
        self.Original = CardOrder(33, "Original")

        self.card_order = self.Alphabetical.val  # Terms are arranged alphabetically based on the 1st side only

        if self.import_file_request:
            self.import_term_file(self.filepath, self.import_file_name, self.w_file)

        self.read_work_file()

        self.sort_and_shuffle_term_list()

        self.get_conf_from_file()

    @staticmethod
    def display_pop_up(pu_type, txt):
        """
        Function displays three types of pop-up messages without showing the root window.
        The root window has to be destroyed each time.
        Function has side effect: the main window of the app created later goes to
        background. This problem is fixed with the command: window.attributes('-topmost', 'true')
        The argument 'pu_type' is the type of the pop-up (a.k.a. messagebox)
        The argument 'txt' is the displayed text
        """
        msg = tk.Tk()
        msg.withdraw()
        pu_title = pu_type
        if pu_type == PopUpType.Warning:
            tk.messagebox.showwarning(title=pu_title, message=txt)
        elif pu_type == PopUpType.Error:
            tk.messagebox.showerror(title=pu_title, message=txt)
        elif pu_type == PopUpType.Info:
            tk.messagebox.showinfo(title=pu_title, message=txt)
        else:
            print("Unexpected value of pu_type argument:", pu_type)
        msg.destroy()

    def import_term_file(self, in_f_path, in_f_name, w_file_name):
        """
        Description: This function creates a work file and copies the content of
        the imported file to a work file. It also adds default tagging.
        This is done only if the work file cannot be found.
        Note: This function will be used for merging the two files

        :param in_f_path: the path to the directory of the imported file and the work file
        :param in_f_name: the name of the imported file
        :param in_f_name: the name of the work file
        :return: None
        """
        in_file_path = in_f_path + in_f_name
        in_line_list = []  # list of lines read from the import file
        p_line = -1
        try:
            in_file_ref = open(in_file_path, "r")
        except OSError as e:
            wrn_txt = "Couldn't open a file to be imported"
            print(e, wrn_txt)
            self.display_pop_up(PopUpType.Warning, wrn_txt)
            return
        try:
            for t_idx, in_line in enumerate(in_file_ref):
                if in_line.count(self.f_separator) > 1:
                    p_line = t_idx
                    raise ValueError
                in_line_list.append(in_line.split(self.f_separator))
        except ValueError:
            warning_txt = "Found an unexpected separator character '" + self.f_separator + \
                          "' in line " + str(p_line) +\
                          " of the imported file. " + "The file was not imported."
            print(warning_txt)
            self.display_pop_up(PopUpType.Warning, warning_txt)
            return
        finally:
            in_file_ref.close()

        w_file_path = pathlib.Path(self.filepath+w_file_name)
        if w_file_path.is_file():
            # work file exists - add here the ability to merge with an imported file
            print("Work file found. No file importing was performed")
            return
        else:
            print("Work file not found. Import is attempted")
            try:
                w_file_ref = open(w_file_path, "w")
            except OSError as e:
                err_txt = "couldn't open the work file for writing"
                print(e, err_txt)
                self.display_pop_up(PopUpType.Error, err_txt)
                sys.exit()

        for d_line in in_line_list:
            w_file_ref.write(d_line[self.lang1_idx].rstrip() + self.f_separator +
                             d_line[self.lang2_idx].strip() + self.f_separator +
                             self.term1 + " " + self.NoTag.d_txt + self.f_separator +
                             self.term2 + " " + self.NoTag.d_txt + "\n")
        self.display_pop_up(PopUpType.Info, "File was imported")
        w_file_ref.close()

    def read_work_file(self):
        # read the vocabulary list from the work-file
        try:
            w_fl_ref = open(self.filepath+self.w_file, "r", encoding="utf8")
        except OSError:
            print("Couldn't open the work file")
            sys.exit()

        for r_line in w_fl_ref:
            line_content = r_line.split(self.f_separator)
            self.term_list.append(line_content)

        print("The 1st line from the work file: ", self.term_list[0])
        w_fl_ref.close()

    @staticmethod
    def use_1st_str(lst1):
        return lst1[0].capitalize()

    @staticmethod
    def str_to_bool(s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            raise ValueError

    def sort_and_shuffle_term_list(self):
        sort_lst = []
        for ln_idx, line in enumerate(self.term_list):
            sort_lst.append([line[0], ln_idx])

        sort_lst.sort(key=self.use_1st_str)
        for line in sort_lst:
            self.ab_sort_list.append(line[1])

        self.shuffled_list = list(range(len(self.term_list)))
        random.shuffle(self.shuffled_list)

    def get_tag_dt_txt(self, line):
        """Returns the tag value for a line of data and the shown language  """
        lang_idx = self.card_side
        data_text1 = self.term_list[line][lang_idx + 2]
        # parse the text to remove the language
        if data_text1.startswith(self.term1):
            data_text = data_text1.removeprefix(self.term1 + " ")
        elif data_text1.startswith(self.term2):
            data_text = data_text1.removeprefix(self.term2 + " ").rstrip()
        else:
            raise ValueError
        return data_text

    def set_act_line(self):
        """
        Set the global parameter act_ln (actual line) depending on the card order
        """
        if self.card_order == self.Original.val:
            self.act_ln = self.filtered_term_list[self.line_number]
        elif self.card_order == self.Alphabetical.val:
            self.act_ln = self.filtered_ab_sort_list[self.line_number]
        elif self.card_order == self.Random.val:
            self.act_ln = self.filtered_shuffled_list[self.line_number]
        else:
            raise ValueError

    def update_tag_in_w_file(self, line_num, lang_idx, tag):
        """
        Write the tagging string into the work file
        This is done when the tagging radio button is changed
        :param line_num:
        :param lang_idx:
        :param tag:
        :return:
        """
        with FileInput(files=[self.filepath+self.w_file], inplace=True) as wf:
            if lang_idx == self.lang1_idx:
                lang_tag_idx = self.lang1_tag_idx
                language = self.term1
            elif lang_idx == self.lang2_idx:
                lang_tag_idx = self.lang2_tag_idx
                language = self.term2
            else:
                raise ValueError
            for idx, line in enumerate(wf):
                line = line.rstrip()
                info = line.split(self.f_separator)
                if idx == line_num:
                    info[lang_tag_idx] = language + " " + tag
                line = self.f_separator.join(str(x) for x in info)
                print(line)

    def save_config_to_file(self):
        sets_conf_struct = [{"ID": 1001, "title": "Verbs", "no_of_terms": 20,
                            "params": {"cnf_front_side": self.front_side,
                                       "filter": 0,
                                 "card_order": "Original",
                                 "last_card": 7}
                            }]


        sets_conf_struct.append( {"ID": 1002, "title": "Nouns","no_of_terms": 30,})
        sets_conf_struct[0]["no_of_terms"] = 25
        sets_config_name = "sets_config.json"
        with open(sets_config_name, "w") as write_file:
            json.dump(sets_conf_struct, write_file, indent=4)

    def get_conf_from_file(self):
        sets_config_name = "sets_config.json"
        with open(sets_config_name, "r") as read_file:
            sets_conf_struct = json.load(read_file)
            print(sets_conf_struct)
        pass



class StudySetConf:
    """
    Each object maintains parameters of a study-set
    """
    def __init__(self, s_set_id, s_set_title, s_set_front_side, s_set_filter, s_set_card_order, s_set_last_card=0):
        self.id_key = "ID"
        self.id_val = s_set_id
        self.title_key = "Title"
        self.title_val = s_set_title
        self.front_side_key = "Front_side"
        self.front_side_val = s_set_front_side
        self.filter_key = "Filter"
        self.filter_val = s_set_filter
        self.card_order_key = "Card_order"
        self.filter_val = s_set_card_order
        self.last_card_key = "Last_card"
        self.last_card_val = s_set_last_card
        self.tags_key = "Set_tags"
        self.tags_val = []
        self.s_set_conf = {self.id_key:self.id_val, elf.title_key: elf.title_val}

    def get_study_set_id(self):
        return self.id_val

    def change_title(self, new_title):
        self.s_set_conf[self.title_key] = new_title



class MainWin:
    BUTTON_FONT = "Helvetica 16"
    RADIO_BUTTON_FONT = "Helvetica 14"
    RB_BG = "white smoke"  # Radio Button Background color
    L2_FRAME_BG = "white smoke"  # The background color of level 2 frames

    def __init__(self, window, app):
        window.title("Study Cards")
        window.geometry('1100x700')
        window.resizable(False, False)
        title1_txt = app.term1 + " " + app.term2 + " Vocabulary"
        tk.Label(window, text=title1_txt, font="Helvetica 20 bold").place(relx=0.3, rely=0.0)
        title2_txt = "Study Set: " + app.set_title
        tk.Label(window, text=title2_txt, font="Helvetica 16 bold").place(relx=0.4, rely=0.05)

        window.attributes('-topmost', 'true')
        self._conf_frame = config_frame.ConfFrame(self, window, app)
        self._prsnt_frame = presnt_frame.PresentationFrame(self, window, app)
        self._app = app
        self._window = window

    def flash_cards_button_clicked(self):
        self._conf_frame.config_frame_obj.place_forget()
        self._prsnt_frame.presentation_frame_obj.place(relx=0.1, rely=0.1)
        self._conf_frame.create_filtered_index_lists(self._app)
        self._prsnt_frame.nxt_back_button_clicked(nxt=True, start_over=True)

    def config_button_clicked(self):
        self._conf_frame.config_frame_obj.place(relx=0.1, rely=0.1)
        self._prsnt_frame.presentation_frame_obj.place_forget()

    def on_close(self):
        print("Main Window is closing, write the configuration to JSON file")
        self._app.save_config_to_file()
        self._window.destroy()

def main():
    if sys.version_info[0] < 3:
        raise Exception("Must use Python 3")
    app = StudyCardsApp()
    window = tk.Tk()  # The root
    m_win = MainWin(window, app)
    window.protocol("WM_DELETE_WINDOW", m_win.on_close)
    window.mainloop()


if __name__ == "__main__":
    main()
