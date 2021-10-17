import discord
from discord.utils import get
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice
from requests import post

template_embed = None

class Other(commands.Cog):
    def __init__(self, bot, ctemplate_embed):
        self.bot = bot
        global template_embed
        template_embed = ctemplate_embed
    
    @slash_command(description = "The people behind the bot")
    async def credits(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name = "Developer(s)", value = "ninjadev64#0861", inline = False)
        embed.add_field(name = "Badge emojis", value = "EkoKit24#4602", inline = False)
        embed.add_field(name = "Random stuff and ideas (unofficial)", value = "Blaze#2299\nPerestuken#8688 / Perestuken#6263", inline = False)
        await ctx.send(embed = embed)

    @slash_command(description = "Invite the bot to your server")
    async def invite(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name = "Invite the bot to your server", value = "Please note that while the bot is in development you won't be able to use slash commands in your server!\nhttps://ninjadev64.github.io/Fruity/", inline = False)
        await ctx.send(embed = embed)

    @slash_command(description = "Ping? Pong!")
    async def ping(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name = "Ping? Pong!", value = str(round(self.bot.latency * 1000)) + "ms", inline = False)
        await ctx.send(embed = embed)

    @slash_command(description = "Command restricted to the bot owner")
    async def log(self, ctx):
        embed = deepcopy(template_embed)
        appinfo = await self.bot.application_info()
        if ctx.author != appinfo.owner:
            embed.colour = discord.Color.red()
            embed.add_field(name = "Missing permissions", value="This command is restricted to the bot owner")
            await ctx.send(embed = embed)
            return
        await ctx.send(post("https://api.mclo.gs/1/log", data = {"content": open("log.txt", "r").read()}).json().get("url"), ephemeral = True)

    # CitrusDev server only
    @slash_command(description = "Suggest anything for any CitrusDev project", guild_ids = [874266744456376370], options = [
            Option("project", "Project", OptionType.STRING, True, [
                OptionChoice("Fruity", "Fruity"),
                OptionChoice("CitrusFFA", "CitrusFFA")
            ]),
            Option("suggestion", "Suggestion", OptionType.STRING, True)
    ])
    async def suggest(self, ctx, project = None, suggestion = None):
        embed = deepcopy(template_embed)
        embed.set_author(name = "Suggestion")
        embed.add_field(name = project, value = suggestion, inline = False)
        embed.set_footer(text = ctx.author.name + "#" + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
        message = await self.bot.get_channel(889086565287079946).send(embed = embed)
        await message.add_reaction(get(self.bot.get_guild(837212681198108692).emojis, name = 'Completed'))
        await message.add_reaction(get(self.bot.get_guild(837212681198108692).emojis, name = 'Cancelled'))
        await ctx.send("<#889086565287079946>", ephemeral = True)