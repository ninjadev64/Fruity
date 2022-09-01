import discord
from discord.utils import get
import unicodedata
from copy import deepcopy
from discord.ext import commands
from discord.app_commands import command, describe
from time import time

template_embed = None

class Other(commands.Cog):
	def __init__(self, bot, ctemplate_embed, client_session):
		self.bot = bot
		self.session = client_session
		self.start_time = round(time())
		global template_embed; template_embed = ctemplate_embed
	
	@command(description = "The people behind the bot")
	async def credits(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Developer(s)", value = "ninjadev64#0861", inline = False)
		embed.add_field(name = "Badge emojis", value = "EkoKit24#4602", inline = False)
		embed.add_field(name = "Random stuff and ideas (unofficial)", value = "Blaze#2299\nPerestuken#8688", inline = False)
		await ctx.response.send_message(embed = embed)

	@command(description = "Invite the bot to your server")
	async def invite(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Invite the bot to your server <:FruityMentionReaction:888004953455616040>", value = "https://fruity.amansprojects.com/")
		view = discord.ui.View()
		view.add_item(discord.ui.Button(label = "Invite", style = discord.ButtonStyle.url, url = "https://fruity.amansprojects.com/"))
		await ctx.response.send_message(embed = embed, view = view)

	@command(description = "Ping? Pong!")
	async def ping(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Ping? Pong!", value = str(round(self.bot.latency * 1000)) + "ms")
		await ctx.response.send_message(embed = embed)

	@command(description = "Bot statistics")
	async def stats(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Bot statistics", value = 
		f"Program started: <t:{self.start_time}:R>\n" + 
		f"Server count: {len(self.bot.guilds)} guilds")
		await ctx.response.send_message(embed = embed)

	@command(description = "Converts Unicode values to characters")
	@describe(value = "Unicode value or name, e.g. U+A3 or \"pound sign\" for £")
	async def character(self, ctx, value: str):
		embed = deepcopy(template_embed)
		try:
			if value.lower().startswith(("u+", "0x")):
				char = chr(int(value[2:], base=16))

			elif value.isdecimal():
				char = chr(int(value))

			elif len(value) > 1:
				char = unicodedata.lookup(value)

			else:
				char = value

		except (ValueError, OverflowError, KeyError):
			embed.colour = discord.Colour.red()
			embed.add_field(name = "Error", value = "You entered an invalid Unicode code point or name.")

		else:
			embed.title = f"U+{ord(char):0>4X} {char}"
			if unicodedata.name(char, None) is not None:
				embed.add_field(name = "Name", value = unicodedata.name(char))

			if unicodedata.numeric(char, None) is not None:
				embed.add_field(name = "Numeric value", value = format(unicodedata.numeric(char), "g"))

			if not char.isprintable():
				embed.description = "Control character"

		await ctx.response.send_message(embed = embed)

	@command(description = "Command restricted to the bot owner")
	async def log(self, ctx):
		embed = deepcopy(template_embed)
		appinfo = await self.bot.application_info()
		while True is not False: # don't question it
			if appinfo.team is not None:
				if ctx.user.id in [member.id for member in appinfo.team.members]:
					break
			elif ctx.user == appinfo.owner:
				break
			embed.colour = discord.Color.red()
			embed.add_field(name = "Missing permissions", value="This command is restricted to the bot owner")
			await ctx.response.send_message(embed = embed, ephemeral = True)
			return
		await ctx.response.send_message(
			(await (await self.session.post("https://api.mclo.gs/1/log", data = {"content": open("log.txt", "r").read()})).json()).get("url"),
			ephemeral = True
		)