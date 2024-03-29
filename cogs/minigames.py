import typing
import discord
from copy import deepcopy
from random import randint, sample, choice
from discord.ext import commands
from discord.app_commands import command, describe

from firebase_admin import firestore

words = open("words.txt").read().splitlines()

template_embed = None
db = None
answers = {}
channels = {}

class Minigames(commands.Cog):
	def __init__(self, bot, ctemplate_embed, cdb, users_ref):
		self.bot = bot
		self.users_ref = users_ref
		global template_embed, db, cursor
		template_embed = ctemplate_embed
		db = cdb
	
	@command(description = "Try a simple equation")
	async def math(self, ctx):
		num1 = randint(1, 50)
		num2 = randint(1, 50)
		operation = randint(0, 1)
		operation_strings = [" + ", " - "]

		embed = deepcopy(template_embed)
		embed.add_field(name = "Solve this", value = str(num1) + operation_strings[operation] + str(num2), inline = True)
		await ctx.response.send_message(embed = embed)
		if operation == 0: answer = num1 + num2
		if operation == 1: answer = num1 - num2
		answers[ctx.user.id] = str(answer)
		channels[ctx.user.id] = ctx.channel.id

	@command(description = "Unscramble a jumbled-up word")
	async def unscramble(self, ctx):
		word = words[randint(0, 999)]
		word_list = list(word)
		word_scrambled = ''.join(sample(word_list, len(word_list)))
		if word_scrambled == word:
			await self.unscramble(self, ctx)
			return
		embed = deepcopy(template_embed)
		embed.add_field(name = "Unscramble this", value = word_scrambled, inline = True)
		await ctx.response.send_message(embed = embed)
		answers[ctx.user.id] = word
		channels[ctx.user.id] = ctx.channel.id

	@command(description = "Flip a coin")
	async def coinflip(self, ctx, side: typing.Literal["heads", "tails"]):
		embed = deepcopy(template_embed)
		flipped_side = choice(["heads", "tails"])
		if flipped_side == side:
			embed.colour = discord.Colour.green()
			embed.add_field(name = "You win!", value = "The coin landed " + flipped_side + " side up.")
			self.users_ref.document(str(ctx.user.id)).set({ "points": firestore.Increment(5) }, merge = True)
		else:
			embed.colour = discord.Colour.red()
			embed.add_field(name = "You lose!", value = "The coin landed " + flipped_side + " side up.")
			self.users_ref.document(str(ctx.user.id)).set({ "points": firestore.Increment(-2) }, merge = True)
		await ctx.response.send_message(embed = embed)