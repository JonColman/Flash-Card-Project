from abc import ABC, abstractmethod

class FileWriter(ABC):

    @abstractmethod
    def save_progress_file(self, file_path:str, data: list[str]):
        """Saves a file so that each word is on a seperate line"""
        pass

class CSVWriter(FileWriter):

    def save_progress_file(self, file_path:str, data: list[str]):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(data))