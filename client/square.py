import pygame

from constants import *

class Square:
    def __init__(self, rect, x_index, y_index):
        self.rect = rect
        self.role = None
        self.x_index = x_index
        self.y_index = y_index

    # add a sprite to square and draw on screen
    def add_sprite(self, screen, role):
        if self.role == None:
            square_center_x, square_center_y = self.rect.center
            sprite = SPRITES[role]
            screen.blit(sprite, (square_center_x - sprite.get_width() / 2, square_center_y - sprite.get_height() / 2))
            return True
        return False
