import discord, sys
from discord.ext import commands
import random

class General:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print('------')
        await self.bot.start_cleaning_games()

    @commands.command(pass_context=True)
    async def teams(self, ctx, *players): #players is discord.Member or str
        """Chooses teams randomly. If the caller is in a voice channel, list will be taken from fellow voicers."""
        author = ctx.message.author
            
        if len(players) == 0:
            try:
                players = author.voice.voice_channel.voice_members
            except AttributeError:
                await self.bot.say("```Error: You are not in a voice channel and you have not provided any players!```")
                return
        
        teammates = []
        for player in players:
            try:
                teammates.append(player)
            except AttributeError:
                teammates.append(str(player))
         
        random.shuffle(teammates)
        list_midpt = len(teammates)//2
        
        message = "**Team 1: **"
        for i, teammate in enumerate(teammates):
            if (i == list_midpt):
                message += "\n\n**Team 2: **"
            try:
                message += "{} ".format(teammate.mention)
            except AttributeError:
                message += "{} ".format(teammate)
        
        await self.bot.say(message, delete_after=self.bot.msg_expire*4)

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('```Format has to be in NdN!```')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command()
    async def joined(self, member : discord.Member):
        """Says when a member joined."""
        await self.bot.say('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command()
    async def test(self):
        """Tests if the bot is on."""
        await self.bot.say("I'm up, I'm up, I'm fucked up but I'm up.")
        
    @commands.command(pass_context=True)
    async def suckmeoff(self, ctx):
        """Sigh David"""
        message = "Ya dude no problem" if ctx.message.author.id == "137022865458331649" else "Suck what?"
        await self.bot.say(message, delete_after=self.bot.msg_expire*2)
            
    @commands.command()
    async def shutdown(self):
        await self.bot.say("Goodbye!")
        sys.exit(0)

def setup(bot):
    bot.add_cog(General(bot))