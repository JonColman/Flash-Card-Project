from view.view import View

class CardManager:

    def __init__(self, view: View):
        self.view = view

    def change_card_words(self, foreign: str, english: str):
        self.view.change_word(foreign, english)

    def flip_card(self):
        self.view.new_card()