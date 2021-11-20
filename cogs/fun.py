import discord
from aiohttp import ClientSession
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice

template_embed = None
session = ClientSession()

class Fun(commands.Cog):
    def __init__(self, bot, ctemplate_embed):
        self.bot = bot
        self.sra = "https://some-random-api.ml/"
        global template_embed; template_embed = ctemplate_embed
    
    @slash_command(description = "Get an animal fact and image", options = [
        Option("animal", "Animal", OptionType.STRING, True, [
            OptionChoice("dog", "dog"),
            OptionChoice("cat", "cat"),
            OptionChoice("panda", "panda"),
            OptionChoice("fox", "fox"),
            OptionChoice("koala", "koala"),
            OptionChoice("bird", "bird")
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
            Option("font", "Font (see https://artii.herokuapp.com/fonts_list)", OptionType.STRING, False)
    ])
    async def asciify(self, ctx, input = "", font = None):
        embed = deepcopy(template_embed)
        if font is None: response = await session.get("https://artii.herokuapp.com/make?text=" + input)
        else: response = await session.get("https://artii.herokuapp.com/make?text=" + input + "&font=" + font)
        embed.add_field(name = "(^・ω・^)", value = "```" + await response.text() + "```")
        await ctx.send(embed = embed)

    @slash_command(description = "Fail the interaction, because why not")
    async def fail(self, ctx): pass