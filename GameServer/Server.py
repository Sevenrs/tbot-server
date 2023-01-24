#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import socket
import _thread
from . import Client, Connection, session


class Socket:
    """
    GameServer constructor
    """

    def __init__(self, port, relay_tcp_server):
        self.port = port

        # Client container
        self.clients = []

        # Client ID container
        self.client_ids = []

        # Room container
        self.rooms = {}

        # Session container and session handler
        self.sessions = []
        self.session_handler = None

        # Access to the relay server
        self.relay_server = relay_tcp_server

    """
    This method will listen for new connections
    """

    def listen(self):
        try:

            # Start the server by binding a TCP socket to the right port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.port))
                server.listen()

                print('[GameServer]: Started on port', self.port)

                # Create new instance of the connection handler
                connection_handler = Connection.Handler(self)

                # Create new instance of the session handler and assign to self
                self.session_handler = session.Session(self)

                # Listen for new connections
                while True:
                    # Accept the new client and handle the connection in a separate thread
                    client, address = server.accept()
                    _thread.start_new_thread(Client.Client,
                                             (client, address, self, connection_handler, self.session_handler,))

        except Exception as e:
            print('[GameServer]: Failed to start Game Server. Perhaps the port is already in use. Exception:', e)
