import os

def find_languages():
    files = os.listdir("./data")
    return [name.split("_")[0] for name in files if not "learned" in name]