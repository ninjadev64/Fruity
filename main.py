from cogs.fun import Fun
from cogs.minigames import Minigames, answers, channels
from cogs.points import Points
from cogs.other import Other
from cogs.help import Help

# Import required modules
import os
from copy import deepcopy
from pathlib import Path

import discord
import dotenv
from discord.utils import get
from discord.ext import commands, tasks
from aiohttp import ClientSession
from datetime import datetime

import firebase_admin
from firebase_admin import firestore
firebase_admin.initialize_app(firebase_admin.credentials.Certificate("firebaseKey.json"))
db = firestore.client()
users_ref = db.collection("Users")

class Bot(commands.Bot):
	async def setup_hook(self) -> None:
		session = ClientSession()
		await self.add_cog(Fun(self, template_embed, session))
		await self.add_cog(Minigames(self, template_embed, db, users_ref))
		await self.add_cog(Points(self, template_embed, db, users_ref))
		await self.add_cog(Other(self, template_embed, session))
		await self.add_cog(Help(self, template_embed))
		await self.tree.sync()
		self.remove_command("help")

		if (os.getenv("TOPGGTOKEN") != None):
			import topgg
			bot.topggpy = topgg.DBLClient(bot, os.getenv("TOPGGTOKEN"), autopost = True)
			bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/webhook", os.getenv("TOPGGPASSWORD"))
			bot.topgg_webhook.run(5000)

dotenv.load_dotenv(dotenv_path = Path("tokens.env"))
intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix = "?", intents = intents)

# A template embed to use elsewhere in the bot
template_embed = discord.Embed()
template_embed.colour = discord.Color.blue()

@tasks.loop(seconds = 600)
async def update_status():
	await bot.change_presence(activity = discord.Streaming(
		name = f"/help | {len(bot.guilds)} guilds",
		url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
	))

# Start bot presence loop and print a list of guild names 
@bot.event
async def on_ready():
	for guild in bot.guilds: print(guild.name)
	update_status.start()

# Log commands to log.txt
@bot.event
async def on_interaction(ctx):
	if ctx.type == discord.InteractionType.application_command:
		file = open("log.txt", "a")
		file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + ctx.user.name + " issued command /" + ctx.command.name + "\n")
		file.close()

# Reward users when they vote on top.gg
@bot.event
async def on_dbl_vote(data):
	user = await bot.fetch_user(data.get("user"))
	embed = deepcopy(template_embed)
	embed.add_field(name = "Vote success", value = """
You successfully voted on top.gg!
[Vote again tomorrow](https://top.gg/bot/851508305573445703/vote)
	""")
	embed.set_footer(text = "(+20 points)")
	await user.send(embed = embed)

	users_ref.document(str(user.id)).set({ "points": firestore.Increment(20) }, merge = True)

@bot.event
async def on_message(message):
	msg = message.content.lower()
	if message.author == bot.user: return
	
	# React to message if it mentions the bot
	if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
		await message.add_reaction(get(bot.get_guild(874266744456376370).emojis, name = 'FruityMentionReaction'))

	# Handle answer marking
	stored_answer = answers.get(message.author.id)
	channel_id = channels.get(message.author.id)
	if stored_answer is not None:
		if not channel_id == message.channel.id: return
		embed = deepcopy(template_embed)
		
		if msg == stored_answer:
			embed.colour = discord.Colour.green()
			embed.add_field(name = "Correct!", value = f"{stored_answer} was the correct answer!", inline = False)
			embed.set_footer(text = "(+5 points)")
			users_ref.document(str(message.author.id)).set({ "points": firestore.Increment(5) }, merge = True)
		else:
			embed.colour = discord.Colour.red()
			embed.add_field(name = "Incorrect!", value = f"{stored_answer} was the correct answer!", inline = False)
			embed.set_footer(text = "(-2 points)")
			users_ref.document(str(message.author.id)).set({ "points": firestore.Increment(-2) }, merge = True)
		await message.reply(embed = embed, mention_author = False)
		del answers[message.author.id]

# Run the bot
try: bot.run(os.getenv("TOKEN")) 
except discord.errors.HTTPException: os.system("kill 1")