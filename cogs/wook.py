import os
from colorama import Fore
from dislash import slash_command, ActionRow, Button, ButtonStyle
from discord.ext import commands
from copy import deepcopy

clear = Fore.RESET
dc = Fore.GREEN + "|" + clear # dc = door character
ec = Fore.RED + "e" + clear # ec = enemy character
sd = Fore.RED + "V" + clear # spike down
sl = Fore.RED + "<" + clear # spike left
sr = Fore.RED + ">" + clear # spike right
tp1 = Fore.YELLOW + "■" + clear # teleporter 1
tp2 = Fore.CYAN + "■" + clear # teleporter 2

levels = [
	[
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
	],
	[
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
		["#"," "," "," "," "," ", sd," "," "," "," "," ","#"," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," ","#"," ", " ","#"],
		["#"," "," "," "," "," "," "," "," "," "," ", sl,"#"," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
		["#"," "," "," "," "," "," "," "," "," "," ", sl,"#"," "," ", dc],
		["#"," "," "," "," "," "," ","#"," "," "," "," ","#"," "," ", dc],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ", dc],
		["#"," "," "," ","#","#","#","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
	],
	[
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," ","#",tp1,"#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," ","#","#","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," ","#",tp2,"#"," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," ","#","#","#"," "," "," "," "," ", dc],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
	],
	[
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
		["#"," "," "," "," "," "," "," "," ","#"," "," "," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," "," "," ","#"," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ", dc],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," ","#"," "," "," ","#"],
		["#"," "," "," "," "," "," "," "," ","#"," "," "," "," "," ","#"],
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
	],
]

messages = {
    0: "Use the buttons to move!",
    1: "Try to avoid the spikes!",
    2: "Good luck reaching the door!",
    3: "Longgg level!"
}

class Wook(commands.Cog):
    def __init__(self, bot, template_embed):
        self.bot = bot
        self.games = {}
        self.template_embed = template_embed

    # @slash_command(description = "Wook!")
    async def wook(self, ctx):
        if self.games.get(ctx.author.id) is None:
            self.games[ctx.author.id] = Game(self)
        await self.games[ctx.author.id].entry(ctx)

class Game():
    def __init__(self, cog):
        self.level = 0
        self.player_index = (1, 1)
        self.tp1_index = (2, 6)
        self.tp2_index = (7, 8)
        self.cog = cog

    def check_index(self, tuple):
        char = levels[self.level][tuple[0]][tuple[1]]
        if (char == dc):
            if not (self.level + 1 > (len(levels) - 1)):
                self.level = self.level + 1
                self.player_index = (1, 1)
            else:
                self.message.edit("GG!")
                del self.cog.games[self.user.id]
            return False
        elif char == ec or char == sl or char == sd:
            self.player_index = (1, 1)
            return False
        elif char == tp1:
            self.player_index = self.tp2_index
            return False
        elif char == tp2:
            self.player_index = self.tp1_index
            return False
        if (char == "#"): return False
        else: return True

    async def entry(self, ctx):
        self.user = ctx.author

        actionrow = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Up",
                custom_id="up"
            ),
            Button(
                style=ButtonStyle.green,
                label="Down",
                custom_id="down"
            ),
            Button(
                style=ButtonStyle.green,
                label="Left",
                custom_id="left"
            ),
            Button(
                style=ButtonStyle.green,
                label="Right",
                custom_id="right"
            )
        )

        self.message = await ctx.send("Wook! Press any key to start.", components = [actionrow])
        on_click = self.message.create_click_listener(timeout = 600)

        @on_click.matching_id("up")
        async def up(ctx):
            newindex = ((self.player_index[0] - 1), self.player_index[1])
            if self.check_index(newindex):
                self.player_index = newindex
        @on_click.matching_id("down")
        async def down(ctx):
            newindex = ((self.player_index[0] + 1), self.player_index[1]) 
            if self.check_index(newindex):
                self.player_index = newindex
        @on_click.matching_id("left")
        async def left(ctx):
            newindex = (self.player_index[0], (self.player_index[1] - 1)) 
            if self.check_index(newindex):
                self.player_index = newindex
        @on_click.matching_id("right")
        async def right(ctx):
            newindex = (self.player_index[0], (self.player_index[1] + 1)) 
            if self.check_index(newindex):
                self.player_index = newindex

        @on_click.no_checks()
        async def any(ctx):
            field = ""
            kmap = []
            for ri, rv in enumerate(levels[self.level]):
                row = []
                for ci, cv in enumerate(rv):
                    if (ri, ci) == self.player_index:
                        row.append("\u001b[34m@\u001b[0m")
                    else:
                        row.append(cv)
                kmap.append(row)
                
            for row in kmap:
                field = field + (' '.join(row)) + "\n"
                
            field = field + str(self.player_index)
            
            embed = deepcopy(self.cog.template_embed)
            embed.add_field(name = messages.get(self.level), value = "```ansi\n" + field + "```")
            await ctx.message.edit(embed = embed, components = [actionrow])
            await ctx.create_response(type = 6)
        
        @on_click.timeout
        async def on_timeout():
            await self.message.edit("Game timed out due to 10 minutes of play.", embed = None)