import socket
import threading
from _thread import start_new_thread

from services.GameSettings import GameSettings as gs


class SocketClient:
    def __init__(self, menu_view_controller):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.menu_view_controller = menu_view_controller
        self.game_view_controller = None
        self.port = gs.SERVERPORT

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.port))
            self.menu_view_controller.received_msg(self.socket.recv(512).decode('utf-8'))
        except socket.error as e:
            self.menu_view_controller.run_menu_loop(False)
            print('[SocketClient-Info] Error in message ', e)

    def send(self, msg):
        try:
            if msg:
                self.socket.send(str.encode(msg+'\n'))
                print('[SocketClient-Info] send MSG: ', msg)
        except socket.error as e:
            print('Error in message ', e)

    def receive(self):
            msg_list = self.socket.recv(512).decode('utf-8').splitlines()
            for msg_decoded in msg_list:
                print('[SocketClient-Info] resveived MSG: ', msg_decoded)
                if msg_decoded == 'host-connected':
                    self.menu_view_controller.run_menu_loop_thread.start()
                    self.menu_view_controller.menu_view.kill_mainloop()
                    self.send("Hallo Max, i bims 1 Nachricht vong 1 Computerprogramm")
                    self.menu_view_controller.run_menu_loop(True)
                    self.send("Hallo Max, i bims 2 Nachricht vong 1 Computerprogramm")
                elif msg_decoded == 'player-joined':
                    variable= False
                    self.menu_view_controller.introduce_to_opponent()
                elif msg_decoded[0:9] == 'hubendubel:':
                    keyword = msg_decoded[0:9]
                    restword = msg_decoded[9:]
                    print('keyword:', keyword)
                    print('restword:', restword)
                    print(msg_decoded[0:9])
