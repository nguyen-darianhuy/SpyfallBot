import discord, sys
import spyfallbot
from discord.ext import commands
import random

bot = spyfallbot.SpyfallBot(command_prefix='?', msg_expire=40)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')

@bot.command(pass_context=True)
async def teams(ctx, *players): #players is discord.Member or str
    """Chooses teams randomly. If the caller is in a voice channel, list will be taken from fellow voicers."""
    author = ctx.message.author
        
    if len(players) == 0:
        try:
            players = author.voice.voice_channel.voice_members
        except AttributeError:
            await bot.say("```Error: You are not in a voice channel and you have not provided any players!```", delete_after=bot.msg_expire)
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
    
    await bot.say(message, delete_after=bot.msg_expire*2)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('```Format has to be in NdN!```', delete_after=bot.msg_expire)
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result, delete_after=bot.msg_expire)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices), delete_after=bot.msg_expire)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member), delete_after=bot.msg_expire)

@bot.command()
async def test():
    """Tests if the bot is on."""
    await bot.say("I'm up, I'm up, I'm fucked up but I'm up.", delete_after=bot.msg_expire)
    
@bot.command(pass_context=True)
async def suckmeoff(ctx):
    """Sigh David"""
    message = "Ya dude no problem" if ctx.message.author.id == "137022865458331649" else "Suck what?"
    await bot.say(message, delete_after=bot.msg_expire*2)
        
@bot.command()
async def shutdown():
    await bot.say("Goodbye!")
    sys.exit(0)

# Spyfall Commands

@bot.command(pass_context=True)
async def join(ctx):
    try:
        bot.spyfall.add_player(ctx.message.author)
    except RuntimeError as e:
        await bot.say(e)

@bot.command(pass_context=True)        
async def leave(ctx):
    try:
        bot.spyfall.remove_player(ctx.message.author)
    except RuntimeError as e:
        await bot.say(e)
        
@bot.command()        
async def start():
    try:
        await bot.spyfall.start()
    except RuntimeError as e:
        await bot.say(e)
        
#if __name__ == "__main__":
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')