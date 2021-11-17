import random
import tkinter as tk
import tkinter.messagebox
import pathlib
import sys
from fileinput import FileInput
import json
from configparser import ConfigParser
import config_frame as cfr
import presnt_frame as prf
from constants import Const, PopUpType, LnIdx, GuiTc, CrdOrdr, Tag, Fltr


class StudyCardsApp:
    def __init__(self, root):
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
        self.filter_cards_val = 0
        self.running_study_set_conf = {}
        self.study_set_conf_list = []
        self.reset_cards_request = False
        self.untagged_filter_list_size = 0
        self.high_filter_list_size = 0
        self.med_filter_list_size = 0
        self.low_filter_list_size = 0
        self.gen_filter_list_size = 0
        self.card_order = CrdOrdr.Alphabetical.val  # Terms are arranged alphabetically based on the 1st side only
        self.term1 = None
        self.term2 = None
        self.terms = [None, None]
        self.current_set_id = None
        self.current_set_title = None
        self.current_import_file_name = None
        self.current_w_file = None
        self.current_import_file_request = None
        self.state_of_study_sets = []
        self.allow_to_save_the_state_of_study_sets = False
        self.id_list = None

        self.read_configuration_file()


    def read_shuffle_etc(self):  # refactor name !!!
        if self.current_import_file_request:
            self.import_term_file(Const.FILE_PATH, self.current_import_file_name, self.current_w_file)

        self.read_work_file()

        self.sort_and_shuffle_term_list()

        self.get_study_set_conf_from_file()


    def read_configuration_file(self):
        """
        Reading the configuration of all the study sets in the config.ini file
        Each study set configuration is read into a dictionary.
        All these dictionaries are appended into a list
        :return: None
        """
        self.study_set_conf_list = []
        self.config_object = ConfigParser()
        self.config_object.read("config.ini")

        app_info = self.config_object["APP_INFO"]
        self.term1 = app_info["term1"]
        self.term2 = app_info["term2"]
        self.terms = [self.term1, self.term2]

        study_sets = self.config_object["STUDY_SETS_ID_LIST"]
        self.id_list = study_sets["id_list"].split(",")

        # read config of multiple sets
        for s_set_id in self.id_list:
            study_set_cnf = self.config_object["STUDY_SET_"+s_set_id]
            study_set_cnf_dir = {}
            study_set_cnf_dir["study_set_id"] = s_set_id
            study_set_cnf_dir["import_file_request"] = self.str_to_bool(study_set_cnf["import_file_request"])
            study_set_cnf_dir["import_file_name"] = study_set_cnf["import_file_name"]
            study_set_cnf_dir["study_set_title"] = study_set_cnf["study_set_title"]
            study_set_cnf_dir["w_file"] = "work_file_" + s_set_id + ".txt"
            self.study_set_conf_list.append(study_set_cnf_dir)


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
        if pu_type == PopUpType.WARNING:
            tk.messagebox.showwarning(title=pu_title, message=txt)
        elif pu_type == PopUpType.ERROR:
            tk.messagebox.showerror(title=pu_title, message=txt)
        elif pu_type == PopUpType.INFO:
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
            self.display_pop_up(PopUpType.WARNING, wrn_txt)
            return
        try:
            for t_idx, in_line in enumerate(in_file_ref):
                if in_line.count(Const.F_SEPARATOR) > 1:
                    p_line = t_idx
                    raise ValueError
                in_line_list.append(in_line.split(Const.F_SEPARATOR))
        except ValueError:
            warning_txt = "Found an unexpected separator character '" + Const.F_SEPARATOR + \
                          "' in line " + str(p_line) +\
                          " of the imported file. " + "The file was not imported."
            print(warning_txt)
            self.display_pop_up(PopUpType.WARNING, warning_txt)
            return
        finally:
            in_file_ref.close()

        w_file_path = pathlib.Path(Const.FILE_PATH+w_file_name)
        if w_file_path.is_file():
            # work file exists - add here the ability to merge with an imported file
            print("Work file found. No file importing was performed")
            return
        else:
            print("Work file not found. Import is attempted")
            try:
                w_file_ref = open(w_file_path, "w")
            except OSError as e:
                err_txt = "couldn't open the work file for writing. Exiting the application."
                print(e, err_txt)
                self.display_pop_up(PopUpType.ERROR, err_txt)
                sys.exit()

        for d_line in in_line_list:
            w_file_ref.write(d_line[LnIdx.TERM1_IDX].rstrip() + Const.F_SEPARATOR +
                             d_line[LnIdx.TERM2_IDX].strip() + Const.F_SEPARATOR +
                             self.term1 + " " + Tag.NoTag.d_txt + Const.F_SEPARATOR +
                             self.term2 + " " + Tag.NoTag.d_txt + "\n")
        self.display_pop_up(PopUpType.INFO, "File was imported")
        w_file_ref.close()

    def read_work_file(self):
        # read the vocabulary list from the work-file
        try:
            w_fl_ref = open(Const.FILE_PATH+self.current_w_file, "r", encoding="utf8")
        except OSError:
            disp_txt = "Couldn't open the work file. Exiting the application."
            print(disp_txt)
            self.display_pop_up(PopUpType.ERROR, disp_txt)
            sys.exit()

        self.term_list = []
        for r_line in w_fl_ref:
            line_content = r_line.split(Const.F_SEPARATOR)
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
        self.ab_sort_list = []
        for line in sort_lst:
            self.ab_sort_list.append(line[1])

        self.shuffled_list = list(range(len(self.term_list)))
        random.shuffle(self.shuffled_list)

    def get_tag_dt_txt(self, line):
        """ Returns the tag value for a line of data and the shown side  """
        term_idx = self.front_side
        data_text1 = self.term_list[line][term_idx + 2]
        dbg_txt = self.term_list[line]

        # parse the text to remove the language
        if data_text1.startswith(self.term1):
            pref_len = len(self.term1) + 1
            data_text = data_text1[pref_len:]
        elif data_text1.startswith(self.term2):
            pref_len = len(self.term2) + 1
            data_text = data_text1[pref_len:].rstrip()
        else:
            raise ValueError(dbg_txt)
        return data_text

    def set_act_line(self):
        """
        Set the global parameter act_ln (actual line) depending on the card order
        """
        if self.card_order == CrdOrdr.Original.val:
            self.act_ln = self.filtered_term_list[self.line_number]
        elif self.card_order == CrdOrdr.Alphabetical.val:
            self.act_ln = self.filtered_ab_sort_list[self.line_number]
        elif self.card_order == CrdOrdr.Random.val:
            self.act_ln = self.filtered_shuffled_list[self.line_number]
        else:
            raise ValueError

    def update_tag_in_w_file(self, line_num, term_idx, tag):
        """
        Write the tagging string into the work file
        This is done when the tagging radio button is changed
        :param line_num:
        :param term_idx:
        :param tag:
        :return:
        """
        with FileInput(files=[Const.FILE_PATH+self.current_w_file], inplace=True) as wf:
            if term_idx == LnIdx.TERM1_IDX:
                lang_tag_idx = LnIdx.TERM1_TAG_IDX
                term = self.term1
            elif term_idx == LnIdx.TERM2_IDX:
                lang_tag_idx = LnIdx.TERM2_TAG_IDX
                term = self.term2
            else:
                raise ValueError
            for idx, line in enumerate(wf):
                line = line.rstrip()
                info = line.split(Const.F_SEPARATOR)
                if idx == line_num:
                    info[lang_tag_idx] = term + " " + tag
                line = Const.F_SEPARATOR.join(str(x) for x in info)
                print(line)

    def save_state_of_study_sets(self):
        study_set_found = False
        for study_set in self.state_of_study_sets:
            if self.current_set_id == study_set["ID"]:
                study_set_found = True
                study_set["cnf_front_side"] = self.front_side
                study_set["filter"] = self.filter_cards_val
                study_set["card_order"] = self.card_order
                study_set["last_card"] = self.line_number

        if not study_set_found:
            self.state_of_study_sets.append({"ID": self.current_set_id, "title": self.current_set_title,
                                            "no_of_terms": len(self.term_list), "cnf_front_side": self.front_side,
                                             "filter": self.filter_cards_val, "card_order": self.card_order,
                                             "last_card": self.line_number,
                                             "untagged_filter_list_size": self.untagged_filter_list_size,
                                             "high_filter_list_size": self.high_filter_list_size,
                                             "med_filter_list_size": self.med_filter_list_size,
                                             "low_filter_list_size": self.low_filter_list_size,
                                             "gen_filter_list_size": self.gen_filter_list_size
                                             })
        sets_config_name = "sets_config.json"
        with open(sets_config_name, "w") as write_file:
            json.dump(self.state_of_study_sets, write_file, indent=4)
        print("configuration saved to JSON")

    def get_study_set_conf_from_file(self):
        sets_config_name = "sets_config.json"
        try:
            read_file = open(sets_config_name, "r")
            sets_conf_struct = json.load(read_file)
        except Exception as e:
            wrn_txt = "Couldn't open and read JSON study-sets-configuration file. Using default values"
            print(e, wrn_txt)
            self.display_pop_up(PopUpType.WARNING, wrn_txt)
            self.use_s_set_default_conf()
            return

        self.state_of_study_sets = sets_conf_struct
        study_set_found = False
        for s_set_conf in sets_conf_struct:
            if int(s_set_conf["ID"]) == int(self.current_set_id):
                study_set_found = True
                self.running_study_set_conf = s_set_conf
                self.line_number = self.running_study_set_conf["last_card"]
                self.card_order = self.running_study_set_conf["card_order"]
                self.front_side = self.running_study_set_conf["cnf_front_side"]
                self.back_side = 1 - self.front_side
                self.filter_cards_val = self.running_study_set_conf["filter"]
                self.untagged_filter_list_size = self.running_study_set_conf["untagged_filter_list_size"]
                self.high_filter_list_size = self.running_study_set_conf["high_filter_list_size"]
                self.med_filter_list_size = self.running_study_set_conf["med_filter_list_size"]
                self.low_filter_list_size = self.running_study_set_conf["low_filter_list_size"]
                self.gen_filter_list_size = self.running_study_set_conf["gen_filter_list_size"]
                break
        if not study_set_found:
            self.use_s_set_default_conf()

    def use_s_set_default_conf(self):
        self.line_number = 0
        self.card_order = 11
        self.front_side = 0
        self.back_side = 1 - self.front_side
        self.filter_cards_val = 0


