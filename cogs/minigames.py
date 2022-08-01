import discord
from copy import deepcopy
from random import randint, sample, choice
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice

from firebase_admin import firestore

words = open("words.txt").read().splitlines()

template_embed = None
db = None

class Minigames(commands.Cog):
	def __init__(self, bot, ctemplate_embed, cdb, users_ref):
		self.bot = bot
		self.users_ref = users_ref
		global template_embed, db, cursor
		template_embed = ctemplate_embed
		db = cdb
	
	@slash_command(description = "Do a short maths equation")
	async def math(self, ctx):
		num1 = randint(1, 50)
		num2 = randint(1, 50)
		operation = randint(0, 1)
		operation_strings = [" + ", " - "]

		embed = deepcopy(template_embed)
		embed.add_field(name = "Solve this", value = str(num1) + operation_strings[operation] + str(num2), inline = True)
		await ctx.send(embed = embed)
		if operation == 0: answer = num1 + num2
		if operation == 1: answer = num1 - num2
		self.users_ref.document(str(ctx.author.id)).set({ "answer": str(answer), "channel": ctx.channel.id }, merge = True)

	@slash_command(description = "Unscramble a jumbled-up word")
	async def unscramble(self, ctx):
		word = words[randint(0, 999)]
		word_list = list(word)
		word_scrambled = ''.join(sample(word_list, len(word_list)))
		if word_scrambled == word:
			await self.unscramble(self, ctx)
			return
		embed = deepcopy(template_embed)
		embed.add_field(name = "Unscramble this", value = word_scrambled, inline = True)
		await ctx.send(embed = embed)
		self.users_ref.document(str(ctx.author.id)).set({ "answer": word, "channel": ctx.channel.id }, merge = True)

	@slash_command(description = "Flip a coin", options = [
			Option("side", "Side", OptionType.STRING, True, [
				OptionChoice("heads", "heads"),
				OptionChoice("tails", "tails")
			])
	])
	async def coinflip(self, ctx, side=None):
		embed = deepcopy(template_embed)
		flipped_side = choice(["heads", "tails"])
		if flipped_side == side:
			embed.colour = discord.Color.green()
			embed.add_field(name = "You win!", value = "The coin landed " + flipped_side + " side up.")
			self.users_ref.document(str(ctx.author.id)).set({ "points": firestore.Increment(5) }, merge = True)
		else:
			embed.colour = discord.Color.red()
			embed.add_field(name = "You lose!", value = "The coin landed " + flipped_side + " side up.")
			self.users_ref.document(str(ctx.author.id)).set({ "points": firestore.Increment(-2) }, merge = True)
		await ctx.send(embed = embed)