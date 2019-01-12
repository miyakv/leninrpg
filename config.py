WALL = 1
LOCATION_EXIT = -1
PLAYER = 'p'
import sprites


def draw(tile_type, screen, i, j, cell_size):
    if tile_type == 1:
        sprites.wall.draw(i, j, cell_size, screen)
    if tile_type == 'p':
        sprites.player.draw(i, j, cell_size, screen)


