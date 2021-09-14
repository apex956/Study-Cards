# Copyright 2021 The StudyCards Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

"""
Description: This is the main module of the Study Cards application for studying languages or
memorizing facts.
Created: August 2021
Authors: Amir Bar-Sever
Programming language: Python 3
Status: work in progress
"""

from study_cards_b import *

def display_pop_up(pu_type, txt):
    msg = tk.Tk()
    msg.withdraw()
    if pu_type == PopUpType.Warning:
        tk.messagebox.showwarning(title="Warning", message=txt)
    elif pu_type == PopUpType.Error:
        tk.messagebox.showwarning(title="Error", message=txt)
    elif pu_type == PopUpType.Info:
        tk.messagebox.showinfo(title="Info", message=txt)
    msg.destroy()

def word_list_import(in_f_path, in_f_name):
    """
    Description: This function opens and reads the text file imported from the Quizlet application
    It writes the content to a work file and adds default meta data
    Note that running this function erases the meta data replacing it with default values

    :param f_path: the path to the directory where the imported file and the work file are
    :param f_name: the name of the text file to be imported
    :return:
    """
    in_file_path = in_f_path + in_f_name
    in_line_list = []
    p_line = -1
    try:
        in_file_ref = open(in_file_path, "r")
    except OSError as e:
        wrn_txt = "Couldn't open a file to be imported"
        print(e, wrn_txt)
        display_pop_up(PopUpType.Warning, wrn_txt)
        return
    try:
        for t_idx, in_line in enumerate(in_file_ref):
            if in_line.count(f_separator) > 1:
                p_line = t_idx
                raise ValueError
            in_line_list.append(in_line.split(f_separator))
    except ValueError:
        warning_txt = "Found an unexpected separator character '" + f_separator + \
                      "' in line " + str(p_line) +\
                      " of the imported file. " + "The file was not imported."
        print(warning_txt)
        display_pop_up(PopUpType.Warning, warning_txt)
        return
    finally:
        in_file_ref.close()
    print("There are {} terms in the imported file".format(len(in_line_list)))

    w_file_path = pathlib.Path(filepath+w_file)
    if w_file_path.is_file():
        # work file exists - add here the ability to merge with an imported file
        print("Work file found. No import performed")
        return
    else:
        print("Work file not found. Import is attempted")
        try:
            w_file_ref = open(w_file_path, "w")
        except OSError as e:
            err_txt = "couldn't open the work file for writing"
            print(e, err_txt)
            display_pop_up(PopUpType.Error, err_txt)
            sys.exit()

    for d_line in in_line_list:
        w_file_ref.write(d_line[lang1_idx].rstrip() + f_separator +
                     d_line[lang2_idx].strip() + f_separator +
                     language1 + " " + NoTag.d_txt + f_separator +
                     language2 + " " + NoTag.d_txt + "\n")
    display_pop_up(PopUpType.Info, "File was imported")
    w_file_ref.close()

if import_word_file:
    word_list_import(filepath, import_file_name)

def read_work_file():
    global term_list
    # read the vocabulary list from the work-file
    try:
        w_fl_ref = open(filepath+w_file, "r")
    except OSError:
        print("Couldn't open the work file")
        sys.exit()

    for r_line in w_fl_ref:
        line_content = r_line.split(f_separator)
        term_list.append(line_content)

    print("The 1st line from the work file: ", term_list[0])
    w_fl_ref.close()

read_work_file()

# sort the list of terms
def use_1st_str(lst1):
    return lst1[0].capitalize()

def sort_and_shuffle_term_list():
    global ab_sort_lst
    global shuffled_list
    sort_lst = []
    for ln_idx, line in enumerate(term_list):
        sort_lst.append([line[0], ln_idx])

    sort_lst.sort(key=use_1st_str)
    for line in sort_lst:
        ab_sort_lst.append(line[1])
    #print("ab_sort_lst", ab_sort_lst[0], ab_sort_lst[1])

    shuffled_list = list(range(len(term_list)))
    random.shuffle(shuffled_list)

