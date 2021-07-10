#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"
# This file is the entry point for Bout server

import _thread
import threading
from LoginServer        import Server as LoginServer
from ChannelServer      import Server as ChannelServer
from RoomHostServer     import Server as RoomHostServer
from GameServer         import Server as GameServer
from relay_tcp_server   import server as relay_tcp_server
from relay_udp_server   import server as relay_udp_server

"""
This method will start all services
"""
def main():
    print('[Bout Galaxy]: Server version:', __version__)

    '''
    Create a new instance of the relay TCP server
    '''
    relay_tcp = relay_tcp_server.RelayTCPServer(11004)
    _thread.start_new_thread(relay_tcp.listen, ())

    '''
    Create a new instance of GameServer so we can access its values from any server
    Then, run the server on a new thread and inherit the state of the relay TCP server
    '''
    game_server = GameServer.Socket(11002, relay_tcp)
    _thread.start_new_thread(game_server.listen, ())
    
    # Start the Channel Server
    _thread.start_new_thread(ChannelServer.Socket, (11010,))

    # Start the RoomHost Server
    _thread.start_new_thread(RoomHostServer.Socket, (11011, game_server,))

    # Start the relay UDP server and inherit the state of the relay TCP server
    _thread.start_new_thread(relay_udp_server.RelayUDPServer, (11013, relay_tcp,))

    # Use the main thread as the login server
    LoginServer.Socket(11000)
    
# Only run the entry point code when needed
if __name__ == '__main__':
    main()
