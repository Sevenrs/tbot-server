import socket
import _thread
from relay_udp_server import router
from Packet.ReadDatagram import ReadDatagram as ReadDatagram

class RelayUDPServer:

    def __init__(self, port, relay_tcp_server):
        self.port   = port
        self.name   = 'RelayUDPServer'
        self.relay  = relay_tcp_server
        self.socket = None

        self.listen()

    # Attempt to start a UDP server on the port given
    def listen(self):
        try:

            self.socket = server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.socket.bind(('0.0.0.0', self.port))

            print('[{0}]: Started on port {1}'.format(self.name, self.port))

            # Listen for new connections
            while True:
                message, address = self.socket.recvfrom(65565)
                _thread.start_new_thread(RelayUDPClient, (message, address, self))

        except Exception as e:
            print("[{0}]: Failed to bind because: {1}".format(self.name, e))

class RelayUDPClient:

    def __init__(self, data, address, server):
        self.data       = data
        self.address    = address
        self.server     = server

        self.handle()

    '''
    Read packet and determine what to do in the router
    '''
    def handle(self):
        print("[{0}]: New connection from {1}:{2}".format(self.server.name, self.address[0], self.address[1]))
        packet = ReadDatagram(self.data)
        router.route(self.__dict__, packet)