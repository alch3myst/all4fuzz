import sys
import chardet

# Load file lines to array


def loadWordlist(location, index, encoding):
    try:
        # Wordlist load
        with open(location, 'r', encoding=encoding) as wordlists:
            wordlists = wordlists.readlines()
        wordlists = [x.strip() for x in wordlists]

        # Return a list with all lines splited asa arrai
        return wordlists[index:], len(wordlists)
    except FileNotFoundError as e:
        print('Failed to load file, try again')
        sys.exit(8)
