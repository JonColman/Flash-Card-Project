from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import Combobox

import os

BACKGROUND_COLOR = "#B1DDC6"


class View:

    def __init__(self):
        self.root = Tk()
        self.root.configure(background=BACKGROUND_COLOR, padx=50, pady=50)

        self.images = {
            'front' : PhotoImage(file="./images/card_front.png"),
            'back'  : PhotoImage(file="./images/card_back.png"),
            'right' : PhotoImage(file="./images/right.png"),
            'wrong' : PhotoImage(file="./images/wrong.png"),
            'lang'  : PhotoImage(file="./images/languages.png")
        }

        self.card_sides = {
            'front' : self._create_card_canvas(),
            'back'  : self._create_card_canvas(),
        }

        self.language_titles = {
            'front' : 'French',
            'back'  : 'English',
        }

        self.language_title_labels = {}
        self.language_word_labels = {}

        self.button_canvases = {
            'wrong' : self._create_button_canvas(),
            'right' : self._create_button_canvas(),
        }

        self.choose_lang_canvas = self._create_canvas(width=200, height=100)

        self._configure_card()
        self._configure_buttons()

        self._grid_components()

        self.BUTTON_BOUNDS_X = (83,178)
        self.BUTTON_BOUNDS_Y = (0, 96)

        self.afterID = self.root.after(5000, self._flip_card_canvas, False)

    def _configure_card(self):
        for key, canvas in self.card_sides.items():
            canvas.create_image(400,263,image=self.images[key])
            canvas.configure(highlightthickness=0)

            title_label = canvas.create_text(400,163,
                                             text=self.language_titles[key],
                                             font=("Courier", 26, "bold")
                                             )
            self.language_title_labels[key] = title_label

            word_label = canvas.create_text(400, 303,
                                            text="",
                                            font=("Courier", 20, "bold")
                                            )
            self.language_word_labels[key] = word_label

    def _configure_buttons(self):
        for key, canvas in self.button_canvases.items():
            canvas.create_image(130,50,image=self.images[key])
            canvas.configure(highlightthickness=0)

    def _grid_components(self):
        self.card_sides['front'].grid(row=0, column=0, columnspan=3)

        self.button_canvases['wrong'].grid(row=1, column=0, sticky="we")
        self.button_canvases['right'].grid(row=1, column=2, sticky="we")

        self.choose_lang_canvas.grid(row=1, column=1, sticky="we")
        self.choose_lang_canvas.create_image(130, 50, image=self.images['lang'])
        self.choose_lang_canvas.configure(highlightthickness=0)

    def _turn_card(self, side1: str, side2: str):
        self.card_sides[side1].grid_forget()
        self.card_sides[side2].grid(row=0, column=0, columnspan=3)

    def _reset_after_timer(self):
        self.root.after_cancel(self.afterID)
        self.afterID = self.root.after(5000, self._flip_card_canvas, False)

    def _flip_card_canvas(self, flip_later = False):
        if self.card_sides['front'].grid_info():
            self._turn_card('front', 'back')
        else:
            self._turn_card('back', 'front')
        if flip_later:
            self._reset_after_timer()

    def new_card(self):
        if self.card_sides['back'].grid_info():
            self._turn_card('back', 'front')
        self._reset_after_timer()

    def _create_canvas(self, width, height):
        return Canvas(self.root,
                      width=width,
                      height=height,
                      background=BACKGROUND_COLOR
                      )

    def _create_card_canvas(self):
        return self._create_canvas(width=800, height=526)

    def _create_button_canvas(self):
        return self._create_canvas(width=200, height=100)

    def change_word(self, foreign: str, english: str):
        """Changes the word on both foreign and english side of card"""
        self.card_sides['front'].itemconfig(
                    self.language_word_labels['front'],
                    text=foreign
                    )

        self.card_sides['back'].itemconfig(
                    self.language_word_labels['back'],
                    text=english
                    )
        self.root.update()

    def set_button_command(self, command, button: str):
        #<Button-1> -> Left Mouse Click
        self.button_canvases[button].bind("<Button-1>", command)

    def set_language_button_command(self, command, languages):
        def popup_dialog(event):
            button_bounds_x = (70, 190)
            button_bounds_y = (0, 97)

            if button_bounds_x[0] <= event.x <= button_bounds_x[1]:
                if button_bounds_y[0] <= event.y <= button_bounds_y[1]:
                    result = DropdownDialog(self.root, [
                        lang.title() for lang in languages
                    ]).result
                    if not result is None:
                        command(result.lower())
            return

        self.choose_lang_canvas.bind("<Button-1>", popup_dialog)

    def check_button_bounds(self, event):
        return self.BUTTON_BOUNDS_X[0] <= event.x <= self.BUTTON_BOUNDS_X[1] \
            and self.BUTTON_BOUNDS_Y[0] <= event.y <= self.BUTTON_BOUNDS_Y[1]

    def set_language(self, language: str):
        self.root.title(f"{language.title()} to English flashcards")
        self.language_titles['front'] = language
        self.card_sides['front'].itemconfig(
                self.language_title_labels['front'],
                text=language.title()
        )

    def mainloop(self):
        self.root.mainloop()


class DropdownDialog(simpledialog.Dialog):

    def __init__(self, parent, values, title=None):
        self.values = values
        self.label = None
        self.combo = None
        self.result = None
        super().__init__(parent, title=title)

    def body(self, master):
        self.label = Label(master, text="Choose a foreign language: ")
        self.label.pack(pady=10)

        self.combo = Combobox(master, values=self.values)
        self.combo.pack(pady=10)
        self.combo.current(0)

        return self.combo

    def apply(self):
        self.result = self.combo.get()