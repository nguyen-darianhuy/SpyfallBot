import discord, sys
from .spyfall.game import Game
from discord.ext import commands

class Spyfall:
    """Cog for running a game of Spyfall."""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def join(self, ctx, game_host : discord.Member):
        """Join a hosted Spyfall game.\nEX: ?join @LoopyFruits"""
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```".format(game_host.display_name))
            return
        game = self.bot.games[game_host]
        try:
            player = ctx.message.author
            game.add_player(player)
            await self.bot.say("{} joined {}'s Spyfall! {}.".format(player.mention, game_host.mention, game.declare_players_msg()))
        except (RuntimeError, ValueError) as e:
            await self.bot.say(e)
            return

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Leave a hosted Spyfall game.\nNOTE: If the host leaves, the room will close!"""
        player = ctx.message.author
        
        for game in self.bot.games.values():
            if player in game.players:
                break
        else:
            await self.bot.say("```ERR: You aren't in a game!```")
            return
            
        try:
            if player is game.host:
                game.remove_player(player)
                del self.bot.games[player]
                msg = "{} is no longer hosting a Spyfall game!".format(player.mention)
            else:
                game.remove_player(player)
                msg = "{} left {}'s Spyfall! {}.".format(player.mention, game.host.mention, game.declare_players_msg())
        except (RuntimeError, ValueError) as e:
            msg = e
        finally:
            await self.bot.say(msg)
            
    @commands.command(pass_context=True)
    async def players(self, ctx, game_host : discord.Member = None):
        """List the players in someone's Spyfall game.\nEX: ?players @Lily\nNOTE: The host can use it without naming the game host."""
        player = ctx.message.author
        if not game_host:
            game_host = player
            
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```".format(game_host.display_name))
            return
        
        game = self.bot.games[game_host]
        await self.bot.say("{}: {}".format(game.declare_players_msg(), game.player_names))

    @commands.command()
    async def games(self):
        """List the Spyfall rooms currently being hosted."""
        await self.bot.say(self.bot.format_gameslist())
        
    @commands.command(pass_context=True)
    async def start(self, ctx, use_dlc=None):
        """Opens a Spyfall room, or starts a Spyfall game if used as a host.\nEX: ?start dlc"""
        player = ctx.message.author
        
        if player not in self.bot.games:
            self.bot.games[player] = Game(host=player)
            self.bot.games[player].add_player(player)
            await self.bot.say("{0.mention} is now hosting a Spyfall game! Join by typing: `?join @{0.display_name}`".format(player))
            return
            
        game = self.bot.games[player]
      
        try:
            await game.start(use_dlc)
            await self.bot.say("**{}'s Spyfall has begun!**".format(player.display_name))
        except RuntimeError as e:
            await self.bot.say(e, delete_after=self.bot.msg_expire)
            return
           
        for player, role in game.players.items():
            card_msg = "{}'s Spyfall game:\n".format(game.host.display_name)
            if role == "Spy":
                card_msg += "Location: **UNKNOWN**\nYou are the **Spy**!"
            else:
                card_msg += "Location: **{}**\nRole: **{}**".format(game.current_location.name, role)
                
            await self.bot.send_message(player, card_msg)
            
    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stops a currently running Spyfall game, used by room hosts."""
        player = ctx.message.author
        if player not in self.bot.games:
            await self.bot.say("```ERR: You aren't hosting a game!```")
            return
        game = self.bot.games[player]
        try: 
            game.stop()
            msg = "```The Spyfall round has been ended.\n"
            msg += "It turns out that {0.spy.display_name} was the Spy at the {0.current_location.name}!```".format(game)
            await self.bot.say(msg)
        except RuntimeError as e:
            await self.bot.say(e)
            return

def setup(bot):
    bot.add_cog(Spyfall(bot))