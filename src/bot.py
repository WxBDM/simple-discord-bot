#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:00:57 2021

A simplistic discord bot. This can be built and expanded upon. It contains basic
administrative-like stuff (mute, whois, etc), as well as a few fun commands right
out of the box.

It also includes functionality to read/write to/from a database to store information
such as the bot owner ID, channels to write into, etc.

"""

import discord
from discord.ext import commands
import os
import random
import sys

# package-related imports
import decorator_checks as checks
import admin
import utils

bot = commands.Bot(command_prefix = '.') # create the bot
bot.remove_command('help') # this will allow you to get the help menu.

# Instatiate classes for admin and general usage
admin_commands = admin.AdminCommands(bot)
admin.setup(bot)

# Role ID listing. The database uses


@bot.event # when the bot first starts up, send a message and let dev know it's working.
async def on_ready():        
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------\n')

# When someone sends a message in Discord, we want this to run.
@bot.event
async def on_message(message):

    # need this here in the event that the bot calls itself. Can be bad.
    if message.author == bot.user:
        return    

    # ===============
    # More logic goes here whenever someone messages the channel.
    # ===============

    # You need this code here, otherwise the bot won't work!
    await bot.process_commands(message)

# This is where we handle errors.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # If the command is not found, then tell the user it's not found.
        await ctx.send("Command not found.")
        
    elif isinstance(error, commands.errors.CheckFailure):
        pass
    else:
        # If you would like to log what happened, code can go here to do so.
        raise error

# This is helpful so that you don't have to continually restart terminal
# to restart the bot. Huge +1 for devs.
@bot.command(aliases=["r"]) #can either do .r or .restart
@checks.has_role_id(727957642844176474)
async def restart(ctx):    
    await ctx.message.add_reaction("\U00002705")
    os.system("clear")
    os.execv(sys.executable, ['python'] + sys.argv)

# do an 8ball response
@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, text : str = None):
    
    if text == None:
        await ctx.send("You have to include a phrase!")
        return
    
    choices = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.',
             'Cannot predict now.', 'Concentrate and ask again.',
             "Don't count on it.", 'It is certain.', 'It is decidedly so.']
    
    n = random.randint(0, len(choices))
    
    await ctx.send(choices[n])


bot.run(os.getenv('TORNADO_TALK_SECRET_KEY'))
