import sys
import threading
from _thread import start_new_thread

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

    def set_username(self, value):
        print(value)
        self.player.username = value

    def set_is_player_host(self, value, is_player_host):
        print(value)
        print(is_player_host)
        self.player.is_host = value

    def show_next_menu(self):
        if self.player.is_host:
            self.run_socket_server()
        else:
            pass

    def run_socket_server(self):
        print('geklickt')

    def menu_loop(self):
        start_game = False

        while not start_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.menu_view.initial_menu.draw(self.menu_view.screen)
            self.menu_view.initial_menu.update(events)
            pygame.display.flip()
            print('in der Schleife drinne')


if __name__ == '__main__':
    mvc = NewMenuViewController()
    mvc.menu_loop()
