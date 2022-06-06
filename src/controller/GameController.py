import math
import sys

import numpy
import pygame

from services.GameSettings import GameSettings as gs


class GameController:

    def __init__(self):
        pygame.init()
        self.pitch = self.build_pitch(gs.ROW, gs.COLUMN)
        self.screen = pygame.display.set_mode(gs.PITCH_SIZE)

    @staticmethod
    def build_pitch(row, column):
        return numpy.zeros((row, column))

    def throw_coin(self, row, col, coin):
        self.pitch[row][col] = coin

    def is_valid_move(self, col):
        return self.pitch_view.pitch[gs.ROW - 1][col] == 0

    def get_next_open_row(self, col):
        for row in range(gs.ROW):
            if self.pitch_view.pitch[row][col] == 0:
                return row

    def play_game(self):
        game_over = False
        turn = 0

        while not game_over:
            self.pitch_view.draw_pitch()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    self.pitch_view.draw_coin(posx)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.pitch_view.screen, gs.EMPTY_SLOT_COLOR, (0, 0, gs.WIDTH, gs.ELEMENT_SIZE))

                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx / gs.ELEMENT_SIZE))

                        if self.is_valid_move(col):
                            row = self.get_next_open_row(col)
                            self.throw_coin(row, col, 1)

                            # if winning_move(board, 1):
                            #     label = myfont.render("Player 1 wins!!", 1, RED)
                            #     screen.blit(label, (40, 10))
                            #     game_over = True

                self.pitch_view.draw_pitch()


if __name__ == '__main__':
    gc = GameController()
    gc.play_game()
