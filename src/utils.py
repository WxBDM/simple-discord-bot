#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 21:55:28 2021

A utilities file to provide additional functionality.
"""

from datetime import datetime
import discord

def dt_obj_to_str(dt_obj):
    '''Utility function to convert a datetime.datetime object to a string
    representation
    
    Format used: MM/DD/YYYY HH:MM'''
    
    return dt_obj.strftime("%m/%d/%Y %H:%M")

def str_to_dt_obj(string):
    '''Utility function to convert a string in MM/DD/YYYY HH:MM to a datetime
    object.'''
    
    return datetime.strptime(string, "%m/%d/%Y %H:%M")

def get_utc_time():
    return datetime.utcnow()

class Embed:
    
    '''Embed class to aid in creating embeds'''

    def __init__(self, title, description = None, color = 0xffffff):

        if description != None:
            self.embed = discord.Embed(title = title, description = description,
                color = color)
        else:
            self.embed = discord.Embed(title = title, color = color)

    def set_thumbnail(self, url):
        self.embed.set_thumbnail(url = url)

    def add_text(self, name = '\u200b', value = '\u200b', inline = False):
        self.embed.add_field(name = name, value = value, inline = inline)

    def create_embed(self):
        pass

    def to_ctx(self):
        return self.embed

    