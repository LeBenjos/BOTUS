# Transform suggested word in a emoji word
def transform_suggested_word(key_word, word):
    # emojis for letters
    correct_letter = ":red_square: "
    replace_letter = ":yellow_circle: "
    unknow_letter = ":blue_square: "
    dash_letter = ":heavy_minus_sign: "
    key_word = list(key_word)
    letter_key_word = list(key_word)
    # First letter is give so we delet this one
    del letter_key_word[0]
    # Check for correct letter
    for i in range(1, len(key_word), 1):
        if word[i] == key_word[i]:
            if word[i] == "-":
                key_word[i] = dash_letter
            else:
                key_word[i] = correct_letter
            letter_key_word.remove(word[i])
    # Check for replace letter
    for i in range(1, len(key_word), 1):
        if key_word[i] != correct_letter and key_word[i] != dash_letter:
            if word[i] in letter_key_word:
                key_word[i] = replace_letter
                letter_key_word.remove(word[i])
            else:
                key_word[i] = unknow_letter
    # Give the first letter
    key_word[0] = ":regional_indicator_" + key_word[0] + ": "
    # Return the suggested word in emoji
    return key_word