sort_and_shuffle_term_list()

# -------- Start of GUI functions ------------

def get_tag_dt_txt(line):
    """Returns the tag value for a line of data and the shown language  """
    lang_idx = card_side
    data_text1 = term_list[line][lang_idx + 2]
    # parse the text to remove the language
    if data_text1.startswith(language1):
        data_text = data_text1.removeprefix(language1 + " ")
    elif data_text1.startswith(language2):
        data_text = data_text1.removeprefix(language2 + " ").rstrip()
    else:
        raise ValueError
    return data_text


def create_filtered_index_list():
    global filtered_ab_sort_lst
    global filtered_shuffled_list
    global filtered_term_list
    global filtered_list_size
    filtered_ab_sort_lst.clear()
    filtered_shuffled_list.clear()
    filtered_term_list.clear()

    filter_val = filter_cards.get()
    if filter_val == NO_FILTER[VAL]:
        filtered_ab_sort_lst = ab_sort_lst[:]
        filtered_shuffled_list = shuffled_list[:]
        filtered_term_list = list(range(len(term_list)))
        filtered_list_size = len(term_list)
        return
    else:
        if filter_val == UNTAGGED_FILTER[VAL]:
            expected_tag_dt_txt = NoTag.d_txt
        elif filter_val == LOW_FILTER[VAL]:
            expected_tag_dt_txt = LowTag.d_txt
        elif filter_val == MED_FILTER[VAL]:
            expected_tag_dt_txt = MedTag.d_txt
        elif filter_val == HIGH_FILTER[VAL]:
            expected_tag_dt_txt = HighTag.d_txt
        elif filter_val == GEN_FILTER[VAL]:
            expected_tag_dt_txt = GenTag.d_txt
        else:
            expected_tag_dt_txt = ""  # Need to handle
            print("Filter not found!")

        if mode == "alphabetical":
            for m_idx in ab_sort_lst:
                if get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                    filtered_ab_sort_lst.append(m_idx)
            filtered_list_size = len(filtered_ab_sort_lst)
        elif mode == "random":
            for m_idx in shuffled_list:
                if get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                    filtered_shuffled_list.append(m_idx)
            filtered_list_size = len(filtered_shuffled_list)
        elif mode == "original":
            for a_idx  in range(len(term_list)):
                if get_tag_dt_txt(a_idx) == expected_tag_dt_txt:
                    filtered_term_list.append(a_idx)
            filtered_list_size = len(filtered_term_list)


def set_tag_rb(line):
    """
    Set tagging radio buttons to values in the data structure!
    set the tag radio button of the requested line
    to be called when changing the line
    :param line: the current actual line
    :return: none
    """
    global tagging_var
    data_text = get_tag_dt_txt(line)
    val = tdtv_dir[data_text]
    tagging_var.set(val)

def update_tag_in_w_file(line_num, lang_idx, tag):
    """
    Write the tagging string into the work file
    This is done when the tagging radio button is changed
    :param line_num:
    :param lang_idx:
    :param tag:
    :return:
    """
    with FileInput(files=[filepath+w_file], inplace=True) as wf:
        if lang_idx == lang1_idx:
            lang_tag_idx = lang1_tag_idx
            language = language1
        elif lang_idx == lang2_idx:
            lang_tag_idx = lang2_tag_idx
            language = language2
        else:
            return  # need to raise exception
        for idx, line in enumerate(wf):
            line = line.rstrip()
            info = line.split(f_separator)
            if idx == line_num:
                info[lang_tag_idx] = language + " " + tag
            line = f_separator.join(str(x) for x in info)
            print(line)

def nxt_button_clicked():
    nxt = True
    nxt_back_button_clicked(nxt)

def back_button_clicked():
    nxt = False
    nxt_back_button_clicked(nxt)

