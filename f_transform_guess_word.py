# Transform word to guess in a emoji word
def transform_guess_word(key_word, word, emoji_suggested_word):
    # emojis for letters
    lettre_1 = ":regional_indicator_"
    lettre_2 = ": "
    correct_lettre = ":red_square: "
    unknow_lettre = ":blue_square: "
    dash_lettre = ":heavy_minus_sign: "
    # At the start
    if word == None:
        word = list(key_word)
        word[0] = lettre_1 + key_word[0] + lettre_2
        # Transforme word to guess in emoji
        for i in range(1, len(word), 1):
            if word[i] == "-":
                word[i] = dash_lettre
            else:
                word[i] = unknow_lettre
        return word
    # Compare word suggest and word to guess and replace the word to guess with the good emoji
    else:
        for i in range(1, len(key_word), 1):
            if word[i] == unknow_lettre:
                if emoji_suggested_word[i] == correct_lettre:
                    word[i] = lettre_1 + key_word[i] + lettre_2
                elif word[i] == "-":
                    word[i] = dash_lettre
                else:
                    word[i] = unknow_lettre
        # Return the word to guess in emoji
        return word