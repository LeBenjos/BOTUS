# Discord BOTUS
import nest_asyncio
import discord
from discord.ext import commands, tasks
from datetime import *
from c_player import *
from f_choice_day_word import *
from f_get_leaderboard import *
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
if datetime.today().hour <= 7:
  date_day = datetime.today().day-1
else:
  date_day = datetime.today().day
reset_hour = 7
first_day = datetime.today()
channel_id = 0
all_player = [Player(None,None,None,None)]
nb_player = 1
server_name = ""
#--------------------------------------Print when the bot is ready--------------------------------------

@client.event
async def on_ready():
    print("BOTUS is ready")

#--------------------------------------Reset the day word at 7am--------------------------------------
@tasks.loop(minutes=1)
async def reset_day_word(client):
  # Get local variables
  global fr_day_word, en_day_word, date_day, channel_id, reset_hour, all_player, server_name
  if date_day != date.today().day and datetime.today().hour >= reset_hour and channel_id != 0:
    date_day = date.today().day
    await client.get_channel(channel_id).send(f"@everyone :wave:  **Hello {server_name}, it's {date.today().day}/{date.today().month}/{date.today().year}, at {reset_hour}h! :city_sunset: \nIt's BOTUS time, good luck and have a good day!** :blush: ")
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
      await message.channel.send(f"{author} :warning: **The bot has no assigned channel where it could express itself** \n\nPlease give him a channel with : '**!channel [id_channel]**'")
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
          await message.channel.send(f"{message.author.mention} :confetti_ball: **Congratulation, you found the word of the day! You win {(6-all_player[current_player].chance)*10} points!** :partying_face: ")
        # If he try and miss
        else:
          await message.channel.send(f"{message.author.mention} :loudspeaker: **Remaining chance(s) : {(5-all_player[current_player].chance)} **")
          all_player[current_player].chance = all_player[current_player].chance + 1
          print(f"{all_player[current_player].pseudo}, remaining chance(s) : {6 - all_player[current_player].chance}")
          # If player miss 6 times
          if all_player[current_player].chance == 6:
            await message.channel.send(f"{message.author.mention} :x: **Sorry, you didn’t find the word of the day that was '{fr_day_word.upper()}'... You win {(6-all_player[current_player].chance)*10} points today...** :sob: ")
      # If len suggested word ≠ len day word
      else:
        await message.channel.send(f"{message.author.mention} :warning: **the number of characters must be equal to {len(fr_day_word)}**!")
    # If first letter isn't correct
    else:
      await message.channel.send(f"{message.author.mention} :warning: **The first letter of the word must begin with : {fr_day_word[0].upper()}**!")
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
          await message.channel.send(f"{message.author.mention} :confetti_ball: **Congratulation, you found the word of the day! You win {(6-all_player[current_player].chance)*10} points!** :partying_face: ")
        else:
          await message.channel.send(f"{message.author.mention} :loudspeaker: **Remaining chance(s) : {(5-all_player[current_player].chance)} ** ")
          all_player[current_player].chance = all_player[current_player].chance + 1
          print(f"{all_player[current_player].pseudo}, remaining chance(s) : {6 - all_player[current_player].chance}")
          if all_player[current_player].chance == 6:
            await message.channel.send(f"{message.author.mention} :x: **Sorry, you didn’t find the word of the day that was '{en_day_word.upper}'... You win {(6-all_player[current_player].chance)*10} points today...** :sob: ")
      else:
        await message.channel.send(f"{message.author.mention} :warning: **the number of characters must be equal to {len(en_day_word)}**!")
    else:
      await message.channel.send(f"{message.author.mention} :warning: **The first letter of the word must begin with : {en_day_word[0].upper()}**!")

#--------------------------------------Commands--------------------------------------

