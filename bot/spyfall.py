import discord, sys
import spyfallbot
import asyncio
import random, threading

class Spyfall:
    """Represents a game of Spyfall."""
    def __init__(self, bot, game_time=800):
        self.players = []
        self.bot = bot
        
        self.locations = [
            "Airplane", "Bank", "Beach", "Casino", 
            "Cathedral", "Circus", "Corporate Party", "Crusader Army", 
            "Day Spa", "Hospital", "Hotel", "Military Base", 
            "Movie Studio", "Ocean Liner", "Passenger Train", "Pirate Ship", 
            "Polar Station", "Police Station", "Restaurant" ,"School", 
            "Service Station", "Space Station", "Submarine", "Supermarket", 
            "Broadway Theater", "University"]
        self.dlc_locations = [
            "Hogwarts", "Death Star", "World War II Battlefield", "Senior Prom", "Terrorist Training Camp"]
        self.dlc_added = False
        self.running = False
    def add_player(self, player : discord.Member):
        if self.running:
            raise RuntimeError("```ERR: Game is running!```")
        if player not in self.players:
            self.players.append(player)
        else:
            raise ValueError("```ERR: You are already added!```")         
        
    def remove_player(self, player : discord.Member):
        if not self.running:
            raise RuntimeError("```ERR: Game is running!```")
        if player in self.players:
            self.players.remove(player)
        else:
            raise ValueError("```ERR: You aren't even playing!```")
        
    def playerlist(self):
        return "There are {} players: {}".format(len(self.players), [player.display_name for player in self.players]) if self.players else "No one is playing! :frowning:" 
        
    async def start(self, use_dlc):
        if self.running:
            raise RuntimeError("```ERR: Game is running!```")
        self.running = True

        random.shuffle(self.players)
        
        if not self.dlc_added and use_dlc:
            self.locations.extend(self.dlc_locations)
            self.dlc_added = True
        current_location = random.choice(self.locations)
        
        async def deal_cards(self):
            for i, player in enumerate(self.players):
                card = "You are the spy!" if i == len(self.players)-1 else "Location: {}".format(current_location)
                await self.bot.send_message(player, card)
         
        await deal_cards(self)
        await asyncio.sleep(10)
        if self.running:
            self.stop(reuse_players=True)
        
    def stop(self, reuse_players):
        if not self.running: 
            raise RuntimeError("```ERR: Game hasn't started!```")
        self.running = False
        
        if not reuse_players:
            players = []
       
        
        
        