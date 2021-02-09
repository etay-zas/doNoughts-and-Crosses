import pygame
from square import Square
from constants import *


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.rect = pygame.Rect(BOARD_ZERO_POINT, BOARD_SIZE_TUPLE)
        pygame.draw.rect(screen, "black", self.rect)
        self.squares = self.init_and_draw(screen)

    # create the squares array and draw the board
    def init_and_draw(self, screen):
        game = []
        for x in range(NUMBER_OF_SQUARES_IN_ROW):
            line = []
            for y in range(NUMBER_OF_SQUARES_IN_ROW):
                square_x = SQUARE_OVAERALL_SIZE * x + SQUARE_BORDER_WIDTH + BOARD_ZERO_X
                square_y = SQUARE_OVAERALL_SIZE * y + SQUARE_BORDER_WIDTH + BOARD_ZERO_Y
                square_rect = pygame.Rect((square_x, square_y), SQUARE_SIZE_TUPLE)
                square = Square(square_rect, x, y)
                pygame.draw.rect(screen, "white", square)
                line.append(square)
            game.append(line)
        return game
