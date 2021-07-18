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

    # Attempt to close the connection
    try:
        print("[{0}]: Disconnected from {1}:{2}".format(client['server'].name, client['socket'].getpeername()[0],
                                                        client['socket'].getpeername()[1]))

        client['socket'].shutdown(socket.SHUT_RDWR)
        client['socket'].close()
    except Exception:
        pass