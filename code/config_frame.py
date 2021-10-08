import tkinter as tk
from constants import Const,GuiTc, CrdOrdr, Cnf, Fltr, Tag

class ConfFrame:
    def __init__(self, main_win, window, app):
        self._app = app
        config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                                     width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        config_frame.place(relx=0.1, rely=0.1)
        self.config_frame_obj = config_frame

        card_order_frame = tk.LabelFrame(config_frame, text="Card Order", font="Helvetica 14", width=205,
                                         height=170, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        card_order_frame.place(relx=0.1, rely=0.05)

        self.card_order_v = tk.IntVar()
        self.card_order_v.set(app.card_order)  # set the default radio button

        tk.Radiobutton(card_order_frame, text=CrdOrdr.Alphabetical.txt + " (" +Cnf.term1+")", variable=self.card_order_v,
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

        tk.Radiobutton(filter_cards_frame, text=Fltr.NO_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.NO_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=Fltr.LOW_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.LOW_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.2)

        tk.Radiobutton(filter_cards_frame, text=Fltr.MED_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.MED_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.35)

        tk.Radiobutton(filter_cards_frame, text=Fltr.HIGH_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.HIGH_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.5)

        tk.Radiobutton(filter_cards_frame, text=Fltr.GEN_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.GEN_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.65)

        tk.Radiobutton(filter_cards_frame, text=Fltr.UNTAGGED_FLTR[Fltr.TXT], variable=self._filter_cards,
                       value=Fltr.UNTAGGED_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.8)

        front_side_frame = tk.LabelFrame(config_frame, text="Cards front side", font="Helvetica 14",
                                         width=170, height=120, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        front_side_frame.place(relx=0.1, rely=0.5)

        self.lang1_var = tk.IntVar()

        tk.Radiobutton(front_side_frame, text=Cnf.term1, variable=self.lang1_var,
                       value=0, command=self.change_lang_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(front_side_frame, text=Cnf.term2, variable=self.lang1_var,
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
        filter_val = self._app.filter_cards_val
        if filter_val == Fltr.NO_FLTR[Fltr.VAL]:
            app.filtered_ab_sort_list = app.ab_sort_list[:]
            app.filtered_shuffled_list = app.shuffled_list[:]
            app.filtered_term_list = list(range(len(app.term_list)))
            app.filtered_list_size = len(app.term_list)
            return
        else:
            if filter_val == Fltr.UNTAGGED_FLTR[Fltr.VAL]:
                expected_tag_dt_txt = Tag.NoTag.d_txt
            elif filter_val == Fltr.LOW_FLTR[Fltr.VAL]:
                expected_tag_dt_txt = Tag.LowTag.d_txt
            elif filter_val == Fltr.MED_FLTR[Fltr.VAL]:
                expected_tag_dt_txt = Tag.MedTag.d_txt
            elif filter_val == Fltr.HIGH_FLTR[Fltr.VAL]:
                expected_tag_dt_txt = Tag.HighTag.d_txt
            elif filter_val == Fltr.GEN_FLTR[Fltr.VAL]:
                expected_tag_dt_txt = Tag.GenTag.d_txt
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
                print(app.filtered_term_list)
                print(expected_tag_dt_txt)
            else:
                raise ValueError


