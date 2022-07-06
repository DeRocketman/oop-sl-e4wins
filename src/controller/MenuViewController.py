import sys

import pygame
from requests import get

from services.GameSettings import GameSettings as gs
from controller.GameViewController import GameController
from model.Player import Player
from services.SocketClient import SocketClient
from services.SocketServer import SocketServer
from view.MenuView import MenuView


# Controller class for MenuView
class MenuViewController:
    def __init__(self):
        pygame.init()
        self.player = Player()
        self.opponent = Player()
        self.opponent.username = ''
        self.menu_view = MenuView(self)
        self.socket_client = SocketClient(self)
        self.socket_server = SocketServer()
        self.ip_public = get('https://api.ipify.org').content.decode('utf8')  # gets the own public ip from router
        self.temp_server_ip = ''
        self.current_menu = self.menu_view.initial_menu
        self.game_is_run = False
        self.game_over = False
        self.revenge_count = 0

    def set_username(self, value):
        if not value:
            self.player.username = 'unnamed'
            return 'unnamed'
        self.player.username = value
        return value

    def set_is_player_host(self, value, is_player_host):
        self.player.is_host = value
        self.player.is_host = is_player_host

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
        self.menu_view.draw_wait_for_connection_menu(label_text)
        self.current_menu = self.menu_view.wait_for_connection_menu

    def introduce_to_opponent(self):
        self.socket_client.send(f'username:{self.player.username}\n')

    def run_socket_server(self):
        self.socket_server.run_server()
        self.socket_client.server_ip = self.socket_server.ip
        self.socket_client.connect()

    def start_game(self):
        gc = GameController(self.socket_client, self.socket_server, self.player, self.opponent, self, self.menu_view)
        self.game_is_run = True
        self.socket_client.game_view_controller = gc
        gc.play_game()

    def menu_loop(self):
        clock = pygame.time.Clock()
        while not self.game_is_run or not self.game_over:
            clock.tick(gs.FPS)
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

    def wait_for_restart(self):
        if not self.player.revenge:
            self.player.revenge = True
            self.socket_client.send('revenge')

    def revenge_counter(self):
        self.revenge_count += 1
        if self.revenge_count == 2:
            self.revenge_count = 0
            self.player.revenge = False
            self.start_game()

    def no_revenge(self):
        self.socket_client.send('coward')

    def exit_game(self):
        if self.socket_client.is_connected:
            if self.player.is_host:
                self.socket_client.send('host_disconnected')
                self.socket_client.receive()
                self.game_over = True
                pygame.time.wait(500)
            elif self.socket_client:
                self.socket_client.send('opponent_disconnected')
                self.socket_client.receive()
                self.game_over = True
                pygame.time.wait(500)
        pygame.quit()
        sys.exit()
