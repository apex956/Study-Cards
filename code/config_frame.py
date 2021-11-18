import tkinter as tk
from constants import Const,GuiTc, CrdOrdr, Fltr, Tag

class ConfFrame:
    def __init__(self, main_win, window, app):
        self._app = app
        config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                                     width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        self.config_frame_obj = config_frame

        card_order_frame = tk.LabelFrame(config_frame, text="Card Order", font="Helvetica 14", width=205,
                                         height=170, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        card_order_frame.place(relx=0.1, rely=0.05)

        self.card_order_v = tk.IntVar()
        self.card_order_v.set(app.card_order)  # set the default radio button

        local_text = CrdOrdr.Alphabetical.txt + " (" +self._app.term1+")"
        tk.Radiobutton(card_order_frame, text=local_text, variable=self.card_order_v,
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
                                           width=280, height=220, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        filter_cards_frame.place(relx=0.6, rely=0.05)

        local_txt = Fltr.NO_FLTR[Fltr.TXT] + " (" + str(len(self._app.term_list)) + " cards)"
        tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.NO_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        local_txt = Fltr.LOW_FLTR[Fltr.TXT] + " (" + str(self._app.low_filter_list_size) + " cards)"
        self.low_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.LOW_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.low_fltr_rb.place(relx=0.0, rely=0.2)

        local_txt = Fltr.MED_FLTR[Fltr.TXT] + " (" + str(self._app.med_filter_list_size) + " cards)"
        self.med_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.MED_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.med_fltr_rb.place(relx=0.0, rely=0.35)

        local_txt = Fltr.HIGH_FLTR[Fltr.TXT] + " (" + str(self._app.high_filter_list_size) + " cards)"
        self.high_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.HIGH_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.high_fltr_rb.place(relx=0.0, rely=0.5)

        local_txt = Fltr.GEN_FLTR[Fltr.TXT] + " (" + str(self._app.gen_filter_list_size) + " cards)"
        self.gen_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.GEN_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.gen_fltr_rb.place(relx=0.0, rely=0.65)

        local_txt = Fltr.UNTAGGED_FLTR[Fltr.TXT] + " (" + str(self._app.untagged_filter_list_size) + " cards)"
        self.untagged_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                                          value=Fltr.UNTAGGED_FLTR[Fltr.VAL], command=self.update_filter,
                                          font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.untagged_rb.place(relx=0.0, rely=0.8)

        front_side_frame = tk.LabelFrame(config_frame, text="Cards front side", font="Helvetica 14",
                                         width=170, height=120, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        front_side_frame.place(relx=0.1, rely=0.5)

        self.lang1_var = tk.IntVar()

        tk.Radiobutton(front_side_frame, text=self._app.term1, variable=self.lang1_var,
                       value=0, command=self.change_lang_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(front_side_frame, text=self._app.term2, variable=self.lang1_var,
                       value=1, command=self.change_lang_order,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.4)

        self.lang1_var.set(self._app.front_side)

        tk.Button(config_frame, text="Show Flashcards", font=GuiTc.BUTTON_FONT,
                  command=main_win.flash_cards_button_clicked).place(relx=0.7, rely=0.8)

        tk.Button(config_frame, text="Reset Flashcards", font=GuiTc.BUTTON_FONT,
                  command=self.reset_cards).place(relx=0.4, rely=0.8)


        tk.Button(config_frame, text="Go to set selection", font=GuiTc.BUTTON_FONT,
                  command=main_win.set_selection_button_clicked).place(relx=0.1, rely=0.8)

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
        self.update_size_of_filtered_lists()


    def reset_cards(self):
        self._app.line_number = 0

    def create_filtered_index_lists(self, app, filter_val, card_order):
        """Possible refactoring: move this function to the study_cards_app module"""
        app.filtered_ab_sort_list.clear()
        app.filtered_shuffled_list.clear()
        app.filtered_term_list.clear()
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
                raise ValueError("Filter not found")

            if card_order == CrdOrdr.Alphabetical.val:
                for m_idx in app.ab_sort_list:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_ab_sort_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_ab_sort_list)
            elif card_order == CrdOrdr.Random.val:
                for m_idx in app.shuffled_list:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_shuffled_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_shuffled_list)
            elif card_order == CrdOrdr.Original.val:
                for a_idx in range(len(app.term_list)):
                    if app.get_tag_dt_txt(a_idx) == expected_tag_dt_txt:
                        app.filtered_term_list.append(a_idx)
                app.filtered_list_size = len(app.filtered_term_list)
            else:
                raise ValueError

    def update_size_of_filtered_lists(self):
        """To be called only in the config frame"""
        self.create_filtered_index_lists(self._app, Fltr.UNTAGGED_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.untagged_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.UNTAGGED_FLTR[Fltr.TXT] + " (" + str(self._app.untagged_filter_list_size) + " cards)"
        self.untagged_rb.config(text=local_txt)

        self.create_filtered_index_lists(self._app, Fltr.HIGH_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.high_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.HIGH_FLTR[Fltr.TXT] + " (" + str(self._app.high_filter_list_size) + " cards)"
        self.high_fltr_rb.config(text=local_txt)

        self.create_filtered_index_lists(self._app, Fltr.MED_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.med_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.MED_FLTR[Fltr.TXT] + " (" + str(self._app.med_filter_list_size) + " cards)"
        self.med_fltr_rb.config(text=local_txt)

        self.create_filtered_index_lists(self._app, Fltr.LOW_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.low_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.LOW_FLTR[Fltr.TXT] + " (" + str(self._app.low_filter_list_size) + " cards)"
        self.low_fltr_rb.config(text=local_txt)

        self.create_filtered_index_lists(self._app, Fltr.GEN_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.gen_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.GEN_FLTR[Fltr.TXT] + " (" + str(self._app.gen_filter_list_size) + " cards)"
        self.gen_fltr_rb.config(text=local_txt)
