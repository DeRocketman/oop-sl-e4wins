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

    def draw_pitch(self):
        for col in range(gs.COLUMN):
            for row in range(gs.ROW):
                pygame.draw.rect(self.screen, gs.PITCH_COLOR,
                                 (col * gs.ELEMENT_SIZE, row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE, gs.ELEMENT_SIZE,
                                  gs.ELEMENT_SIZE))
                pygame.draw.circle(self.screen, gs.EMPTY_SLOT_COLOR, (int(col * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2),
                                                                      int(row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE +
                                                                          gs.ELEMENT_SIZE / 2)), gs.RADIUS)

        for col in range(gs.COLUMN):
            for row in range(gs.ROW):
                if self.pitch[row][col] == 1:
                    pygame.draw.circle(self.screen, gs.PLAYER_ONE_COLOR, (
                        int(col * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2),
                        700 - int(row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2)),
                                       gs.RADIUS)
                elif self.pitch[row][col] == 2:
                    pygame.draw.circle(self.screen, gs.PLAYER_TWO_COLOR, (
                        int(col * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2),
                        700 - int(row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2)), gs.RADIUS)
        pygame.display.update()

    def throw_coin(self, row, col, coin):
        self.pitch[row][col] = coin

    def play_game(self):
        game_over = False
        turn = 0
        self.draw_pitch()

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.quit():
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, gs.EMPTY_SLOT_COLOR, (0, 0, gs.WIDTH, gs.ELEMENT_SIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(self.screen, gs.PLAYER_ONE_COLOR, (posx, int(gs.ELEMENT_SIZE / 2)),
                                           gs.RADIUS)
                    else:
                        pygame.draw.circle(self.screen, gs.PLAYER_TWO_COLOR, (posx, int(gs.ELEMENT_SIZE / 2)),
                                           gs.RADIUS)
            pygame.display.update()


if __name__ == '__main__':
    gc = GameController()
    gc.play_game()
