 #!/usr/bin/env python3
__author__      = "Icseon"
__copyright__   = "Copyright (C) 2021 Icseon"

import time, _thread

'''
This class is responsible for handling temporary sessions between one or more clients.
This is used for trading, friend requests, guild invite requests and trade requests.
'''
class Session:

    """ Session constructor """
    def __init__(self, server):
        self.server = server

    '''
    This method will create a new session
    '''
    def create(self, type, clients=[], data={}, expires_after=0):

        session = {
            'type':     type,
            'clients':  clients,
            'data':     data
        }

        self.server.sessions.append(session)

        if expires_after > 0:
            _thread.start_new_thread(self.expire_after, (session, expires_after,))

        return session

    '''
    This method will send a packet to every client in the session
    '''
    def broadcast(self, session, packet):
        for client in session['clients']:
            client['socket'].send(packet)

    '''
    This method will destroy an existing session
    '''
    def destroy(self, session):
        if session in self.server.sessions:
            self.server.sessions.remove(session)

    '''
    This method will destroy a session after a specific amount of seconds
    '''
    def expire_after(self, session, seconds=0):
        time.sleep(seconds)
        self.destroy(session)