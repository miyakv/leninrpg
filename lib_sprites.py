import pygame
import config


size = width, height = 400, 400
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
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
brick_image = load_image('brick.jpg')
door_image = load_image('door3.png', (255, 255, 255))
door1_image = load_image('door1.png', (255, 255, 255))
lenin_image = load_image('lenin.gif', (112, 96, 67))
standart_size = 16


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
        self.rect.y = y
        self.now = 0
        group.add(self)

    def update(self):
        print(self.now)
        if self.now == 0:
            self.image = door1_image
            self.rect.x += config.TILE_SIZE
            self.now = 1
        else:
            self.image = door_image
            self.rect.x -= config.TILE_SIZE
            self.now = 0

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.update()


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
        return False

    def move(self, direction):
        if direction == 'down':
            self.rect.y += config.TILE_SIZE
        if direction == 'up':
            self.rect.y -= config.TILE_SIZE
        if direction == 'left':
            self.rect.x -= config.TILE_SIZE
        if direction == 'right':
            self.rect.x += config.TILE_SIZE
        if not self.possible_move():
            if direction == 'down':
                self.rect.y -= config.TILE_SIZE
            if direction == 'up':
                self.rect.y += config.TILE_SIZE
            if direction == 'left':
                self.rect.x += config.TILE_SIZE
            if direction == 'right':
                self.rect.x -= config.TILE_SIZE


