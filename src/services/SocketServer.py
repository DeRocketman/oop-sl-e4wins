import socket
from _thread import *

from services.GameSettings import GameSettings as gs


class SocketServer:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        print('Server ', self.ip)
        self.port = gs.SERVER_PORT
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
            client.send(str.encode('host-connected\n'))
            print('[Server-Info] host-connected')
        else:
            for stored_client in self.client_list:
                stored_client.send(str.encode(f'player-joined\n'))
                print("[Server-Info] player-joined")
        while True:
            try:
                msg = client.recv(512)
                reply_list = msg.decode('utf-8').splitlines()

                if len(reply_list) > 0:
                    for reply in reply_list:
                        if msg:
                            # print(f'[Server-Info] Received: {reply}')
                            # print(f'[Server-Info] Sending to all: {reply}')
                            pass
                        if reply == 'standby':
                            client.send(str.encode(f'{reply}\n'))
                        elif reply == 'game_over':
                            break
                        else:
                            # send to both player
                            for player in self.client_list:
                                player.send(msg)

            except socket.error as e:
                # print(f'[Server-Info] Error in message: {e}')
                break
        print('[Server-Info] Connection Closed')
        self.close_connection(client)

    def build_connection(self):
        while True:
            try:
                client, addr = self.socket.accept()
                self.client_list.append(client)
                start_new_thread(self.threaded_client, (client,))
            except socket.error as e:
                print(f'[Server-Info] Error in message {e}')

    def close_connection(self, client):
        client.close()
        self.client_list.remove(client)
