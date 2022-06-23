import socket
from _thread import *

from services.GameSettings import GameSettings as gs


class SocketServer:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        print('Server ', self.ip)
        self.port = gs.SERVERPORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_list = []
        self.message_list = {}

    def run_server(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        self.socket.listen(2)  # Only Two clients may connect (Player 1 and Player 2)
        print('Server is running, waiting for connection')
        start_new_thread(self.build_connection, ())

    def threaded_client(self, client):
        if len(self.client_list) == 1:
            client.send(str.encode('host-connected'))
            print('host-connected')
        else:
            for stored_client in self.client_list:
                stored_client.send(str.encode('player-joined'))
                print("player-joined")

        while True:
            try:
                msg = client.recv(512)
                reply = msg.decode('utf-8')

                if msg:
                    print('Message on Server:')
                    print('Received: ', reply)
                    print('Sending to all', reply)
                # send to both player
                for player in self.client_list:
                    player.sendall(str.encode(reply))

            except socket.error as e:
                print('Error in message ', e)
                break

    def build_connection(self):
        while True:
            client, addr = self.socket.accept()
            self.client_list.append(client)
            start_new_thread(self.threaded_client, (client,))
