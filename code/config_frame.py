import tkinter as tk
import study_cards_app
from constants import Const,GuiTc, CrdOrdr

class ConfFrame:
    def __init__(self, main_win, window, app):
        self._app = app

        self.VAL = 0  # index for value
        self.TXT = 1  # index for radio button text
        self.NO_FLTR = [0, "All"]
        self.LOW_FLTR = [1, "No knowl. tag"]  # level of knowledge of studied terms
        self.MED_FLTR = [2, "Medium knowl. tag"]
        self.HIGH_FLTR = [3, "Good knowl. tag"]
        self.GEN_FLTR = [4, "Minor issues tag"]  # for example: spelling problems
        self.UNTAGGED_FLTR = [5, "Untagged"]

        config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                                     width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        config_frame.place(relx=0.1, rely=0.1)
        self.config_frame_obj = config_frame

        card_order_frame = tk.LabelFrame(config_frame, text="Card Order", font="Helvetica 14", width=205,
                                         height=170, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        card_order_frame.place(relx=0.1, rely=0.05)

        self.card_order_v = tk.IntVar()
        self.card_order_v.set(app.card_order)  # set the default radio button

        tk.Radiobutton(card_order_frame, text=CrdOrdr.Alphabetical.txt + " (" +app.term1+")", variable=self.card_order_v,
                       value=CrdOrdr.Alphabetical.val, command=self.update_card_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.1)

        tk.Radiobutton(card_order_frame, text=CrdOrdr.Random.txt, variable=self.card_order_v,
                       value=CrdOrdr.Random.val, command=self.update_card_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.3)

        tk.Radiobutton(card_order_frame, text=CrdOrdr.Original.txt, variable=self.card_order_v,
                       value=CrdOrdr.Original.val, command=self.update_card_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.5)

        self._filter_cards = tk.IntVar()
        self._filter_cards.set(app.filter_cards_val)

        filter_cards_frame = tk.LabelFrame(config_frame, text="Show cards", font="Helvetica 14",
                                           width=230, height=220, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        filter_cards_frame.place(relx=0.6, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=self.NO_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.NO_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=self.LOW_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.LOW_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.2)

        tk.Radiobutton(filter_cards_frame, text=self.MED_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.MED_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.35)

        tk.Radiobutton(filter_cards_frame, text=self.HIGH_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.HIGH_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.5)

        tk.Radiobutton(filter_cards_frame, text=self.GEN_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.GEN_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.65)

        tk.Radiobutton(filter_cards_frame, text=self.UNTAGGED_FLTR[self.TXT], variable=self._filter_cards,
                       value=self.UNTAGGED_FLTR[self.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.8)

        front_side_frame = tk.LabelFrame(config_frame, text="Cards front side", font="Helvetica 14",
                                         width=170, height=120, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        front_side_frame.place(relx=0.1, rely=0.5)

        self.lang1_var = tk.IntVar()

        tk.Radiobutton(front_side_frame, text=app.term1, variable=self.lang1_var,
                       value=0, command=self.change_lang_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(front_side_frame, text=app.term2, variable=self.lang1_var,
                       value=1, command=self.change_lang_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.4)

        self.lang1_var.set(self._app.front_side)

        tk.Button(config_frame, text="Show Flashcards", font=GuiTc.BUTTON_FONT,
                  command=main_win.flash_cards_button_clicked).place(relx=0.6, rely=0.8)

        tk.Button(config_frame, text="Reset Flashcards", font=GuiTc.BUTTON_FONT,
                  command=self.reset_cards).place(relx=0.1, rely=0.8)


    def update_card_order(self):
        self._app.card_order = self.card_order_v.get()
        self.reset_cards()

    def update_filter(self):
        self._app.filter_cards_val = self._filter_cards.get()
        self.reset_cards()

    def change_lang_order(self):
        self._app.front_side = self.lang1_var.get()
        self._app.back_side = 1 - self._app.front_side
        self.reset_cards()

    def reset_cards(self):
        self._app.line_number = 0


    def create_filtered_index_lists(self, app):
        app.filtered_ab_sort_list.clear()
        app.filtered_shuffled_list.clear()
        app.filtered_term_list.clear()

        filter_val = self._filter_cards.get()
        if filter_val == self.NO_FLTR[self.VAL]:
            app.filtered_ab_sort_list = app.ab_sort_list[:]
            app.filtered_shuffled_list = app.shuffled_list[:]
            app.filtered_term_list = list(range(len(app.term_list)))
            app.filtered_list_size = len(app.term_list)
            return
        else:
            if filter_val == self.UNTAGGED_FLTR[self.VAL]:
                expected_tag_dt_txt = app.NoTag.d_txt
            elif filter_val == self.LOW_FLTR[self.VAL]:
                expected_tag_dt_txt = app.LowTag.d_txt
            elif filter_val == self.MED_FLTR[self.VAL]:
                expected_tag_dt_txt = app.MedTag.d_txt
            elif filter_val == self.HIGH_FLTR[self.VAL]:
                expected_tag_dt_txt = app.HighTag.d_txt
            elif filter_val == self.GEN_FLTR[self.VAL]:
                expected_tag_dt_txt = app.GenTag.d_txt
            else:
                print("Filter not found!")
                raise ValueError

            if app.card_order == CrdOrdr.Alphabetical.val:
                for m_idx in app.ab_sort_list:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_ab_sort_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_ab_sort_list)
            elif app.card_order == CrdOrdr.Random.val:
                for m_idx in app.shuffled_list:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_shuffled_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_shuffled_list)
            elif app.card_order == CrdOrdr.Original.val:
                for a_idx in range(len(app.term_list)):
                    if app.get_tag_dt_txt(a_idx) == expected_tag_dt_txt:
                        app.filtered_term_list.append(a_idx)
                app.filtered_list_size = len(app.filtered_term_list)
            else:
                raise ValueError


