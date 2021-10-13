import discord
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command, user_command, Option, OptionType

template_embed = None
db = None
cursor = None

class Points(commands.Cog):
    def __init__(self, bot, ctemplate_embed, cdb, ccursor):
        self.bot = bot
        global template_embed, db, cursor
        template_embed = ctemplate_embed
        db = cdb
        cursor = ccursor
    
    @slash_command(description="See how many points a user has", options=[
        Option("user", "User", OptionType.USER)
    ])
    async def points(self, ctx, user=None):
        user = user or ctx.author
        cursor.execute("SELECT Points FROM Points WHERE ID = ?", (user.id,))
        points_data = cursor.fetchone()
        if points_data is None: cursor.execute("""INSERT INTO Points(ID, Points)
        VALUES(?,?)""", (user.id, 0))
        embed = deepcopy(template_embed)
        cursor.execute("SELECT Points from Points WHERE ID = ?", (user.id,))
        for x in cursor.fetchall():
            embed.add_field(name="Points", value=user.name + "#" + user.discriminator + " has " + str(x[0]) + " points.", inline=False)
            await ctx.send(embed=embed)

    @slash_command(description="View the top 5 players for points")
    async def leaderboard(self, ctx):
        strings = []
        embed = deepcopy(template_embed)
        cursor.execute("SELECT * FROM Points ORDER BY Points DESC LIMIT 5")
        place = 1
        for x in cursor.fetchall():
            user = await self.bot.fetch_user(x[0])
            strings.append(str(place)+". " + user.name + "#" + user.discriminator + ": " + str(x[1]))
            place = place + 1
        embed.add_field(name="Leaderboard", value="\n".join(strings), inline=False)
        await ctx.send(embed=embed)
    
    @user_command(name="fruity points")
    async def context_points(self, ctx): await self.points(self, ctx, ctx.user)