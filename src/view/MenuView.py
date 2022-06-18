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
        self.menu.add.button('Weiter', onselect=self.mvc.show_connect_menu)

        self.menu.mainloop(self.screen)

    def draw_connect_player(self):
        pass