@client.command()
# Start the day game
async def play(ctx, arg):
  # Get local variables
  global fr_day_word, en_day_word, channel_id, reset_hour
  try:
    # Force people to play in private with the bot
    if ctx.channel.name:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Please write the message '**!play [your_language]**' here, in private!")
  except AttributeError:
    # If people play for the first time, he need to register
    if not get_player(ctx.author.id, all_player):
      await ctx.send(f"{ctx.author.mention} :loudspeaker: You must first register with '**!register**' before you can play!")
      return
    current_player = get_player(ctx.author.id, all_player)
    # Player start the game
    if all_player[current_player].game == 0:
      # FR
      if arg == ('fr'):
        # The player join the game
        if fr_day_word != None:
          all_player[current_player].emoji_day_word = transform_guess_word(fr_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
          await ctx.send("".join(all_player[current_player].emoji_day_word))
          all_player[current_player].game = 1
        # If the game don't have start
        else:
          await ctx.send(f"{ctx.author.mention} :loudspeaker: Don’t be impatient, you can play from **{reset_hour}h**")
      # EN
      elif arg == ('en'):
        if en_day_word != None:
          all_player[current_player].emoji_day_word = transform_guess_word(en_day_word, all_player[current_player].emoji_day_word, all_player[current_player].emoji_suggested_word)
          await ctx.send("".join(all_player[current_player].emoji_day_word))
          all_player[current_player].game = 3
        else:
          await ctx.send(f"{ctx.author.mention} :loudspeaker: Don’t be impatient, you can play from **{reset_hour}h**")
      # Other languages
      else:
        await ctx.send(f"{ctx.author.mention} :warning: Please specify your language : '**!play [your_language]**' \n\n**Available languages :** \n\n:flag_fr:  Français : **fr** \n-------------------- \n:flag_gb:  English : **en**")
    # If the player are already in the day_game
    elif all_player[current_player].game == 1 or all_player[current_player].game == 3:
      await ctx.author.send(f"{ctx.author.mention} :warning: Your part is already running...")
    # If the player has already play today
    else:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Sorry but you already played today! \n**Come back tomorrow!** :hourglass: ")

@client.command()
# Have rules
async def rules(ctx):
  global reset_hour, server_name
  await ctx.send(f"{ctx.author.mention} :pencil: **Here are the BOTUS rules :** \nEvery day on the server **{server_name}** at **{reset_hour}h** a random word is chosen.\nYou have **6 attempts** to find the word **encrypted in emoji** of which you only know the first letter! \n\n:pushpin:  **Here’s what emojis represent :** \n:blue_square:  - **Letter we don’t know** \n:yellow_circle:  - **The letter is in the word, but not in the right place** \n:red_square:  - **The letter is in the right place** \n:heavy_minus_sign:  - **a hyphen** \n:regional_indicator_a: [...] :regional_indicator_z:  - **The letter is in its exact place** \n\n:pushpin: **Here is the list of orders :** \n**!register** : In order to save yourself if you’ve never played before \n**!play [your_language]** : To start a game in the desired language \n**!leaderboard** : See the server player ranking **{server_name}** \n**!stats ** : See your statistics \n**!spy [@target]** : See statistics of the targeted player")

@client.command()
# Have stats
async def stats(ctx):
  global first_day, all_player, server_name
  current_player = get_player(ctx.author.id, all_player)
  best_player = get_best_player(all_player)
  await ctx.send(f'{ctx.author.mention} :clock2: The bot has been on the **{server_name}** since **{first_day.day}/{first_day.month}/{first_day.year}** \n:busts_in_silhouette: There are currently **{len(all_player)} players**\n:index_pointing_at_the_viewer: You have **{all_player[current_player].score} points** \n:trophy: The best player is **<@{all_player[best_player].id}>** with **{all_player[best_player].score} points**')

@client.command()
# Spy a player
async def spy(ctx, arg):
  global all_player
  try:
    target_id = get_target_id(arg)
    target = get_player(target_id, all_player)
    await ctx.send(f':disguised_face: <@{all_player[target].id}> currently has **{all_player[target].score} points**')
  except ValueError:
    await ctx.send(f'{ctx.author.mention} :warning: Be careful to use the command correctly by identifying the player : **!spy [@joueurcible]**')

@client.command()
# Get the leaderboard
async def leaderboard(ctx):
  global all_player, server_name
  if len(all_player) <= 1:
    await ctx.send(f"{ctx.author.mention} :warning: **No one is registered at the {server_name} server BOTUS**")
  else:
    server_leaderboard = get_leaderboard(all_player)
    current_leaderboard = ""
    for i in range (0,len(server_leaderboard),1):
      if i == 0:
        current_leaderboard = ":first_place: - " + "<@" + str(server_leaderboard[len(server_leaderboard)-1-i].id) + "> with **" + str(server_leaderboard[len(server_leaderboard)-1-i].score) + "points** \n"
      elif i == 1:
        current_leaderboard = current_leaderboard + ":second_place: - " + "<@" + str(server_leaderboard[len(server_leaderboard)-1-i].id) + "> with **" + str(server_leaderboard[len(server_leaderboard)-1-i].score) + "points** \n"
      elif i == 2:
        current_leaderboard = current_leaderboard + ":third_place: - " + "<@" + str(server_leaderboard[len(server_leaderboard)-1-i].id) + "> with **" + str(server_leaderboard[len(server_leaderboard)-1-i].score) + "points** \n"
      else:
        current_leaderboard = current_leaderboard + "**" + str(i+1) + " -** <@" + str(server_leaderboard[len(server_leaderboard)-1-i].id) + "> with **" + str(server_leaderboard[len(server_leaderboard)-1-i].score) + "points** \n"
    await ctx.send(f'{ctx.author.mention} :medal: **Here is the {server_name} server leaderboard :** \n{current_leaderboard}')

@client.command()
# Register
async def register(ctx):
  global nb_player, all_player, reset_hour, server_name
  try:
    if ctx.channel.name:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: Please write the message '**!register**' here, in private!")
  except AttributeError:
    if test_register_player(ctx.author.id, all_player):
      all_player.append(Player(nb_player, ctx.author.name, ctx.author.id, ctx.channel.id))
      await ctx.author.send(f":confetti_ball: **Welcome {ctx.author.mention}, you are now registered!** :partying_face: \nSo you can participate in the **daily BOTUS** organized by the **{server_name}** server! :white_check_mark: \nEvery morning at **{reset_hour}h**, you can come and write '**!play [your_langue]**'. \nIf you have any questions you can mp <@213020663894507520> on discord! See you soon! :wave: ")
      nb_player = nb_player + 1
    else:
      await ctx.author.send(f"{ctx.author.mention} :loudspeaker: You’re already registered!")

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
          await ctx.send(f"@everyone :warning: **The bot will now talk in the channel : '{client.get_channel(channel_id).name}'.** \n\nYou can change the channel at any time with the command '**!channel [id_channel]**'. \n\nYou can only start playing at the next reset at **{reset_hour}h**! \n\nMeanwhile register with '**!register**'!")
          server_name = ctx.guild.name
          # Start the loop
          reset_day_word.start(client)
        else:
          await ctx.send(f"{ctx.author.mention} :warning: **Only server administrators can use this command!**")
    # If the entered ID does not belong to any channel
    except AttributeError:
      await ctx.send(f"{ctx.author.mention} :warning: **This ID does not match any of your channels!**")
  # If the ID is not correctly written
  except ValueError:
    await ctx.send(f"{ctx.author.mention} :warning: **Please enter a valid ID!**")

# Bot Token
client.run("")