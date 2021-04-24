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

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.args = args
        self.kwargs = kwargs

    async def cog_check(self, ctx):
        '''Checks to make sure you have the admin role.'''
        
        admin_id = self.kwargs['admin_id']
        
        role_list = [x.id for x in ctx.message.author.roles] # get list of roles
        if admin_id in role_list:
            return True # the user running the command has the admin role.
        
        # If the user doesn't have the role, let them know.
        role_name = discord.utils.get(ctx.guild.roles, id = admin_id)
        if role_name == None:
            await ctx.send("You do not have the role needed to use this command.")
            await ctx.send(f"Note: Unable to find role name. ID: {self.admin_id}")
            return False
        
        # if all goes right, it should print this message. Above is for when
        #   something goes wrong and it can't find the role.
        await ctx.send(f"You must have the {role_name} role in order to run this command.")
        return False

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        # create an embed for a deleted message.
        embed = utils.Embed(f"Deleted message")
        
        # Embeds are weird, just check the message to see char limit. this can be
        #   changed.
        if len(message.content) > 250:
            val_msg = f"Channel: <#{message.channel.id}>\n"\
            f"User: <@!{message.author.id}>\nMessage: {message.content[0:250]}...\n\n"\
            f"Time (UTC): {utils.dt_obj_to_str(utils.get_utc_time())}"
        else:
            val_msg = f"Channel: <#{message.channel.id}>\n"\
                f"User: <@!{message.author.id}>\nMessage: {message.content}\n\n"\
                f"Time (UTC): {utils.dt_obj_to_str(utils.get_utc_time())}"
        
        embed.add_text(name = "Details", value = val_msg)
        embed.set_thumbnail(message.author.avatar_url)
        
        # get the logging channel
        channel = message.guild.get_channel(self.kwargs['logging_channel_id'])
        await channel.send(embed = embed.to_ctx()) # send the message
        
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

def setup(bot, *args, **kwargs):
    bot.add_cog(AdminCommands(bot, *args, **kwargs))