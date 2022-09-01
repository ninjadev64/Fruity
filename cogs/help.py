import discord
from copy import deepcopy
from discord.ext import commands
from discord.ui import Select, View 
from discord.app_commands import command, describe

template_embed = None

embeds = { }

class HelpSelect(Select):
	def __init__(self):
		options = [
			discord.SelectOption(label = "Fun", emoji = "🎭"),
			discord.SelectOption(label = "Minigames", emoji = "🎲"),
			discord.SelectOption(label = "Points", emoji = "🏆"),
			discord.SelectOption(label = "Other", emoji = "❓")
		]
		super().__init__(custom_id = "help", placeholder = "Choose one...", min_values = 1, max_values = 1, options = options)
	
	async def callback(self, ctx):
		await ctx.response.send_message(embed = embeds[self.values[0]], ephemeral = True)

class Help(commands.Cog):
	def __init__(self, bot, ctemplate_embed):
		self.bot = bot
		global template_embed, template_help_embed
		template_embed = ctemplate_embed

		for name, cog in self.bot.cogs.items():
			embed = deepcopy(template_embed)
			for command in cog.get_app_commands():
				args = (' '.join([f'[{arg.name}: {arg.type.name}]' for arg in command.parameters]) if hasattr(command, "parameters") else "")
				embed.add_field(name = f"/{command.name} {args}", value = command.description, inline = False)
			embeds[name] = embed

	@command(description = "Displays help information for this bot")
	async def help(self, ctx):
		view = View(timeout = 300)
		view.add_item(HelpSelect())

		embed = deepcopy(template_embed)
		embed.title = "Fruity: Help"
		embed.description = "Choose a category!"
		await ctx.response.send_message(embed = embed, view = view, ephemeral = True)