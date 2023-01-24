import socket

'''
This method will close a relay tcp client's connection and perform a clean-up as well
'''


def close_connection(client):
    # If the client is in the server's client container, remove it from the container
    if client in client['server'].clients:
        client['server'].clients.remove(client)

    # If the ID is in the ID container, remove the ID from the container
    if 'id' in client and client['id'] in client['server'].ids:
        client['server'].ids.remove(client['id'])

    # If the client has an attached game_client, remove the reference to it
    if 'game_client' in client:

        # If the game client has a relay_client attached to it, remove the reference to it
        if 'relay_client' in client['game_client']:
            client['game_client'].pop('relay_client')

        # Remove game_client reference from this client
        client.pop('game_client')

    # Attempt to close the connection
    try:
        print("[{0}]: Disconnected from {1}:{2}".format(client['server'].name, client['socket'].getpeername()[0],
                                                        client['socket'].getpeername()[1]))

        client['socket'].shutdown(socket.SHUT_RDWR)
        client['socket'].close()
    except Exception:
        pass
