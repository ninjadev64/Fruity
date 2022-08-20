import typing
import discord
from copy import deepcopy
from discord.ext import commands
from discord.app_commands import command, describe, ContextMenu
from firebase_admin.firestore import Query

template_embed = None
db = None

class Points(commands.Cog):
	def __init__(self, bot, ctemplate_embed, cdb, users_ref):
		self.bot = bot
		self.users_ref = users_ref
		global template_embed, db, cursor
		template_embed = ctemplate_embed
		db = cdb

		self.points_ctx_menu = ContextMenu(name = "fruity points", callback = self.context_points)
		self.bot.tree.add_command(self.points_ctx_menu)

	async def cog_unload(self): self.bot.tree.remove_command(self.points_ctx_menu.name, type = self.points_ctx_menu.type)
	
	async def points(self, ctx, user: typing.Union[discord.Member, discord.User]):
		user = user or ctx.user
		embed = deepcopy(template_embed)
		embed.add_field(name = "Points", value = f"{user.name}#{user.discriminator}" + f" has {self.users_ref.document(str(user.id)).get(field_paths = ['points']).to_dict().get('points')} points.", inline = False)
		await ctx.response.send_message(embed = embed)

	@command(name = "points", description = "See how many points a user has")
	async def slash_points(self, ctx, user: typing.Optional[typing.Union[discord.Member, discord.User]]):
		await self.points(ctx, user or ctx.user)

	async def context_points(self, ctx, user: typing.Union[discord.Member, discord.User]):
		await self.points(ctx, user)

	@command(description = "View the top 10 players for points")
	async def leaderboard(self, ctx):
		strings = []
		embed = deepcopy(template_embed)
		query = self.users_ref.order_by("points", direction = Query.DESCENDING).limit(10)
		place = 1
		for x in query.get():
			doc = x.to_dict()
			user = await self.bot.fetch_user(x.id)
			strings.append(f"{place}. {user.name}#{user.discriminator}: {doc.get('points')}")
			place = place + 1
		embed.add_field(name = "Leaderboard", value = "\n".join(strings), inline = False)
		await ctx.response.send_message(embed = embed)

	def unlocked(self, points, requirement):
		if (requirement - points) > 0: return f"{requirement - points} points to go"
		else: return "**Unlocked**"

	@command(description = "Display your shiny badges")
	async def badges(self, ctx):
		embed = deepcopy(template_embed)
		points = self.users_ref.document(str(ctx.user.id)).get(field_paths = ['points']).to_dict().get('points')
		badges = []
		contributors = [806550260126187560, 865290525258547220]
		if points >= 500: badges.append("<:FruityBadge500:899226499259990057>")
		if points >= 1000: badges.append("<:FruityBadge1000:899226539906961418>")
		if points >= 2500: badges.append("<:FruityBadge2500:899234759585169498>")
		if points >= 5000: badges.append("<:FruityBadge5000:899235047419301970>")
		if ctx.user.id in contributors: badges.append("<:FruityBadgeContributors:899270459474997301>")
		if badges == []: badges.append("No badges")
		embed.add_field(name = f"{ctx.user.name}#{ctx.user.discriminator}'s badges", value = f"""
<:FruityBadge500:899226499259990057> {self.unlocked(points, 500)}
<:FruityBadge1000:899226539906961418> {self.unlocked(points, 1000)}
<:FruityBadge2500:899234759585169498> {self.unlocked(points, 2500)}
<:FruityBadge5000:899235047419301970> {self.unlocked(points, 5000)}
		""", inline = True)
		embed.set_footer(text = "Badges by EkoKit24#4602")
		await ctx.response.send_message(''.join(badges), embed = embed)

	@command(description = "Top.gg vote link")
	async def vote(self, ctx):
		embed = deepcopy(template_embed)
		embed.add_field(name = "Top.gg vote link", value = "Vote on top.gg to claim your reward of 20 points!\nhttps://top.gg/bot/851508305573445703/vote")
		await ctx.response.send_message(embed = embed, ephemeral = True)