import pygame

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
updoor_image = load_image('door.png')
lenin_image = load_image('lenin.jpg', (255, 255, 255))
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


class UpDoor(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = updoor_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__()
        self.group = group
        self.image = lenin_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)


def make_room(sprite, pos, x, y, door_pos_x, door_down=True):
    a, b = pos
    bricks = set()
    if door_down:
        for i in range(x):
            brick1 = sprite(all_sprites, i*standart_size + a, b)
            bricks.add(brick1)
            if i != door_pos_x:
                brick4 = sprite(all_sprites, i*standart_size + a, y*standart_size + b)
                bricks.add(brick4)
        for j in range(y):
            brick3 = sprite(all_sprites, x*standart_size + a, j*standart_size + b)
            bricks.add(brick3)
            brick2 = sprite(all_sprites, a, j*standart_size + b)
            bricks.add(brick2)
        brick = sprite(all_sprites, x*standart_size + a, y*standart_size + b)
        bricks.add(brick)
        door = Door(all_sprites, door_pos_x*standart_size + a, y*standart_size + b)
        bricks.add(door)
    else:
        for i in range(x):
            if i != door_pos_x:
                brick1 = sprite(all_sprites, i*standart_size + a, b)
                bricks.add(brick1)
            brick4 = sprite(all_sprites, i*standart_size + a, y*standart_size + b)
            bricks.add(brick4)
        for j in range(y):
            brick3 = sprite(all_sprites, x*standart_size + a, j*standart_size + b)
            brick2 = sprite(all_sprites, a, j*standart_size + b)
            bricks.add(brick3)
            bricks.add(brick2)
        brick = sprite(all_sprites, x*standart_size + a, y*standart_size + b)
        door = UpDoor(all_sprites, door_pos_x*standart_size + a, b)
        bricks.add(door)
    all_sprites.add(bricks)


player = Player(all_sprites, 30, 26)
make_room(Brick, (10, 10), 20, 10, 5)
make_room(Brick, (10, 200), 10, 5, 5, False)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.rect.y += 10
            if event.key == pygame.K_UP:
                player.rect.y -= 10
            if event.key == pygame.K_LEFT:
                player.rect.x -= 10
            if event.key == pygame.K_RIGHT:
                player.rect.x += 10

    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
