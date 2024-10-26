from abc import ABC, abstractmethod
import pandas as pd

class FileReader(ABC):

    @abstractmethod
    def read_translation_file(self, filepath:str) -> dict[str, str]:
        """Reads a file that should have words in one language in one
         column, and it's translation in another.\n
         Raises a FileNotFoundError if the file cannot be found"""
        pass

    @abstractmethod
    def read_progress_file(self, filepath:str) -> list[str]:
        """Reads a file that should have words in the language to be
        learned.\n
        Returns the translation as a list[str]\n
        Raises a FileNotFoundError if file cannot be found"""

class CSVReader(FileReader):

    def read_translation_file(self, filepath:str):
        data = pd.read_csv(filepath_or_buffer=filepath)
        language_keys = data.keys()
        trans_dict = {data[language_keys[0]][x] : data[language_keys[1]][x] for x
                      in data[language_keys[0]].keys()}
        return trans_dict

    def read_progress_file(self, filepath:str) -> list[str]:
        with open(filepath, "r") as file:
            return file.readlines()