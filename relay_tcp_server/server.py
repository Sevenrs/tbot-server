import socket
import _thread
from relay_tcp_server import router
from Packet.Read import Read as PacketRead

class RelayTCPServer:

    def __init__(self, port):
        self.port = port
        self.name = 'RelayTCPServer'

        self.clients = []
        self.ids = []

    '''
    Attempt to start a server on the port specified
    '''
    def listen(self):
        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.port))
                server.listen()
                print('[{0}]: Started on port {1}'.format(self.name, self.port))

                # Keep listening for new connections
                while True:
                    client, address = server.accept()
                    _thread.start_new_thread(RelayTCPClient, (client, address, self,))

        except Exception as e:
            print("[{0}]: Failed to bind because: {1}".format(self.name, e))

class RelayTCPClient:

    def __init__(self, socket, address, server):
        self.socket     = socket
        self.address    = address
        self.server     = server
        self.handle()

    def handle(self):
        print("[{0}]: New connection from {1}:{2}".format(self.server.name, self.address[0], self.address[1]))

        while True:
            try:
                packet = PacketRead(self.socket)
                router.route(self.__dict__, packet)
            except Exception as e:
                print("[{0}]: Disconnected from {1}:{2}".format(self.server.name, self.address[0], self.address[1]))

                f = open('relay_exceptions', 'a')
                f.write(e)
                f.close()

                # If the client is in the server client container, remove it from the server client container
                if self.__dict__ in self.server.clients:
                    self.server.clients.remove(self.__dict__)

                # If the ID is in the ID container, and our client has an ID assigned to it, remove it from the ID container
                if hasattr(self, 'id') and self.id in self.server.ids:
                    self.server.ids.remove(self.id)

                # Finally, close the client's socket entirely. It may already be closed, but in exceptions it may still remain open
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                    self.socket.close()
                except Exception:
                    pass
                break