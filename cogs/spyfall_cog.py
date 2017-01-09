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

    @commands.command(pass_context=True)
    async def leave(self, ctx, game_host : discord.Member = None):
        """Leave a hosted Spyfall game.\nEX: ?leave @Noah\nNOTE: The host can close his/her room with only ?leave"""
        if not game_host:
            game_host = ctx.message.author
            
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```".format(game_host.display_name))
            return
            
        game = self.bot.games[game_host]
        player = ctx.message.author
        
        if player is game_host:
            del self.bot.games[player]
            await self.bot.say("{} is no longer hosting a Spyfall game!".format(player.mention))
            return
            
        try:
            game.remove_player(player)
            await self.bot.say("{} left {}'s Spyfall! {}.".format(player.mention, game_host.mention, game.declare_players_msg()))
        except (RuntimeError, ValueError) as e:
            await self.bot.say(e)
            
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
        user = ctx.message.author
        
        if user not in self.bot.games:
            self.bot.games[user] = Game(self.bot, host=user)
            self.bot.games[user].add_player(user)
            await self.bot.say("{0.mention} is now hosting a Spyfall game! Join by typing: `?join @{0.display_name}`".format(user))
            return
            
        game = self.bot.games[user]
        if not game.players:
            voice_members = ctx.message.author.voice_channel.voice_members
            if voice_members:
                map(game.add_player, voice_members)
            else:
                await self.bot.say("```Error: There are no players!```")
        try:
            await self.bot.say("**{}'s Spyfall has begun!**".format(user.display_name))
            await game.start(use_dlc)
        except RuntimeError as e:
            await self.bot.say(e, delete_after=self.bot.msg_expire)
            
    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stops a currently running Spyfall game, used by room hosts."""
        user = ctx.message.author
        if user not in self.bot.games:
            await self.bot.say("```ERR: You aren't hosting a game!```")
            return
        game = self.bot.games[user]
        try: 
            game.stop()
            msg = "```The Spyfall round has been ended.\n"
            msg += "It turns out that {0.spy.display_name} was the Spy at the {0.current_location.name}!```".format(game)
            await self.bot.say(msg)
        except RuntimeError as e:
            await self.bot.say(e)

def setup(bot):
    bot.add_cog(Spyfall(bot))