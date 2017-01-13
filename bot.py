import asyncio
import discord, sys
from cogs.spyfall import game
from discord.ext import commands
import random

class SpyfallBot(commands.Bot):
    """
    Represents a discord Spyfall bot.
    
    This class is a subclass of :class:'discord.commands.Bot'
    
    Attributes
    -----------
    msg_expire : float
        The amount of time in seconds before the bot deletes its own message.
    games : dict
        A dictionary of Spyfall games being hosted at the moment.
    """
    def __init__(self, command_prefix, msg_expire=0, **options):
        description = '''A bot that runs Spyfall. Built by Darian. Runs on async Python.'''
        super().__init__(command_prefix, description=description, **options)
        self.msg_expire = msg_expire
        self.games = {}
            
    async def start_cleaning_games(self):
        while self.is_logged_in:
            await asyncio.sleep(3600) #checks every hour
            print("Cleaned {} games".format(self.clean_games()))
        
    def clean_games(self):
        games_deleted = 0
        
        for game_host in list(self.games.keys()): #Necessary to prevent mutatating while iterating sin
            if game_host.status == discord.Status.offline:
                del self.games[game_host]
                games_deleted += 1
                
        return games_deleted
        
    #Override
    def say(self, *args, **kwargs):
        return super().say(*args, delete_after=self.msg_expire)
    
    def format_gameslist(self) -> str:
        gameslist = "```Gamehost            Players\n"
        gameslist += "-"*27
        gameslist += "\n"
        if not self.games:
            gameslist += "There are no games being hosted right now! :("
        for game_host, game in self.games.items():
            gameslist += "{:20}{:7}\n".format("@"+game_host.display_name, len(game.players))
        return gameslist+"```"