#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:47:23 2021

Class for administrative commands.

"""

import discord
import utils
from discord.ext import commands

import database as db

class AdminCommands(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.args = args
        self.kwargs = kwargs
        self._db = db.Database() # just instantiate it.

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
        
        '''On a deleted message, post in the deleted messages channel who, when,
        and what the message is.'''
        
        if ctx.message.author == self.bot.user:
            return
        
        # create an embed for a deleted message.
        embed = utils.Embed("Deleted message")
        
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
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        
        '''Logs if a message got edited.'''
        
        if before.author == self.bot.user:
            return
        
        # create an embed for a deleted message.
        embed = utils.Embed("Edited message")
        
        # Embeds are weird, just check the message to see char limit. this can be
        #   changed.
        
        msg_info = [msg.content[0:250] + "..." if len(msg.content) > 250 else msg.content 
                    for msg in [before, after]]
        
        val_msg = f"Channel: <#{before.channel.id}>\n"\
        f"User: <@!{before.author.id}>\n\n"\
        f'**Before:** {msg_info[0]}\n'\
        f'**After:** {msg_info[1]}\n\n'\
        f"Time (UTC): {utils.dt_obj_to_str(utils.get_utc_time())}"
        
        embed.add_text(name = "Details", value = val_msg)
        embed.set_thumbnail(before.author.avatar_url)
        
        # get the logging channel
        channel = before.guild.get_channel(self.kwargs['logging_channel_id'])
        await channel.send(embed = embed.to_ctx()) # send the message
    
    @commands.command()
    async def mute(self, ctx, memberID : int = None):
        
        if memberID is None:
            await ctx.send("You must include a member ID.")
            return
        
        # get the role information in the database. See docstring for return
        #   value structure.
        db_query = self._db.get_muted_role_id()
        if db_query.is_unsucessful:
            await ctx.send(db_query.message)
            return
        
        muted_role_id = db_query.data[0][-1]
        
        # fetch the member with the appropriate ID
        try:
            # returns a member object based off of ID.
            user = await ctx.guild.fetch_member(memberID)
        except:
            await ctx.send(f"User with ID {memberID} not found.")
            return
        
        muted_role = discord.utils.get(ctx.guild.roles, id = muted_role_id)
        if muted_role is None: # it's not in the database.
            await ctx.send(f"Role not found in database. ID: {muted_role_id}.")
            return
        
        # check to make sure that the role of the bot is higher than the muted role.
        guild_roles = list(reversed([r.name for r in ctx.guild.roles]))

        if guild_roles.index(muted_role.name) < guild_roles.index(self.bot.user.name):
            await ctx.send(f"{guild_roles.name} role is higher than me in heirarchy! Make sure it's lower than me.")
            return

        # if we get here, the user will be muted.
        await user.add_roles(muted_role)
        
        # A bit more robust than just sending a message, ensure that the user
        #   has the muted role.
        user_roles = [r.id for r in user.roles]
        if muted_role_id in user_roles:
            await ctx.send("The user is already muted!")
            return
        
        await ctx.send(f"{user.name} has been muted! Remember to unmute them!")
        return

    @commands.command()
    async def unmute(self, ctx, memberID : int = None):
        
        if memberID is None:
            await ctx.send("You must include a member ID.")
            return
        
        # get the role information in the database. See docstring for return
        #   value structure.
        db_query = self._db.get_muted_role_id()
        if db_query.is_unsucessful:
            await ctx.send(db_query.message)
            return
        
        muted_role_id = db_query.data[0][-1]
        
        # fetch the member with the appropriate ID
        try:
            # returns a member object based off of ID.
            user = await ctx.guild.fetch_member(memberID)
        except:
            await ctx.send(f"User with ID {memberID} not found.")
            return
        
        muted_role = discord.utils.get(ctx.guild.roles, id = muted_role_id)
        if muted_role is None: # it's not in the database.
            await ctx.send(f"Role not found in database. ID: {muted_role_id}.")
            return
        
        # check to make sure that the role of the bot is higher than the muted role.
        guild_roles = list(reversed([r.name for r in ctx.guild.roles]))

        if guild_roles.index(muted_role.name) < guild_roles.index(self.bot.user.name):
            await ctx.send(f"{guild_roles.name} role is higher than me in heirarchy! Make sure it's lower than me.")
            return

        # if we get here, the user will be muted.
        await user.remove_roles(muted_role)
        
        # A bit more robust than just sending a message, ensure that the user
        #   has the muted role.
        user_roles = [r.id for r in user.roles]
        if muted_role_id not in user_roles:
            await ctx.send("This person is not muted.")
            return
        
        await ctx.send(f"{user.name} has been unmuted! Freedom, at last!")
        return

    @commands.command(aliases=["addrole"])
    async def registerrole(self, ctx, role : discord.Role = None):
        
        if role is None:
            await ctx.send("You must mention a role.")
            return
    
        db_query = self._db.create_new_role_id(role.name, int(role.id))
        if db_query.is_unsucessful: # if it's unsucessful, send an error message.
            await ctx.send(db_query.message)
            return
        
        # if it was sucessful, send a sucess message.
        await ctx.send(db_query.message)
    
    @commands.command(aliases=['viewroles', 'seeroles', 'showroles'])
    async def seeregisteredroles(self, ctx):
        '''Allows the user to see all of the registered roles.'''
        
        db_query = self._db.get_all_roles()
        if db_query.is_unsucessful: # if it's unsucessful, send an error message.
            await ctx.send(db_query.message)
            return
        
        # if there's nothing in the daatabase.
        if len(db_query.data) == 0:
            await ctx.send("There is nothing in the database.")
            return
            
        # create a string representation of the db query
        roles_str = [f"Name: {row[1]}, ID: {row[2]}" for row in db_query.data]
        roles_str = "\n".join(roles_str)
        
        await ctx.send(roles_str)
        
    @commands.command(aliases=["removerole"])
    async def unregisterrole(self, ctx, role : discord.Role = None):
        
        if role is None:
            await ctx.send("You must mention a role.")
            return
        
        # something a bit more robust is to ensure that the user wants to delete
        #   the role. A confirmation message with a reaction?
        
        # Now remove the role.
        db_query = self._db.remove_role_id(int(role.id))
        if db_query.is_unsucessful: # if it's unsucessful, send an error message.
            await ctx.send(db_query.message)
            return 
        
        await ctx.send(db_query.message)
        
    @commands.command()
    async def whois(self, ctx, memberID):
        '''Allows admins to see who a member is'''
        
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
    
    
    
    