from lib_board import Board
import config


class Location(Board):
    def __init__(self, h, w, list, tile_size = 8): # list should not contain outer walls
        super().__init__(w + 2, h + 2, tile_size)
        for i in range(self.height):
            for j in range(self.width):
                if self.border(i, j):
                    self.board[i][j] = config.WALL
                else:
                    self.board[i][j] = list[i - 1][j - 1] # puts list in self.board

    def border(self, i, j):
        return (i in [self.height, 0] or j in [self.width, 0])

