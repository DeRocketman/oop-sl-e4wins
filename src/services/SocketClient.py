import socket
import threading

from services.GameSettings import GameSettings as gs


class SocketClient:
    def __init__(self, menu_view_controller):
        self.menu_view_controller = menu_view_controller
        self.game_view_controller = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.port = gs.SERVERPORT
        self.send_msg_thread = threading.Thread(target=self.send)
        self.receive_msg_thread = threading.Thread(target=self.receive)

    def connect(self):
        try:
            self.client.connect((self.server_ip, self.port))
            self.menu_view_controller.received_msg(self.client.recv(512).decode('utf-8'))
            self.receive_msg_thread.start()
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
            print('socket_client resceived_msg: ', msg_decoded)
            if msg_decoded == 'host-connected' or 'player-joined':
                self.menu_view_controller.received_msg(msg_decoded)
            elif msg_decoded[0:9] == 'username:':
                print(msg_decoded[0:9])
                self.menu_view_controller.received_msg(msg_decoded[9:])
