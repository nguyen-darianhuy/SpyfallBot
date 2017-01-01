import asyncio
import discord, sys
import spyfall
from discord.ext import commands
import random

class SpyfallBot(commands.Bot):
    """Represents a discord Spyfall bot.
    
    This class is a subclass of :class:'discord.commands.Bot'
    
    Attributes
    -----------
    msg_expire : float
        The amount of time in seconds before the bot deletes its own message.
    """
    def __init__(self, command_prefix, msg_expire=0, description=None, **options):
        description = '''A bot that runs spyfall. Built by Darian. Runs on Python.'''
        super().__init__(command_prefix, description=description)
        self.msg_expire = msg_expire
        self.spyfall = spyfall.Spyfall(self)
