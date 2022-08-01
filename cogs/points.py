import discord
from copy import deepcopy
from discord.ext import commands
from dislash import slash_command, user_command, Option, OptionType

template_embed = None
db = None

class Points(commands.Cog):
	def __init__(self, bot, ctemplate_embed, cdb, users_ref):
		self.bot = bot
		self.users_ref = users_ref
		global template_embed, db, cursor
		template_embed = ctemplate_embed
		db = cdb
	
	@slash_command(description="See how many points a user has", options=[
		Option("user", "User", OptionType.USER)
	])
	async def points(self, ctx, user=None):
		user = user or ctx.author
		embed = deepcopy(template_embed)
		embed.add_field(name = "Points", value = f"{user.name}#{user.discriminator}" + f" has {self.users_ref.document(str(user.id)).get(field_paths = ['points']).to_dict().get('points')} points.", inline = False)
		await ctx.send(embed = embed)

	@user_command(name="fruity points")
	async def context_points(self, ctx): await self.points(self, ctx, ctx.user)

	@slash_command(description="View the top 10 players for points")
	async def leaderboard(self, ctx):
		strings = []
		embed = deepcopy(template_embed)
		query = self.users_ref.order_by("points").limit_to_last(10)
		place = 1
		for x in query.get():
			doc = x.to_dict()
			user = await self.bot.fetch_user(doc.get('id'))
			strings.append(f"{place}. {user.name}#{user.discriminator}: {doc.get('points')}")
			place = place + 1
		embed.add_field(name = "Leaderboard", value = "\n".join(strings), inline = False)
		await ctx.send(embed = embed)

	def unlocked(self, points, requirement):
		if (requirement - points) > 0: return f"{requirement - points} points to go"
		else: return "**Unlocked**"

	@slash_command(description="Shiny badges")
	async def badges(self, ctx):
		embed = deepcopy(template_embed)
		points = self.users_ref.document(str(ctx.author.id)).get(field_paths = ['points']).to_dict().get('points')
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