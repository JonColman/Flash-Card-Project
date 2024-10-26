from control.card_manager import CardManager
from model.file_reader import FileReader, CSVReader
from model.file_writer import FileWriter, CSVWriter

from view.view import View
from model.word_manager import WordManager


class GameManager:

    def __init__(self, view: View,
                 file_reader: FileReader = CSVReader(),
                 file_writer: FileWriter = CSVWriter()
                 ):
        """Reader/Writer must inherit from base class in file_reader.py / file_writer.py\n
        Defaults: CSVReader / CSVWriter"""

        self.cm: CardManager = CardManager(view)
        self.wm: WordManager = WordManager(
            file_reader=file_reader,
            file_writer=file_writer
        )

        self.view = view
        self.set_language(self.wm.get_languages()[0])
        self.view.set_button_command(command=self._wrong_action, button="wrong")
        self.view.set_button_command(command=self._right_action, button="right")
        self.view.set_language_button_command(
            command=self.set_language,
            languages=self.wm.get_languages()
        )
        self.get_random_word()

    def get_random_word(self):
        foreign, english = self.wm.choose_random_word()
        self.cm.change_card_words(foreign=foreign, english=english)
        self.cm.flip_card()

    def _wrong_action(self, event):
        if self.view.check_button_bounds(event):
            self.get_random_word()

    def _right_action(self, event):
        if self.view.check_button_bounds(event):
            self.wm.learn_word()
            self.get_random_word()

    def set_language(self, language: str):
        self.view.set_language(language)
        self.wm.set_language(language)
        self.get_random_word()
