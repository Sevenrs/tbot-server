#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"
# This file is the entry point for Bout server

import _thread
import threading
from LoginServer    import Server as LoginServer
from ChannelServer  import Server as ChannelServer
from RoomHostServer import Server as RoomHostServer
from GameServer     import Server as GameServer

"""
This method will start all services
"""
def main():
    print('[Bout Galaxy]: Server version:', __version__)

    '''
    Create a new instance of GameServer so we can access its values from any server
    Then, run the server on a new thread
    '''
    game_server = GameServer.Socket(11002)
    _thread.start_new_thread(game_server.listen, ())

    # Start the Login Server in a separate thread on port 11000
    _thread.start_new_thread(LoginServer.Socket, (11000,))
    
    # Start the Channel Server
    _thread.start_new_thread(ChannelServer.Socket, (11010,))

    # Start the RoomHost Server
    _thread.start_new_thread(RoomHostServer.Socket, (11011, game_server,))

    # Without waiting, the main thread would be killed.
    print("End the process to kill the server")
    while True: pass
    
# Only run the entry point code when needed
if __name__ == '__main__':
    main()
