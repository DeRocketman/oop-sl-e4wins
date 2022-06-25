from _thread import start_new_thread

import pygame
from requests import get
from model.Player import Player
from services.SocketClient import SocketClient
from services.SocketServer import SocketServer
from view.MenuView import MenuView


class MenuViewController:
    def __init__(self):
        pygame.init()
        self.player = Player()
        self.opponent = Player()
        self.menu_view = MenuView(self)
        self.socket_client = SocketClient(self)
        self.socket_server = SocketServer()
        self.ip_public = get('https://api.ipify.org').content.decode('utf8')
        self.temp_server_ip = ''

    def set_opponent_name(self, name):
        if name != self.player.username:
            self.opponent.username = name

    def set_player_name(self, value):
        self.player.username = value

    def set_is_player_host(self, value, is_player_host):
        self.player.is_host = is_player_host

    def set_temp_server_ip(self, value):
        self.temp_server_ip = value

    def show_menu(self):
        self.menu_view.draw_username_input()

    def run_socket_server(self):
        if self.player.is_host:
            self.socket_server.run_server()
            self.socket_client.server_ip = self.socket_server.ip
            self.socket_client.connect()

        else:
            self.menu_view.draw_connect_player(self.player.is_host, self.socket_server.ip, self.ip_public, '')

    def show_connect_menu(self, success):
        label_text = None
        if success:
            label_text = 'Alles IO, warte auf Verbindung'
        else:
            label_text = 'Ups, da lief etwas schief\nbitte neustarten'
        self.menu_view.draw_connect_player(self.player.is_host, self.socket_server.ip, self.ip_public, label_text)

    def connect_to_host(self):
        self.socket_client.server_ip = self.temp_server_ip
        self.socket_client.connect()

    def introduce_to_opponent(self):
        self.socket_client.send('username:'+self.player.username)

    def start_game(self):
        if self.opponent.username != '':
            print('lets start the game')
            print('this player: ', self.player.username)
            print('opponent player: ', self.opponent.username)

    def received_msg(self, msg):
        print(msg)
        if msg == 'host-connected':
            self.show_connect_menu(True)
        elif msg == 'player-joined':
            self.introduce_to_opponent()
        else:
            self.set_opponent_name(msg)
            self.start_game()


if __name__ == '__main__':
    mvcon = MenuViewController()
    mvcon.show_menu()
