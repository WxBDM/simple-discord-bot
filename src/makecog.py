#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:52:37 2021

This file generates general cogs for the user so that they don't have to
    create their own.

"""

import os
import sys

cwd = os.getcwd()

# check to make sure directory and file name is there.
if len(sys.argv) != 2:
    print("Only include 1 name for cog stub.")
    exit()
     
# capitalize the stub name, also remove "cog" at the end in the event they
# accidentally put it there.
stub_name = sys.argv[1].capitalize()
if stub_name[-3:].lower() == 'cog':
    stub_name = stub_name[:-3]

if stub_name + "cog.py" in list(os.listdir(os.getcwd())):
    print("ERROR: {}cog.py already in directory.".format(stub_name))
    exit()
    
stub = f"""
from discord.ext import commands

class {stub_name}Commands(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.args = args
        self.kwargs = kwargs
        
        # =============================
        # put any instanced variables here.
        # =============================
        
    # =======================
    # If you'd like role/channel checking, use the below (cog_check) method.
    # Note that this is specific to this cog.
    #
    # async def cog_check(self, ctx):
    #   '''This method is used to check a role/channel'''
    #    
    #   if ctx.message.author.id = 1234561234:
    #       return True
    #   return False
    # =======================

    
    # =======================
    # Any "listener" commands (i.e. on_message, on_startup, etc)
    #   will go here. Note: it is important that you have @commands.Cog.listener()
    #   as a decorator!Sample:
    #
    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #    channel = member.guild.system_channel
    #    if channel is not None:
    #        await channel.send('Welcome member!')
    # =======================
    
    
    # ======================
    # Any commands (i.e. .ping, .8ball, .catphoto) that are part of this cog
    #   go here. Note: it is important that you use `self` as an argument.
    #   Sample:
    #
    # @commands.command(aliases=["catpls"])
    # async def catphoto(self, ctx):
    #    '''Sends a cat image'''
    #    await ctx.send("Browse imgur's collection of cats: https://imgur.com/r/cats")
    # ======================

def setup(bot, *args, **kwargs):
    bot.add_cog({stub_name}Commands(bot, *args, **kwargs))

"""

file = open(f"cogs/{stub_name.lower()}cog.py", 'w')
file.write(stub)
print(f"Cog stub successfully created: cogs/{stub_name.lower()}cog.py")
file.close()



