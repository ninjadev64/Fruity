import discord, os, dotenv, random, sqlite3
from discord import Color
from dislash import InteractionClient, Option, OptionType
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
from copy import deepcopy
with sqlite3.connect("jester.db") as db:
    cursor=db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Answers(
    ID text PRIMARY KEY,
    Answer text NOT NULL);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Points(
    ID text PRIMARY KEY,
    Points integer NOT NULL);""")

load_dotenv(dotenv_path=Path("token.env"))
bot = commands.Bot(command_prefix="?")
bot.remove_command('help')
guilds = [856954305214545960, 820256957369679882, 851058836776419368, 883055870496366663, 851082689699512360]
slash = InteractionClient(bot, test_guilds=guilds)
words = open("words.txt").read().splitlines()

# A template embed to use elsewhere in the bot
template_embed = discord.Embed()
template_embed.colour = Color.blue()
template_embed.set_author(name="Jester", icon_url="https://ninjadev64.github.io/Jester/avatar.webp")

@bot.event
async def on_ready():
    print('Logged in')
    await bot.change_presence(activity=discord.Game(name="a fun game"))

@slash.slash_command(description="Displays help information for this bot", guild_ids=guilds)
async def help(ctx):
    embed=deepcopy(template_embed)
    embed.add_field(name="/help", value="Display this help menu", inline=False)
    embed.add_field(name="/points [user]", value="See how many points a user has", inline=False)
    embed.add_field(name="/math", value="Do a short maths equation", inline=False)
    embed.add_field(name="/unscramble", value="Unscramble a jumbled-up word", inline=False)
    embed.add_field(name="/leaderboard", value="View the top 5 players for points", inline=False)
    embed.add_field(name="/credits", value="The people behind the bot", inline=False)
    embed.add_field(name="You can use \"?\" as an alternate prefix", value="Otherwise use Discord slash commands", inline=True)
    await ctx.send(embed=embed)

@slash.slash_command(description="Do a short maths equation", guild_ids=guilds)
async def math(ctx):
    num1 = random.randint(1,50)
    num2 = random.randint(1,50)
    operation = random.randint(0,2)
    operation_strings = [" + ", " - ", " x "]

    embed=deepcopy(template_embed)
    embed.add_field(name="Solve this", value=str(num1) + operation_strings[operation] + str(num2), inline=True)
    await ctx.send(embed=embed)
    if operation == 0: answer = num1 + num2
    if operation == 1: answer = num1 - num2
    if operation == 2: answer = num1 * num2
    cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer)
    VALUES(?,?)""", (ctx.author.id, answer))
    db.commit()

@slash.slash_command(description="Unscramble a jumbled-up word", guild_ids=guilds)
async def unscramble(ctx):
    word = words[random.randint(0,999)]
    word_list = list(word)
    random.shuffle(word_list)
    word_scrambled = ''.join(word_list)
    if word_scrambled == word:
        await unscramble(ctx)
        return
    embed=deepcopy(template_embed)
    embed.add_field(name="Unscramble this", value=word_scrambled, inline=True)
    await ctx.send(embed=embed)
    cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer)
    VALUES(?,?)""", (ctx.author.id, word))
    db.commit()

@slash.slash_command(description="See how many points a user has", guild_ids=guilds, options=[
        Option("user", "Optionally choose a user", OptionType.USER)
    ])
async def points(ctx, user=None):
    user = user or ctx.author
    cursor.execute("SELECT Points FROM Points WHERE ID = ?", (user.id,))
    points_data=cursor.fetchone()
    if points_data is None: cursor.execute("""INSERT INTO Points(ID, Points)
    VALUES(?,?)""", (user.id, 0))
    embed=deepcopy(template_embed)
    cursor.execute("SELECT Points from Points WHERE ID = ?", (user.id,))
    for x in cursor.fetchall():
        embed.add_field(name="Points", value=user.name + "#" + user.discriminator + " has " + str(x[0]) + " points.", inline=False)
        await ctx.send(embed=embed)

@slash.slash_command(description="View the top 5 players for points", guild_ids=guilds)
async def leaderboard(ctx):
    strings = []
    embed=deepcopy(template_embed)
    cursor.execute("SELECT * FROM Points ORDER BY Points DESC LIMIT 5")
    for x in cursor.fetchall():
        user = await bot.fetch_user(x[0])
        strings.append(user.name + "#" + user.discriminator + ": " + str(x[1]))
    embed.add_field(name="Leaderboard", value="\n".join(strings), inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == bot.user: return
    cursor.execute("SELECT Answer FROM Answers WHERE ID = ?", (message.author.id,))
    data=cursor.fetchone()
    if data is not None:
        embed=deepcopy(template_embed)
        cursor.execute("SELECT Points FROM Points WHERE ID = ?", (message.author.id,))
        points_data=cursor.fetchone()
        if points_data is None: cursor.execute("""INSERT INTO Points(ID, Points)
        VALUES(?,?)""", (message.author.id, 0))
        if msg == data[0]:
            embed.colour = Color.green()
            embed.add_field(name="Correct!", value=data[0] + " was the correct answer!", inline=False)
            cursor.execute("UPDATE Points SET Points = Points + 5 WHERE ID = ?", (message.author.id,))
        else:
            embed.colour = Color.red()
            embed.add_field(name="Incorrect!", value=data[0] + " was the correct answer!", inline=False)
            cursor.execute("UPDATE Points SET Points = Points - 2 WHERE ID = ?", (message.author.id,))
        await message.reply(embed=embed, mention_author=False)
        cursor.execute('DELETE FROM Answers WHERE ID=?', (message.author.id,))
        db.commit()
    await bot.process_commands(message)

@slash.slash_command(description="The people behind the bot", guild_ids=guilds)
async def credits(ctx):
    embed=deepcopy(template_embed)
    embed.add_field(name="Developer(s)", value="ninjagamer64#0861 (aka ninjadev64)", inline=False)
    embed.add_field(name="Random stuff and ideas (unofficial)", value="Blaze#2299\n Perestuken#6263", inline=False)
    await ctx.send(embed=embed)

@slash.slash_command(description="Invite the bot to your server", guild_ids=guilds)
async def invite(ctx):
    embed=deepcopy(template_embed)
    embed.set_author(name="Jester", icon_url="https://ninjadev64.github.io/Jester/avatar.webp", url="https://ninjadev64.github.io/Jester")
    embed.add_field(name="Invite the bot to your server", value="Please note that while the bot is in development you won't be able to use slash commands in your server!\n https://ninjadev64.github.io/Jester", inline=False)
    await ctx.send(embed=embed)

# Add alternate "?" prefix for slash commands
@bot.command(name="help")
async def prefixed_help(ctx): await help(ctx)
@bot.command(name="points")
async def prefixed_points(ctx): await points(ctx)
@bot.command(name="math")
async def prefixed_math(ctx): await math(ctx)
@bot.command(name="unscramble")
async def prefixed_unscramble(ctx): await unscramble(ctx)
@bot.command(name="leaderboard")
async def prefixed_leaderboard(ctx): await leaderboard(ctx)
@bot.command(name="credits")
async def prefixed_credits(ctx): await credits(ctx)

bot.run(os.getenv("TOKEN")) 
