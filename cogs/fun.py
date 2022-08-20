import typing
import discord
from aiohttp import ClientSession
from copy import deepcopy
from art import text2art
from os import getenv
from discord.ext import commands
from discord.app_commands import command, describe, Group

template_embed = None

class Fun(commands.Cog):
	def __init__(self, bot, ctemplate_embed, client_session):
		self.bot = bot
		self.sra = "https://some-random-api.ml/"
		self.weather_key = getenv("WEATHERKEY")
		self.flight_key = getenv("FLIGHTKEY")

		self.session = client_session

		try: from geopy.geocoders import Nominatim; self.gn = Nominatim(user_agent = "Fruity")
		except: self.gn = None
		
		global template_embed; template_embed = ctemplate_embed
	
	@command(description = "Get an animal fact and image")
	async def animal(self, ctx, animal: typing.Literal["dog", "cat", "panda", "fox", "red_panda", "koala", "bird", "raccoon", "kangaroo"]):
		response = await self.session.get(self.sra + "animal/" + animal)
		json = await response.json()
		embed = deepcopy(template_embed)
		embed.add_field(name = animal.capitalize(), value = json.get("fact"))
		embed.set_image(url = json.get("image"))
		embed.set_footer(text = "Powered by Some Random API", icon_url = "https://i.some-random-api.ml/logo.png")
		await ctx.response.send_message(embed = embed)

	@command(description = "Random joke generator")
	async def joke(self, ctx):
		response = await self.session.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
		json = await response.json()
		embed = deepcopy(template_embed)
		if json.get("type") == "single": embed.add_field(name = "Joke", value = json.get("joke"), inline = False)
		if json.get("type") == "twopart":
			embed.add_field(name = "Setup", value = json.get("setup"), inline = False)
			embed.add_field(name = "Delivery", value = json.get("delivery"), inline = False)
		embed.set_footer(text = "Powered by JokeAPI", icon_url = "https://raw.githubusercontent.com/Sv443/JokeAPI/master/docs/static/icon_1000x1000.png")
		await ctx.response.send_message(embed = embed)

	@command(description = "Get a song's lyrics")
	async def lyrics(self, ctx, song: str):
		response = await self.session.get(self.sra + "lyrics?title=" + song)
		json = await response.json()
		embed = deepcopy(template_embed)
		embed.set_footer(text = "Powered by Some Random API", icon_url = "https://i.some-random-api.ml/logo.png")
		embed.set_author(name = ctx.user.name, icon_url = ctx.user.avatar)
		if json.get("error") is not None:
			embed.add_field(name = "Error", value = json.get("error"), inline = False)
			embed.colour = discord.Color.red()
			await ctx.response.send_message(embed = embed, ephemeral = True)
			return False
		else:
			embed.set_thumbnail(url = json.get("thumbnail")[next(iter(json.get("thumbnail")))])
			embed.add_field(name = json.get("title"), value = "by " + json.get("author"), inline = False)
			lyrics = json.get("lyrics")
			lyrics = (lyrics[:1021] + '...') if len(lyrics) > 1021 else lyrics
			embed.add_field(name = "Song lyrics", value = lyrics, inline = False)
		await ctx.response.send_message("Full lyrics: <" + json.get("links")[next(iter(json.get("links")))] + ">", embed = embed)

	@command(description = "Echo your input")
	async def echo(self, ctx, input: str):
		await ctx.response.send_message(input, ephemeral = True)

	@command(description = "ASCIIfy your input")
	async def asciify(self, ctx, input: str, font: typing.Optional[str]):
		embed = deepcopy(template_embed)
		if font is None: value = text2art(input)
		else: value = text2art(input, font)

		for line in value.splitlines():
			if len(line) > 56:
				embed.add_field(name = "Error", value = "Your input was too long! It might look really weird but I'll send it anyway:", inline = False)
				embed.colour = discord.Color.red()
				break

		embed.add_field(name = "(^・ω・^)", value = "```" + value + "```")

		try: await ctx.response.send_message(embed = embed)
		except discord.errors.HTTPException: await ctx.response.send_message("Your input was way too long!", ephemeral = True)

	@command(description = "Fails the interaction, because why not")
	async def fail(self, ctx): pass

	weather_group = Group(name = "weather", description = "Checks the weather")

	@weather_group.command(description = "Checks the weather")
	@describe(city = "The closest city to the location you want the weather for")
	async def city(self, ctx, city: str):
		if (self.gn is None):
			await ctx.response.send_message("The person hosting this Fruity instance has not installed the required module for this command. Please use `/weather coords` instead.", ephemeral = True); return
		
		try: coords = self.gn.geocode(city)[1]
		except TypeError: await ctx.response.send_message("The city you entered was invalid. Try again, or use `/weather coords`.", ephemeral = True)
		response = await self.session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={self.weather_key}&units=metric")
		json = await response.json()

		embed = deepcopy(template_embed)
		embed.add_field(name = json.get("weather")[0].get("main"), value = json.get("weather")[0].get("description"), inline = False)
		embed.add_field(name = "Temperature", value = f'{json.get("main").get("temp")} °C', inline = False)
		embed.colour = discord.Colour.blue()
		embed.set_footer(text = f"Weather right now in {city.title()}")
		
		await ctx.response.send_message(embed = embed)

	@weather_group.command(description = "Checks the weather")
	async def coords(self, ctx, latitude: float, longitude: float):
		response = await self.session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.weather_key}&units=metric")
		json = await response.json()

		embed = deepcopy(template_embed)
		embed.add_field(name = json.get("weather")[0].get("main"), value = json.get("weather")[0].get("description"), inline = False)
		embed.add_field(name = "Temperature", value = f'{json.get("main").get("temp")} °C', inline = False)
		embed.colour = discord.Colour.blue()
		embed.set_footer(text = f"Weather right now in {json.get('name').title()}")
		
		await ctx.response.send_message(embed = embed)

	@command(description = "Retrieve details about a flight (unstable)")
	@describe(flight = "Flight IATA code (e.g. BA198)")
	async def plane(self, ctx, flight: str):
		json = (await (await self.session.get(f"https://airlabs.co/api/v9/flights?api_key={self.flight_key}&flight_iata={flight}")).json()).get("response")[0]

		embed = deepcopy(template_embed)
		embed.add_field(name = "Flight", value = json.get("flight_iata"))
		embed.add_field(name = "Status", value = json.get("status"), inline = False)
		embed.add_field(name = "Departed from", value = json.get("dep_iata"))
		embed.add_field(name = "Arriving at", value = json.get("arr_iata"), inline = False)

		if (self.gn is not None):
			try: embed.add_field(name = "Flying over", value = self.gn.reverse(f"{json.get('lat')}, {json.get('lng')}").address, inline = False)
			except AttributeError: pass

		await ctx.response.send_message(embed = embed)