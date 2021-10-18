import tkinter as tk
from constants import Const, LnIdx, GuiTc, Trm, Tag, Fltr


class PresentationFrame:
    def __init__(self, main_win, window, app):
        self._app = app
        self.card_text = []  # The text of both sides of the current card

        presentation_frame = tk.LabelFrame(window, text="Flashcards", font="Helvetica 14", width=900,
                                           height=600, bg="gray99",  bd=1, relief=tk.SOLID)

        self.presentation_frame_obj = presentation_frame

        tagging_frame = tk.LabelFrame(presentation_frame, text="Tagging", font="Helvetica 14", width=180,
                                      height=300, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        tagging_frame.place(relx=0.75, rely=0.2)
        
        self.tagging_var = tk.IntVar()
        
        tag_rad1 = tk.Radiobutton(tagging_frame, text=Tag.NoTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.NoTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad1.place(relx=0.1, rely=0.1)

        tag_rad2 = tk.Radiobutton(tagging_frame, text=Tag.LowTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.LowTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad2.place(relx=0.1, rely=0.2)
        
        tag_rad3 = tk.Radiobutton(tagging_frame, text=Tag.MedTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.MedTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad3.place(relx=0.1, rely=0.3)

        tag_rad4 = tk.Radiobutton(tagging_frame, text=Tag.HighTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.HighTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad4.place(relx=0.1, rely=0.4)
        
        tag_rad5 = tk.Radiobutton(tagging_frame, text=Tag.GenTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.GenTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad5.place(relx=0.1, rely=0.5)
        
        cards_frame = tk.LabelFrame(presentation_frame, text="Cards", font="Helvetica 14", width=600,
                                    height=300, bg=GuiTc.L2_FRAME_BG,  bd=1, relief=tk.SOLID)
        cards_frame.place(relx=0.05, rely=0.2)

        tk.Button(presentation_frame, text="Next card", font=GuiTc.BUTTON_FONT,
                  command=self.nxt_button_clicked).place(relx=0.3, rely=0.8)
        
        tk.Button(presentation_frame, text="Previous card", font=GuiTc.BUTTON_FONT,
                  command=self.back_button_clicked).place(relx=0.05, rely=0.8)
        
        tk.Button(presentation_frame, text="Flip side", font=GuiTc.BUTTON_FONT,
                  command=self.flip_button_clicked).place(relx=0.5, rely=0.8)

        tk.Button(presentation_frame, text="Go to Config", font=GuiTc.BUTTON_FONT,
                  command=main_win.config_button_clicked).place(relx=0.8, rely=0.8)
        
        # show the card number sequentially:
        self.label1 = tk.Label(presentation_frame, text="", font="Helvetica 16")
        self.label1.place(relx=0.05, rely=0.1)
        
        self.shown_l_word = tk.Label(cards_frame, font="Helvetica 18 ", justify=tk.CENTER,
                                     wraplength=450, width=39, height=9)
        self.shown_l_word.place(relx=0.045, rely=0.05)  # width and height in characters not pixels

        window.bind("<space>", self.space_bar_key)
        window.bind("<Right>", self.right_arrow_key)
        window.bind("<Left>", self.left_arrow_key)
        window.bind("<Down>", self.down_arrow_key)

    def space_bar_key(self, event):
        self.flip_button_clicked()

    def down_arrow_key(self, event):
        self.flip_button_clicked()

    def right_arrow_key(self, event):
        self.nxt_button_clicked()

    def left_arrow_key(self, event):
        self.back_button_clicked()

    def item_tagging(self):
        app = self._app

        if app.front_side == 0:
            lang_idx = LnIdx.TERM1_IDX
        elif app.front_side == 1:
            lang_idx = LnIdx.TERM2_IDX
        else:
            lang_idx = -1

        d_txt = Tag.tvdt_dir[self.tagging_var.get()]
        app.update_tag_in_w_file(app.act_ln, lang_idx, d_txt)  # use act_line
        app.term_list[app.act_ln][lang_idx+2] = Trm.terms[lang_idx]+" "+d_txt
        app.reset_cards_request = True

    def nxt_button_clicked(self):
        nxt = True
        self.nxt_back_button_clicked(nxt)

    def back_button_clicked(self):
        nxt = False
        self.nxt_back_button_clicked(nxt)

    def nxt_back_button_clicked(self, nxt, continue_cards=False):
        app = self._app
        txt_filter = " (" + Fltr.filter_val_to_txt(app.filter_cards_val) + ")"
        if app.filtered_list_size <= 0:
            label1_txt = "Card number " + str(0) + " of " + str(0) + " cards" + txt_filter
            self.shown_l_word.configure(text="", bg=GuiTc.FRONT_CARD_COLOR)
        else:
            if nxt:
                if continue_cards:
                    pass
                else:
                    app.line_number += 1
            else:
                app.line_number -= 1

            # loop forever
            if app.line_number > app.filtered_list_size - 1:
                app.line_number = 0
            elif app.line_number < 0:
                app.line_number = app.filtered_list_size - 1

            app.set_act_line()
            self.card_text = [app.term_list[app.act_ln][LnIdx.TERM1_IDX].rstrip(),
                              app.term_list[app.act_ln][LnIdx.TERM2_IDX].strip()]

            self.shown_l_word.configure(text=self.card_text[app.front_side], bg=GuiTc.FRONT_CARD_COLOR)
            app.card_side = app.front_side
            self.set_tag_rb(app.act_ln)

            label1_txt = "Card number " + str(app.line_number + 1) + " of " + \
                         str(app.filtered_list_size) + " cards" + txt_filter
        self.label1.configure(text=label1_txt)

    def flip_button_clicked(self):
        app = self._app
        if app.filtered_list_size < 1:
            return
        if app.card_side == app.front_side:
            self.shown_l_word.configure(text=self.card_text[app.back_side], bg=GuiTc.BACK_CARD_COLOR)
            app.card_side = app.back_side
        else:
            self.shown_l_word.configure(text=self.card_text[app.front_side], bg=GuiTc.FRONT_CARD_COLOR)
            app.card_side = app.front_side

    def set_tag_rb(self, line):
        """
        Set tagging radio buttons to values in the data structure!
        set the tag radio button of the requested line
        to be called when changing the line
        :param line: the current actual line
        :return: none
        """
        data_text = self._app.get_tag_dt_txt(line)
        val = Tag.tdtv_dir[data_text]
        self.tagging_var.set(val)
