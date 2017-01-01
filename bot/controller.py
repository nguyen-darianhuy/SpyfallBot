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
    
    await bot.say(message, delete_after=bot.msg_expire*3)

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
        player = ctx.message.author
        bot.spyfall.add_player(player)
        await bot.say("{} joined Spyfall! There are now {} players.".format(player.mention, len(bot.spyfall.players)))
    except (RuntimeError, ValueError) as e:
        await bot.say(e, delete_after=bot.msg_expire)
        

@bot.command(pass_context=True)        
async def leave(ctx):
    try:
        player = ctx.message.author
        bot.spyfall.remove_player(player)
        await bot.say("{} left Spyfall! There are now {} players.".format(player.mention, len(bot.spyfall.players)))
    except (RuntimeError, ValueError) as e:
        await bot.say(e, delete_after=bot.msg_expire)
        
@bot.command()
async def players():
    await bot.say(bot.spyfall.playerlist())
    
@bot.command(pass_context=True)        
async def start(ctx, use_dlc=False):
    if not bot.spyfall.players:
        voice_members = ctx.message.author.voice_channel.voice_members
        if voice_members:
            map(bot.spyfall.add_player, voice_members)
        else:
            await bot.say("```Error: There are no players!```")
    try:
        await bot.say("**Spyfall has begun!**")
        await bot.spyfall.start(use_dlc)
    except RuntimeError as e:
        await bot.say(e, delete_after=bot.msg_expire)
        
@bot.command(pass_context=True)
async def stop(reuse_players=True):
    try: 
        bot.spyfall.stop(reuse_players)
        await bot.say("```Manually ended the Spyfall round.```")
    except RuntimeError as e:
        await bot.say(e)
        
#if __name__ == "__main__":
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')