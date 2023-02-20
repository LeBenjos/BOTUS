# Discord motus bot
import nest_asyncio
import discord 
from datetime import *
from f_choice_day_word import *
from f_remove_accent import *
from f_transform_guess_word import *
from f_transform_suggested_word import *

# Varaibles for discord bot
nest_asyncio.apply()
intents = discord.Intents.all()
intents.messages = True
intents.members = True
intents.typing = True
client = discord.Client(intents=intents)

# Set local variables
# Languages
fr_day_word = choice_day_word("fr")
en_day_word = choice_day_word("en")
# Variables
date_day = datetime.today().day-1
day_hour = 7
first_day = datetime.today().day

# Print when the bot is ready
@client.event
async def on_ready():
    print("Botjos is ready")

# Action start when you send a message
@client.event
async def on_message(message):
  # Get local variables
  global fr_day_word, en_day_word, date_day, day_hour

  # Refresh the day word
  if date_day != date.today().day and datetime.today().hour >= 7:
    date_day = date.today().day
    await message.channel.send(f"Hello il est {day_hour}h! C'est l'heure du MOTUS, bonne chance et bonne journée! :blush: ")
    fr_day_word = choice_day_word("fr")
    en_day_word = choice_day_word("en")

  # The bot does not interact with himself
  if message.author == client.user:
    return

  # Transforme all message in low charactere
  message.content = message.content.lower()

  # Start the day_game
  if message.content == ('!fr'):
    await message.channel.send(fr_day_word)
  elif message.content == ('!en'):
    await message.channel.send(en_day_word)
  elif message.content == ('!rules'):
    await message.channel.send(f'ECRIRE LES REGLES (commandes, langues, heure de changement, comment jouer)')
  elif message.content == ('!stats'):
    await message.channel.send(f'ECRIRE LES STATS (Premier jour, nb participant, best participant, stats player)')


# Bot Token
client.run("")