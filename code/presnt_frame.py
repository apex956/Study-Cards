import tkinter as tk
from constants import Const, LnIdx, GuiTc, Tag, Fltr
import logging
from inspect import currentframe, getframeinfo

class PresentationFrame:
    def __init__(self, main_win, window, app):
        self._app = app
        self._main_win = main_win
        self._tag_was_changed = False
        self.card_text = []  # The text of both sides of the current card
        self.max_length_of_tag_history = 5

        presentation_frame = tk.LabelFrame(window, text="Flashcards", font="Helvetica 14", width=900,
                                           height=600, bg="gray99",  bd=1, relief=tk.SOLID)

        self.presentation_frame_obj = presentation_frame

        tagging_frame = tk.LabelFrame(presentation_frame, text="Knowledge Tag", font="Helvetica 14", width=185,
                                      height=190, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        tagging_frame.place(relx=0.75, rely=0.15)

        consistency_frame = tk.LabelFrame(presentation_frame, text="Tag Consistency", font="Helvetica 14", width=185,
                                      height=70, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        consistency_frame.place(relx=0.75, rely=0.5)

        history_frame = tk.LabelFrame(presentation_frame, text="Tag History", font="Helvetica 14", width=185,
                                      height=72, bg=GuiTc.L2_FRAME_BG, bd=1, relief=tk.SOLID)
        history_frame.place(relx=0.75, rely=0.65)

        self.tagging_var = tk.IntVar()
        
        tag_rad1 = tk.Radiobutton(tagging_frame, text=Tag.NoTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.NoTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad1.place(relx=0.1, rely=0.03)
        tag_rad1.config(state=tk.DISABLED)

        tag_rad2 = tk.Radiobutton(tagging_frame, text=Tag.LowTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.LowTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad2.place(relx=0.1, rely=0.2)
        
        tag_rad3 = tk.Radiobutton(tagging_frame, text=Tag.MedTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.MedTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad3.place(relx=0.1, rely=0.37)

        tag_rad4 = tk.Radiobutton(tagging_frame, text=Tag.HighTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.HighTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad4.place(relx=0.1, rely=0.54)
        
        tag_rad5 = tk.Radiobutton(tagging_frame, text=Tag.GenTag.rb_txt, variable=self.tagging_var,
                                  value=Tag.GenTag.val, command=self.item_tagging,
                                  font=GuiTc.R_B_FONT, bg=GuiTc.RB_BG)
        tag_rad5.place(relx=0.1, rely=0.71)
        
        cards_frame = tk.LabelFrame(presentation_frame, text="Cards", font="Helvetica 14", width=600,
                                    height=360, bg=GuiTc.L2_FRAME_BG,  bd=1, relief=tk.SOLID)
        cards_frame.place(relx=0.05, rely=0.15)

        tk.Button(presentation_frame, text="Next card", font=GuiTc.BUTTON_FONT,
                  command=self.nxt_button_clicked).place(relx=0.3, rely=0.85)
        
        tk.Button(presentation_frame, text="Previous card", font=GuiTc.BUTTON_FONT,
                  command=self.back_button_clicked).place(relx=0.05, rely=0.85)
        
        tk.Button(presentation_frame, text="Flip side", font=GuiTc.BUTTON_FONT,
                  command=self.flip_button_clicked).place(relx=0.5, rely=0.85)

        tk.Button(presentation_frame, text="Back to config.", font=GuiTc.BUTTON_FONT,
                  command=main_win.config_button_clicked).place(relx=0.8, rely=0.85)
        
        # show the card number sequentially:
        self.label1 = tk.Label(presentation_frame, text="", font="Helvetica 16")
        self.label1.place(relx=0.05, rely=0.05)
        
        self.shown_l_word = tk.Label(cards_frame, font="Helvetica 18 ", justify=tk.CENTER,
                                     wraplength=450, width=39, height=10)
        self.shown_l_word.place(relx=0.045, rely=0.05)  # width and height in characters not pixels

        self.label2 = tk.Label(consistency_frame, text="", font="Helvetica 14")
        self.label2.place(relx=0.05, rely=0.1)

        self.label3 = tk.Label(history_frame, text="", font="Helvetica 14")
        self.label3.place(relx=0.05, rely=0.2)


        window.bind("<space>", self.space_bar_key)
        window.bind("<Right>", self.right_arrow_key)
        window.bind("<Left>", self.left_arrow_key)
        window.bind("<Down>", self.down_arrow_key)

    def space_bar_key(self, event):
        if self._main_win.active_presentation_frame:
            self.flip_button_clicked()

    def down_arrow_key(self, event):
        if self._main_win.active_presentation_frame:
            self.flip_button_clicked()

    def right_arrow_key(self, event):
        if self._main_win.active_presentation_frame:
            self.nxt_button_clicked()

    def left_arrow_key(self, event):
        if self._main_win.active_presentation_frame:
            self.back_button_clicked()

    def item_tagging(self, tag_changed=True):
        """
        This method is called when a tag radio button is clicked or
        when the Next button is clicked
        Tagging history is updated and saved
        It updates the tag and the history in the work file and in term_list[]
        """
        app = self._app
        self._tag_was_changed = True

        if app.front_side == 0:
            lang_idx = LnIdx.TERM1_IDX
        elif app.front_side == 1:
            lang_idx = LnIdx.TERM2_IDX
        else:
            raise ValueError

        d_txt = Tag.tvdt_dir[self.tagging_var.get()]

        # DEBUG CODE +++++++++
        #old_tag_txt = app.term_list[app.act_ln][lang_idx + 2]
        #old_tag_number = Tag.tdtv_dir[" ".join(app.term_list[app.act_ln][lang_idx + 2].split()[-2:])]
        #new_tag_txt = app.terms[lang_idx] + " " + d_txt

        new_tag_number = self.tagging_var.get()
        tag_history = app.get_tag_dt_txt(line=app.act_ln, get_tag_history=True)
        if len(tag_history) >= self.max_length_of_tag_history:
            tag_history = tag_history[:-1]

        # DEBUG CODE +++++++++
        #print(f"Tag was changed from {old_tag_txt} [{old_tag_number}] to {new_tag_txt}[{new_tag_number}]")
        dbg_module_line = " Module:" + __name__ + " Line:" + str(getframeinfo(currentframe()).lineno)
        app.logger.debug("Tag history is:" + str(tag_history) + dbg_module_line)

        addition_to_d_txt = "{" + str(new_tag_number) + tag_history + "}"
        d_txt += addition_to_d_txt

        app.update_tag_in_w_file(app.act_ln, lang_idx, d_txt)  # use act_line
        app.term_list[app.act_ln][lang_idx+2] = app.terms[lang_idx]+" "+d_txt

        if tag_changed:  # do not reset the cards if just the Next button was clicked
            app.reset_cards_request = True

    def nxt_button_clicked(self):
        """
        Note: recording tag history only in the forward direction.
        Presumably going backward is done only for checking
        """
        nxt = True
        if not self._tag_was_changed:  # avoid calling the method again
            self.item_tagging(False)
        self._tag_was_changed = False
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
                msg = tk.Tk()
                msg.withdraw()
                msg_box = tk.messagebox.askyesnocancel('Flash Cards', 'Start Over?')
                if msg_box:
                    app.line_number = 0
                    msg.destroy()
                else:
                    app.line_number -= 1
                    msg.destroy()
                    return

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

            consistency, tag_history = self.tag_stability_score()
            self.label2.configure(text=consistency)
            self.label3.configure(text=tag_history)

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
        Set tagging radio buttons to values in the data structure
        set the tag radio button of the requested line
        to be called when changing the line
        :param line: the current actual line
        :return: none
        """
        data_text = self._app.get_tag_dt_txt(line=line, get_tag_history=False)
        val = Tag.tdtv_dir[data_text]
        self.tagging_var.set(val)

    def tag_stability_score(self):
        """
        A somewhat arbitrary set of rules for stability scores
        Toggling between the "good" and "minor" tags does not affect the stability score

        """
        tag_history = self._app.get_tag_dt_txt(line=self._app.act_ln, get_tag_history=True)
        # remove "no tag" and replace "minor" with "good"
        tag_history1 = tag_history.replace("0", "")
        tag_history2 = tag_history1.replace("4", "3")
        if len(tag_history2) < 4:
            outcome = "Undetermined"
        elif len(tag_history2) > self.max_length_of_tag_history:
            outcome = "Error!"
        else:
            if len(tag_history2) == self.max_length_of_tag_history:
                tag_history3 = tag_history2[:-1]  # never mind the oldest one
            else:
                tag_history3 = tag_history2
            # if last 4 are the same
            if tag_history3 == len(tag_history3)*tag_history3[0]:
                outcome = "High"
            # if last 3 are the same
            elif tag_history2[0] == tag_history2[1] and tag_history2[0] == tag_history2[2]:
                outcome = "Medium"
            else:
                outcome = "Low"

        tag_history_letters1 =tag_history2.replace("1", "P ")
        tag_history_letters2 =tag_history_letters1.replace("2", "M ")
        tag_history_letters3 =tag_history_letters2.replace("3", "G ")
        return outcome, tag_history_letters3

