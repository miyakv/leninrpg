import pygame
from lib_sprites import *
from config import *
import time

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60

grey = (120, 120, 120)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
bright_green = (20, 200, 20)
block_color = (53, 115, 255)
bright_red = (200, 20, 20)


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
        self.tile_group = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.workers = pygame.sprite.Group()
        self.run()

    def run(self):
        self.game_intro()
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
                elif level[y][x] == 's':
                    Tile('street', self.tile_group, x * TILE_SIZE, y * TILE_SIZE)

        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '_':
                    Door(self.all_sprites, x * TILE_SIZE, y * TILE_SIZE)
                elif level[y][x] == 'b':
                    Tile('grey_wood', self.boarding, x * TILE_SIZE, y * TILE_SIZE)
        return new_player

    def game_intro(self):
        intro = True
        largeText = pygame.font.SysFont("comicsansms", 80)
        TextSurf, TextRect = self.text_objects("Red Flag", largeText)
        TextRect.center = (250, 95)
        fon = images['menu']
        pygame.mixer.music.load('data/main.mp3')
        pygame.mixer.music.play(9999)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill((0, 0, 0))
            screen.blit(fon, (0, 0))
            screen.blit(TextSurf, TextRect)

            self.button("Start!", 100, 450, 100, 50,green,bright_green, self.factory_level)
            self.button("Quit", 300, 450, 100, 50, red,bright_red, self.quitgame)

            pygame.display.update()
            clock.tick(15)

    def factory_level(self):
        going = False
        self.boarding = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.arrow = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.player = self.generate_level(self.load_level('factory.txt'))
        clock = pygame.time.Clock()
        pressed_left = pressed_right = pressed_up = pressed_down = False
        camera = Camera()
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

            camera.update(self.player)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            for tile in self.tile_group:
                camera.apply(tile)
            for obj in self.boarding:
                camera.apply(obj)

            if pygame.sprite.spritecollideany(self.player, self.boarding):
                    going = True

            if going:
                self.workers.update()
            screen.fill(grey)
            self.tile_group.draw(screen)
            self.all_sprites.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        screen.blit(textSurf, textRect)

    def load_level(self, filename):
        filename = 'data/' + filename
        with open(filename, 'r') as map_file:
            level_map = [line.strip() for line in map_file]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def quitgame(self):
        pygame.quit()
        quit()


game = Game()
