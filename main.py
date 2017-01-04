from bot import SpyfallBot
bot = SpyfallBot(command_prefix='?', msg_expire=30)

bot.load_extension("cogs.general_cog")
bot.load_extension("cogs.spyfall_cog")
bot.run('MjEwMTk1NDA5NzA3MDczNTM2.C0d-8A.d3hKVWpPFO87ab7emD3luVc6TXQ')