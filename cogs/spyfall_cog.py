import discord, sys
from .spyfall.game import Game
from discord.ext import commands

class Spyfall:
    """Cog for running a game of Spyfall."""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def join(self, ctx, game_host : discord.Member):
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```")
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
        if not game_host:
            game_hot = ctx.message.author
            
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```")
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
        if not game_host:
            game_host = ctx.message.author
            
        if game_host not in self.bot.games:
            await self.bot.say("```ERR: {} isn't hosting a game!```")
            return
            
        game = self.bot.games[game_host]
        await self.bot.say("{}: {}".format(game.declare_players_msg(), game.player_names))

    @commands.command()
    async def games(self):
        await self.bot.say(self.bot.format_gameslist())
        
    @commands.command(pass_context=True)        
    async def start(self, ctx, use_dlc=None):
        user = ctx.message.author
        
        if user not in self.bot.games:
            self.bot.games[user] = Game(self.bot, host=user)
            self.bot.games[user].add_player(user)
            await self.bot.say("{} is now hosting a Spyfall game! Join by typing: `?join @{}`".format(user.mention, user.display_name))
            return
            
        game = self.bot.games[user]
        if not game.players:
            voice_members = ctx.message.author.voice_channel.voice_members
            if voice_members:
                map(game.add_player, voice_members)
            else:
                await self.bot.say("```Error: There are no players!```")
        try:
            await self.bot.say("**{}'s Spyfall has begun!**".format(user.mention))
            await game.start(use_dlc)
        except RuntimeError as e:
            await self.bot.say(e, delete_after=self.bot.msg_expire)
            
    @commands.command(pass_context=True)
    async def stop(self, ctx, reuse_players="reuse"):
        user = ctx.message.author
        if user not in self.bot.games:
            await self.bot.say("```ERR: You aren't hosting a game!```")
            return
        game = self.bot.games[user]
        try: 
            game.stop(reuse_players)
            await self.bot.say("```The Spyfall round has been ended.\nIt turns out that {} was the Spy at the {}!```".format(game.spy.display_name, game.current_location.name))
        except RuntimeError as e:
            await self.bot.say(e)

def setup(bot):
    bot.add_cog(Spyfall(bot))