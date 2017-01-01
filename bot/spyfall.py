import discord, sys
import spyfallbot
import random

class Spyfall:
    """Represents a game of Spyfall."""
    def __init__(self, bot):
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
            
        self.running = False
    def add_player(self, player : discord.Member):
        if not self.running:
            self.players.append(player)
        else:
            raise RuntimeError("Game is running!")
        
    def remove_player(self, player : discord.Member):
        if not self.running:
            self.players.remove(player)
        else:
            raise RuntimeError("Game is running!")
        
    async def start(self, use_dlc):
        if self.running:
            raise RuntimeError("Game is running!")
        self.running = True
        random.shuffle(players)
        
        if use_dlc == False or use_dlc.lower().startswith("dlc"):
            locations = locations.append(dlc_locations)
            self.dlc_added = True
        current_location = random.choice(locations)
        
        async def deal_cards(self):
            for i, player in enumerate(self.players):
                card = "You are the spy!" if i == len(self.players)-1 else "Location: {}".format(current_location)
                await self.bot.send_message(player, card)
         
        await deal_cards(self)
        
    def stop(self, reuse_players):
        if not self.running: 
            raise RuntimeError("Game hasn't started!")
        self.running = False
        
        if ()
        
        