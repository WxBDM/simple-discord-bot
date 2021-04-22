#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 21:55:28 2021

A utilities file to provide additional functionality.
"""

from datetime import datetime

def dt_obj_to_str(dt_obj):
    '''Utility function to convert a datetime.datetime object to a string
    representation
    
    Format used: MM/DD/YYYY HH:MM'''
    
    return dt_obj.strftime("%m/%d/%Y %H:%M")

def str_to_dt_obj(string):
    '''Utility function to convert a string in MM/DD/YYYY HH:MM to a datetime
    object.'''
    
    return datetime.strptime(string, "%d/%m/%Y %H:%M")

