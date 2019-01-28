import pygame
from lib_sprites import *
from config import *

pygame.mixer.init()
pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.arrow = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.workers = pygame.sprite.Group()
        self.goal = Goal('brick', self.all_sprites, 0, 0)
        self.factory_level()
        pygame.quit()

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    Brick(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
                elif level[y][x] == '@':
                    new_player = Player(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
                elif level[y][x] == 'f':
                    Tile('factory', self.tile_group, x * TILE_SIZE, y * TILE_SIZE)
                elif level[y][x] == 'w':
                    self.all_sprites.add(Worker(self.workers, x * TILE_SIZE, y * TILE_SIZE))
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '_':
                    Door(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
        return new_player

    def check_for_goal(self):
        if self.goal.done:
            return True
        return False

    def factory_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.arrow = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.player = self.generate_level(load_level('factory.txt'))
        clock = pygame.time.Clock()
        pressed_left = pressed_right = pressed_up = pressed_down = False
        camera = Camera()
        pygame.mouse.set_visible(False)
        arrow = Arrow(self.arrow)
        self.arrow.add(arrow)
        running = True
        x, y = 5, 9
        self.goal = Goal('grey_wood', self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    arrow.rect.x = x
                    arrow.rect.y = y
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

            camera.update(self.player)

            for sprite in self.all_sprites:
                camera.apply(sprite)

            for tile in self.tile_group:
                camera.apply(tile)

            if self.check_for_goal():
                screen.fill(pygame.Color('red'))
                for worker in self.workers:
                     worker.update()
            else:
                screen.fill((255, 255, 255))
            self.tile_group.draw(screen)
            self.all_sprites.draw(screen)
            self.arrow.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


game = Game()
