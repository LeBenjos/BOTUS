# Discord motus bot
import nest_asyncio
import discord
from discord.ext import commands, tasks
from datetime import *
from f_choice_day_word import *
from f_remove_accent import *
from f_transform_guess_word import *
from f_transform_suggested_word import *

# Variables for discord bot
nest_asyncio.apply()
intents = discord.Intents.all()
intents.messages = True
intents.members = True
intents.typing = True
client = commands.Bot(command_prefix="!", intents=intents)

# Set local variables
# Languages
fr_day_word = None
en_day_word = None
# Variables
# SUPPR le "-1" pour éviter que le bot change de mot dès qu'il pop sur un autre serveur (si j'ajoute le cross serveur)
date_day = datetime.today().day-1
reset_hour = 7
first_day = datetime.today().day
game = 0
channel_id = 0

# Print when the bot is ready
@client.event
async def on_ready():
    print("Botjos is ready")

# Reset the day word at 7am
# SUPPR Changer la valeur de la loop pour éviter d'envoyé trop de requêtes au serveur.
@tasks.loop(minutes=1)
async def reset_day_word(client):
  # Get local variables
  global fr_day_word, en_day_word, date_day, channel_id, reset_hour
  #SUPPR
  print(fr_day_word)
  if date_day != date.today().day and datetime.today().hour >= reset_hour and channel_id != 0:
    date_day = date.today().day
    await client.get_channel(channel_id).send(f"@everyone **Hello, on est le {date.today().day}/{date.today().month}/{date.today().year}, il est {reset_hour}h! \nC'est l'heure du MOTUS, bonne chance et bonne journée!** :blush: ")
    fr_day_word = choice_day_word("fr")
    en_day_word = choice_day_word("en")
    #SUPRR
    print(fr_day_word)

# Action start when you send a message
@client.event
async def on_message(message):
  # Get local variables
  global game, channel_id

  # The bot does not interact with himself
  if message.author == client.user:
    return
  
  # Transforme all message in low charactere
  message.content = message.content.lower()

  if message.content.startswith('!'):
    # Force to give a channel to the bot
    if channel_id == 0 and not message.content.startswith('!channel'):
      author = message.author.mention
      await message.channel.send(f"{author} :warning: **Le bot n'a pas de channel attribué où il pourrait s'exprimer** \n\nMerci de lui attribuer un channel avec : '**!channel [id_channel]**'")
      return
    # Allow all commands when the bot has a channel
    else:
      await client.process_commands(message)
      return

  # GAME
  if game == 1:
    pass

# Commands
@client.command()
# Start the day game
async def play(ctx, arg):
  # Get local variables
  global fr_day_word, en_day_word, game, channel_id
  
  # Languages
  if arg == ('fr'):
    await ctx.send(fr_day_word)
    game = 1
  elif arg == ('en'):
    await ctx.send(en_day_word)
    game = 1
  else:
    author = ctx.author.mention
    await ctx.send(f"{author} :warning: Merci de préciser votre langue : '**!play [votre langue]**' \n\n**Langues disponibles :** \n\n:flag_fr:  Français : **fr** \n-------------------- \n:flag_gb:  English : **en**")

@client.command()
# Have rules
async def rules(ctx):
  await ctx.send('ECRIRE LES REGLES (commandes, langues, heure de changement, comment jouer)')

@client.command()
# Have stats
async def stats(ctx):
  await ctx.send('ECRIRE LES STATS (Premier jour, nb participant, best participant, stats player)')

@client.command()
# Channel ID
async def channel(ctx, arg):
  global channel_id, reset_hour
  # Check if the ID is correctly written (without strings)
  try:
    channel_id = int(arg)
    # Check if the channel id is correct
    try: 
      if client.get_channel(channel_id).name:
        await ctx.send(f"@everyone :warning: **Le bot va maintenant parler dans le channel : '{client.get_channel(channel_id).name}'.** \n\nVous pouvez modifier le channel a tout moment avec la commande '**!channel [id_channel]**'. \n\nVous ne pourrez commencer à jouer qu'au prochain reset à {reset_hour}h du matin!")
        # Start the loop
        reset_day_word.start(client)
    # If the entered ID does not belong to any channel
    except AttributeError:
      author = ctx.author.mention
      await ctx.send(f"{author} :warning: **Cet ID ne correspond à aucun de vos channels!**")
  # If the ID is not correctly written
  except ValueError:
    author = ctx.author.mention
    await ctx.send(f"{author} :warning: **Merci de de rentrer un ID valide!**")
  

# Bot Token
client.run("")