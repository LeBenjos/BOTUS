from unidecode import unidecode

# Use unideco to remove all accents
def remove_accents(word):
    word = unidecode(word)
    return word