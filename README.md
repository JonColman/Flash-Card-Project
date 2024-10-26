# Foreign Language Flash Cards

This is a fairly basic python app with tkinter GUI, with a button to confirm the user knows a word, a button to confirm 
the user does not, and a button which loads a dialog to select a different foreign language.

The project has French and Turkish translations pre-installed

## Package Dependencies

This project depends on the pandas package, which can be installed via pip:
`pip install pandas`

Otherwise, the package can be installed on Pycharm via:

`File > Settings > Python Interpreter`

## Extending File Reading/Writing

While the project contains the means to read CSV files, file_reader.py and file_writer.py contain a base
FileReader/FileWriter abstract class that can be inherited from, in the event you wish to read words in a different
format

## Inputting different languages

### File naming

Users can compile their own lists of translations to use in the program. The user must name their translation file as:

*\<language\>_words.\<format\>*

For example: turkish_words.csv

This is so that the project can recognise the language name, and label accordingly. All translation files must be saved
in the data directory

### CSV Layout

Each line of your language csv file must be in the following format:

*\<foreign word\>,\<english word\>*

For example in French: deux,two

Each translation must be on a separate line, with no empty whitespace
