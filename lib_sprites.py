import pygame
from config import *
import os
import random

pygame.mixer.init()

open_door = pygame.mixer.Sound('waves/open.wav')
close_door = pygame.mixer.Sound('waves/close.wav')

size = width, height = 400, 400
screen = pygame.display.set_mode(size)
STEP = 5


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load('pics/'+name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
brick_image = load_image('black_brick.png')
door_image = load_image('door4.png')
door1_image = load_image('door1.png')
lenin_image = load_image('lenin.gif', (255, 255, 255))
mouse_image = load_image('mouse.png', (0, 0, 0))
wood_image = load_image('wood.jpg')
brick_font_image = load_image('brick_font.jpeg')
grey_wood = load_image('grey_wood.jpeg')
great_wood = load_image('black_wood.jpg')
factory_image = load_image('factory.jpg')
worker_image = load_image('worker.png', (255, 255, 255))
dead_worker = load_image('dead_worker.png', (255, 255, 255))
images = {'brick': brick_font_image, 'wood': great_wood, 'factory': factory_image,
          'worker': worker_image, 'dead_worker': dead_worker, 'grey_wood': grey_wood}


class Brick(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = brick_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group.add(self)


class Door(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 50 - 15
        self.now = 0
        group.add(self)

    def update(self):
        if self.now == 0:
            self.rect.x += TILE_SIZE
            copy = self.rect
            self.image = door1_image
            self.rect = self.image.get_rect()
            self.rect.x = copy.x - self.rect.y
            self.rect.y = copy.y
            self.now = 1
            open_door.play()
        else:
            copy = self.rect
            self.image = door_image
            self.rect.x -= TILE_SIZE
            self.rect = self.image.get_rect()
            self.rect.x += copy.x
            self.rect.y += copy.y
            self.now = 0
            close_door.play()

    def get_event(self, event):
        if self.collidepoint(event.pos):
            self.update()

    def collidepoint(self, point):
        x1, y1, a, b = self.rect
        x1 -= 10
        x3, y3 = x1 + a, y1 + b
        x2, y2 = point
        if x1 <= x2 <= x3 and y1 <= y2 <= y3:
            return True
        return False


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, tile_group, pos_x, pos_y):
        super().__init__(tile_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(pos_x,
                                               pos_y)


class Worker(pygame.sprite.Sprite):
    def __init__(self, worker_group, pos_x, pos_y):
        super().__init__(worker_group)
        self.image = images['worker']
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = images['dead_worker']


class Player(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = lenin_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.money = 0
        self.health = 100
        self.inventory = {}

        group.add(self)

    def possible_move(self):
        info = pygame.sprite.spritecollide(self, self.group, False)
        if len(info) == 1:
            return True
        else:
            for i in info:
                if type(i) == Goal:
                    i.done = True
        return False

    def move(self, direction):
        if direction == 'down':
            self.rect.y += STEP
        if direction == 'up':
            self.rect.y -= STEP
        if direction == 'left':
            self.rect.x -= STEP
        if direction == 'right':
            self.rect.x += STEP
        if not self.possible_move():
            if direction == 'down':
                self.rect.y -= STEP
            if direction == 'up':
                self.rect.y += STEP
            if direction == 'left':
                self.rect.x += STEP
            if direction == 'right':
                self.rect.x -= STEP


class Goal(Tile):
    def __init__(self, tile_type, tile_group, pos_x, pos_y):
        super().__init__(tile_type, tile_group, pos_x, pos_y)
        self.done = False


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        self.group = group
        self.image = mouse_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)



