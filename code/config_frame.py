import tkinter as tk
import study_cards_app

class Conf_Frame:
    def __init__(self, main_win, window, app):
        self._app = app

        R_B_FONT = study_cards_app.MainWin.RADIO_BUTTON_FONT
        R_B_BG = study_cards_app.MainWin.RB_BG
        BUTTON_FONT = study_cards_app.MainWin.BUTTON_FONT

        config_frame = tk.LabelFrame(window, text="Configuration", font="Helvetica 14",
                                     width=900, height=600, bg="gray99", bd=1, relief=tk.SOLID)
        config_frame.place(relx=0.1, rely=0.1)
        self._config_frame = config_frame

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

        filter_cards_frame = tk.LabelFrame(config_frame, text="Filter", font="Helvetica 14",
                                           width=250, height=220, bg="white smoke", bd=1, relief=tk.SOLID)
        filter_cards_frame.place(relx=0.5, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=app.NO_FLTR[app.TXT], variable=filter_cards,
                     value=app.NO_FLTR[app.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.05)

        tk.Radiobutton(filter_cards_frame, text=app.LOW_FLTR[app.TXT], variable=filter_cards,
                     value=app.LOW_FLTR[app.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.2)

        tk.Radiobutton(filter_cards_frame, text=app.MED_FLTR[app.TXT], variable=filter_cards,
                     value=app.MED_FLTR[app.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.35)

        tk.Radiobutton(filter_cards_frame, text=app.HIGH_FLTR[app.TXT], variable=filter_cards,
                     value=app.HIGH_FLTR[app.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.5)

        tk.Radiobutton(filter_cards_frame, text=app.GEN_FLTR[app.TXT], variable=filter_cards,
                     value=app.GEN_FLTR[app.VAL], command=self.update_filter,
                     font=R_B_FONT, bg=R_B_BG).place(relx=0.0, rely=0.65)

        tk.Radiobutton(filter_cards_frame, text=app.UNTAGGED_FLTR[app.TXT], variable=filter_cards,
                       value=app.UNTAGGED_FLTR[app.VAL], command=self.update_filter,
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
        self.front_side = self.lang1_var.get()
        self.back_side = 1 - self.front_side

