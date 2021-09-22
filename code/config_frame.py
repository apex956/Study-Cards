import tkinter as tk
import study_cards_app

class Conf_Frame:
    def __init__(self, main_win, window, app):
        self._app = app

        # The filter does not change with 1st language
        self.VAL = 0  # index for value
        self.TXT = 1  # index for radio button text
        self.NO_FLTR = [0, "Show all"]
        self.LOW_FLTR = [1, "Show low"]  # level of knowledge of studied terms
        self.MED_FLTR = [2, "Show medium"]
        self.HIGH_FLTR = [3, "Show high"]
        self.GEN_FLTR = [4, "Show generic"]  # for example: spelling problems
        self.UNTAGGED_FLTR = [5, "Show untagged"]

        R_B_FONT = study_cards_app.MainWin.RADIO_BUTTON_FONT
        R_B_BG = study_cards_app.MainWin.RB_BG
        BUTTON_FONT = study_cards_app.MainWin.BUTTON_FONT

        config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                                     width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        config_frame.place(relx=0.1, rely=0.1)
        self.config_frame_obj = config_frame

        card_order_frame = tk.Frame(config_frame, width=150, height=160, bg="white smoke",  bd=1, relief=tk.SOLID)
        card_order_frame.place(relx=0.1, rely=0.05)
        tk.Label(card_order_frame, text="Card Order:", font="Helvetica 16", bg="white smoke")\
            .place(relx=0.0, rely=0.0)

        card_order = tk.IntVar()

        rad1 = tk.Radiobutton(card_order_frame, text='Alphabetical', variable=card_order, value=1,
                              command=self.alphabetical_selected,
                              font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.2)

        rad2 = tk.Radiobutton(card_order_frame, text='Random', variable=card_order, value=2,
                              command=self.random_selected,
                              font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.4)

        rad3 = tk.Radiobutton(card_order_frame, text='Original', variable=card_order, value=3,
                              command=self.original_selected,
                              font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.6)

        card_order.set(1)  # set the default radio button

        filter_cards = tk.IntVar()
        self._filter_cards = filter_cards

        filter_cards_frame = tk.LabelFrame(config_frame, text="Filter", font="Helvetica 14",
                                           width=250, height=220, bg="white smoke", bd=1, relief=tk.SOLID)
        filter_cards_frame.place(relx=0.5, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=self.NO_FLTR[self.TXT], variable=filter_cards,
                       value=self.NO_FLTR[self.VAL], command=self.update_filter,
                       font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=self.LOW_FLTR[self.TXT], variable=filter_cards,
                     value=self.LOW_FLTR[self.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.2)

        tk.Radiobutton(filter_cards_frame, text=self.MED_FLTR[self.TXT], variable=filter_cards,
                     value=self.MED_FLTR[self.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.35)

        tk.Radiobutton(filter_cards_frame, text=self.HIGH_FLTR[self.TXT], variable=filter_cards,
                     value=self.HIGH_FLTR[self.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.5)

        tk.Radiobutton(filter_cards_frame, text=self.GEN_FLTR[self.TXT], variable=filter_cards,
                     value=self.GEN_FLTR[self.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.65)

        tk.Radiobutton(filter_cards_frame, text=self.UNTAGGED_FLTR[self.TXT], variable=filter_cards,
                       value=self.UNTAGGED_FLTR[self.VAL], command=self.update_filter,
                       font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.8)

        filter_cards.set(0)  # set the default radio button

        front_side_frame = tk.LabelFrame(config_frame, text="Front side", font="Helvetica 14",
                                         width=200, height=120, bg="white smoke", bd=1, relief=tk.SOLID)
        front_side_frame.place(relx=0.1, rely=0.5)

        self.lang1_var = tk.IntVar()

        front_side_rad1 = tk.Radiobutton(front_side_frame, text=app.language1, variable=self.lang1_var,
                                         value=0, command=self.change_lang_order,
                                         font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.05)

        front_side_rad2 = tk.Radiobutton(front_side_frame, text=app.language2, variable=self.lang1_var,
                                         value=1, command=self.change_lang_order,
                                         font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.4)

        tk.Button(config_frame, text="Show Flash Cards", font=BUTTON_FONT,
                  command=main_win.flash_cards_button_clicked).place(relx=0.7, rely=0.8)

    def alphabetical_selected(self):
        self._app.mode = "alphabetical"

    def random_selected(self):
        self._app.mode = "random"

    def original_selected(self):
        self._app.mode = "original"

    def update_filter(self):
        pass

    def change_lang_order(self):
        self._app.front_side = self.lang1_var.get()
        self._app.back_side = 1 - self._app.front_side

    def create_filtered_index_lists(self, app):
        app.filtered_ab_sort_lst.clear()
        app.filtered_shuffled_list.clear()
        app.filtered_term_list.clear()

        filter_val = self._filter_cards.get()
        if filter_val == self.NO_FLTR[self.VAL]:
            app.filtered_ab_sort_lst = app.ab_sort_lst[:]
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
                expected_tag_dt_txt = ""  # Need to handle
                print("Filter not found!")

            if app.mode == "alphabetical":
                for m_idx in app.ab_sort_lst:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_ab_sort_lst.append(m_idx)
                app.filtered_list_size = len(app.filtered_ab_sort_lst)
            elif app.mode == "random":
                for m_idx in app.shuffled_list:
                    if app.get_tag_dt_txt(m_idx) == expected_tag_dt_txt:
                        app.filtered_shuffled_list.append(m_idx)
                app.filtered_list_size = len(app.filtered_shuffled_list)
            elif app.mode == "original":
                for a_idx in range(len(app.term_list)):
                    if app.get_tag_dt_txt(a_idx) == expected_tag_dt_txt:
                        app.filtered_term_list.append(a_idx)
                app.filtered_list_size = len(app.filtered_term_list)


