import discord, sys
import random

class Location:
    def __init__(self, name, roles):
        self.name = name
        self.generic_role = roles[0]
        self.roles = roles[1:]
        
class Game:
    """Represents a game of Spyfall."""
    def __init__(self, host, game_time=480):
        self.players = {}
        self.host = host #discord.Member
        self.game_time = game_time #default 8 minutes
        
        self.dlc_added = False
        self.running = False
        
        self.current_location = None
        self.locations = [
            Location("Passenger Airplane", ["Economy Class Passenger", "First Class Passenger", "Air Marshall", "Flight Attendant", "Pilot", "Co-Pilot"]),
            Location("Bank Robbery", ["Customer", "Manager", "Teller", "Security Guard", "Robber", "Getaway Car Driver"]),
            Location("Beach", ["Beach Goer", "Beach Photographer", "Lifeguard", "Ice Cream Salesman", "Wave Surfer", "Snorkeler"]),
            Location("Casino", ["Gambler", "Dealer", "Bartender", "Security Guard", "Manager", "Professional"]),
            Location("Cathedral", ["Church Goer", "Sinner", "Priest", "Pope", "Cardinal", "Choirboy/girl"]),
            Location("Circus Tent", ["Visitor", "Magician", "Clown", "Animal Trainer", "Juggler"]),
            Location("Corporate Meeting", ["Desk-job Worker", "Intern", "Manager","Secretary"]),
            Location("Crusader Army", ["Knight", "Archer", "Squire", "Imprisoned Saracen", "Monk"]),
            Location("Day Spa", ["Customer", "Stylist", "Masseuse", "Manicurist", "Owner"]),
            Location("Embassy", ["Refugee", "Diplomat", "Government Official", "Ambassador", "Security Guard"]),
            Location("Hospital", ["Patient", "Nurse", "Surgeon", "Anesthesiologist", "Intern"]),
            Location("Hotel", ["Guest", "Doorman", "Manager", "Bartender", "Bellboy"]),
            Location("Military Base", ["Soldier", "Deserter", "Medic", "Colonel", "Sniper", "Commander"]),
            Location("Movie Studio", ["Actor", "Cameraman", "Director", "Producer", "Stuntman", "Costume Artist"]),
            Location("Ocean Liner", ["Rich Passenger", "Captain", "Musician", "Bartender", "Waiter"]),
            Location("Passenger Train", ["Passenger", "Train Attendant", "Train Driver", "Stoker", "Railroad Baron"]),
            Location("Pirate Ship", ["Pirate", "Captain", "Prisoner", "Cannoneer", "Piedmont Hills Student", "Cook"]),
            Location("Polar Station", ["Scientist", "Geologist", "Expedition Leader", "Hydrologist", "Meteorologist"]),
            Location("Police Station", ["Criminal", "Parole Officer", "Detective", "Police Officer", "Journalist"]),
            Location("Restaurant", ["Customer", "Waiter", "Chef", "Food Critic", "Sous Chef"]),
            Location("School", ["Student", "Gym Teacher", "Principal", "Janitor", "Cafeteria Lady", "Mr. Zhu"]),
            Location("Auto Repair Station", ["Customer", "Mechanic", "Tire Specialist", "Carwash Girl", "Manager"]),
            Location("Space Station", ["Astronaut", "Alien", "Engineer", "Scientist", "Pilot"]),
            Location("Submarine", ["Sailor", "Sonar Technician", "Radioman", "Navigator", "Electrician"]),
            Location("Supermarket", ["Customer", "Cashier", "Butcher", "Janitor", "Shelf Stocker"]),
            Location("Broadway Theater", ["Visitor", "Actor", "Prompter", "Cashier", "Director", "Prima Donna"]),
            Location("University", ["Undergraduate Student", "Graduate Student", "Professor", "Janitor", "Dean", "Frat Bro"]),
        ]
        self.dlc_locations = [
            #"Hogwarts", "Death Star", "World War II Battlefield", "Senior Prom" #to be included
        ]
        
            
    def add_player(self, player : discord.Member):
        if self.running:
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
        if player not in self.players:
            self.players[player] = None;
        else:
            raise ValueError("```ERR: You are already added!```")         
        
    def remove_player(self, player : discord.Member):
        if self.running:
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
        if player in self.players:
            del self.players[player]
        else:
            raise ValueError("```ERR: You aren't even playing!```")
                
    async def start(self, use_dlc):
        if self.running:
            raise RuntimeError("```ERR: {}'s Game is running!```".format(self.host.display_name))
        self.running = True

        if not self.dlc_added and use_dlc:
            self.locations.extend(self.dlc_locations)
            self.dlc_added = True
            
        random.shuffle(self.players)
        
        self.current_location = random.choice(self.locations)
        self.locations.remove(self.current_location)
        
        current_roles = self.current_location.roles
        random.shuffle(current_roles)
        current_roles.append("Spy")
                
        self._assign_roles()          
            
    def _assign_roles(self):
        location = self.current_location
        for player in self.players:
            try:
                role = location.roles.pop()
            except IndexError:
                role = location.generic_role
                
            self.players[player] = role
                
    def stop(self):
        if not self.running: 
            raise RuntimeError("```ERR: Your game hasn't started!```")
        self.running = False
    
    @property
    def player_names(self) -> str:
        return [player.display_name for player in self.players] if self.players else ":("
        
    @property
    def spy(self):
        for player, role in self.players.items():
            if role == "Spy":
                return player
        
    def declare_players_msg(self) -> str:
        player_amt = len(self.players)
        if player_amt > 1:
            msg = "There are now {} players".format(player_amt)
        elif player_amt == 1:
            msg = "There is now 1 player".format(player_amt)
        else: #this should never execute
            print("Else in game.declare_players_msg executed.")
            msg = "No one is playing!"
        return msg