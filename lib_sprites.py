import pygame

size = width, height = 400, 400
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


all_sprites = pygame.sprite.Group()
brick_image = load_image('brick.jpg')
door_image = load_image('door3.png')
standart_size = 16


class Brick(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = brick_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)


class Door(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)


def make_room(sprite, x, y, door_pos=1):
    for i in range(x):
        brick1 = sprite(all_sprites, i*standart_size, 0)
        if i != door_pos:
            brick4 = sprite(all_sprites, i*standart_size, y*standart_size)
    for j in range(y):
        brick3 = sprite(all_sprites, x*standart_size, j*standart_size)
        brick2 = sprite(all_sprites, 0, j*standart_size)
    brick = sprite(all_sprites, x*standart_size, y*standart_size)
    door = Door(all_sprites, door_pos*standart_size, y*standart_size)


make_room(Brick, 20, 10, 5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
