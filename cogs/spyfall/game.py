import discord, sys
import asyncio
import random, threading

class Game:
    """Represents a game of Spyfall."""
    def __init__(self, bot, host, game_time=480):
        self.players = []
        self.bot = bot
        self.host = host #discord.Member
        self.game_time = game_time #default 8 minutes
        self.info = """
            A game of Spyfall is made up of several short rounds. 
            In each round the players find themselves in a certain location with a specific role assigned to each player. 
            One player is always a spy who doesn’t know where they are. 
            The spy’s mission is to listen carefully, identify the location, and keep from blowing his cover. 
            Each non-spy must give an oblique hint to the other non-spies suggesting that he knows the location’s identity, 
            thus proving he’s not the spy. 
            Observation, concentration, nonchalance, and cunning — 
            you’ll need all of them in this game.
            
            Stay on your toes!
            """
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
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
        if player not in self.players:
            self.players.append(player)
        else:
            raise ValueError("```ERR: You are already added!```")         
        
    def remove_player(self, player : discord.Member):
        if self.running:
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
        if player in self.players:
            self.players.remove(player)
        else:
            raise ValueError("```ERR: You aren't even playing!```")
    
    async def start(self, use_dlc):
        if self.running:
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
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
            
    def stop(self, reuse_players):
        if not self.running: 
            raise RuntimeError("```ERR: {}'s Game hasn't started!```".format(self.host.display_name))
        self.running = False
        
        if not reuse_players:
            players = []
    
    @property
    def player_names(self) -> str:
        return [player.display_name for player in self.players] if self.players else ":frowning:"
        
    def declare_players_msg(self) -> str:
        msg = ""
        player_amt = len(self.players)
        if player_amt > 1:
            msg = "There are now {} players".format(player_amt)
        elif player_amt == 1:
            msg = "There is now 1 player".format(player_amt)
        else:
            msg = "No one is playing!"
        return msg