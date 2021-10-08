# Import required modules
import os
import random
import sqlite3
from copy import deepcopy
from pathlib import Path

import discord
import dotenv
import requests
from discord.ext import commands
from discord.utils import get
from dislash import (InteractionClient, Option, OptionChoice,
                     OptionType, SelectMenu, SelectOption, ContextMenuInteraction)

# Set up database
with sqlite3.connect("fruity.db") as db:
    cursor=db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Answers(
    ID text PRIMARY KEY,
    Answer text NOT NULL,
    Channel text NOT NULL);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Points(
    ID text PRIMARY KEY,
    Points integer NOT NULL);""")

dotenv.load_dotenv(dotenv_path=Path("tokens.env"))
bot = commands.Bot(command_prefix="?", status=discord.Status.idle)
bot.remove_command('help')
guilds = [856954305214545960, 851058836776419368, 883055870496366663, 851082689699512360, 837212681198108692, 874266744456376370, 832948547610607636, 862792174847655977]
slash = InteractionClient(bot, test_guilds=guilds)
words = open("words.txt").read().splitlines()
sra = "https://some-random-api.ml/"

# A template embed to use elsewhere in the bot
template_embed = discord.Embed()
template_embed.colour = discord.Color.blue()

# An extension of the template embed to use in all help command embeds
template_help_embed=deepcopy(template_embed)
template_help_embed.set_footer(text="You can use \"?\" as an alternate\nprefix for some commands")

# Set bot presence and print a list of guild names 
@bot.event
async def on_ready():
    for guild in bot.guilds: print(guild.name)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help | " + str(len(bot.guilds)) + " guilds"))

# React to select menu changes
@bot.event
async def on_dropdown(ctx):
    if ctx.component.custom_id == "help":
        if ctx.select_menu.selected_options[0].value == "fun":
            await ctx.respond(type=7, embed=HelpEmbeds.getFunEmbed(), components = HelpComponents.fun)
        if ctx.select_menu.selected_options[0].value == "minigames":
            await ctx.respond(type=7, embed=HelpEmbeds.getMinigamesEmbed(), components = HelpComponents.minigames)
        if ctx.select_menu.selected_options[0].value == "points":
            await ctx.respond(type=7, embed=HelpEmbeds.getPointsEmbed(), components = HelpComponents.points)
        if ctx.select_menu.selected_options[0].value == "other":
            await ctx.respond(type=7, embed=HelpEmbeds.getOtherEmbed(), components = HelpComponents.other)

# A class for static methods and fields related to help embeds for global usage
class HelpEmbeds:
    @staticmethod
    def getFunEmbed():
        embed = deepcopy(template_help_embed)
        embed.add_field(name="/animal [animal]", value="Get an animal fact and cute image", inline=False)
        embed.add_field(name="/joke", value="Random joke generator", inline=False)
        embed.add_field(name="/echo [input]", value="Echo your input", inline=False)
        return embed

    @staticmethod
    def getMinigamesEmbed():
        embed = deepcopy(template_help_embed)
        embed.add_field(name="/math", value="Do a short maths equation", inline=False)
        embed.add_field(name="/unscramble", value="Unscramble a jumbled-up word", inline=False)
        embed.add_field(name="/coinflip [side]", value="Flip a coin", inline=False)
        return embed

    @staticmethod
    def getPointsEmbed():
        embed = deepcopy(template_help_embed)
        embed.add_field(name="/points [user]", value="See how many points a user has", inline=False)
        embed.add_field(name="/leaderboard", value="View the top 5 players for points", inline=False)
        return embed

    @staticmethod
    def getOtherEmbed():
        embed = deepcopy(template_help_embed)
        embed.add_field(name="/credits", value="The people behind the bot", inline=False)
        embed.add_field(name="/invite", value="Invite the bot to your server", inline=False)
        embed.add_field(name="/ping", value="Ping? Pong!", inline=False)
        return embed

# A class for static methods and fields related to help select menu components for global usage
class HelpComponents():
    custom_id="help"
    placeholder="Category"
    max_values=1
    fun = [SelectMenu(custom_id=custom_id, placeholder=placeholder, max_values=max_values,
                options=[
                    SelectOption("Fun", "fun", default=True),
                    SelectOption("Minigames", "minigames"),
                    SelectOption("Points", "points"),
                    SelectOption("Other", "other")
    ])]
    minigames = [SelectMenu(custom_id=custom_id, placeholder=placeholder, max_values=max_values,
                options=[
                    SelectOption("Fun", "fun"),
                    SelectOption("Minigames", "minigames", default=True),
                    SelectOption("Points", "points"),
                    SelectOption("Other", "other")
    ])]
    points = [SelectMenu(custom_id=custom_id, placeholder=placeholder, max_values=max_values,
                options=[
                    SelectOption("Fun", "fun"),
                    SelectOption("Minigames", "minigames"),
                    SelectOption("Points", "points", default=True),
                    SelectOption("Other", "other")
    ])]
    other = [SelectMenu(custom_id=custom_id, placeholder=placeholder, max_values=max_values,
                options=[
                    SelectOption("Fun", "fun"),
                    SelectOption("Minigames", "minigames"),
                    SelectOption("Points", "points"),
                    SelectOption("Other", "other", default=True)
    ])]

@slash.slash_command(description="Displays help information for this bot", options=[
        Option("category", "Category", OptionType.STRING, False, [
            OptionChoice("Fun", "fun"),
            OptionChoice("Minigames", "minigames"),
            OptionChoice("Points", "points"),
            OptionChoice("Other", "other")
        ])
])
async def help(ctx, category="fun"):
    if category == "fun":
        await ctx.send(embed=HelpEmbeds.getFunEmbed(), components = HelpComponents.fun)
    if category == "minigames":
        await ctx.send(embed=HelpEmbeds.getMinigamesEmbed(), components = HelpComponents.minigames)
    if category == "points":
        await ctx.send(embed=HelpEmbeds.getPointsEmbed(), components = HelpComponents.points)
    if category == "other":
        await ctx.send(embed=HelpEmbeds.getOtherEmbed(), components = HelpComponents.other)

@slash.slash_command(description="Do a short maths equation")
async def math(ctx):
    num1 = random.randint(1,50)
    num2 = random.randint(1,50)
    operation = random.randint(0, 1)
    operation_strings = [" + ", " - "]

    embed = deepcopy(template_embed)
    embed.add_field(name="Solve this", value=str(num1) + operation_strings[operation] + str(num2), inline=True)
    await ctx.send(embed=embed)
    if operation == 0: answer = num1 + num2
    if operation == 1: answer = num1 - num2
    cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer, Channel)
    VALUES(?,?,?)""", (ctx.author.id, answer, ctx.channel.id))
    db.commit()

