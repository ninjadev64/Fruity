import discord
from copy import deepcopy
from random import randint, shuffle, choice
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice

words = open("words.txt").read().splitlines()

template_embed = None
db = None
cursor = None

class Minigames(commands.Cog):
    def __init__(self, bot, ctemplate_embed, cdb, ccursor):
        self.bot = bot
        global template_embed, db, cursor
        template_embed = ctemplate_embed
        db = cdb
        cursor = ccursor
    
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
        cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer, Channel)
        VALUES(?,?,?)""", (ctx.author.id, answer, ctx.channel.id))
        db.commit()

    @slash_command(description = "Unscramble a jumbled-up word")
    async def unscramble(self, ctx):
        word = words[randint(0,999)]
        word_list = list(word)
        shuffle(word_list)
        word_scrambled = ''.join(word_list)
        if word_scrambled == word:
            await self.unscramble(ctx)
            return
        embed = deepcopy(template_embed)
        embed.add_field(name = "Unscramble this", value = word_scrambled, inline = True)
        await ctx.send(embed = embed)
        cursor.execute("""INSERT OR REPLACE INTO Answers(ID, Answer, Channel)
        VALUES(?,?,?)""", (ctx.author.id, word, ctx.channel.id))
        db.commit()

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
            cursor.execute("UPDATE Points SET Points = Points + 5 WHERE ID = ?", (ctx.author.id))
        else:
            embed.colour = discord.Color.red()
            embed.add_field(name = "You lose!", value = "The coin landed " + flipped_side + " side up.")
            cursor.execute("UPDATE Points SET Points = Points - 2 WHERE ID = ?", (ctx.author.id))
        db.commit()
        await ctx.send(embed = embed)