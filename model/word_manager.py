from model.file_reader import CSVReader, FileReader
from model.file_writer import CSVWriter, FileWriter
from random import choice

from utils import languages


class WordManager:
    def __init__(self,
                 file_reader: FileReader = CSVReader(),
                 file_writer: FileWriter = CSVWriter()
                 ):
        """Reader/Writer must inherit from base class in file_reader.py / file_writer.py\n
        Defaults: CSVReader / CSVWriter"""
        self.language_paths = {
        }

        self.progress_paths = {
        }

        self._load_languages()

        self.current_language = list(self.language_paths.keys())[0]

        self.file_reader = file_reader

        self.file_writer = file_writer
        self.learned_words = []
        self.words_to_learn = []
        self.translations = {}

        self._load_translations()
        self._load_progress()

        self.current_word = None

    def get_languages(self):
        return list(self.language_paths.keys())

    def _load_languages(self):
        for language in languages.find_languages():
            self.language_paths[language] = f"./data/{language}_words.csv"
            self.progress_paths[language] = f"./data/learned_{language}_words.csv"


    def set_language(self, language: str):
        if not language in self.language_paths.keys():
            print(f"This application currently does not have {language}"
                  f" translation data.\n\n"
                  f"Or the translation data is not named in the form: "
                  f"<language>_words.csv i.e. french_words.csv")
            return False
        elif language == self.current_language:
            return True
        else:
            self.current_language = language
            self._load_translations()
            self._load_progress()
            return True

    def _load_translations(self):
        try:
            self.translations = self.file_reader.read_translation_file(
                self.language_paths[self.current_language]
            )
        except KeyError:
            print(f"Application does not have translation data for "
                  f"{self.current_language}!")

    def _load_progress(self):
        if len(self.translations) == 0:
            print("Load a translation file before attempting to load "
                  "progress file!")
            return False
        else:
            try:
                self.learned_words = self.file_reader\
                        .read_progress_file(
                            self.progress_paths[self.current_language]
                        )

            except FileNotFoundError:
                self.learned_words = []
            finally:
                self.words_to_learn = [
                    word for word in self.translations.keys()
                    if not word in self.words_to_learn
                ]
                return True

    def _save_progress(self):
        self.file_writer.save_progress_file(
            self.progress_paths[self.current_language],
            self.learned_words
        )

    def learn_word(self):
        self.learned_words.append(self.current_word)
        self.words_to_learn.remove(self.current_word)
        self._save_progress()

    def choose_random_word(self) -> tuple[str, str]:
        """Returns (foreign word, english word)"""
        foreign = choice(self.words_to_learn)
        english = self.translations[foreign]
        self.current_word = foreign
        return foreign, english
