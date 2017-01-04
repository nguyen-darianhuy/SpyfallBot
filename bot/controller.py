import discord, sys
import spyfall, spyfallbot
from discord.ext import commands
import random
import asyncio

bot = spyfallbot.SpyfallBot(command_prefix='?', msg_expire=30)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await start_timer()
    
async def start_timer():
    while bot.is_logged_in:
        await asyncio.sleep(3600) #checks every hour
        print("Cleaned {} games".format(bot.clean_games))

@bot.command(pass_context=True)
async def teams(ctx, *players): #players is discord.Member or str
    """Chooses teams randomly. If the caller is in a voice channel, list will be taken from fellow voicers."""
    author = ctx.message.author
        
    if len(players) == 0:
        try:
            players = author.voice.voice_channel.voice_members
        except AttributeError:
            await bot.say("```Error: You are not in a voice channel and you have not provided any players!```")
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
    
    await bot.say(message, delete_after=bot.msg_expire*4)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('```Format has to be in NdN!```')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
async def test():
    """Tests if the bot is on."""
    await bot.say("I'm up, I'm up, I'm fucked up but I'm up.")
    
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

def declare_players_msg(game):
    msg = ""
    player_amt = len(game.players)
    if player_amt > 1:
        msg = "There are now {} players".format(player_amt)
    elif player_amt == 1:
        msg = "There is now 1 player".format(player_amt)
    else:
        msg = "No one is playing!"
    return msg
    
@bot.command(pass_context=True)
async def join(ctx, game_host : discord.Member):
    if game_host not in bot.games:
        await bot.say("```ERR: {} isn't hosting a game!```")
        return
    game = bot.games[game_host]
    try:
        player = ctx.message.author
        game.add_player(player)
        await bot.say("{} joined {}'s Spyfall! {}.".format(player.mention, game_host.mention, declare_players_msg(game)))
    except (RuntimeError, ValueError) as e:
        await bot.say(e)
        

@bot.command(pass_context=True)        
async def leave(ctx, game_host : discord.Member):
    if game_host not in bot.games:
        await bot.say("```ERR: {} isn't hosting a game!```")
        await bot.say(game_host)
        await bot.say(bot.games)
        return
        
    game = bot.games[game_host]
    player = ctx.message.author
    
    if player is game_host:
        del bot.games[player]
        await bot.say("{} is no longer hosting a Spyfall game!".format(player.mention))
        return
        
    try:
        game.remove_player(player)
        await bot.say("{} left {}'s Spyfall! {}.".format(player.mention, game_host.mention, declare_players_msg(game)))
    except (RuntimeError, ValueError) as e:
        await bot.say(e)
        
@bot.command()
async def players(game_host : discord.Member):
    if game_host not in bot.games:
        await bot.say("```ERR: {} isn't hosting a game!```")
        return
    game = bot.games[game_host]
    await bot.say("{}: {}".format(declare_players_msg(game), game.get_playerlist()))

@bot.command()
async def games():
    await bot.say(bot.format_gameslist())
    
@bot.command(pass_context=True)        
async def start(ctx, use_dlc=False):
    user = ctx.message.author
    if user not in bot.games:
        bot.games[user] = spyfall.Spyfall(bot, host=user)
        bot.games[user].add_player(user)
        await bot.say("{} is now hosting a Spyfall game! Join by typing: `?join @{}`".format(user.mention, user.display_name))
        return
        
    game = bot.games[user]
    if not game.players:
        voice_members = ctx.message.author.voice_channel.voice_members
        if voice_members:
            map(game.add_player, voice_members)
        else:
            await bot.say("```Error: There are no players!```")
    try:
        await bot.say("**{}'s Spyfall has begun!**".format(user.mention))
        await game.start(use_dlc)
    except RuntimeError as e:
        await bot.say(e, delete_after=bot.msg_expire)
        
@bot.command(pass_context=True)
async def stop(ctx, reuse_players=True):
    user = ctx.message.author
    if user not in bot.games:
        await bot.say("```ERR: You aren't hosting a game!```")
        return
    game = bot.games[user]
    try: 
        game.stop(reuse_players)
        await bot.say("```Manually ended the Spyfall round.```")
    except RuntimeError as e:
        await bot.say(e)
        
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')
