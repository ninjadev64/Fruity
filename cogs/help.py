import discord
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice, SelectMenu, SelectOption

template_embed = None
template_help_embed = None

# A class for static methods and fields related to help embeds for global usage
class HelpEmbeds:
	@staticmethod
	def getFunEmbed():
		embed = deepcopy(template_help_embed)
		embed.add_field(name = "/animal [animal]", value = "Get an animal fact and image", inline = False)
		embed.add_field(name = "/lyrics [song]", value = "Get a song's lyrics", inline = False)
		embed.add_field(name = "/joke", value = "Random joke generator", inline = False)
		embed.add_field(name = "/echo [input]", value = "Echo your input", inline = False)
		embed.add_field(name = "/asciify [input]", value = "ASCIIfy your input", inline = False)
		embed.add_field(name = "/fail", value = "Fail the interaction, because why not", inline = False)
		return embed

	@staticmethod
	def getMinigamesEmbed():
		embed = deepcopy(template_help_embed)
		embed.add_field(name = "/math", value = "Do a short maths equation", inline = False)
		embed.add_field(name = "/unscramble", value = "Unscramble a jumbled-up word", inline = False)
		embed.add_field(name = "/coinflip [side]", value = "Flip a coin", inline = False)
		return embed

	@staticmethod
	def getPointsEmbed():
		embed = deepcopy(template_help_embed)
		embed.add_field(name = "/points [user]", value = "See how many points a user has", inline = False)
		embed.add_field(name = "/leaderboard", value = "View the top 10 players for points", inline = False)
		embed.add_field(name = "/badges", value = "Shiny badges", inline = False)
		embed.add_field(name = "/vote", value = "Top.gg vote link", inline = False)
		return embed

	@staticmethod
	def getOtherEmbed():
		embed = deepcopy(template_help_embed)
		embed.add_field(name = "/credits", value = "The people behind the bot", inline = False)
		embed.add_field(name = "/invite", value = "Invite the bot to your server", inline = False)
		embed.add_field(name = "/ping", value = "Ping? Pong!", inline = False)
		embed.add_field(name = "/stats", value = "Bot statistics", inline = False)
		return embed

# A class for static methods and fields related to help select menu components for global usage
class HelpComponents():
	custom_id = "help"
	max_values = 1
	fun = [SelectMenu(custom_id = custom_id, max_values = max_values,
				options = [
					SelectOption("Fun", "fun", default = True),
					SelectOption("Minigames", "minigames"),
					SelectOption("Points", "points"),
					SelectOption("Other", "other")
	])]
	minigames = [SelectMenu(custom_id = custom_id, max_values = max_values,
				options = [
					SelectOption("Fun", "fun"),
					SelectOption("Minigames", "minigames", default = True),
					SelectOption("Points", "points"),
					SelectOption("Other", "other")
	])]
	points = [SelectMenu(custom_id = custom_id, max_values = max_values,
				options = [
					SelectOption("Fun", "fun"),
					SelectOption("Minigames", "minigames"),
					SelectOption("Points", "points", default = True),
					SelectOption("Other", "other")
	])]
	other = [SelectMenu(custom_id = custom_id, max_values = max_values,
				options = [
					SelectOption("Fun", "fun"),
					SelectOption("Minigames", "minigames"),
					SelectOption("Points", "points"),
					SelectOption("Other", "other", default = True)
	])]

class Help(commands.Cog):
	def __init__(self, bot, ctemplate_embed):
		self.bot = bot
		global template_embed, template_help_embed
		template_embed = ctemplate_embed

		# An extension of the template embed to use in all help command embeds
		template_help_embed = deepcopy(template_embed)
		template_help_embed.set_footer(text = "Use the selector below to view commands from other categories!")
	
	@commands.Cog.listener()
	async def on_dropdown(self, ctx):
		if ctx.component.custom_id == "help":
			if ctx.select_menu.selected_options[0].value == "fun":
				await ctx.respond(type = 7, embed = HelpEmbeds.getFunEmbed(), components = HelpComponents.fun)
			if ctx.select_menu.selected_options[0].value == "minigames":
				await ctx.respond(type = 7, embed = HelpEmbeds.getMinigamesEmbed(), components = HelpComponents.minigames)
			if ctx.select_menu.selected_options[0].value == "points":
				await ctx.respond(type = 7, embed = HelpEmbeds.getPointsEmbed(), components = HelpComponents.points)
			if ctx.select_menu.selected_options[0].value == "other":
				await ctx.respond(type = 7, embed = HelpEmbeds.getOtherEmbed(), components = HelpComponents.other)

	@slash_command(description = "Displays help information for this bot", options = [
		Option("category", "Category", OptionType.STRING, False, [
			OptionChoice("Fun", "fun"),
			OptionChoice("Minigames", "minigames"),
			OptionChoice("Points", "points"),
			OptionChoice("Other", "other")
		])
	])
	async def help(self, ctx, category="fun"):
		if category == "fun": embed = HelpEmbeds.getFunEmbed(); components = HelpComponents.fun;
		elif category == "minigames": embed = HelpEmbeds.getMinigamesEmbed(); components = HelpComponents.minigames;
		elif category == "points": embed = HelpEmbeds.getPointsEmbed(); components = HelpComponents.points;
		elif category == "other": embed = HelpEmbeds.getOtherEmbed(); components = HelpComponents.other;
		await ctx.send(embed = embed, components = components)