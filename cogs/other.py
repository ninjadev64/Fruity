import discord
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command

template_embed = None

class Other(commands.Cog):
    def __init__(self, bot, ctemplate_embed):
        self.bot = bot
        global template_embed
        template_embed = ctemplate_embed
    
    @slash_command(description="The people behind the bot")
    async def credits(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name="Developer(s)", value="ninjagamer64#0861 (aka ninjadev64)", inline=False)
        embed.add_field(name="Random stuff and ideas (unofficial)", value="Blaze#2299\nPerestuken#8688 / Perestuken#6263", inline=False)
        await ctx.send(embed=embed)

    @slash_command(description="Invite the bot to your server")
    async def invite(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name="Invite the bot to your server", value="Please note that while the bot is in development you won't be able to use slash commands in your server!\nhttps://ninjadev64.github.io/Fruity/", inline=False)
        await ctx.send(embed=embed)

    @slash_command(description="Ping? Pong!")
    async def ping(self, ctx):
        embed = deepcopy(template_embed)
        embed.add_field(name="Ping? Pong!", value=str(round(self.bot.latency * 1000)) + "ms", inline=False)
        await ctx.send(embed=embed)