import pygame

from services.GameSettings import GameSettings as gs


class PitchView:

    def __init__(self, pitch):
        self.pitch = pitch
        self.screen = pygame.display.set_mode(gs.PITCH_SIZE)

    def draw_pitch(self):
        for col in range(gs.COLUMN):
            for row in range(gs.ROW):
                self.draw_rect(col, row, gs.PITCH_COLOR)
                self.draw_circle(col, row, gs.EMPTY_SLOT_COLOR)

        for col in range(gs.COLUMN):
            for row in range(gs.ROW):
                if self.pitch[row][col] == 1:
                    self.draw_circle(col, row, gs.PLAYER_ONE_COLOR)
                elif self.pitch[row][col] == 2:
                    self.draw_circle(col, row, gs.PLAYER_TWO_COLOR)

        pygame.display.update()

    def draw_coin(self, pos_x):

        # self.draw_rect(pos_x, 0, gs.EMPTY_SLOT_COLOR)
        turn = 0
        if turn == 0:
            self.draw_motion_circle(pos_x, gs.PLAYER_ONE_COLOR)
        else:
            self.draw_motion_circle(pos_x, gs.PLAYER_TWO_COLOR)
        pygame.display.update()

    def draw_rect(self, col, row, color):
        pygame.draw.rect(self.screen, color,
                         (col * gs.ELEMENT_SIZE, row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE, gs.ELEMENT_SIZE,
                          gs.ELEMENT_SIZE))

    def draw_circle(self, col, row, color):
        pygame.draw.circle(self.screen, color, (int(col * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2),
                                                int(row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE +
                                                    gs.ELEMENT_SIZE / 2)), gs.RADIUS)

    def draw_motion_circle(self, pos_x, color):
        pygame.draw.rect(self.screen, gs.EMPTY_SLOT_COLOR, (0, 0, gs.WIDTH, gs.ELEMENT_SIZE))
        pygame.draw.circle(self.screen, color, (pos_x, int(gs.ELEMENT_SIZE / 2)),
                           gs.RADIUS)