def set_act_line (line):
    """
    Set the global parameter act_ln (actual line) depending on the mode
    :param line:  line_number
    """
    global act_ln
    if mode == "original":
        act_ln = filtered_term_list[line_number]
    elif mode == "alphabetical":
        act_ln = filtered_ab_sort_lst[line_number]
    elif mode == "random":
        act_ln = filtered_shuffled_list[line_number]


def nxt_back_button_clicked(nxt, start_over = False):
    global line_number
    global card_text
    global card_side

    if filtered_list_size <= 0:
        label1_txt = "Card number " + str(0) + " of " + str(0) + " cards"
        shown_l_word.configure(text="")
        enable_disable_tag_radio_buttons(False)
    else:
        if nxt:
            line_number += 1
        else:
            line_number -= 1

        # loop forever
        if line_number > filtered_list_size - 1:
            line_number = 0
        elif line_number < 0:
            line_number = filtered_list_size - 1

        # start over
        if start_over:
            line_number = 0

        set_act_line(line_number)
        card_text = [term_list[act_ln][lang1_idx].rstrip(), term_list[act_ln][lang2_idx].strip()]

        shown_l_word.configure(text=card_text[front_side])
        card_side = front_side
        set_tag_rb(act_ln)

        label1_txt = "Card number " + str(line_number + 1) + " of " + str(filtered_list_size) + " cards"
        enable_disable_tag_radio_buttons(True)
    label1.configure(text=label1_txt)

def enable_disable_tag_radio_buttons(enable):
    global tag_rad1
    global tag_rad2
    global tag_rad3
    global tag_rad4
    global tag_rad5
    if enable:
        tag_rad1['state'] = tk.NORMAL
        tag_rad2['state'] = tk.NORMAL
        tag_rad3['state'] = tk.NORMAL
        tag_rad4['state'] = tk.NORMAL
        tag_rad5['state'] = tk.NORMAL
    else:
        tag_rad1['state'] = tk.DISABLED
        tag_rad2['state'] = tk.DISABLED
        tag_rad3['state'] = tk.DISABLED
        tag_rad4['state'] = tk.DISABLED
        tag_rad5['state'] = tk.DISABLED

def flip_button_clicked():
    global card_side
    if card_side == front_side:
        shown_l_word.configure(text=card_text[back_side])
        card_side = back_side
        enable_disable_tag_radio_buttons(False)
    else:
        shown_l_word.configure(text=card_text[front_side])
        card_side = front_side
        enable_disable_tag_radio_buttons(True)


def alphabetical_selected():
    global mode
    mode = "alphabetical"

def random_selected():
    global mode
    mode = "random"

def original_selected():
    global mode
    mode = "original"

def flash_cards_button_clicked():
    config_frame.place_forget()
    presentation_frame.place(relx=0.1, rely=0.1)
    create_filtered_index_list()
    nxt_back_button_clicked(nxt=True, start_over=True)

def config_button_clicked():
    config_frame.place(relx=0.1, rely=0.1)
    presentation_frame.place_forget()

def item_tagging():
    global term_list
    tag_val = tagging_var.get()
    if front_side == 0:
        lang_idx = lang1_idx
    elif front_side == 1:
        lang_idx = lang2_idx
    else:
        lang_idx = -1  # !!! this whole section needs to be improved !!!
    #print("Selected marking:", act_ln, lang_idx, tag_val)  # debug
    d_txt = tvdt_dir[tag_val]
    update_tag_in_w_file(act_ln, lang_idx, d_txt)  # use act_line
    term_list[act_ln][lang_idx+2] = languages[lang_idx]+" "+d_txt

def change_lang_order():
    global front_side
    global back_side
    front_side = lang1_var.get()
    back_side = 1 - front_side

def update_filter():
    pass

'''---GUI Elements---'''

BUTTON_FONT = "Helvetica 16"
RADIO_BUTTON_FONT = "Helvetica 14"
RB_BG = "white smoke"  # Radio Button Background color

