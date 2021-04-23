#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:03:12 2021

A file for handling DiscordPy errors.

Totally not copy/pasta from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

"""

import discord
import traceback
import sys
from discord.ext import commands

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return
        
        # ignored errors
        ignored = (commands.NoPrivateMessage, discord.HTTPException,
                   commands.CheckFailure)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'**{ctx.message.content}** is not a valid command.')

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='repeat', aliases=['mimic', 'copy'])
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
