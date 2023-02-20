from faker import Faker
from unidecode import unidecode

#Fonction choix du mot du jour (5 lettres minimum)
def choice_day_word(langue):
    if langue == "fr":
        random_word = Faker('fr_FR').word()
        while (len(random_word) < 5 or len(random_word) > 10) or "-" in random_word or "'" in random_word:
            return choice_day_word(langue)
        return random_word
    else:
        random_word = Faker().word()
        while (len(random_word) < 5 or len(random_word) > 10) or "-" in random_word or "'" in random_word:
            return choice_day_word("en")
        return random_word

#Fonction qui enlève les accents aux mots
def remove_accents(word):
    word = unidecode(word)
    return word 
    
#Fonction qui transforme le mot proposé
def transform_suggested_word(key_word, word):
  correct_lettre = ":red_square: "
  replace_lettre = ":yellow_circle: "
  unknow_lettre = ":blue_square: "
  dash_lettre = ":heavy_minus_sign: "
  key_word = list(key_word)
  lettre_key_word = list(key_word)
  del lettre_key_word[0]
  for i in range(1,len(key_word),1):
    if word[i] == key_word[i]:
      if word[i] == "-":
        key_word[i] = dash_lettre
      else:
        key_word[i] = correct_lettre
      lettre_key_word.remove(word[i])
  for i in range(1,len(key_word),1):
    if key_word[i] != correct_lettre and key_word[i] != dash_lettre:
      if word[i] in lettre_key_word:
        key_word[i] = replace_lettre
        lettre_key_word.remove(word[i])
      else:
        key_word[i] = unknow_lettre
  key_word[0] = ":regional_indicator_" + key_word[0] + ": "
  return key_word

#Fonction qui traduit en emoji
def transform_emoji_word(key_word, word, emoji_suggested_word):
  lettre_1 = ":regional_indicator_"
  lettre_2 = ": "
  correct_lettre = ":red_square: "
  unknow_lettre = ":blue_square: "
  dash_lettre = ":heavy_minus_sign: "
  if word == None:
    word = list(key_word)
    word[0] = lettre_1 + key_word[0] + lettre_2
    for i in range(1,len(word),1):
      if word[i] == "-":
        word[i] = dash_lettre
      else:
        word[i] = unknow_lettre
    return word
  else:
    for i in range(1,len(key_word),1):
      if word[i] == unknow_lettre:
        if emoji_suggested_word[i] == correct_lettre:
          word[i] = lettre_1 + key_word[i] + lettre_2
        elif word[i] == "-":
          word[i] = dash_lettre
        else:
          word[i] = unknow_lettre
    return word

#Choix du mot du jour
day_word = remove_accents(choice_day_word("fr"))
print(day_word)

#Mot valide ou non
suggested_word = None
emoji_day_word = None
emoji_suggested_word = None
i = 0
while suggested_word != day_word and i < 6:
  emoji_day_word = transform_emoji_word(day_word, emoji_day_word, emoji_suggested_word)
  print("".join(emoji_day_word))
  print("ici-1")
  suggested_word = input().lower()
  suggested_word = remove_accents(suggested_word)
  if len(suggested_word) == len(day_word):
    if suggested_word[0] != day_word[0]:
      print("Le mot doit commencer par la lettre :", day_word[0])
      if emoji_suggested_word == None:
        emoji_suggested_word = emoji_day_word
    else:
      emoji_suggested_word = transform_suggested_word(day_word, suggested_word)
      print("".join(emoji_suggested_word))
      if suggested_word == day_word:
        emoji_day_word = transform_emoji_word(day_word, emoji_day_word, emoji_suggested_word)
        print("".join(emoji_day_word))
        print("C'EST GAGNÉ")
      else:
        print("Dommage, nombre d'essai(s) restant(s) :", 5-i)
        i=i+1
  else:
    print("Le nombres de lettres n'est pas correcte")
    if emoji_suggested_word == None:
      emoji_suggested_word = emoji_day_word