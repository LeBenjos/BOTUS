from faker import Faker

# Use faker to choose a random word
def choice_day_word(language):
    # Play in french
    if language == "fr":
        random_word = Faker('fr_FR').word()
        while (len(random_word) < 5 or len(random_word) > 10) or "'" in random_word:
            return choice_day_word(language)
        return random_word
    # Play in english
    elif language == "en":
        random_word = Faker().word()
        while (len(random_word) < 5 or len(random_word) > 10) or "'" in random_word:
            return choice_day_word("en")
        return random_word
    # Other languages
    else:
        return "Désolé pour l'instant seulement 2 langues sont disponibles"