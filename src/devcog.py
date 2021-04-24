
from discord.ext import commands
import os
import sys

class DevCommands(commands.Cog):
    
    '''A cog specifically for developers (i.e. bot owner).'''

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.args = args
        self.kwargs = kwargs
        
        # =============================
        # put any instanced variables here.
        # =============================
        
    async def cog_check(self, ctx):
        '''This method is used to check a role/channel'''
        
        if ctx.message.author.id == self.bot.owner_id:
            return True
      
        await ctx.send("You cannot run this command, as you are not a developer.")
        return False

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')
    
    @commands.command(aliases=["r"])
    async def restart(self, ctx):    
        await ctx.message.add_reaction('\U0001f44d')
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)

def setup(bot, *args, **kwargs):
    bot.add_cog(DevCommands(bot, *args, **kwargs))

