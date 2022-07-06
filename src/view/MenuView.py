import pygame
import pygame_menu

from services.GameSettings import GameSettings as gs


class MenuView:
    def __init__(self, menu_view_controller):
        self.mvc = menu_view_controller
        self.screen = pygame.display.set_mode(gs.PITCH_SIZE)

        self.initial_menu = pygame_menu.Menu(
            enabled=True, title='4WinsPy',
            height=700,
            width=700,
            theme=pygame_menu.themes.THEME_DEFAULT
        )
        self.wait_for_connection_menu = pygame_menu.Menu(
            enabled=True, title='4WinsPy',
            height=700,
            width=700,
            theme=pygame_menu.themes.THEME_DEFAULT
        )

        self.connect_to_host_menu = pygame_menu.Menu(
            enabled=True, title='4WinsPy',
            height=700,
            width=700,
            theme=pygame_menu.themes.THEME_DEFAULT
        )

        self.after_game_menu = pygame_menu.Menu(
            enabled=True, title='4WinsPy',
            height=700,
            width=700,
            theme=pygame_menu.themes.THEME_DEFAULT
        )

        self.draw_initial_menu()
        self.draw_after_game_menu()

    def draw_initial_menu(self):
        username_field = self.initial_menu.add.text_input('Benutzername: ', onchange=self.mvc.set_username, maxchar=15)
        username_field.set_default_value(self.mvc.player.username)
        self.initial_menu.add.selector('Spiel leiten / teilnehmen: ', [('\tteilnehmen\t', False), ('\tleiten\t', True)],
                                       onchange=self.mvc.set_is_player_host)
        self.initial_menu.add.button('Weiter', self.mvc.show_next_menu)

    def draw_wait_for_connection_menu(self, success):
        self.wait_for_connection_menu.add.label(f'Deine öffentliche IP: {self.mvc.ip_public}')
        self.wait_for_connection_menu.add.label('')
        self.wait_for_connection_menu.add.label(f'Deine private IP: {self.mvc.socket_server.ip}')
        self.wait_for_connection_menu.add.label('')
        self.wait_for_connection_menu.add.label('Teile IP deinem Spielpartner mit')
        self.wait_for_connection_menu.add.label(success)

    def draw_connect_to_host_menu(self):
        self.connect_to_host_menu.add.text_input('Bitte IP des Spielleiters eingeben: ', default='192.168.188.102',
                                                 onchange=self.mvc.set_temp_server_ip)
        self.connect_to_host_menu.add.button('Verbinden', self.mvc.connect_to_host)

    def draw_after_game_menu(self):
        self.after_game_menu.add.button('Nochmal', self.mvc.wait_for_restart)
        self.after_game_menu.add.button('Beenden', self.mvc.no_revenge)
