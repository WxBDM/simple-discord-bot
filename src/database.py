#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 17:06:58 2021

A file to interact with a database locally. It utilizes the SQLite funcitonality
from Python's standard library.

Note that this purely handles the database communications; there is no outputs
    sent to the discord bot.

"""

import sqlite3
import os
import sys

from dataclasses import dataclass, field

class Database:

    @dataclass
    class ErrorMsg:
        '''A dataclass for error messages. Makes things easier on user end
        to check if there was an error'''
        
        message: str # the error message.
        is_unsucessful: bool = True # used for user readability for the bot.
        
    def __init__(self):
        self.file = "simple-database.db"
    
    def _check_if_table_exists(self, table_name):
        
        '''Checks to see if a table exists.
        
        Returns True if it does, False otherwise.
        
        Assumes the connection is open.'''
        
        exists = None
        query_str = f"SELECT * FROM {table_name}"
        
        try:
            # just try getting the table.
            self._cursor.execute(query_str)
        except sqlite3.OperationalError:
            exists = False
            
        if exists is None:
            exists = True
            
        return exists
    
    def _check_if_row_exists(self, table_name, column_name, row_element):
        '''Checks to ensure that a row exists. This should be called after
        you check to make sure the table exists. This should also only be called
        if updating a row in the database.
        
        Note that this checks the ID.
        
        Returns True if it does, returns False otherwise.
        
        Assumes the connection is open.'''
        
        exists = None
        
        # in the instance it's a number.
        if isinstance(row_element, int):
            row_name = row_element
        else:
            row_name = row_element.lower()
        
        query_str = f"SELECT EXISTS(SELECT * FROM {table_name} WHERE {column_name.lower()} = '{row_name}');"

        # Exists acts a bit different, it will return 0 if it doesn't exist
        #   or it'll return 1 if it exists.

        try:
            query = self._cursor.execute(query_str)
            if query.fetchone()[0] == 0: 
                exists = False
        except sqlite3.OperationalError: # if it gets here, this row doesn't exist.
            exists = False
        
        if exists is None:
            exists = True
        
        return exists
    
    def open_connection(self, **kwargs):
        '''Opens the connection to the DB.'''
        
        try: # future update: this needs to get changed to checking if file exists.
            open(self.file) # try to open the file.
        except IOError:
            msg = f"Error: {self.file} not found."
            return self.self.self.ErrorMsg(msg)
        
        # file was sucessfully
        self._conn = sqlite3.connect(self.file, **kwargs)     
        self._cursor = self._conn.cursor()
        
    def close_connection(self, **kwargs):
        '''Closes the connection to the DB. Resets variables.'''
        
        self._conn.close(**kwargs)
        
        # reset these variables.
        self._conn = None
        self._cursor = None
    
    def _modify_id(self, table_name, modification_type, ID, verbose, name = None):
        
        # more data validation
        mod_type = modification_type.lower()
        
        # make sure it's either add or emove
        if mod_type not in ['add', 'modify', 'remove']:
            msg = f"Modification should be either 'add' or 'modify'. Found: {modification_type}."
            if verbose: print(msg)
            return self.ErrorMsg(msg)
        
        # ensure data type is valid for name and ID
        if not isinstance(ID, int):
            msg = f"ID must be of type int. Found: {type(ID)}."
            if verbose: print(msg)
            return self.ErrorMsg(msg)
        
        if not isinstance(name, str):
            msg = f"name must be of type string. Found: {type(name)}."
            if verbose: print(msg)
            return self.ErrorMsg(msg)
        
        # Data validation OK.
        if verbose: print(f"Data validation OK. Table name: {table_name}")
        
        self.open_connection()
        
        # check to make sure table is in there.
        table_exists = self._check_if_table_exists(table_name)
        if not table_exists:
            msg = f"Table {table_name} does not exist."
            if verbose: print(msg)
            self.close_connection()
            return self.ErrorMsg(msg)
        
        # check to make sure element exists
        row_exists = self._check_if_row_exists(table_name, 'discordID', ID)
        
        if mod_type == 'modify':
            if not row_exists:
                msg = f"{name} role doesn't exist in {table_name} table."
                if verbose: print(msg)
                self.close_connection()
                return self.ErrorMsg(msg)
        
            query = f"UPDATE {table_name} SET name = ?, discordID = ?"
            self._cursor.execute(query, (name.lower(), ID))
            self._conn.commit()
            
            self.close_connection()
            return self.ErrorMsg('Sucessful', False)
        
        elif mod_type == "add":
            if row_exists:
                msg = f"{name} role is already registered."
                if verbose: print(msg)
                self.close_connection()
                return self.ErrorMsg(msg)
    
            query = f"INSERT INTO {table_name}(name, discordID) VALUES(?, ?)"
            self._cursor.execute(query, (name.lower(), ID))
            self._conn.commit()
            
            self.close_connection()
            return self.ErrorMsg(f"{name} has been registered.", False)
        
        elif mod_type == "remove":
            if not row_exists:
                msg = f"{ID} doesn't exist in {table_name} table."
                if verbose: print(msg)
                self.close_connection()
                return self.ErrorMsg(msg)
        
            query = f"DELETE FROM {table_name} WHERE discordID='{ID}';"
            print(query)
            self._cursor.execute(query)
            self._conn.commit()
            
            self.close_connection()
            return self.ErrorMsg(f'Sucessfully removed {ID}', False)
        
        else:
            msg = "Something not tested has gone wrong."
            if verbose: print(msg)
            return self.ErrorMsg(msg)

    
    # ===========
    # USER DEFINED FUNCTIONS
    # ===========    

    def create_new_channel_id(self, channel_name, channel_id, verbose = False):
        '''Creates a new channel ID in the database'''
        
        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('channels', 'add', channel_id, verbose, name = channel_name)

    def create_new_role_id(self, role_name, role_id, verbose = False):
        '''Creates a new role ID in the database'''
        
        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('roles', 'add', role_id, verbose, name = role_name)
    
    def remove_channel_id(self, channel_id, verbose = False):
        '''Removes a channel ID in the database'''
        
        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('channels', 'remove', channel_id, verbose, name = "")

    def remove_role_id(self, role_id, verbose = False):
        '''Removes a role ID in the database'''
        
        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('roles', 'remove', role_id, verbose, name = "")
    
    def set_channel_id(self, channel_name, channel_id, verbose = False):
        '''Modifies a channel ID in the database'''
        
        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('channels', 'modify', channel_id, verbose, name = channel_name)
    
    def set_role_id(self, role_name, role_id, verbose = False):
        '''Modifies a role ID in the database'''

        # (table_name, modification_type, name, discordID, verbose)
        return self._modify_id('roles', 'modify', role_id, verbose, name = role_name)
        
    def get_muted_role_id(self, verbose = False):
        
        self.open_connection()
        
        # check to make sure table is in there.
        table_exists = self._check_if_table_exists('roles')
        if not table_exists:
            msg = "Table roles does not exist."
            if verbose: print(msg)
            self.close_connection()
            return self.ErrorMsg(msg)
        
        role_exists = self._check_if_row_exists('roles', 'name', 'muted')
        if not role_exists:
            msg = "Muted role does not exist."
            if verbose: print(msg)
            self.close_connection()
            return self.ErrorMsg(msg)
        
        query_str = "SELECT * FROM roles WHERE name = 'muted'"
        query = self._conn.execute(query_str)
        query = query.fetchall()
        self.close_connection()
        
        # prep to give user the muted role id.
        return_val = self.ErrorMsg('Retrieved muted role sucessfully!', False)
        return_val.data = query
        return return_val
    
    def get_all_roles(self, verbose = False):
        
        self.open_connection()
        
        # check to make sure table is in there.
        table_exists = self._check_if_table_exists('roles')
        if not table_exists:
            msg = "Table roles does not exist."
            if verbose: print(msg)
            self.close_connection()
            return self.ErrorMsg(msg)
    
        query_str = "SELECT * FROM roles"
        query = self._conn.execute(query_str)
        query = query.fetchall()
        self.close_connection()
        
        return_val = self.ErrorMsg('All roles have been retrieved.', False)
        return_val.data = query
        return return_val
    
    # ===================
    # Put here your functions for database communications.
    # Note that you will have to call self.open_connection()
    #   before you execute a SQL query. BE SURE YOU CLOSE THE DATABASE
    #   BY DOING self.close_connection() BEFORE REUTURNING A VALUE
    
    
    # ===================


if __name__ == "__main__":
    db = Database()
    print(db.get_all_roles())
