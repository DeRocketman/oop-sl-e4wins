import pygame

from services.GameSettings import GameSettings as gs


class GameView:

    def __init__(self, pitch):
        self.pitch = pitch
        self.screen = pygame.display.set_mode(gs.PITCH_SIZE)

    def draw_pitch(self):
        for col in range(gs.COLUMN):  # draws the empty pitch
            for row in range(gs.ROW):
                self.draw_rect(col, row, gs.PITCH_COLOR)
                self.draw_circle(col, row, gs.EMPTY_SLOT_COLOR)

        for col in range(gs.COLUMN):  # fills the pitch with coins
            for row in range(gs.ROW):

                if self.pitch[row][col] == 1:
                    self.draw_pitch_circle(col, row, gs.PLAYER_ONE_COLOR)

                elif self.pitch[row][col] == 2:
                    self.draw_pitch_circle(col, row, gs.PLAYER_TWO_COLOR)
        pygame.display.update()

    def draw_coin(self, pos_x, current_player):
        if current_player == 1:
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

    def draw_pitch_circle(self, col, row, color):
        pygame.draw.circle(self.screen, color, (
            int(col * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2),
            gs.HEIGHT - int(row * gs.ELEMENT_SIZE + gs.ELEMENT_SIZE / 2)), gs.RADIUS)

    def draw_win(self, current_player, winner_name):
        my_font = pygame.font.SysFont("monospace", 45)
        if current_player == 1:
            label = my_font.render(f'{winner_name} gewinnt!', True, gs.PLAYER_ONE_COLOR)
            print(winner_name)
        else:
            label = my_font.render(f'{winner_name} gewinnt!', True, gs.PLAYER_TWO_COLOR)
            print(winner_name)
        self.screen.blit(label, (40, 10))

    def draw_connection_lost(self):
        my_font = pygame.font.SysFont("monospace", 45)
        label = my_font.render(f'Connection lost', True, gs.PLAYER_ONE_COLOR)
        self.screen.blit(label, (40, 10))
        self.draw_pitch()
        