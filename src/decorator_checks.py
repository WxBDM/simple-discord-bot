#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:11:11 2021

This file is used to check roles and channels in a given discord server.

"""

from discord.ext import commands

def is_role_id(roleID):
    '''Decorater used to determine if the user ID is valid for role checking.'''
    
    def is_role_id_predicate(ctx):
        
        role_list = [x.id for x in ctx.message.author.roles] # get list of roles
        
        if roleID in role_list:
            return True # the user running the command has the role.
        
        return False # the user running the command is not of the role.
    
    return commands.check(is_role_id_predicate)


def is_channel(expected_channel_id, this_channel_id):
    '''Decorater used to determine if the user ID is valid for role checking.'''
    
    def is_channel_predicate(ctx):
                
        if expected_channel_id == this_channel_id:
            return True # the user running the command is in the right channel
        
        return False # the user running the command is in the wrong channel.
    
    return commands.check(is_channel_predicate)
