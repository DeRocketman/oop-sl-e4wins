import math
import sys

import numpy
import numpy as np
import pygame

from services.GameSettings import GameSettings as gs
from view.PitchView import PitchView


class GameController:

    def __init__(self):
        pygame.init()
        self.pitch_view = PitchView(self.build_pitch(gs.ROW, gs.COLUMN))

    @staticmethod
    def build_pitch(row, column):
        return numpy.zeros((row, column))

    def throw_coin(self, row, col, coin):
        print("DROPPIECE")
        print("ROW ", row, "COL ", col)
        self.pitch_view.pitch[row][col] = coin

    def is_valid_move(self, col):
        return self.pitch_view.pitch[gs.ROW - 1][col] == 0

    def get_next_open_row(self, col):
        for row in range(gs.ROW):
            if self.pitch_view.pitch[row][col] == 0:
                print("Reihe: ", row)
                return row

    def print_board_for_look(self):
        print(np.flip(self.pitch_view.pitch, 0))

    @staticmethod
    def switch_player(current_player):
        if current_player == 1:
            return 2
        else:
            return 1

    def check_win(self, coin):
        # Check horizontal locations for win
        for col in range(gs.COLUMN - 3):
            for row in range(gs.ROW):
                if self.pitch_view.pitch[row][col] == coin and self.pitch_view.pitch[row][col + 1] == coin and \
                        self.pitch_view.pitch[row][col + 2] == coin and self.pitch_view.pitch[row][col + 3] == coin:
                    return True

        # Check vertical locations for win
        for col in range(gs.COLUMN):
            for row in range(gs.ROW - 3):
                if self.pitch_view.pitch[row][col] == coin and self.pitch_view.pitch[row + 1][col] == coin and \
                        self.pitch_view.pitch[row + 2][col] == coin and self.pitch_view.pitch[row + 3][col] == coin:
                    return True

        # Check positively sloped diaganols
        for col in range(gs.COLUMN - 3):
            for row in range(gs.ROW - 3):
                if self.pitch_view.pitch[row][col] == coin and self.pitch_view.pitch[row + 1][col + 1] == coin and \
                        self.pitch_view.pitch[row + 2][col + 2] == coin and \
                        self.pitch_view.pitch[row + 3][col + 3] == coin:
                    return True

        # Check negatively sloped diaganols
        for col in range(gs.COLUMN - 3):
            for row in range(3, gs.ROW):
                if self.pitch_view.pitch[row][col] == coin and self.pitch_view.pitch[row - 1][col + 1] == coin and \
                        self.pitch_view.pitch[row - 2][col + 2] == coin and \
                        self.pitch_view.pitch[row - 3][col + 3] == coin:
                    return True

    def play_game(self):
        game_over = False
        current_player = 1

        while not game_over:
            self.pitch_view.draw_pitch()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pos_x = event.pos[0]
                    self.pitch_view.draw_coin(pos_x, current_player)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.pitch_view.screen, gs.EMPTY_SLOT_COLOR, (0, 0, gs.WIDTH, gs.ELEMENT_SIZE))
                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / gs.ELEMENT_SIZE))
                    row = self.get_next_open_row(col)

                    if self.is_valid_move(col):
                        self.throw_coin(row, col, current_player)
                        self.print_board_for_look()
                        if self.check_win(current_player):
                            self.pitch_view.draw_win(current_player)
                            self.pitch_view.draw_pitch()
                            game_over = True

                        current_player = self.switch_player(current_player)

            if game_over:
                pygame.time.wait(3000)



if __name__ == '__main__':
    gc = GameController()
    gc.play_game()
