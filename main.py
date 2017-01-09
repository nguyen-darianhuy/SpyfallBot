from bot import SpyfallBot
import discord, sys
from discord.ext import commands

bot = SpyfallBot(command_prefix='?', msg_expire=10, help_attrs=dict(hidden=True))

extensions = [
    "cogs.general_cog",
    "cogs.spyfall_cog",
]

for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        #brilliant hack borrowed from RoboDanny
        print("Failed to load extension {}\n{}: {}".format(extension, type(e).__name__, e)) 
        raise e
        
@bot.event
async def on_ready():
    print('Logged in as:\n{}\n{}'.format(bot.user.name, "-"*len(bot.user.name)))
        
    await bot.start_cleaning_games()
    
@bot.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    command = ctx.command
    msg = ""
    #user errors
    if isinstance(error, commands.MissingRequiredArgument):
        msg = "```ERR: {}```".format(str(error))
        await bot.send_message(channel, msg)
        
        help = bot.commands["help"]
        await ctx.invoke(help, ctx.invoked_with)
        
    #system errors
    elif isinstance(error, commands.CommandInvokeError): #also borrowed from RoboDanny
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
    elif isinstance(error, commands.CommandNotFound):
        print("{0.display_name} tried to use the command {1}".format(author, command))
    
@bot.command(hidden=True)
async def shutdown():
    """Shuts the bot down."""
    await bot.say("Goodbye!")
    
    await bot.logout();
    await bot.close();
    raise KeyboardInterrupt("Bot Shutdown.")
        
@bot.command(hidden=True)
async def test():
    """A quick ping to test if the bot is working."""
    await bot.say("I'm up, I'm up, I'm fucked up but I'm up.")
    
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')