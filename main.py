#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 - 2021 Icseon"
__version__ = "1.2"
# This file is the entry point for the T-Bot Rewritten server

import _thread
import threading
from login_tcp_server   import server as login_tcp_server
from ChannelServer      import Server as ChannelServer
from RoomHostServer     import Server as RoomHostServer
from GameServer         import Server as GameServer
from relay_tcp_server   import server as relay_tcp_server
from relay_udp_server   import server as relay_udp_server

"""
This method will start all services
"""
def main():
    print('[T-Bot Rewritten]: Server version:', __version__)

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
    _thread.start_new_thread(ChannelServer.Socket, (11010, game_server))

    # Start the RoomHostServer
    room_host_server = RoomHostServer.Socket(11011, game_server)
    _thread.start_new_thread(room_host_server.listen, ())

    # Start the relay UDP server and inherit the state of the relay TCP server as well as the RoomHostServer
    _thread.start_new_thread(relay_udp_server.RelayUDPServer, (11013, relay_tcp, room_host_server,))

    # Use the main thread as the login server
    (login_tcp_server.LoginTCPServer(11000)).listen()
    
# Only run the entry point code when needed
if __name__ == '__main__':
    main()
