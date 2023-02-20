# Discord BOTUS
import nest_asyncio
import discord
from discord.ext import commands, tasks
from datetime import *
from c_player import *
from f_choice_day_word import *
from f_get_player import *
from f_remove_accent import *
from f_test_register_player import *
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
if datetime.today().hour < 7:
  date_day = datetime.today().day-1
else:
  date_day = datetime.today().day-1
reset_hour = 7
first_day = datetime.today()
channel_id = 0
all_player = [Player(0,None,0,0)]
nb_player = 0
server_name = ""

#--------------------------------------Print when the bot is ready--------------------------------------

@client.event
async def on_ready():
    print("BOTUS is ready")

#--------------------------------------Reset the day word at 7am--------------------------------------

@tasks.loop(minutes=1)
async def reset_day_word(client):
  # Get local variables
  global fr_day_word, en_day_word, date_day, channel_id, reset_hour, all_player
  if date_day != date.today().day and datetime.today().hour >= reset_hour and channel_id != 0:
    date_day = date.today().day
    await client.get_channel(channel_id).send(f"@everyone **Hello, on est le {date.today().day}/{date.today().month}/{date.today().year}, il est {reset_hour}h! \nC'est l'heure du BOTUS, bonne chance et bonne journée!** :blush: ")
    fr_day_word = remove_accents(choice_day_word("fr"))
    en_day_word = remove_accents(choice_day_word("en"))
    # Reset all player variables
    for i in range (0,len(all_player),1):
      all_player[i].game = 0
      all_player[i].chance = 0
      all_player[i].suggested_word = None
      all_player[i].emoji_day_word = None
      all_player[i].emoji_suggested_word = None
    print(f"FR : {fr_day_word}, EN : {en_day_word}")

#--------------------------------------Action start when you send a message--------------------------------------

