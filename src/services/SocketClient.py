import socket

from services.GameSettings import GameSettings as gs


class SocketClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.port = gs.SERVERPORT

    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
            return self.client.recv(512).decode()
        except socket.error as e:
            print('Error in message ', e)

    def send(self, msg):
        try:
            self.client.sendall(str.encode(msg))
        except socket.error as e:
            print('Error in message ', e)

    def receive(self):
        while True:
            msg_decoded = self.client.recv(512).decode('utf-8')
