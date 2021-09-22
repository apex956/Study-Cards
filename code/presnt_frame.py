import tkinter as tk
import study_cards_app

class Presentation_Frame:
    def __init__(self, main_win, window, app):
        R_B_FONT = main_win.RADIO_BUTTON_FONT
        R_B_BG = main_win.RB_BG
        BUTTON_FONT = main_win.BUTTON_FONT

        self._app = app
        self.card_text = []  # The text of both sides of the current card

        presentation_frame = tk.LabelFrame(window, text="Flashcards", font="Helvetica 14", width=900,
                                           height=600, bg="gray99",  bd=1, relief=tk.SOLID)

        self.presentation_frame_obj = presentation_frame

        tagging_frame = tk.LabelFrame(presentation_frame, text="Tagging", font="Helvetica 14", width=170,
                                      height=300, bg="white smoke", bd=1, relief=tk.SOLID)
        tagging_frame.place(relx=0.75, rely=0.2)
        
        self.tagging_var = tk.IntVar()
        
        tag_rad1 = tk.Radiobutton(tagging_frame, text=app.NoTag.rb_txt, variable=self.tagging_var,
                                  value=app.NoTag.val, command=self.item_tagging,
                                  font=R_B_FONT, bg=R_B_BG)
        tag_rad1.place(relx=0.1, rely=0.1)

        tag_rad2 = tk.Radiobutton(tagging_frame, text=app.LowTag.rb_txt, variable=self.tagging_var,
                                  value=app.LowTag.val, command=self.item_tagging,
                                  font=R_B_FONT, bg=R_B_BG)
        tag_rad2.place(relx=0.1, rely=0.2)
        
        tag_rad3 = tk.Radiobutton(tagging_frame, text=app.MedTag.rb_txt, variable=self.tagging_var,
                                  value=app.MedTag.val, command=self.item_tagging,
                                  font=R_B_FONT, bg=R_B_BG)
        tag_rad3.place(relx=0.1, rely=0.3)

        tag_rad4 = tk.Radiobutton(tagging_frame, text=app.HighTag.rb_txt, variable=self.tagging_var,
                                  value=app.HighTag.val, command=self.item_tagging,
                                  font=R_B_FONT, bg=R_B_BG)
        tag_rad4.place(relx=0.1, rely=0.4)
        
        tag_rad5 = tk.Radiobutton(tagging_frame, text=app.GenTag.rb_txt, variable=self.tagging_var,
                                  value=app.GenTag.val, command=self.item_tagging,
                                  font=R_B_FONT, bg=R_B_BG)
        tag_rad5.place(relx=0.1, rely=0.5)
        
        cards_frame = tk.LabelFrame(presentation_frame, text="Cards", font="Helvetica 14", width=600,
                                    height=300, bg="gray99",  bd=1, relief=tk.SOLID)
        cards_frame.place(relx=0.05, rely=0.2)

        tk.Button(presentation_frame, text="Next card", font=BUTTON_FONT,
                  command=self.nxt_button_clicked).place(relx=0.05, rely=0.1)
        
        tk.Button(presentation_frame, text="Previous card", font=BUTTON_FONT,
                  command=self.back_button_clicked).place(relx=0.2, rely=0.1)
        
        tk.Button(presentation_frame, text="Flip side", font=BUTTON_FONT,
                  command=self.flip_button_clicked).place(relx=0.4, rely=0.1)

        tk.Button(presentation_frame, text="Go to Config", font=BUTTON_FONT,
                  command=main_win.config_button_clicked).place(relx=0.1, rely=0.8)
        
        # show the card number sequentially:
        self.label1 = tk.Label(presentation_frame, text="", font="Helvetica 16")
        self.label1.place(relx=0.65, rely=0.1)
        
        self.shown_l_word = tk.Label(cards_frame, font="Helvetica 18 ", justify=tk.CENTER,
                                wraplength=450, width=35, height=9)
        self.shown_l_word.place(relx=0.05, rely=0.05)  # width and height in characters not pixels

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
        tag_val = self.tagging_var.get()

        if app.front_side == 0:
            lang_idx = app.lang1_idx
        elif app.front_side == 1:
            lang_idx = app.lang2_idx
        else:
            lang_idx = -1  # !!! this whole section needs to be improved !!!
        #print("Selected marking:", act_ln, lang_idx, tag_val)  # debug

        d_txt = app.tvdt_dir[tag_val]
        app.update_tag_in_w_file(app.act_ln, lang_idx, d_txt)  # use act_line
        app.term_list[app.act_ln][lang_idx+2] = app.languages[lang_idx]+" "+d_txt

    def nxt_button_clicked(self):
        nxt = True
        self.nxt_back_button_clicked(nxt)

    def back_button_clicked(self):
        nxt = False
        self.nxt_back_button_clicked(nxt)

    def nxt_back_button_clicked(self, nxt, start_over = False):
        app = self._app
        if app.filtered_list_size <= 0:
            label1_txt = "Card number " + str(0) + " of " + str(0) + " cards"
            self.shown_l_word.configure(text="")
            #enable_disable_tag_radio_buttons(False)
        else:
            if nxt:
                app.line_number += 1
            else:
                app.line_number -= 1

            # loop forever
            if app.line_number > app.filtered_list_size - 1:
                app.line_number = 0
            elif app.line_number < 0:
                app.line_number = app.filtered_list_size - 1

            # start over
            if start_over:
                app.line_number = 0

            app.set_act_line(app.line_number)
            self.card_text = [app.term_list[app.act_ln][app.lang1_idx].rstrip(), app.term_list[app.act_ln][app.lang2_idx].strip()]

            self.shown_l_word.configure(text=self.card_text[app.front_side])
            app.card_side = app.front_side
            self.set_tag_rb(app.act_ln)

            label1_txt = "Card number " + str(app.line_number + 1) + " of " + str(app.filtered_list_size) + " cards"
            #enable_disable_tag_radio_buttons(True)
        self.label1.configure(text=label1_txt)

    def flip_button_clicked(self):
        app = self._app
        if app.card_side == app.front_side:
            self.shown_l_word.configure(text=self.card_text[app.back_side])
            app.card_side = app.back_side
            #enable_disable_tag_radio_buttons(False)
        else:
            self.shown_l_word.configure(text=self.card_text[app.front_side])
            app.card_side = app.front_side
            #enable_disable_tag_radio_buttons(True)

    def set_tag_rb(self, line):
        """
        Set tagging radio buttons to values in the data structure!
        set the tag radio button of the requested line
        to be called when changing the line
        :param line: the current actual line
        :return: none
        """
        data_text = self._app.get_tag_dt_txt(line)
        val = self._app.tdtv_dir[data_text]
        self.tagging_var.set(val)

    def enable_disable_tag_radio_buttons(self, enable):

        '''
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
        '''