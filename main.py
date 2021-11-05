from cogs.help import Help
from cogs.fun import Fun
from cogs.minigames import Minigames
from cogs.points import Points
from cogs.other import Other

# Import required modules
import os
import sqlite3
from copy import deepcopy
from pathlib import Path

import discord
import dotenv
import topgg
from discord.utils import get
from discord.ext import commands
from dislash import InteractionClient
from datetime import datetime

# Set up database
with sqlite3.connect("fruity.db") as db: cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Answers(
	ID text PRIMARY KEY,
	Answer text NOT NULL,
	Channel text NOT NULL);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Points(
	ID text PRIMARY KEY,
	Points integer NOT NULL);""")

dotenv.load_dotenv(dotenv_path = Path("tokens.env"))
bot = commands.Bot(command_prefix = "?", status = discord.Status.idle)
bot.remove_command("help")

bot.topggpy = topgg.DBLClient(bot, os.getenv("TOPGGTOKEN"), autopost = True)
bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/webhook", os.getenv("TOPGGPASSWORD"))
bot.topgg_webhook.run(5000)

if os.getenv("GUILDS") == "ALL": slash = InteractionClient(bot)
else:
	guilds = []
	for id in os.getenv("GUILDS").split(", "): guilds.append(int(id))
	slash = InteractionClient(bot, test_guilds = guilds)

# A template embed to use elsewhere in the bot
template_embed = discord.Embed()
template_embed.colour = discord.Color.blue()

bot.add_cog(Help(bot, template_embed))
bot.add_cog(Fun(bot, template_embed))
bot.add_cog(Minigames(bot, template_embed, db, cursor))
bot.add_cog(Points(bot, template_embed, db, cursor))
bot.add_cog(Other(bot, template_embed))

# Set bot presence and print a list of guild names 
@bot.event
async def on_ready():
	for guild in bot.guilds: print(guild.name)
	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "/help | " + str(len(bot.guilds)) + " guilds"))

# Log commands to log.txt
@bot.event
async def on_slash_command(ctx):
	file = open("log.txt", "a")
	file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + ctx.author.name + " issued command /" + ctx.data.name + "\n")
	file.close()

# Reward users when they vote on top.gg
@bot.event
async def on_dbl_vote(data):
	user = await bot.fetch_user(data.get("user"))
	embed = deepcopy(template_embed)
	embed.add_field(name = "Vote success", value = """You successfully voted on top.gg!
	[Vote again tomorrow](https://top.gg/bot/851508305573445703/vote)""")
	embed.set_footer(text = "(+20 points)")
	await user.send(embed = embed)
	cursor.execute("SELECT Points FROM Points WHERE ID = ?", (user.id,))
	if cursor.fetchone() is None: cursor.execute("""INSERT INTO Points(ID, Points)
	VALUES(?,?)""", (user.id, 0))
	cursor.execute("UPDATE Points SET Points = Points + 20 WHERE ID = ?", (user.id,))
	db.commit()

@bot.event
async def on_message(message):
	msg = message.content.lower()
	if message.author == bot.user: return
	
	# React to message if it mentions the bot
	if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
		await message.add_reaction(get(bot.get_guild(874266744456376370).emojis, name = 'FruityMentionReaction'))

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
			embed.add_field(name = "Correct!", value = stored_answer[0] + " was the correct answer!", inline = False)
			embed.set_footer(text = "(+5 points)")
			cursor.execute("UPDATE Points SET Points = Points + 5 WHERE ID = ?", (message.author.id,))
		else:
			embed.colour = discord.Color.red()
			embed.add_field(name = "Incorrect!", value = stored_answer[0] + " was the correct answer!", inline = False)
			embed.set_footer(text = "(-2 points)")
			cursor.execute("UPDATE Points SET Points = Points - 2 WHERE ID = ?", (message.author.id,))
		await message.reply(embed=embed, mention_author=False)
		cursor.execute('DELETE FROM Answers WHERE ID=?', (message.author.id,))
		db.commit()

# Run the bot
bot.run(os.getenv("TOKEN")) 