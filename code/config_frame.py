import tkinter as tk
from constants import Const,GuiTc, CrdOrdr, Fltr, Tag
import logging
import random


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

        local_text = CrdOrdr.Alphabetical.txt + " (" + self._app.term1+")"
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

        filter_cards_frame = tk.LabelFrame(config_frame, text="Group by Knowledge Tags", font="Helvetica 14",
                                           width=280, height=270, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        filter_cards_frame.place(relx=0.6, rely=0.05)

        local_txt = Fltr.NO_FLTR[Fltr.TXT] + " (" + str(len(self._app.term_list)) + " cards)"
        tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.NO_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG).place(relx=0.0, rely=0.02)

        local_txt = Fltr.LOW_FLTR[Fltr.TXT] + " (" + str(self._app.low_filter_list_size) + " cards)"
        self.low_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.LOW_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG, fg="red")
        self.low_fltr_rb.place(relx=0.0, rely=0.15)

        local_txt = Fltr.MED_FLTR[Fltr.TXT] + " (" + str(self._app.med_filter_list_size) + " cards)"
        self.med_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.MED_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG, fg="orange")
        self.med_fltr_rb.place(relx=0.0, rely=0.28)

        local_txt = Fltr.HIGH_FLTR[Fltr.TXT] + " (" + str(self._app.high_filter_list_size) + " cards)"
        self.high_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.HIGH_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG, fg="green")
        self.high_fltr_rb.place(relx=0.0, rely=0.54)

        local_txt = Fltr.GEN_FLTR[Fltr.TXT] + " (" + str(self._app.gen_filter_list_size) + " cards)"
        self.gen_fltr_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                       value=Fltr.GEN_FLTR[Fltr.VAL], command=self.update_filter,
                       font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG, fg="purple")
        self.gen_fltr_rb.place(relx=0.0, rely=0.41)

        local_txt = Fltr.UNTAGGED_FLTR[Fltr.TXT] + " (" + str(self._app.untagged_filter_list_size) + " cards)"
        self.untagged_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                                          value=Fltr.UNTAGGED_FLTR[Fltr.VAL], command=self.update_filter,
                                          font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.untagged_rb.place(relx=0.0, rely=0.67)

        local_txt = Fltr.SPACED[Fltr.TXT]
        self.spaced_rb = tk.Radiobutton(filter_cards_frame, text=local_txt, variable=self._filter_cards,
                                          value=Fltr.SPACED[Fltr.VAL], command=self.update_filter,
                                          font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        self.spaced_rb.place(relx=0.0, rely=0.80)

        front_side_frame = tk.LabelFrame(config_frame, text="Cards Front Side", font="Helvetica 14",
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

        status_frame = tk.LabelFrame(config_frame, text="Tag Groups Relative Size", font="Helvetica 14",
                                     width=280, height=100, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        status_frame.place(relx=0.6, rely=0.55)

        self.stat = tk.Canvas(status_frame, width=250, height=40)
        self.stat.place(relx=0.05, rely=0.1)

        tk.Button(config_frame, text="Display flashcards", font=GuiTc.BUTTON_FONT,
                  command=main_win.flash_cards_button_clicked).place(relx=0.7, rely=0.8)

        tk.Button(config_frame, text="Reset flashcards", font=GuiTc.BUTTON_FONT,
                  command=self.reset_cards).place(relx=0.4, rely=0.8)

        tk.Button(config_frame, text="Back to set selection", font=GuiTc.BUTTON_FONT,
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

        if filter_val == Fltr.SPACED[Fltr.VAL]:
            self.filter_the_spaced_repetition_list(app, card_order)
            return

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
                    if app.get_tag_dt_txt(line=m_idx, get_tag_history=False) == expected_tag_dt_txt:
                        app.filtered_ab_sort_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_ab_sort_list)
            elif card_order == CrdOrdr.Random.val:
                for m_idx in app.shuffled_list:
                    if app.get_tag_dt_txt(line=m_idx, get_tag_history=False) == expected_tag_dt_txt:
                        app.filtered_shuffled_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_shuffled_list)
            elif card_order == CrdOrdr.Original.val:
                for a_idx in range(len(app.term_list)):
                    if app.get_tag_dt_txt(line=a_idx, get_tag_history=False) == expected_tag_dt_txt:
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
        if self._app.untagged_filter_list_size <= 0:
            self.untagged_rb.config(state=tk.DISABLED)
        else:
            self.untagged_rb.config(state=tk.NORMAL)

        self.create_filtered_index_lists(self._app, Fltr.HIGH_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.high_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.HIGH_FLTR[Fltr.TXT] + " (" + str(self._app.high_filter_list_size) + " cards)"
        self.high_fltr_rb.config(text=local_txt)
        if self._app.high_filter_list_size <= 0:
            self.high_fltr_rb.config(state=tk.DISABLED)
        else:
            self.high_fltr_rb.config(state=tk.NORMAL)

        self.create_filtered_index_lists(self._app, Fltr.MED_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.med_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.MED_FLTR[Fltr.TXT] + " (" + str(self._app.med_filter_list_size) + " cards)"
        self.med_fltr_rb.config(text=local_txt)
        if self._app.med_filter_list_size <= 0:
            self.med_fltr_rb.config(state=tk.DISABLED)
        else:
            self.med_fltr_rb.config(state=tk.NORMAL)

        self.create_filtered_index_lists(self._app, Fltr.LOW_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.low_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.LOW_FLTR[Fltr.TXT] + " (" + str(self._app.low_filter_list_size) + " cards)"
        self.low_fltr_rb.config(text=local_txt)
        if self._app.low_filter_list_size <= 0:
            self.low_fltr_rb.config(state=tk.DISABLED)
        else:
            self.low_fltr_rb.config(state=tk.NORMAL)

        self.create_filtered_index_lists(self._app, Fltr.GEN_FLTR[Fltr.VAL], CrdOrdr.Original.val)
        self._app.gen_filter_list_size = self._app.filtered_list_size
        local_txt = Fltr.GEN_FLTR[Fltr.TXT] + " (" + str(self._app.gen_filter_list_size) + " cards)"
        self.gen_fltr_rb.config(text=local_txt)
        if self._app.gen_filter_list_size <= 0:
            self.gen_fltr_rb.config(state=tk.DISABLED)
        else:
            self.gen_fltr_rb.config(state=tk.NORMAL)

        self.update_status_frame()

    def update_status_frame(self):
        b1 = self._app.high_filter_list_size
        b2 = self._app.gen_filter_list_size
        b3 = self._app.med_filter_list_size
        b4 = self._app.low_filter_list_size
        b_total = b1 + b2 + b3 + b4
        total_length_pixels = 250
        block_start = 0
        if b_total < 1:
            block1_size = 1
            block2_size = 1
            block3_size = 1
            block4_size = 1
        else:
            block1_size = int(b1 / b_total * total_length_pixels)
            block2_size = int(b2 / b_total * total_length_pixels)
            block3_size = int(b3 / b_total * total_length_pixels)
            block4_size = int(b4 / b_total * total_length_pixels)
        gap = 1
        b1l = block_start
        b1r = block_start + block1_size
        b2l = b1r + gap
        b2r = b2l + block2_size
        b3l = b2r + gap
        b3r = b3l + block3_size
        b4l = b3r + gap
        b4r = b4l + block4_size
        self.stat.delete("all")
        self.stat.create_rectangle(b1l, 10, b1r, 50, fill="green")
        self.stat.create_rectangle(b2l, 10, b2r, 50, fill="purple")
        self.stat.create_rectangle(b3l, 10, b3r, 50, fill="orange")
        self.stat.create_rectangle(b4l, 10, b4r, 50, fill="red")

    def filter_the_spaced_repetition_list(self, app, card_order):
        percent_for_n = 100
        percent_for_p = 90
        percent_for_m = 50
        percent_for_f = 33
        percent_for_g = 25

        counter_n = 0
        counter_p = 0
        counter_m = 0
        counter_f = 0
        counter_g = 0

        def selective_filter(percent, i_idx, i_filtered_sorted_list):
            if random.randrange(100) <= percent:
                i_filtered_sorted_list.append(i_idx)
                return 1
            else:
                return 0

        if card_order == CrdOrdr.Alphabetical.val:
            sorted_list = app.ab_sort_list
            filtered_sorted_list = app.filtered_ab_sort_list
        elif card_order == CrdOrdr.Random.val:
            sorted_list = app.shuffled_list
            filtered_sorted_list = app.filtered_shuffled_list
        elif card_order == CrdOrdr.Original.val:
            sorted_list = list(range(len(app.term_list)))
            filtered_sorted_list = app.filtered_term_list
        else:
            raise ValueError("No such card order type")

        for m_idx in sorted_list:
            tag = app.get_tag_dt_txt(line=m_idx, get_tag_history=False)
            if tag == Tag.NoTag.d_txt:
                counter_n += selective_filter(percent_for_n, m_idx, filtered_sorted_list)
            elif tag == Tag.LowTag.d_txt:
                counter_p += selective_filter(percent_for_p, m_idx, filtered_sorted_list)
            elif tag == Tag.MedTag.d_txt:
                counter_m += selective_filter(percent_for_m, m_idx, filtered_sorted_list)
            elif tag == Tag.GenTag.d_txt:
                counter_f += selective_filter(percent_for_f, m_idx, filtered_sorted_list)
            elif tag == Tag.HighTag.d_txt:
                counter_g += selective_filter(percent_for_g, m_idx, filtered_sorted_list)
            else:
                raise ValueError("No such tagging type")

        app.filtered_list_size = len(filtered_sorted_list)

        #print("counter_n = ", counter_n)
        #print("counter_p = ", counter_p)
        #print("counter_m = ", counter_m)
        #print("counter_f = ", counter_f)
        #print("counter_g = ", counter_g)

        self._app.logger.debug("spaced repetition - number of no tag cards in group"+str(counter_n))
        self._app.logger.debug("spaced repetition - number of low tag cards in group"+str(counter_p))
        self._app.logger.debug("spaced repetition - number of med tag cards in group"+str(counter_m))
        self._app.logger.debug("spaced repetition - number of gen tag cards in group"+str(counter_f))
        self._app.logger.debug("spaced repetition - number of high tag cards in group"+str(counter_g))
