import pygame
import sys
import time
from board import Board
from square import Square
from client import Client
from constants import *


class Game:
    def __init__(self, client):
        self.client = client
        self.is_winner = None
        self.role, self.turn = self.client.get_role_turn()
        if self.client.start(self):
            self.screen, self.board = self.gui_init()
            self.running = True
            self.loop()

    def get_data(self, data):
        """ a 'chose' key packet and a 'finish' key packet might stick together, on a player's last move.
        this function provides an ad-hoc solution """

        finish_index = data.find("finish")
        # check if 'finish' key is in the middle of the data.
        if finish_index > 1:
            data_arr = data[:finish_index].split()
            key = data_arr[0]
            # check that key value is 'chose'
            if key == "chose":
                self.add_enemy_choice(data[:finish_index])
            self.is_winner = int(data[finish_index:].split()[1])
        # only a 'finish' packet is available
        elif finish_index != -1:
            self.is_winner = int(data[finish_index:].split()[1])
        # only a 'chose' packet is available
        else:
            data_arr = data.split()
            key = data_arr[0]
            if key == "chose":
                self.add_enemy_choice(data)

    def add_enemy_choice(self, data):
        # get x and y of squares array from data
        x, y = int(data.split()[1]), int(data.split()[2])
        enemy_role = 1 - self.role
        # add enemy sprite to screen
        self.board.squares[x][y].add_sprite(self.screen, enemy_role)
        # add enemy's choice to squares local array
        self.board.squares[x][y].role = enemy_role
        # change turn
        self.turn = 1-self.turn

    # initialize GUI
    def gui_init(self):
        """ initialize pygame window """

        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("doNoughts and Crosses")
        screen.fill("white")
        board = Board(screen)
        return screen, board

    # available square onclick
    def square_click(self, square):
        """ if square is available, add sprite to window and send choice to server."""
        if square.add_sprite(self.screen, self.role):
            self.client.send_choice(self.role, square.x_index, square.y_index)
            self.turn = 1-self.turn

    # check events. catch square clicks and quit requests
    def event_checker(self):
        for event in pygame.event.get():
            # player clicked close button
            if event.type == pygame.QUIT:
                self.running = False
            # player clicked left mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.turn:
                for y in range(NUMBER_OF_SQUARES_IN_ROW):
                    for x in range(NUMBER_OF_SQUARES_IN_ROW):
                        square = self.board.squares[x][y]
                        # check which square was clicked, if any.
                        if square.rect.collidepoint(event.pos):
                            self.square_click(square)

    # main pygame window loop
    def loop(self):
        # sleep n seconds after game finished, so user can determine his victory/loss
        sleep = 1
        # game loop
        while self.running:
            if self.is_winner == None:
                self.event_checker()
                # write turn info on the lower left side of the screen
                font = pygame.font.SysFont("ComicSans", 42)
                turn_text = "your turn!" if self.turn else "opponent's turn"
                text = font.render(turn_text, True, "black")
                text_margin = SQUARE_BORDER_WIDTH
                text_point = (text_margin , SCREEN_HEIGHT - text.get_height() - text_margin)
                turn_text_rect = pygame.Rect(text_point, (SCREEN_WIDTH, 50))
                pygame.draw.rect(self.screen, "white", turn_text_rect)
                self.screen.blit(text, text_point)
                pygame.display.flip()
            else:
                break
        if self.is_winner != None:
            self.finish(sleep)

    # show the player whether he won or lost
    def finish(self, sleep):
        while sleep > 0:
            time.sleep(1)
            sleep -= 1
        if self.is_winner == 1:
            finish_text = "you won!"
        elif self.is_winner == 2:
            finish_text = "it's a tie"
        else:
            finish_text = "you lose..."
        # clear screen
        self.screen.fill("white")
        # show text
        font = pygame.font.SysFont("ComicSans", 90)
        text = font.render(finish_text, True, "black")
        text_point = ((SCREEN_WIDTH - text.get_width()) / 2 , (SCREEN_HEIGHT - text.get_height()) / 2)
        self.screen.blit(text, text_point)
        # update screen
        pygame.display.flip()
        # check for close button event
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


if __name__ == "__main__":
    try:
        client = Client()
        Game(client)
    except KeyboardInterrupt:
        sys.exit("\nBye!")
