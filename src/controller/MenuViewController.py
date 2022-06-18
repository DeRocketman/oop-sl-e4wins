import pygame

from model.Player import Player
from view.MenuView import MenuView


class MenuViewController:
    def __init__(self):
        pygame.init()
        self.player = Player()
        self.menu_view = MenuView(self)

    def start_game(self):
        pass

    def set_player_name(self, value):
        self.player.username = value

    def set_is_player_host(self, value, is_player_host):
        self.player.is_host = is_player_host
        print(is_player_host)
        print(value)

    def show_menu(self):
        self.menu_view.draw_username_input()

    def show_connect_menu(self):
        print(self.player.username)
        print(self.player.is_host)
        print(self.player.ip)


if __name__ == '__main__':
    mvcon = MenuViewController()
    mvcon.show_menu()