@client.event
async def on_message(message):
  # Get local variables
  global channel_id, fr_day_word, en_day_word, all_player

  # The bot does not interact with himself
  if message.author == client.user:
    return
  
  # Transforme all message in low charactere
  message.content = remove_accents(message.content.lower())

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
  
  # The game
  current_player = get_player(message.author.id, all_player)
  # FR
  if all_player[current_player].game == 1 and all_player[current_player].chance < 6 and message.channel.id == all_player[current_player].id_bot_private_channel:
    # Check if first letter is correct
    if message.content[0] == fr_day_word[0]:
      # Check if len suggested word == len day word
      if len(message.content) == len(fr_day_word):
        # Translate suggested word in emoji
        all_player[current_player].emoji_suggested_word = transform_suggested_word(fr_day_word, message.content)
        await message.channel.send("".join(all_player[current_player].emoji_suggested_word))
        # Translate day word in emoji
        all_player[current_player].emoji_day_word = transform_guess_word(fr_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
        await message.channel.send("".join(all_player[current_player].emoji_day_word))
        # If player find the day word
        if message.content == fr_day_word:
          all_player[current_player].game = 2
          all_player[current_player].score = all_player[current_player].score + ((6-all_player[current_player].chance)*10)
          await message.channel.send(f"{message.author.mention} :confetti_ball: **Bravo, vous avez trouvé le mot du jour! Vous gagnez {(6-all_player[current_player].chance)*10} points!** :partying_face: ")
        # If he try and miss
        else:
          await message.channel.send(f"{message.author.mention} :loudspeaker: **Chance restantes : {(5-all_player[current_player].chance)} **")
          all_player[current_player].chance = all_player[current_player].chance + 1
          print(f"{all_player[current_player].pseudo}, chance restante : {6 - all_player[current_player].chance}")
          # If player miss 6 times
          if all_player[current_player].chance == 6:
            await message.channel.send(f"{message.author.mention} :x: **Désolé, vous n'avez pas trouvé le mot du jour qui était '{fr_day_word.upper()}'... Vous avez {(6-all_player[current_player].chance)*10} points aujourd'hui..** :sob: ")
      # If len suggested word ≠ len day word
      else:
        await message.channel.send(f"{message.author.mention} :warning: **le nombre de caractères doit-être égal à {len(fr_day_word)}**!")
    # If first letter isn't correct
    else:
      await message.channel.send(f"{message.author.mention} :warning: **La première lettre du mot doit commencer par un {fr_day_word[0].upper()}**!")
  # EN
  if all_player[current_player].game == 3 and all_player[current_player].chance < 6 and message.channel.id == all_player[current_player].id_bot_private_channel:
    if message.content[0] == en_day_word[0]:
      if len(message.content) == len(en_day_word):
        all_player[current_player].emoji_suggested_word = transform_suggested_word(en_day_word, message.content)
        await message.channel.send("".join(all_player[current_player].emoji_suggested_word))
        all_player[current_player].emoji_day_word = transform_guess_word(en_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
        await message.channel.send("".join(all_player[current_player].emoji_day_word))
        if message.content == en_day_word:
          all_player[current_player].game = 2
          all_player[current_player].score = all_player[current_player].score + ((6-all_player[current_player].chance)*10)
          await message.channel.send(f"{message.author.mention} :confetti_ball: **Bravo, vous avez trouvé le mot du jour! Vous gagnez {(6-all_player[current_player].chance)*10} points!** :partying_face: ")
        else:
          await message.channel.send(f"{message.author.mention} :loudspeaker: **Chance restantes : {(5-all_player[current_player].chance)} ** ")
          all_player[current_player].chance = all_player[current_player].chance + 1
          print(f"{all_player[current_player].pseudo}, chance restante : {6 - all_player[current_player].chance}")
          if all_player[current_player].chance == 6:
            await message.channel.send(f"{message.author.mention} :x: **Désolé, vous n'avez pas trouvé le mot du jour qui était '{en_day_word.upper}'... Vous avez {(6-all_player[current_player].chance)*10} points aujourd'hui..** :sob: ")
      else:
        await message.channel.send(f"{message.author.mention} :warning: **le nombre de caractères doit-être égal à {len(en_day_word)}**!")
    else:
      await message.channel.send(f"{message.author.mention} :warning: **La première lettre du mot doit commencer par un {en_day_word[0].upper()}**!")

#--------------------------------------Commands--------------------------------------

@client.command()
# Start the day game
async def play(ctx, arg):
  # Get local variables
  global fr_day_word, en_day_word, channel_id, reset_hour
  try:
    # Force people to play in private with the bot
    if ctx.channel.name:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Merci de faire la commande '**!play [votre langue]**' ici, par message privé!")
  except AttributeError:
    # If people play for the first time, he need to register
    if not get_player(ctx.author.id, all_player):
      await ctx.send(f"{ctx.author.mention} :loudspeaker: Tu dois d'abord t'enregistrer avec la commande '**!register**' avant de pouvoir jouer!")
      return
    current_player = get_player(ctx.author.id, all_player)
    # Player start the game
    if all_player[current_player].game == 0:
      # FR
      if arg == ('fr'):
        # If the game is running the player join the game
        if fr_day_word != None:
          all_player[current_player].emoji_day_word = transform_guess_word(fr_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
          await ctx.send("".join(all_player[current_player].emoji_day_word))
          all_player[current_player].game = 1
        # If the game don't have start
        else:
          await ctx.send(f"{ctx.author.mention} :loudspeaker: Ne soyez pas impatient, vous pourrez jouer à partir de **{reset_hour}h du matin**")
      # EN
      elif arg == ('en'):
        if en_day_word != None:
          all_player[current_player].emoji_day_word = transform_guess_word(en_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
          await ctx.send("".join(all_player[current_player].emoji_day_word))
          all_player[current_player].game = 3
        else:
          await ctx.send(f"{ctx.author.mention} :loudspeaker: Ne soyez pas impatient, vous pourrez jouer à partir de **{reset_hour}h du matin**")
      # Other languages
      else:
        await ctx.send(f"{ctx.author.mention} :warning: Merci de préciser votre langue : '**!play [votre langue]**' \n\n**Langues disponibles :** \n\n:flag_fr:  Français : **fr** \n-------------------- \n:flag_gb:  English : **en**")
    # If the player are already in the day_game
    elif all_player[current_player].game == 1 or all_player[current_player].game == 3:
      await ctx.author.send(f"{ctx.author.mention} :warning: Votre partie est déjà en cours...")
    # If the player has already play today
    else:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Désolé mais vous avez déjà joué aujourd'hui! \n**Revenez demain!** :hourglass: ")

@client.command()
# Have rules
async def rules(ctx):
  global reset_hour
  await ctx.send(f"{ctx.author.mention} :pencil: **Voici les règles du BOTUS :** \nChaque jour à **{reset_hour} du matin** un mot aléatoire est choisi.\nVous avez **6 essais** pour trouver le mot **crypté en émoji** dont vous ne connaissez que la première lettre! \n\n:pushpin:  **Voici ce que représente les emojis :** \n:blue_square:  - **Lettre qu'on ne connait pas** \n:yellow_circle:  - **La lettre est dans le mot, mais pas au bon endroit** \n:red_square:  - **La lettre est placé au bon endroit** \n:heavy_minus_sign:  - **Un trait d'union** \n:regional_indicator_a: [...] :regional_indicator_z:  - **La lettre est à son endroit précis** \n\n:pushpin: **Voici la liste des commandes :** \n**!register** : Afin de vous enregistez si vous n'avez jamais joué avant \n**!play [langage]** : Afin de commencer une partie dans la langue souhaitée \n**!players** : Voir tous les participants \n**!stats ** : Voir vos statistiques \n**!spy [@joueurcible]** : Voir les statistiques du joueur ciblé")

@client.command()
# Have stats
async def stats(ctx):
  global first_day, all_player
  current_player = get_player(ctx.author.id, all_player)
  best_player = get_best_player(all_player)
  await ctx.send(f'{ctx.author.mention} :clock2: Le bot est sur le serveur depuis le **{first_day.day}/{first_day.month}/{first_day.year}** \n:busts_in_silhouette: Il y a actuellement **{len(all_player)-1} joueurs**\n:index_pointing_at_the_viewer: Vous avez **{all_player[current_player].score} points** \n:trophy: Le meilleur joueur est **<@{all_player[best_player].id}>** avec **{all_player[best_player].score} points**')

@client.command()
# Spy a player
async def spy(ctx, arg):
  global all_player
  try:
    target_id = get_target_id(arg)
    target = get_player(target_id, all_player)
    await ctx.send(f':disguised_face: <@{all_player[target].id}> a actuellement **{all_player[target].score} points**')
  except ValueError:
    await ctx.send(f'{ctx.author.mention} :warning: Attention à bien utiliser la commande en identifiant le joueur : **!spy [@joueurcible]**')


@client.command()
# Register
async def register(ctx):
  global nb_player, all_player, reset_hour, server_name
  try:
    if ctx.channel.name:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Merci de faire la commande '**!register**' ici, par message privé!")
  except AttributeError:
    if test_register_player(ctx.author.id, all_player):
      nb_player = nb_player + 1
      all_player.append(Player(nb_player, ctx.author.name, ctx.author.id, ctx.channel.id))
      await ctx.author.send(f":confetti_ball: **Bienvenue {ctx.author.mention}, tu es maintenant inscrit!** :partying_face: \nTu peux donc participer au **BOTUS quotidiens** organiser par le serveur **{server_name}**! :white_check_mark: \nTout les matins à **{reset_hour}h**, tu peux venir et écrire '**!play [ta langue]**'. \nSi tu as des question tu peux mp <@213020663894507520> sur discord! À bientôt! :wave: ")
    else:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Tu es déjà enregistré!")

@client.command()
# temporaire pour voir le nombre d'inscrit
async def players(ctx):
  global nb_player, all_player
  player = ""
  for i in range(1, len(all_player),1):
    if i < len(all_player)-1:
      player = player + "<@" + str(all_player[i].id) + ">" + ", "
    else:
      player = player + "<@" + str(all_player[i].id) + ">"
  await ctx.send(f"{ctx.author.mention} :busts_in_silhouette: **Voici les {len(all_player)-1} participants :** {player}")

@client.command()
# Channel ID
async def channel(ctx, arg):
  global channel_id, reset_hour, server_name
  # Check if the ID is correctly written (without strings)
  try:
    channel_id = int(arg)
    # Check if the channel id is correct
    try: 
      if client.get_channel(channel_id).name:
        if ctx.author.guild_permissions.administrator:
          await ctx.send(f"@everyone :warning: **Le bot va maintenant parler dans le channel : '{client.get_channel(channel_id).name}'.** \n\nVous pouvez modifier le channel a tout moment avec la commande '**!channel [id_channel]**'. \n\nVous ne pourrez commencer à jouer qu'au prochain reset à **{reset_hour}h du matin**! \n\nEn attendant inscrivez-vous avec '**!register**'!")
          server_name = ctx.guild.name
          # Start the loop
          reset_day_word.start(client)
        else:
          await ctx.send(f"{ctx.author.mention} :warning: **Seul les administrateurs du serveur peuvent utiliser cette commande!**")
    # If the entered ID does not belong to any channel
    except AttributeError:
      await ctx.send(f"{ctx.author.mention} :warning: **Cet ID ne correspond à aucun de vos channels!**")
  # If the ID is not correctly written
  except ValueError:
    await ctx.send(f"{ctx.author.mention} :warning: **Merci de de rentrer un ID valide!**")

# Bot Token
client.run("")