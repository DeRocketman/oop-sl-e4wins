import socket
from _thread import *

from services.GameSettings import GameSettings as gs


class SocketServer:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = gs.SERVERPORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_server(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        self.socket.listen(2)  # Only Two clients may connect (Player 1 and Player 2)
        print('Server is running, waiting for connection')
        start_new_thread(self.build_connection, ())

    @staticmethod
    def threaded_client(client):
        client.send(str.encode('connected'))

        while True:
            try:
                msg = client.recv(512)
                reply = msg.decode('utf-8')

                if msg:
                    print('Received: ', reply)
                    print('Sending to all', reply)

                client.sendall(str.encode(reply))
            except socket.error as e:
                print('Error in message ', e)
                break

    def build_connection(self):
        while True:
            client, addr = self.socket.accept()
            start_new_thread(self.threaded_client, (client,))
