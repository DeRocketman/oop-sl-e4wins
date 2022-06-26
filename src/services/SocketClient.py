import socket

from services.GameSettings import GameSettings as gs


class SocketClient:
    def __init__(self, menu_view_controller):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.server_ip = 'localhost'
        self.menu_view_controller = menu_view_controller
        self.game_view_controller = None
        self.port = gs.SERVERPORT
        self.is_connected = False

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.port))
            # self.menu_view_controller.received_msg(self.socket.recv(512).decode('utf-8'))
            self.is_connected = True
        except socket.error as e:
            if self.menu_view_controller.player.is_host:
                self.menu_view_controller.show_connect_menu(False)
            print('[SocketClient-Info] Error in message ', e)

    def send(self, msg):
        try:
            if msg:
                self.socket.send(str.encode(msg + '\n'))
                print('[SocketClient-Info] send MSG: ', msg)
        except socket.error as e:
            print('Error in message ', e)

    def receive(self):
        msg_list = self.socket.recv(512).decode('utf-8').splitlines()
        if len(msg_list) > 0:
            for msg_decoded in msg_list:
                print('[SocketClient-Info] resveived MSG: ', msg_decoded)
                if msg_decoded == 'host-connected':
                    self.menu_view_controller.show_connect_menu(True)
                elif msg_decoded == 'player-joined':
                    self.menu_view_controller.introduce_to_opponent()
                elif msg_decoded[0:9] == 'username:':
                    keyword = msg_decoded[0:9]
                    restword = msg_decoded[9:]
                    print('keyword:', keyword)
                    print('restword:', restword)
                    print(msg_decoded[0:9])
        else:
            print('Keine Messages')
        msg_list.clear()