@slash.slash_command(description="Unscramble a jumbled-up word")
async def unscramble(ctx):
    word = words[random.randint(0,999)]
    word_list = list(word)
    random.shuffle(word_list)
    word_scrambled = ''.join(word_list)
    if word_scrambled == word:
        await unscramble(ctx)
        return
    embed = deepcopy(template_embed)
    embed.add_field(name="Unscramble this", value=word_scrambled, inline=True)
    await ctx.send(embed=embed)
    cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer, Channel)
    VALUES(?,?,?)""", (ctx.author.id, word, ctx.channel.id))
    db.commit()

@slash.slash_command(description="Flip a coin", options=[
        Option("side", "Side", OptionType.STRING, True, [OptionChoice("heads", "heads"), OptionChoice("tails", "tails")])
])
async def coinflip(ctx, side=None):
    embed = deepcopy(template_embed)
    flipped_side = random.choice(["heads", "tails"])
    if flipped_side == side:
        embed.colour = discord.Color.green()
        embed.add_field(name="You win!", value="The coin landed " + flipped_side + " side up.")
        cursor.execute("UPDATE Points SET Points = Points + 5 WHERE ID = ?", (ctx.author.id,))
    else:
        embed.colour = discord.Color.red()
        embed.add_field(name="You lose!", value="The coin landed " + flipped_side + " side up.")
        cursor.execute("UPDATE Points SET Points = Points - 2 WHERE ID = ?", (ctx.author.id,))
    await ctx.send(embed=embed)

@slash.slash_command(description="See how many points a user has", options=[
        Option("user", "User", OptionType.USER)
])
async def points(ctx, user=None):
    user = user or ctx.author
    cursor.execute("SELECT Points FROM Points WHERE ID = ?", (user.id,))
    points_data = cursor.fetchone()
    if points_data is None: cursor.execute("""INSERT INTO Points(ID, Points)
    VALUES(?,?)""", (user.id, 0))
    embed = deepcopy(template_embed)
    cursor.execute("SELECT Points from Points WHERE ID = ?", (user.id,))
    for x in cursor.fetchall():
        embed.add_field(name="Points", value=user.name + "#" + user.discriminator + " has " + str(x[0]) + " points.", inline=False)
        await ctx.send(embed=embed)

@slash.slash_command(description="View the top 5 players for points")
async def leaderboard(ctx):
    strings = []
    embed = deepcopy(template_embed)
    cursor.execute("SELECT * FROM Points ORDER BY Points DESC LIMIT 5")
    place = 1
    for x in cursor.fetchall():
        user = await bot.fetch_user(x[0])
        strings.append(str(place)+". " + user.name + "#" + user.discriminator + ": " + str(x[1]))
        place = place + 1
    embed.add_field(name="Leaderboard", value="\n".join(strings), inline=False)
    await ctx.send(embed=embed)

@slash.slash_command(description="Get an animal fact and cute image", options=[
        Option("animal", "Animal", OptionType.STRING, True, [OptionChoice("dog", "dog"), OptionChoice("cat", "cat"), OptionChoice("panda", "panda"), OptionChoice("fox", "fox"), OptionChoice("koala", "koala"), OptionChoice("bird", "bird")])
])
async def animal(ctx, animal=None):
    embed = deepcopy(template_embed)
    embed.add_field(name=animal.capitalize(), value=requests.get(sra + "facts/" + animal).json().get("fact"))
    embed.set_image(url=requests.get(sra + "img/" + animal).json().get("link"))
    embed.set_footer(text="Powered by Some Random API", icon_url="https://i.some-random-api.ml/logo.png")
    await ctx.send(embed=embed)

@slash.slash_command(description="Random joke generator")
async def joke(ctx):
    embed = deepcopy(template_embed)
    json = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode").json()
    if json.get("type") == "single": embed.add_field(name="Joke", value=json.get("joke"), inline=False)
    if json.get("type") == "twopart":
        embed.add_field(name="Setup", value=json.get("setup"), inline=False)
        embed.add_field(name="Delivery", value=json.get("delivery"), inline=False)
    embed.set_footer(text="Powered by JokeAPI", icon_url="https://raw.githubusercontent.com/Sv443/JokeAPI/master/docs/static/icon_1000x1000.png")
    await ctx.send(embed=embed)

@slash.slash_command(description="Get a song's lyrics", options=[
        Option("song", "Song", OptionType.STRING, True)
])
async def lyrics(ctx, song=""):
    json = requests.get(sra + "lyrics?title=" + song).json()
    embed = deepcopy(template_embed)
    embed.set_footer(text="Powered by Some Random API", icon_url="https://i.some-random-api.ml/logo.png")
    if json.get("error") is not None:
        embed.add_field(name="Error", value=json.get("error"), inline=False)
        await ctx.send(embed=embed, ephemeral=True)
        return False
    else:
        embed.set_thumbnail(url=json.get("thumbnail")[next(iter(json.get("thumbnail")))])
        embed.add_field(name=json.get("title"), value="by " + json.get("author"), inline=False)
        lyrics = json.get("lyrics")
        lyrics = (lyrics[:1021] + '...') if len(lyrics) > 1021 else lyrics
        embed.add_field(name="Song lyrics", value=lyrics, inline=False)
    await ctx.send("Full lyrics: <" + json.get("links")[next(iter(json.get("links")))] + ">", embed=embed)

@slash.slash_command(description="Echo your input", options=[
        Option("input", "Input", OptionType.STRING, True)
])
async def echo(ctx, input=""):
    await ctx.send(input, ephemeral=True)

@bot.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == bot.user: return
    
    # React to message if it mentions the bot
    if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
        await message.add_reaction(get(bot.get_guild(874266744456376370).emojis, name='FruityMentionReaction'))

    # Handle answer marking
    cursor.execute("SELECT Answer FROM Answers WHERE ID = ?", (message.author.id,))
    stored_answer = cursor.fetchone()
    cursor.execute("SELECT Channel FROM Answers WHERE ID = ?", (message.author.id,))
    channel_id = cursor.fetchone()
    if stored_answer is not None:
        if not channel_id[0] == str(message.channel.id): return
        embed = deepcopy(template_embed)
        cursor.execute("SELECT Points FROM Points WHERE ID = ?", (message.author.id,))
        stored_points = cursor.fetchone()
        if stored_points is None: cursor.execute("""INSERT INTO Points(ID, Points)
        VALUES(?,?)""", (message.author.id, 0))
        if msg == stored_answer[0]:
            embed.colour = discord.Color.green()
            embed.add_field(name="Correct!", value=stored_answer[0] + " was the correct answer!", inline=False)
            embed.set_footer(text="(+5 points)")
            cursor.execute("UPDATE Points SET Points = Points + 5 WHERE ID = ?", (message.author.id,))
        else:
            embed.colour = discord.Color.red()
            embed.add_field(name="Incorrect!", value=stored_answer[0] + " was the correct answer!", inline=False)
            embed.set_footer(text="(-2 points)")
            cursor.execute("UPDATE Points SET Points = Points - 2 WHERE ID = ?", (message.author.id,))
        await message.reply(embed=embed, mention_author=False)
        cursor.execute('DELETE FROM Answers WHERE ID=?', (message.author.id,))
        db.commit()

    # Process alternate prefix commands
    if msg.startswith("?"):
        msg = msg.lstrip("?")
        commands = ["help", "math", "unscramble", "joke", "points", "leaderboard", "credits", "invite", "ping"]
        if msg in commands: await bot.process_commands(message)

@slash.slash_command(description="The people behind the bot")
async def credits(ctx):
    embed = deepcopy(template_embed)
    embed.add_field(name="Developer(s)", value="ninjagamer64#0861 (aka ninjadev64)", inline=False)
    embed.add_field(name="Random stuff and ideas (unofficial)", value="Blaze#2299\nPerestuken#8688 / Perestuken#6263", inline=False)
    await ctx.send(embed=embed)

@slash.slash_command(description="Invite the bot to your server")
async def invite(ctx):
    embed = deepcopy(template_embed)
    embed.add_field(name="Invite the bot to your server", value="Please note that while the bot is in development you won't be able to use slash commands in your server!\nhttps://ninjadev64.github.io/Fruity/", inline=False)
    await ctx.send(embed=embed)

@slash.slash_command(description="Ping? Pong!")
async def ping(ctx):
    embed = deepcopy(template_embed)
    embed.add_field(name="Ping? Pong!", value=str(round(bot.latency * 1000)) + "ms", inline=False)
    await ctx.send(embed=embed)

# Add alternate "?" prefix for slash commands
@bot.command(name="help")
async def prefixed_help(ctx): await help(ctx)
@bot.command(name="math")
async def prefixed_math(ctx): await math(ctx)
@bot.command(name="unscramble")
async def prefixed_unscramble(ctx): await unscramble(ctx)
@bot.command(name="joke")
async def prefixed_joke(ctx): await joke(ctx)
@bot.command(name="points")
async def prefixed_points(ctx): await points(ctx)
@bot.command(name="leaderboard")
async def prefixed_leaderboard(ctx): await leaderboard(ctx)
@bot.command(name="credits")
async def prefixed_credits(ctx): await credits(ctx)
@bot.command(name="invite")
async def prefixed_invite(ctx): await invite(ctx)
@bot.command(name="ping")
async def prefixed_ping(ctx): await ping(ctx)

@slash.user_command(name="fruity points")
async def context_points(ctx): await points(ctx, ctx.user)

# CitrusDev server only
@slash.slash_command(description="Suggest anything for any CitrusDev project", guild_ids=[874266744456376370], options=[
        Option("project", "Project", OptionType.STRING, True, [OptionChoice("Fruity", "Fruity"), OptionChoice("CitrusFFA", "CitrusFFA")]),
        Option("suggestion", "Suggestion", OptionType.STRING, True)
])
async def suggest(ctx, project=None, suggestion=None):
    embed = deepcopy(template_embed)
    embed.set_author(name="Suggestion")
    embed.add_field(name=project, value=suggestion, inline=False)
    embed.set_footer(text=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.avatar_url)
    message = await bot.get_channel(889086565287079946).send(embed=embed)
    await message.add_reaction(get(bot.get_guild(837212681198108692).emojis, name='Completed'))
    await message.add_reaction(get(bot.get_guild(837212681198108692).emojis, name='Cancelled'))

# Run the bot
bot.run(os.getenv("TOKEN")) 