window = tk.Tk()  # The root
window.title("Study Cards")
window.geometry('1100x700')
window.resizable(False, False)

title1 = tk.Label(window, text=language1 + " " + language2 + " Vocabulary", font="Helvetica 20 bold")
title1.place(relx=0.3, rely=0.0)

title2 = tk.Label(window, text="Study Set: " + set_title, font="Helvetica 16 bold")
title2.place(relx=0.4, rely=0.05)

window.attributes('-topmost', 'true')

'''---Configuration Frame---'''
config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                             width=900, height=600, bg="gray99",  bd=1, relief=tk.SOLID)
config_frame.place(relx=0.1, rely=0.1)

card_order_frame = tk.Frame(config_frame, width=150, height=160, bg="white smoke",  bd=1, relief=tk.SOLID)
card_order_frame.place(relx=0.1, rely=0.05)
tk.Label(card_order_frame, text="Card Order:", font="Helvetica 16", bg="white smoke")\
        .place(relx=0.0, rely=0.0)

card_order = tk.IntVar()

rad1 = tk.Radiobutton(card_order_frame, text='Alphabetical', variable=card_order, value=1,
                      command=alphabetical_selected,
                      font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.2)

rad2 = tk.Radiobutton(card_order_frame, text='Random', variable=card_order, value=2,
                      command=random_selected,
                      font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.4)

rad3 = tk.Radiobutton(card_order_frame, text='Original', variable=card_order, value=3,
                      command=original_selected,
                      font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.6)

card_order.set(1)  # set the default radio button

filter_cards = tk.IntVar()

filter_cards_frame = tk.LabelFrame(config_frame, text="Filter", font="Helvetica 14",
                                   width=250, height=220, bg="white smoke",  bd=1, relief=tk.SOLID)
filter_cards_frame.place(relx=0.5, rely=0.05)

filter_rad1 = tk.Radiobutton(filter_cards_frame, text=NO_FILTER[TXT], variable=filter_cards,
                             value=NO_FILTER[VAL], command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.05)

filter_rad2 = tk.Radiobutton(filter_cards_frame, text=LOW_FILTER[TXT], variable=filter_cards,
                             value=LOW_FILTER[VAL], command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.2)

filter_rad3 = tk.Radiobutton(filter_cards_frame, text=MED_FILTER[TXT], variable=filter_cards,
                             value=MED_FILTER[VAL], command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.35)

filter_rad4 = tk.Radiobutton(filter_cards_frame, text=HIGH_FILTER[TXT], variable=filter_cards,
                             value=HIGH_FILTER[VAL],  command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.5)

filter_rad5 = tk.Radiobutton(filter_cards_frame, text=GEN_FILTER[TXT], variable=filter_cards,
                             value=GEN_FILTER[VAL], command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.65)

filter_rad6 = tk.Radiobutton(filter_cards_frame, text=UNTAGGED_FILTER[TXT], variable=filter_cards,
                             value=UNTAGGED_FILTER[VAL], command=update_filter,
                             font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.8)

filter_cards.set(0)  # set the default radio button


front_side_frame = tk.LabelFrame(config_frame, text="Front side", font="Helvetica 14",
                                     width=200, height=120, bg="white smoke",  bd=1, relief=tk.SOLID)
front_side_frame.place(relx=0.1, rely=0.5)

lang1_var = tk.IntVar()

front_side_rad1 = tk.Radiobutton(front_side_frame, text=language1, variable=lang1_var,
                                value=0, command=change_lang_order,
                                font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.05)

front_side_rad2 = tk.Radiobutton(front_side_frame, text=language2, variable=lang1_var,
                                value=1, command=change_lang_order,
                                font=RADIO_BUTTON_FONT, bg=RB_BG).place(relx=0.0, rely=0.4)

