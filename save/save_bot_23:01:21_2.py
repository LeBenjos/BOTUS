# Discord motus bot
import nest_asyncio
import discord
from discord.ext import commands, tasks
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
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)

# Set local variables
# Languages
fr_day_word = choice_day_word("fr")
en_day_word = choice_day_word("en")
# Variables
date_day = datetime.today().day-1
day_hour = 7
first_day = datetime.today().day
game = 0

# Print when the bot is ready
@client.event
async def on_ready():
    print("Botjos is ready")
    reset_day_word.start()

@tasks.loop(minutes=1)
# Reset the day word
async def reset_day_word():
  global fr_day_word, en_day_word, date_day
  print(fr_day_word)
  if date_day != date.today().day and datetime.today().hour >= 7:
    date_day = date.today().day
    fr_day_word = choice_day_word("fr")
    en_day_word = choice_day_word("en")
    print(fr_day_word)

# Action start when you send a message
@client.event
async def on_message(message):
  # Get local variables
  global game

  # The bot does not interact with himself
  if message.author == client.user:
    return
  
  # Transforme all message in low charactere
  message.content = message.content.lower()

  if message.content.startswith('!'):
    await client.process_commands(message)
    return

  # GAME
  if game == 1:
    pass

# Commands
@client.command()
# Start the day game
async def play(ctx, arg):
  global fr_day_word, en_day_word, game
  # Transforme all message in low charactere
  arg = arg.lower()
  # Languages
  if arg == ('fr'):
    await ctx.send(fr_day_word)
    game = 1
  elif arg == ('en'):
    await ctx.send(en_day_word)
  else:
    await ctx.send("Merci de préciser votre langue : '!play [votre langue]'.")
    await ctx.send("Langues disponibles : \n **Français :** fr \n **English :** en")

# Have rules
async def rules(ctx):
  await ctx.send('ECRIRE LES REGLES (commandes, langues, heure de changement, comment jouer)')

# Have stats
async def stats(ctx):
  await ctx.send('ECRIRE LES STATS (Premier jour, nb participant, best participant, stats player)')

# Bot Token
client.run("")