class MainWin:
    def __init__(self, window):
        main_title = "Study Cards"
        window.title(main_title)
        window.geometry(str(GuiTc.MW_WIDTH)+'x700')
        window.resizable(False, False)
        window.attributes('-topmost', 'true')

        app = StudyCardsApp(window)

        title1_txt = main_title
        ltr_size = 16  # approx number of pixels per letter
        calc_relx = (1 - ((ltr_size * len(title1_txt)) / GuiTc.MW_WIDTH)) / 2
        tk.Label(window, text=title1_txt, font="Helvetica 20 bold").place(relx=calc_relx, rely=0.0)

        self._select_frame = SelectionFrame(window, app, self)
        self._app = app
        self._window = window

    def init_continued(self):
        self._conf_frame = cfr.ConfFrame(self, self._window, self._app)
        self._prsnt_frame = prf.PresentationFrame(self, self._window, self._app)
        return self._conf_frame

    def flash_cards_button_clicked(self):
        self._conf_frame.config_frame_obj.place_forget()
        self._prsnt_frame.presentation_frame_obj.place(relx=0.1, rely=0.1)
        self._conf_frame.create_filtered_index_lists(self._app, self._app.filter_cards_val, self._app.card_order)
        self.handle_card_location()
        self._prsnt_frame.nxt_back_button_clicked(nxt=True, continue_cards=True)

    def config_button_clicked(self):
        self._conf_frame.update_size_of_filtered_lists()
        self._conf_frame.config_frame_obj.place(relx=0.1, rely=0.1)
        self._prsnt_frame.presentation_frame_obj.place_forget()

    def set_selection_button_clicked(self):
        self._app.save_state_of_study_sets()
        self._conf_frame.config_frame_obj.place_forget()
        self._select_frame._select_frame.place(relx=0.1, rely=0.1)  # refactor!

    def on_close(self):
        self.handle_card_location()
        print("Main Window is closing. Writing the configuration to JSON file")
        if self._app.allow_to_save_the_state_of_study_sets:
            self._app.save_state_of_study_sets()
        self._window.destroy()

    def handle_card_location(self):
        """ If the filtered list has changed due to tagging then the location of the last card needs to change.
            For now, just reset to beginning.
        """
        if self._app.reset_cards_request:
            self._conf_frame.reset_cards()
            self._app.reset_cards_request = False


