import discord
from aiohttp import ClientSession
from copy import deepcopy
from art import text2art
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice

template_embed = None
session = ClientSession()

class Fun(commands.Cog):
	def __init__(self, bot, ctemplate_embed, weather_key):
		self.bot = bot
		self.sra = "https://some-random-api.ml/"
		self.weather_key = weather_key
		global template_embed; template_embed = ctemplate_embed
	
	@slash_command(description = "Get an animal fact and image", options = [
		Option("animal", "Animal", OptionType.STRING, True, [
			OptionChoice("dog", "dog"),
			OptionChoice("cat", "cat"),
			OptionChoice("panda", "panda"),
			OptionChoice("fox", "fox"),
			OptionChoice("red panda", "red_panda"),
			OptionChoice("koala", "koala"),
			OptionChoice("bird", "bird"),
			OptionChoice("raccoon", "raccoon"),
			OptionChoice("kangaroo", "kangaroo")
		])
	])
	async def animal(self, ctx, animal = None):
		response = await session.get(self.sra + "animal/" + animal)
		json = await response.json()
		embed = deepcopy(template_embed)
		embed.add_field(name = animal.capitalize(), value = json.get("fact"))
		embed.set_image(url = json.get("image"))
		embed.set_footer(text = "Powered by Some Random API", icon_url = "https://i.some-random-api.ml/logo.png")
		await ctx.send(embed = embed)

	@slash_command(description = "Random joke generator")
	async def joke(self, ctx):
		response = await session.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
		json = await response.json()
		embed = deepcopy(template_embed)
		if json.get("type") == "single": embed.add_field(name = "Joke", value = json.get("joke"), inline = False)
		if json.get("type") == "twopart":
			embed.add_field(name = "Setup", value = json.get("setup"), inline = False)
			embed.add_field(name = "Delivery", value = json.get("delivery"), inline = False)
		embed.set_footer(text = "Powered by JokeAPI", icon_url = "https://raw.githubusercontent.com/Sv443/JokeAPI/master/docs/static/icon_1000x1000.png")
		await ctx.send(embed = embed)

	@slash_command(description = "Get a song's lyrics", options = [
			Option("song", "Song", OptionType.STRING, True)
	])
	async def lyrics(self, ctx, song = "Never gonna give you up"):
		response = await session.get(self.sra + "lyrics?title=" + song)
		json = await response.json()
		embed = deepcopy(template_embed)
		embed.set_footer(text = "Powered by Some Random API", icon_url = "https://i.some-random-api.ml/logo.png")
		if json.get("error") is not None:
			embed.add_field(name = "Error", value = json.get("error"), inline = False)
			embed.colour = discord.Color.red()
			await ctx.send(embed = embed, ephemeral = True)
			return False
		else:
			embed.set_thumbnail(url = json.get("thumbnail")[next(iter(json.get("thumbnail")))])
			embed.add_field(name = json.get("title"), value = "by " + json.get("author"), inline = False)
			lyrics = json.get("lyrics")
			lyrics = (lyrics[:1021] + '...') if len(lyrics) > 1021 else lyrics
			embed.add_field(name = "Song lyrics", value = lyrics, inline = False)
		await ctx.send("Full lyrics: <" + json.get("links")[next(iter(json.get("links")))] + ">", embed = embed)

	@slash_command(description = "Echo your input", options=[
			Option("input", "Input", OptionType.STRING, True)
	])
	async def echo(self, ctx, input = ""): await ctx.send(input, ephemeral = True)

	@slash_command(description = "ASCIIfy your input", options=[
			Option("input", "Input", OptionType.STRING, True),
			Option("font", "Font", OptionType.STRING, False)
	])
	async def asciify(self, ctx, input = "", font = None):
		embed = deepcopy(template_embed)
		if font is None: value = text2art(input)
		else: value = text2art(input, font)

		for line in value.splitlines():
			if len(line) > 56:
				embed.add_field(name = "Error", value = "Your input was too long! It'll look really weird but I'll send it anyway:", inline = False)
				embed.colour = discord.Color.red()
				break

		embed.add_field(name = "(^・ω・^)", value = "```" + value + "```")

		try: await ctx.send(embed = embed)
		except discord.errors.HTTPException: await ctx.send("Your input was way too long!", ephemeral = True)

	@slash_command(description = "Fail the interaction, because why not")
	async def fail(self, ctx): pass

	@slash_command(description = "Checks the weather")
	async def weather(self, ctx): pass # a parent for the below two subcommands

	@weather.sub_command(description = "Checks the weather", options = [
		Option("city", "The closest city to the location you want the weather for", OptionType.STRING, True)
	])
	async def city(self, ctx, city = "London"):
		try: from geopy.geocoders import Nominatim; gn = Nominatim(user_agent = "Fruity")
		except ModuleNotFoundError: await ctx.send("The person hosting this Fruity instance has not installed the required module for this command. Please use `/weather coords` instead.", ephemeral = True); return
		
		try: coords = gn.geocode(city)[1]
		except TypeError: await ctx.send("The city you entered was invalid. Try again, or use `/weather coords`.", ephemeral = True)
		response = await session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={self.weather_key}&units=metric")
		json = await response.json()

		embed = deepcopy(template_embed)
		embed.add_field(name = json.get("weather")[0].get("main"), value = json.get("weather")[0].get("description"), inline = False)
		embed.add_field(name = "Temperature", value = f'{json.get("main").get("temp")} °C', inline = False)
		embed.colour = discord.Colour.blue()
		embed.set_footer(text = f"Weather right now in {city.title()}")
		
		await ctx.send(embed = embed)

	@weather.sub_command(description = "Checks the weather", options = [
		Option("latitude", "Latitude", OptionType.NUMBER, True),
		Option("longitude", "Longitude", OptionType.NUMBER, True)
	])
	async def coords(self, ctx, latitude = 51.5, longitude = 0):
		response = await session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.weather_key}&units=metric")
		json = await response.json()

		embed = deepcopy(template_embed)
		embed.add_field(name = json.get("weather")[0].get("main"), value = json.get("weather")[0].get("description"), inline = False)
		embed.add_field(name = "Temperature", value = f'{json.get("main").get("temp")} °C', inline = False)
		embed.colour = discord.Colour.blue()
		embed.set_footer(text = f"Weather right now in {json.get('name').title()}")
		
		await ctx.send(embed = embed)