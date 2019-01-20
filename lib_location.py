from lib_board import Board
import config
import pygame
import lib_sprites


pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)



class Location(Board):
    def __init__(self, screen, h, w, list, start_tile, tile_size = 8): # list should not contain outer walls
        super().__init__(w + 2, h + 2, tile_size)
        self.screen = screen
        self.start_tile = start_tile
        self.walls = list


    def border(self, i, j):
        return i in [self.height, 0] or j in [self.width, 0]

    def player_enter(self):
        self.board[self.start_tile[0]][self.start_tile[1]] = config.SPRITES['player']
        config.CURRENT_LOCATION = self

    def render_sprites(self, spritegroup):
        spritegroup.draw(self.screen)
        self.walls.draw(self.screen)

    def get_tile(self, x, y):
        return self.board[y][x]

    def edit_tile(self, new_type, x, y):
        try:
            self.board[y][x] = new_type
        except IndexError as ind:
            print(ind, ': position out of board')



