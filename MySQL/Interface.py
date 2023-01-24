#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import mysql.connector
from dotenv import dotenv_values

"""
This method obtains the connector interface
"""


def get_connection():
    try:

        ''' Load database configuration from dotenv '''
        config = dotenv_values('.env')

        connection = mysql.connector.connect(
            host=config["MYSQL_HOST"],
            port=config['MYSQL_PORT'],
            user=config["MYSQL_USER"],
            password=config["MYSQL_PASS"],
            database=config["MYSQL_DATABASE"],
            connect_timeout=10
        )

        connection.autocommit = True
        return connection
    except Exception as e:
        raise Exception('Failed to connect to the database', e)
