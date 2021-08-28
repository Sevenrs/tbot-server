import socket
import _thread
from relay_tcp_server import router, connection
from Packet.Read import Read as PacketRead
import traceback

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

                traceback_str = ''.join(traceback.format_tb(e.__traceback__))

                f = open("relay.log", "a")
                f.write(str(e) + "\n")
                f.write(traceback_str + "\n")
                f.close()

                connection.close_connection(self.__dict__)
                break