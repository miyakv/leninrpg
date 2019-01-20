from lib_board import Board
import config
import pygame
import lib_sprites


pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)


class Location(Board):
    def __init__(self, h, w, list, start_tile, tile_size = 8): # list should not contain outer walls
        super().__init__(w + 2, h + 2, tile_size)
        for i in range(self.height):
            for j in range(self.width):
                if self.border(i, j):
                    self.board[i][j] = 1
                else:
                    try:
                        self.board[i][j] = list[i - 1][j - 1] # puts list in self.board
                    except Exception:
                        pass
        self.start_tile = start_tile


    def border(self, i, j):
        return i in [self.height, 0] or j in [self.width, 0]

    def player_enter(self):
        self.board[self.start_tile[0]][self.start_tile[1]] = config.SPRITES['player']
        config.CURRENT_LOCATION = self

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                config.draw(self.board[i][j], screen, i, j, self.start_tile)

    def get_tile(self, x, y):
        return self.board[y][x]

    def edit_tile(self, new_type, x, y):
        try:
            self.board[y][x] = new_type
        except IndexError as ind:
            print(ind, ': position out of board')



