#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import mysql.connector

"""
This method obtains the connector interface
"""
def GetConnection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="development",
            password="development",
            database="bout",
            connect_timeout=10
        )
        
        connection.autocommit = True
        return connection
    except Exception as e:
        raise Exception('Failed to connect to the database', e)
