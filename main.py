import pygame
from lib_sprites import *
from config import *

pygame.mixer.init()
pygame.init()

size = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = self.generate_level(load_level('level.txt'))
        clock = pygame.time.Clock()
        pressed_left = pressed_right = pressed_up = pressed_down = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for door in self.all_sprites:
                        if type(door) == Door:
                            door.get_event(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pressed_left = True
                    elif event.key == pygame.K_RIGHT:
                        pressed_right = True
                    elif event.key == pygame.K_UP:
                        pressed_up = True
                    elif event.key == pygame.K_DOWN:
                        pressed_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pressed_left = False
                    elif event.key == pygame.K_RIGHT:
                        pressed_right = False
                    elif event.key == pygame.K_UP:
                        pressed_up = False
                    elif event.key == pygame.K_DOWN:
                        pressed_down = False

            if pressed_left:
                self.player.move('left')
            if pressed_right:
                self.player.move('right')
            if pressed_up:
                self.player.move('up')
            if pressed_down:
                self.player.move('down')

            screen.fill((202, 255, 255))
            self.all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    Brick(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
                elif level[y][x] == '@':
                    new_player = Player(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '_':
                    Door(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
        return new_player


game = Game()
