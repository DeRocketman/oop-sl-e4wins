import pygame
import pygame_menu

from services.GameSettings import GameSettings as gs


class MenuView:
    def __init__(self, menu_view_controller):
        self.screen = pygame.display.set_mode(gs.PITCH_SIZE)
        self.menu = pygame_menu.Menu('4WinsPy', 700, 700, theme=pygame_menu.themes.THEME_DEFAULT)
        self.mvc = menu_view_controller

    def draw_username_input(self):
        self.menu.add.text_input('Benutzername: ', default='Python Peter',
                                 onchange=self.mvc.set_player_name)
        self.menu.add.selector('Spiel leiten / teilnehmen: ', [('\tteilnehmen\t', False), ('\tleiten\t', True)],
                               onchange=self.mvc.set_is_player_host)
        self.menu.add.button('Weiter').set_onselect(self.mvc.show_connect_menu)

        self.menu.mainloop(self.screen)

    def draw_connect_player(self, is_host, ip):
        self.menu.close()
        self.reset_menu()
        if is_host:
            self.menu.add.label(f'Deine IP: {ip}')
            self.menu.add.label('Teile diese IP deinem Spielpartner mit')
            self.menu.add.label('Warte auf Verbindung')
        else:
            self.menu.add.text_input('Bitte IP des Spielleiters eingeben: ', default='127.0.0.1',
                                     onchange=self.mvc.set_temp_server_ip)
            self.menu.add.button('Verbinden').set_onselect(self.mvc.connect_to_host)
        self.menu.mainloop(self.screen)

    def reset_menu(self):
        self.menu = pygame_menu.Menu('4WinsPy', 700, 700, theme=pygame_menu.themes.THEME_DEFAULT)