tk.Button(config_frame, text="Show Flash Cards", font=BUTTON_FONT,
          command=flash_cards_button_clicked).place(relx=0.7, rely=0.8)

'''---Presentation Frame---'''

presentation_frame = tk.LabelFrame(window, text="Flashcards", font="Helvetica 14", width=900,
                                   height=600, bg="gray99",  bd=1, relief=tk.SOLID)

tagging_frame = tk.LabelFrame(presentation_frame, text="Tagging", font="Helvetica 14", width=170,
                              height=300, bg="white smoke", bd=1, relief=tk.SOLID)
tagging_frame.place(relx=0.75, rely=0.2)

tagging_var = tk.IntVar()

tag_rad1 = tk.Radiobutton(tagging_frame, text=NoTag.rb_txt, variable=tagging_var,
                          value=NoTag.val, command=item_tagging,
                          font=RADIO_BUTTON_FONT, bg=RB_BG)
tag_rad1.place(relx=0.1, rely=0.1)


tag_rad2 = tk.Radiobutton(tagging_frame, text=LowTag.rb_txt, variable=tagging_var,
                          value=LowTag.val, command=item_tagging,
                          font=RADIO_BUTTON_FONT, bg=RB_BG)
tag_rad2.place(relx=0.1, rely=0.2)

tag_rad3 = tk.Radiobutton(tagging_frame, text=MedTag.rb_txt, variable=tagging_var,
                          value=MedTag.val, command=item_tagging,
                          font=RADIO_BUTTON_FONT, bg=RB_BG)
tag_rad3.place(relx=0.1, rely=0.3)


tag_rad4 = tk.Radiobutton(tagging_frame, text=HighTag.rb_txt, variable=tagging_var,
                          value=HighTag.val, command=item_tagging,
                          font=RADIO_BUTTON_FONT, bg=RB_BG)
tag_rad4.place(relx=0.1, rely=0.4)

tag_rad5 = tk.Radiobutton(tagging_frame, text=GenTag.rb_txt, variable=tagging_var,
                          value=GenTag.val, command=item_tagging,
                          font=RADIO_BUTTON_FONT, bg=RB_BG)
tag_rad5.place(relx=0.1, rely=0.5)

cards_frame = tk.LabelFrame(presentation_frame, text="Cards", font="Helvetica 14", width=600,
                            height=300, bg="gray99",  bd=1, relief=tk.SOLID)
cards_frame.place(relx=0.05, rely=0.2)

tk.Button(presentation_frame, text="Next card", font=BUTTON_FONT,
          command=nxt_button_clicked).place(relx=0.05, rely=0.1)

tk.Button(presentation_frame, text="Previous card", font=BUTTON_FONT,
          command=back_button_clicked).place(relx=0.2, rely=0.1)

tk.Button(presentation_frame, text="Flip side", font=BUTTON_FONT,
          command=flip_button_clicked).place(relx=0.4, rely=0.1)


tk.Button(presentation_frame, text="Go to Config", font=BUTTON_FONT,
          command=config_button_clicked).place(relx=0.1, rely=0.8)

# show the card number sequentially:
label1 = tk.Label(presentation_frame, text="", font="Helvetica 16")
label1.place(relx=0.65, rely=0.1)


shown_l_word = tk.Label(cards_frame, font="Helvetica 18 ", justify=tk.CENTER,
                        wraplength=450, width=35, height=9)
shown_l_word.place(relx=0.05, rely=0.05)  # width and height in characters not pixels


def space_bar_key(event):
    #print("pressed", repr(event.char))
    flip_button_clicked()

def down_arrow_key(event):
    flip_button_clicked()

def right_arrow_key(event):
    nxt_button_clicked()

def left_arrow_key(event):
    back_button_clicked()

window.bind("<space>", space_bar_key)
window.bind("<Right>", right_arrow_key)
window.bind("<Left>", left_arrow_key)
window.bind("<Down>", down_arrow_key)

if __name__ == "__main__":
    window.mainloop()

