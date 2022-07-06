import socket

from services.GameSettings import GameSettings as gs


class SocketClient:
    def __init__(self, menu_view_controller):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.menu_view_controller = menu_view_controller
        self.game_view_controller = None
        self.port = gs.SERVER_PORT
        self.is_connected = False

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.port))
            self.is_connected = True
        except socket.error as e:
            if self.menu_view_controller.player.is_host:
                self.menu_view_controller.show_connect_menu(False)
            print(f'[SocketClient-Info] Error in message: {e}')

    def close_connection(self):
        self.socket.close()
        self.is_connected = False

    def send(self, msg):
        try:
            if msg:
                self.socket.send(str.encode(f'{msg}\n'))
                # print(f'[SocketClient-Info] send MSG: {msg}')
        except socket.error as e:
            print('Error in message ', e)

    def receive(self):
        msg_list = self.socket.recv(512).decode('utf-8').splitlines()
        if len(msg_list) > 0:
            for msg_decoded in msg_list:
                if msg_decoded == 'standby':
                    pass
                else:
                    print(f'[SocketClient-Info] received MSG: {msg_decoded}')
                    if msg_decoded == 'host-connected':
                        self.menu_view_controller.show_connect_menu(True)
                    elif msg_decoded == 'player-joined':
                        self.menu_view_controller.introduce_to_opponent()
                        self.menu_view_controller.start_game()
                    elif msg_decoded[0:9] == 'username:':
                        restword = msg_decoded[9:]
                        self.menu_view_controller.set_opponent_name(restword)
                    elif msg_decoded[0:13] == 'MOUSE_MOTION:':
                        pos_x = msg_decoded[13:]
                        self.game_view_controller.mouse_motion(int(pos_x))
                    elif msg_decoded[0:12] == 'MOUSE_CLICK:':
                        pos_x = msg_decoded[12:]
                        self.game_view_controller.mouse_click(int(pos_x))
                    elif msg_decoded == 'revenge':
                        self.menu_view_controller.revenge_counter()
                    elif msg_decoded == 'coward':
                        self.menu_view_controller.exit_game()
                    elif msg_decoded == 'host_disconnected':
                        self.send('game_over')
                        self.close_connection()
                        break
                    elif msg_decoded == 'opponent_disconnected':
                        self.send('game_over')
                        self.close_connection()
                        break
                    elif msg_decoded == 'close':
                        self.game_view_controller.close_game()
                        break

        msg_list.clear()
