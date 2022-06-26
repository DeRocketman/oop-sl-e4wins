import sys

import pygame
from requests import get

from model.Player import Player
from services.SocketClient import SocketClient
from services.SocketServer import SocketServer
from view.NewMenuView import MenuView


class NewMenuViewController:
    def __init__(self):
        pygame.init()
        self.player = Player()
        self.opponent = Player()
        self.opponent.username = ''
        self.menu_view = MenuView(self)
        self.socket_client = SocketClient(self)
        self.socket_server = SocketServer()
        self.ip_public = get('https://api.ipify.org').content.decode('utf8')
        self.temp_server_ip = ''
        self.current_menu = self.menu_view.initial_menu

    def set_username(self, value):
        self.player.username = value

    def set_is_player_host(self, value, is_player_host):
        self.player.is_host = value

    def set_temp_server_ip(self, value):
        self.temp_server_ip = value

    def set_opponent_name(self, name):
        if name != self.player.username:
            self.opponent.username = name

    def show_next_menu(self):
        if self.player.is_host:
            self.run_socket_server()
        else:
            self.menu_view.draw_connect_to_host_menu()
            self.current_menu = self.menu_view.connect_to_host_menu

    def connect_to_host(self):
        self.socket_client.server_ip = self.temp_server_ip
        self.socket_client.connect()

    def show_connect_menu(self, success):
        if success:
            label_text = 'Alles IO, warte auf Verbindung'
        else:
            label_text = 'Ups, da lief etwas schief\nbitte neustarten'
        self.menu_view.draw_wait_for_connection_menu(label_text, self.ip_public, self.socket_client.server_ip)
        self.current_menu = self.menu_view.wait_for_connection_menu

    def introduce_to_opponent(self):
        self.socket_client.send('username:' + self.player.username)

    def run_socket_server(self):
        self.socket_server.run_server()
        self.socket_client.server_ip = self.socket_server.ip
        self.socket_client.connect()

    @staticmethod
    def i_am_alive():
        print('i am alive')

    def menu_loop(self):
        start_game = False
        while not start_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.socket_client.is_connected:
                self.socket_client.send('standby')
                self.socket_client.receive()
            self.current_menu.draw(self.menu_view.screen)
            self.current_menu.update(events)
            pygame.display.flip()


if __name__ == '__main__':
    mvc = NewMenuViewController()
    mvc.menu_loop()
