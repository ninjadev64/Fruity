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
		if cursor.fetchone() is None: cursor.execute("""INSERT INTO Points(ID, Points)
		VALUES(?,?)""", (user.id, 0))
		embed = deepcopy(template_embed)
		cursor.execute("SELECT Points from Points WHERE ID = ?", (user.id,))
		embed.add_field(name = "Points", value = f"{user.name}#{user.discriminator}" + f" has {cursor.fetchone()[0]} points.", inline = False)
		await ctx.send(embed = embed)

	@user_command(name="fruity points")
	async def context_points(self, ctx): await self.points(self, ctx, ctx.user)

	@slash_command(description="View the top 10 players for points")
	async def leaderboard(self, ctx):
		strings = []
		embed = deepcopy(template_embed)
		cursor.execute("SELECT * FROM Points ORDER BY Points DESC LIMIT 10")
		place = 1
		for x in cursor.fetchall():
			user = await self.bot.fetch_user(x[0])
			strings.append(f"{place}. {user.name}#{user.discriminator}: {x[1]}")
			place = place + 1
		embed.add_field(name = "Leaderboard", value = "\n".join(strings), inline = False)
		await ctx.send(embed = embed)

	def unlocked(self, points, requirement):
	  if (requirement - points) > 0: return f"{requirement - points} points to go"
	  else: return "**Unlocked**"

	@slash_command(description="Shiny badges")
	async def badges(self, ctx):
		cursor.execute("SELECT Points FROM Points WHERE ID = ?", (ctx.author.id,))
		if cursor.fetchone() is None: cursor.execute("""INSERT INTO Points(ID, Points)
		VALUES(?,?)""", (ctx.author.id, 0))
		embed = deepcopy(template_embed)
		cursor.execute("SELECT Points from Points WHERE ID = ?", (ctx.author.id,))
		points = cursor.fetchone()[0]
		badges = []
		contributors = [806550260126187560, 865290525258547220]
		if points >= 500: badges.append("<:FruityBadge500:899226499259990057>")
		if points >= 1000: badges.append("<:FruityBadge1000:899226539906961418>")
		if points >= 2500: badges.append("<:FruityBadge2500:899234759585169498>")
		if points >= 5000: badges.append("<:FruityBadge5000:899235047419301970>")
		if ctx.author.id in contributors: badges.append("<:FruityBadgeContributors:899270459474997301>")
		if badges == []: badges.append("No badges")
		embed.add_field(name = f"{ctx.author.name}#{ctx.author.discriminator}'s badges", value = f"""
<:FruityBadge500:899226499259990057> {self.unlocked(points, 500)}
<:FruityBadge1000:899226539906961418> {self.unlocked(points, 1000)}
<:FruityBadge2500:899234759585169498> {self.unlocked(points, 2500)}
<:FruityBadge5000:899235047419301970> {self.unlocked(points, 5000)}
		""", inline = True)
		embed.set_footer(text = "Badges by EkoKit24#4602")
		await ctx.send(''.join(badges), embed = embed)

	@slash_command(description = "Top.gg vote link")
	async def vote(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Top.gg vote link", value = "Vote on top.gg to claim your reward of 20 points!\nhttps://top.gg/bot/851508305573445703/vote")
		await ctx.send(embed = embed, ephemeral = True)