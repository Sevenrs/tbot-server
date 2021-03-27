#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"
# This file is the entry point for BOUT server

import _thread
from LoginServer    import Server as LoginServer
from ChannelServer  import Server as ChannelServer
from RoomUDPServer  import Server as RoomUDPServer
from GameServer     import Server as GameServer

"""
This method will start all services
"""
def main():
    print('[Bout Galaxy]: Server version:', __version__)

    # Start the Login Server in a seperate thread on port 11000
    _thread.start_new_thread(LoginServer.Socket, (11000,))
    
    # Start the Channel Server
    _thread.start_new_thread(ChannelServer.Socket, (11010,))
    
    # Start the Room UDP Server
    _thread.start_new_thread(RoomUDPServer.Socket, (11011,))
    
    # Start a game server on port 11002
    _thread.start_new_thread(GameServer.Socket, (11002,))

    # Without waiting, the main thread would be killed.
    input("Press Enter to kill all services...\n")
    
# Only run the entry point code when needed
if __name__ == '__main__':
    main()
