#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:47:23 2021

Class for administrative commands.

"""

import discord
import utils
import os
import sys
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, bot, admin_id, *args, **kwargs):
        self.bot = bot
        self.admin_id = admin_id
        
        # args and kwargs, in case they want them.
        self.args = args
        self.kwargs = kwargs

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass
    
    async def cog_check(self, ctx):
        '''Checks to make sure you have the admin role.'''
        
        role_list = [x.id for x in ctx.message.author.roles] # get list of roles
        if self.admin_id in role_list:
            return True # the user running the command has the admin role.
        
        # If the user doesn't have the role, let them know.
        role_name = discord.utils.get(ctx.guild.roles, id = self.admin_id)
        if role_name == None:
            await ctx.send("You do not have the role needed to use this command.")
            await ctx.send(f"Note: Unable to find role name. ID: {self.admin_id}")
            return False
        
        await ctx.send(f"You must have the {role_name} role in order to run this command.")
        return False
    
    @commands.command(aliases=["r"]) #can either do .r or .restart
    async def restart(self,ctx):  
        '''Restarts the bot (used for dev purposes only)'''
        
        await ctx.message.add_reaction("\U00002705")
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)
        
    @commands.command()
    async def whois(self, ctx, memberID):
        
        if memberID == None:
            await ctx.send("You must include a user ID")
            return
        
        try:
            # returns a member object based off of ID.
            user = await ctx.guild.fetch_member(memberID)
        except:
            await ctx.send("User with that ID not found.")
            return
    
        # create an embed with the title of the user, thumbnail is avatar.
        embed_title = "Information for User: " + user.display_name
        embed = discord.Embed(title = embed_title)
        embed.set_thumbnail(url = user.avatar_url)
        
        # Add the usernanme
        embed.add_field(name = "Username", value = user.name + "#" + user.discriminator, 
                        inline = True)
        # Add the ID
        embed.add_field(name = "User ID", value = user.id, inline = True)
    
        # Roles in the server
        roles = user.roles
        roles.pop(0) # removes @everyone
        roles = reversed(roles)
        role_list = ["<@&{}>".format(role.id) for role in roles]
        role_str = ", ".join(role_list)
        embed.add_field(name = "Roles", value = role_str, inline = False)
        
        # When did the account join?
        joined_at_f = utils.dt_obj_to_str(user.joined_at)
        embed.add_field(name = "Joined Server", value = joined_at_f, inline = True)
        
        # When the account was created.
        created_at_f = utils.dt_obj_to_str(user.created_at)
        embed.add_field(name = "Account Created", value = created_at_f, inline = True)    
        
        # Send the message!
        await ctx.send(embed = embed)   

def setup(bot, admin_id, *args, **kwargs):
    bot.add_cog(AdminCommands(bot, admin_id, *args, **kwargs))