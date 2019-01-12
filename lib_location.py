from lib_board import Board


class Location(Board):
    def __init__(self, height, width, tile_size = 8):
        super().__init__(width, height)
