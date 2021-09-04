from discord.ext import commands
from dislash import InteractionClient

bot = commands.Bot(command_prefix="!")
inter_client = InteractionClient(bot, test_guilds=[856954305214545960])
# If 'test_guilds' param isn't specified, the commands are registered globally.
# Global registration takes up to 1 hour.

@inter_client.slash_command(
    name="hello", # Defaults to the function name
    description="Says hello",
    guild_ids=[856954305214545960]
)
async def hello(inter):
    await inter.reply("Hello!")

bot.run("ODUxNTA4MzA1NTczNDQ1NzAz.YL5S6A.EF26W36uXWCkV9zfQq9U2aJma3w")
