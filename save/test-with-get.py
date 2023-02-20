import random
import requests

#Fonction du fichier de la liste des mots
def get_list_of_words():
    response = requests.get(
        'https://www.pallier.org/extra/liste.de.mots.francais.frgut.txt',
        timeout=10)
    string_of_words = response.content.decode('utf-8')
    list_of_words = string_of_words.splitlines()
    return list_of_words

#Fonction choix du mot du jour (5 lettres minimum)
def choice_day_word(list_words):
  random_word = random.choice(list_words)
  while len(random_word) < 5 or len(random_word) > 8:
    return choice_day_word(list_words)
  return random_word

#Fonction qui enlève les accents aux mots
def remove_accents(word):
  split_word = list(word)
  for i in range(0,len(split_word),1):
    if split_word[i] == "é" or split_word[i] == "è" or split_word[i] == "ê" or split_word[i] == "ë" or split_word[i] == "ę" or split_word[i] == "ė" or split_word[i] == "ē":
        split_word[i] = "e"
    elif split_word[i] == "à" or split_word[i] == "â" or split_word[i] == "ª" or split_word[i] == "á" or split_word[i] == "ä" or split_word[i] == "ã" or split_word[i] == "å" or split_word[i] == "ā":
      split_word[i] = "a"
    elif split_word[i] == "û" or split_word[i] == "ù" or split_word[i] == "ü" or split_word[i] == "ú" or split_word[i] == "ū":
      split_word[i] = "u"
    elif split_word[i] == "î" or split_word[i] == "ï" or split_word[i] == "ì" or split_word[i] == "í" or split_word[i] == "į" or split_word[i] == "ī":
      split_word[i] = "i"
    elif split_word[i] == "ô" or split_word[i] == "º" or split_word[i] == "ö" or split_word[i] == "ò" or split_word[i] == "ó" or split_word[i] == "õ" or split_word[i] == "ø" or split_word[i] == "ō":
      split_word[i] = "o"
    elif split_word[i] == "ç" or split_word[i] == "ć" or split_word[i] == "č":
      split_word[i] = "c"
    elif split_word[i] == "ÿ":
      split_word[i] = "y"
    elif split_word[i] == "ñ" or split_word[i] == "ń":
      split_word[i] = "n"
  word = "".join(split_word)
  return word

#Fonction qui enlève les accents aux mots de la liste
def remove_list_accents(list_words):
  for i in range(0,len(list_words)-1,1):
    list_words[i] = remove_accents(list_words[i])
  return list_words
    
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

#Words contient la liste entière des mots
list_words = get_list_of_words()
list_words = remove_list_accents(list_words)
#Choix du mot du jour
day_word = choice_day_word(list_words)
print(day_word)

#Mot valide ou non
suggested_word = None
emoji_day_word = None
emoji_suggested_word = None
i = 0
while suggested_word != day_word and i < 6:
  emoji_day_word = transform_emoji_word(day_word, emoji_day_word, emoji_suggested_word)
  print("".join(emoji_day_word))
  suggested_word = input().lower()
  suggested_word = remove_accents(suggested_word)
  if (suggested_word in list_words) and (len(suggested_word) == len(day_word)):
    if suggested_word[0] != day_word[0]:
      print("Le mot doit commencer par la lettre :", day_word[0])
    else:
      emoji_suggested_word = transform_suggested_word(day_word, suggested_word)
      print("".join(emoji_suggested_word))
      if suggested_word == day_word:
        print("C'EST GAGNÉ")
      else:
        print("Dommage, nombre d'essai(s) restant(s) :", 5-i)
        i=i+1
  elif suggested_word not in list_words:
    print("Vérifier votre orthographe")
    if emoji_suggested_word == None:
      emoji_suggested_word = emoji_day_word
  else:
    print("Le nombres de lettres n'est pas correcte")
    if emoji_suggested_word == None:
      emoji_suggested_word = emoji_day_word
