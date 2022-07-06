import math
import sys

import numpy as np
import pygame

from services.GameSettings import GameSettings as gs
from view.GameView import GameView


class GameController:

    def __init__(self, socket_client, socket_server, player, opponent, mvc, menu_view):
        pygame.init()
        self.mvc = mvc
        self.menu_view = menu_view
        self.game_view = GameView(self.build_pitch(gs.ROW, gs.COLUMN))
        self.socket_client = socket_client
        self.socket_server = socket_server
        self.player = player
        self.opponent = opponent
        self.current_player = self.set_starting_player()
        self.current_player_number = 1
        self.game_over = False

    @staticmethod
    def build_pitch(row, column):
        return np.zeros((row, column))

    def throw_coin(self, row, col, coin):
        print(f'ROW {row} COL {col}')
        self.game_view.pitch[row][col] = coin

    def is_valid_move(self, col):
        return self.game_view.pitch[gs.ROW - 1][col] == 0

    def get_next_open_row(self, col):
        for row in range(gs.ROW):
            if self.game_view.pitch[row][col] == 0:
                print(f'Reihe:{row}')
                return row

    def print_board_for_look(self):
        print(np.flip(self.game_view.pitch, 0))

    def switch_player(self, current_player):
        if self.current_player == self.player:
            self.current_player = self.opponent
        else:
            self.current_player = self.player

        if current_player == 1:
            return 2
        else:
            return 1

    def check_win(self, coin):
        # Check horizontal locations for win
        for col in range(gs.COLUMN - 3):
            for row in range(gs.ROW):
                if self.game_view.pitch[row][col] == coin and self.game_view.pitch[row][col + 1] == coin and \
                        self.game_view.pitch[row][col + 2] == coin and self.game_view.pitch[row][col + 3] == coin:
                    return True

        # Check vertical locations for win
        for col in range(gs.COLUMN):
            for row in range(gs.ROW - 3):
                if self.game_view.pitch[row][col] == coin and self.game_view.pitch[row + 1][col] == coin and \
                        self.game_view.pitch[row + 2][col] == coin and self.game_view.pitch[row + 3][col] == coin:
                    return True

        # Check positively sloped diagonals
        for col in range(gs.COLUMN - 3):
            for row in range(gs.ROW - 3):
                if self.game_view.pitch[row][col] == coin and self.game_view.pitch[row + 1][col + 1] == coin and \
                        self.game_view.pitch[row + 2][col + 2] == coin and \
                        self.game_view.pitch[row + 3][col + 3] == coin:
                    return True

        # Check negatively sloped diagonals
        for col in range(gs.COLUMN - 3):
            for row in range(3, gs.ROW):
                if self.game_view.pitch[row][col] == coin and self.game_view.pitch[row - 1][col + 1] == coin and \
                        self.game_view.pitch[row - 2][col + 2] == coin and \
                        self.game_view.pitch[row - 3][col + 3] == coin:
                    return True

    def mouse_motion(self, pos_x):
        self.game_view.draw_coin(pos_x, self.current_player_number)

    def mouse_click(self, pos_x):
        pygame.draw.rect(self.game_view.screen, gs.EMPTY_SLOT_COLOR, (0, 0, gs.WIDTH, gs.ELEMENT_SIZE))
        col = int(math.floor(pos_x / gs.ELEMENT_SIZE))
        row = self.get_next_open_row(col)

        if self.is_valid_move(col):
            self.throw_coin(row, col, self.current_player_number)
            self.print_board_for_look()
            if self.check_win(self.current_player_number):
                self.game_view.draw_win(self.current_player_number, self.current_player.username)
                self.game_view.draw_pitch()
                self.game_over = True

            self.current_player_number = self.switch_player(self.current_player_number)

    def set_starting_player(self):
        if self.player.is_host:
            return self.player
        else:
            return self.opponent

    def close_game(self):
        self.game_view.draw_connection_lost()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def play_game(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            clock.tick(gs.FPS)
            self.socket_client.send('standby')
            self.socket_client.receive()
            self.game_view.draw_pitch()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.socket_client.send('close')

                if self.current_player == self.player:
                    if event.type == pygame.MOUSEMOTION:
                        pos_x = event.pos[0]
                        self.socket_client.send(f'MOUSE_MOTION:{str(pos_x)}')

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos_x = event.pos[0]
                        self.socket_client.send(f'MOUSE_CLICK:{str(pos_x)}')
                        break

            if self.game_over:
                pygame.time.wait(5000)

                self.mvc.current_menu = self.menu_view.after_game_menu
                self.menu_view.draw_after_game_menu()
                self.mvc.game_is_run = False
