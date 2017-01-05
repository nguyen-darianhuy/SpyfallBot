from bot import SpyfallBot
import discord, sys
from discord.ext import commands

bot = SpyfallBot(command_prefix='?', msg_expire=30, help_attrs=dict(hidden=True)) #hidden=True doesn't seem to be working

extensions = [
    "cogs.general_cog",
    "cogs.spyfall_cog",
]

for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print("Failed to load extension {}\n{}: {}".format(extension, type(e).__name__, e)) #brilliant hack borrowed from RoboDanny
        
@bot.event
async def on_ready():
    print('Logged in as\n{}\n{}'.format(bot.user.name, "------"))
        
    await bot.start_cleaning_games()
    
@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.MissingRequiredArgument):
        msg = "You are missing arguments! Try using `{}help command`".format(bot.command_prefix)
    else:
        raise error
    await bot.send_message(channel, msg)
    
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')