class SelectionFrame:
    def __init__(self, root, app, main_win):
        self._app = app
        self.item_selected = False
        self.selected_index = 0
        self._main_win = main_win
        self._root = root
        self.import_study_set_clicked = False

        title1_txt = "Study Card Sets"
        select_frame = tk.LabelFrame(root, text=title1_txt, font="Helvetica 14",
                                  width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        select_frame.place(relx=0.1, rely=0.1)
        print("select_frame is placed")
        self._select_frame = select_frame

        new_study_set_frame = tk.LabelFrame(select_frame, text="Add a New Study Card Set", font="Helvetica 14", width=320,
                                            height=350, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        new_study_set_frame.place(relx=0.6, rely=0.05)

        list_of_study_sets_frame = tk.LabelFrame(select_frame, text="Select a Study Card Set", font="Helvetica 14",
                                                 width=460,
                                                 height=470, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        list_of_study_sets_frame.place(relx=0.04, rely=0.05)

        self.list_of_study_sets = []
        for s_set_cnf in app.study_set_conf_list:
            self.list_of_study_sets.append(s_set_cnf["study_set_title"])

        lbox_var = tk.StringVar(value=self.list_of_study_sets)
        # tk.Label(list_of_study_sets_frame, text="List of Study Sets", font="Helvetica 14", bg="gray99").place(relx=0.2, rely=0.05)

        self.listbox = tk.Listbox(list_of_study_sets_frame, listvariable=lbox_var, height=13, width=35,
                                  bg=GuiTc.L2_FRAME_BG, font=GuiTc.R_B_FONT, fg="gray20")
        # self.listbox.configure(highlightbackground="black")
        self.listbox.select_set(0)

        self.listbox.place(relx=0.1, rely=0.05)

        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        # link a scrollbar to a list
        scrollbar = tk.Scrollbar(list_of_study_sets_frame, orient='vertical', command=self.listbox.yview)
        scrollbar.place(relx=0.05, rely=0.05, height=300)

        title_label = tk.Label(new_study_set_frame, text='Title', font=('calibre', 12, 'bold'))
        title_label.place(relx=0.05, rely=0.1)

        self.title_var = tk.StringVar()
        title_entry = tk.Entry(new_study_set_frame, textvariable=self.title_var, font=('calibre', 12, 'normal'))
        title_entry.place(relx=0.35, rely=0.1)

        f_name_label = tk.Label(new_study_set_frame, text='File Name', font=('calibre', 12, 'bold'))
        f_name_label.place(relx=0.05, rely=0.3)

        self.f_name_var = tk.StringVar()
        f_name_entry = tk.Entry(new_study_set_frame, textvariable=self.f_name_var, font=('calibre', 12, 'normal'))
        f_name_entry.place(relx=0.35, rely=0.3)

        tk.Button(list_of_study_sets_frame, text="Go to selected set", font=GuiTc.BUTTON_FONT,
                  command=self.go_to_selected_set_button_clicked).place(relx=0.2, rely=0.8)

        tk.Button(new_study_set_frame, text="Import the file", font=GuiTc.BUTTON_FONT,
                  command=self.import_study_set).place(relx=0.2, rely=0.8)

    def items_selected(self, event):
        self.selected_index = self.listbox.curselection()
        self.item_selected = True

    def go_to_selected_set_button_clicked(self):
        if not self.item_selected:  # reverse the logic!
            index = 0
        else:
            index = self.selected_index[0]
        s_set_cnf = self._app.study_set_conf_list[index]
        self._app.current_w_file = s_set_cnf["w_file"]
        self._app.current_set_id = s_set_cnf["study_set_id"]
        self._app.current_set_title = s_set_cnf["study_set_title"]
        self._app.current_import_file_name = s_set_cnf["import_file_name"]
        self._app.current_import_file_request = s_set_cnf["import_file_request"]
        self._app.read_shuffle_etc()

        title2_txt = "Study Set: %s (%s Cards)" % (self._app.current_set_title, str(len(self._app.term_list)))
        ltr_size = 12  # approx number of pixels per letter
        calc_relx = (1 - ((ltr_size * len(title2_txt)) / GuiTc.MW_WIDTH)) / 2
        tk.Label(self._root, text=title2_txt, font="Helvetica 16 bold").place(relx=calc_relx, rely=0.05)

        self._app.allow_to_save_the_state_of_study_sets = True

        # Initialize the config and presentation frames
        conf_frame = self._main_win.init_continued()
        conf_frame.update_size_of_filtered_lists()
        conf_frame.config_frame_obj.place(relx=0.1, rely=0.1)
        self._select_frame.place_forget()

    def import_study_set(self):
        if self.import_study_set_clicked:
            print("Can click only once")
            # Need to disable the button!!
            return
        self.import_study_set_clicked = True
        study_set_title = self.title_var.get()
        import_file_name = self.f_name_var.get()
        # Check valid title
        if len(study_set_title.replace(' ', '')) < 3:
            print("Invalid study set title")
            return

        new_set_id = None
        # find an available ID
        self._app.read_configuration_file()  # Should not be called twice!
        for potential_new_id in range(1002, 1100):
            if str(potential_new_id) not in self._app.id_list:
                new_set_id = potential_new_id
                break

        # update the config.ini file with data of new study set
        config_object = self._app.config_object
        study_sets = config_object["STUDY_SETS_ID_LIST"]
        id_list = study_sets["id_list"]
        id_list = id_list + ","+(str(new_set_id))
        config_object["STUDY_SETS_ID_LIST"] = {"id_list": id_list}
        config_object['STUDY_SET_'+str(new_set_id)] = {'study_set_title': study_set_title,
                                                       'import_file_name': import_file_name,
                                                       'import_file_request': 'True'}
        with open('config.ini', 'w') as configfile:
            config_object.write(configfile)

        self._app.read_configuration_file()  # Should not be called twice! Refactor!

        self.list_of_study_sets = []
        for s_set_cnf in self._app.study_set_conf_list:
            self.list_of_study_sets.append(s_set_cnf["study_set_title"])

        lbox_var = tk.StringVar(value=self.list_of_study_sets)
        self.listbox.configure(listvariable=lbox_var)


def main():
    if sys.version_info[0] < 3:
        raise Exception("Must use Python 3")

    window = tk.Tk()  # The root
    m_win = MainWin(window)
    window.protocol("WM_DELETE_WINDOW", m_win.on_close)
    window.mainloop()


if __name__ == "__main__":
    main()
