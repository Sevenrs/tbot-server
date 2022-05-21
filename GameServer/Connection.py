 #!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import remove_slot
from GameServer.Controllers.trade import exit
from GameServer.Controllers.data.client import PING_TIMEOUT
from relay_tcp_server import connection as relay_connection
import socket, datetime

"""
This file is responsible for dealing with all the clients at once.
For example, this will allow us to retrieve a specific client, or all at once or conditionally.
This is also a container for global functions that we may re-use multiple times
"""
class Handler:
    
    """ Connection handler constructor """
    def __init__(self, server):
        self.server = server
        
    def GetClients(self):

        """ Initialize result """
        result = []
        
        for client in self.server.clients:
            
            ''' Check if the client has a character assigned to it '''
            if 'character' not in client or client['character'] is None:
                continue
            
            ''' Append client to results '''
            result.append(client)
            
        return result

    """
    Method:         get_lobby_clients
    Description:    This will retrieve all clients that are not in a room
    """
    def get_lobby_clients(self):

        """ Initialize result """
        result = []

        # Retrieve all clients not in a room
        for client in self.GetClients():
            if 'room' not in client:
                result.append(client)

        return result
        
    """
    Method:         GetCharacterClient(string CharacterName)
    Description:    This retrieves the client instance belonging to a specific character, if it's online
    Parameters:     1. name     (name of the character we wish to target)
                    2. packet   (optional packet we could send immediately)
    """
    def GetCharacterClient(self, name = '', packet = None):
        
        """ Initialize the result variable """
        result = None

        for client in self.GetClients():
            if client['character']['name'] == name:
                result = client
                break
            
        """
        If we have given a packet, we will send it along
        """
        if result is not None and packet is not None:
            result['socket'].sendall(packet)
    
        return result

    """
    Method:         SendRoomAll
    Description:    This sends a packet to all clients in a specific room
    Parameters:     1. room_id  (slot ID of the target room)
                    2. packet   (packet to send to the clients)
    """
    def SendRoomAll(self, room_id, packet = None):
        for client in self.GetClients():
            if 'room' in client and client['room'] == room_id:
                try:
                    client['socket'].sendall(packet)
                except Exception:
                    pass
    
    """
    Method:         UpdatePlayerStatus
    Description:    This method will notify all clients of the status of the new or existing player
    Parameters:     1. status   (0 = in-room, 1 = online, 2 = offline)
    """
    def UpdatePlayerStatus(self, client, status=1):

        # Construct status packet, we can only do this if we have a character connected to our connection however
        if 'character' in client and client['character'] is not None and client in self.server.clients:
            notification = PacketWrite()
            notification.AddHeader(bytearray([0x27, 0x27]))
            notification.AppendBytes(bytearray([0x01, 0x00]))
            notification.AppendString(client['character']['name'], 15)
            notification.AppendInteger(client['character']['type'], 1, 'little')
            notification.AppendInteger(status, 1, 'little')

            # Broadcast to all clients, if our target client has not been specified
            for connection in self.GetClients():
                try:
                    connection['socket'].sendall(notification.packet)
                except Exception:
                    pass
            
        # If the status is equal to 0, we'll have to close the socket and dispose of the client
        if status == 2:
            self.CloseConnection(client)

    def CloseConnection(self, client):

        # Check if the current client exists in the service client container
        if client in self.server.clients:

            # If the client is in a room, attempt to remove it. We'll give the system overload reason in case the client has exceeded the ping timeout.
            if 'room' in client:
                remove_slot(_args={'server': self.server, 'connection_handler': self}, room_id=client['room'],

                            # 6 = Forced to logout
                            # 3 = System overload

                            client=client, reason=6 if (datetime.datetime.now() - client['last_ping']).total_seconds() < PING_TIMEOUT else 3)

            # If the client is in a trade, end the trade session by invoking a exit request
            if 'trade_session' in client:
                exit(_args={'client': client, 'session_handler': self.server.session_handler})

            self.server.clients.remove(client)
            self.server.client_ids.remove(client['id'])

            # Attempt to shutdown and close the socket
            try:
                client['socket'].shutdown(socket.SHUT_RDWR)
                client['socket'].close()
            except Exception:
                pass

            # If we have a relay client, remove the game_client from it
            if 'relay_client' in client:
                del client['relay_client']['game_client']