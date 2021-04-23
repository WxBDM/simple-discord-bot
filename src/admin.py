#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:47:23 2021

Class for administrative commands.

"""

import discord
import utils
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass
    
    async def cog_check(self, ctx):
        '''Checks to make sure you have the admin role.'''
        role_list = [x.id for x in ctx.message.author.roles] # get list of roles
        roleID = 727957642844176474
        if roleID in role_list:
            return True # the user running the command has the admin role.
        
        return False
    
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

def setup(bot):
    bot.add_cog(AdminCommands(bot))