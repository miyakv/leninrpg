import pygame
from config import *
import os
import random

pygame.mixer.init()

open_door = pygame.mixer.Sound('waves/open.wav')
close_door = pygame.mixer.Sound('waves/close.wav')
car_driving = pygame.mixer.Sound('waves/car.wav')
crash = pygame.mixer.Sound('data/crash.wav')
pm_work = pygame.mixer.Sound('waves/paper_machine.wav')

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
ydoor_image = load_image('door1.png')
lenin_image = load_image('lenin.gif', (255, 255, 255))
mouse_image = load_image('mouse.png', (0, 0, 0))
worker_image = load_image('worker.png', (255, 255, 255))
lenin_car = load_image('lenin_car.jpg', (255, 255, 255))
images = {'worker': worker_image, 'menu': load_image('1.jpg'), 'bordur': load_image('bordur.jpg'),
          'car': load_image('car.png', (255, 255, 255)), 'woody': load_image('woody.png'),
          'brick': brick_image, 'paper': load_image('pm.jpg'), 'news': load_image('news.png'),
          'driving_car': load_image('driving_car.jpg', (255, 255, 255)),
          'lenin': load_image('lenin.gif', (255, 255, 255)), 'empire_flag': load_image('russia_flag.jpg'),
          'game_over': load_image('gameover.jpg'), 'guide_paper': load_image('guide_paper.png'),
          'guide_driving': load_image('guide_driving.png'), 'white': load_image('white.jpg', (255, 255, 255))}


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, group, x, y):
        super().__init__()
        self.group = group
        self.image = images[image]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_able = False
        self.group.add(self)


class Trap(Brick):
    pass


class Boarding(Brick):
    pass


class NPC(Brick):
    pass


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, group, group2, columns, raws, x, y):
        super().__init__(group, group2)
        self.frames = []
        sheet2 = images[sheet]
        self.cut_sheet(sheet2, columns, raws)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.group = group

    def cut_sheet(self, sheet, columns, raws):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // raws)
        for i in range(raws):
            for j in range(columns):
                frame = (self.rect.w * j, self.rect.h * i)
                self.frames.append(sheet.subsurface(pygame.Rect(frame,
                                                    self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.cur_frame + 1 == len(self.frames):
            Paper('news', self.group, self.rect.x + 12, self.rect.y - 15)
        self.image = self.frames[self.cur_frame]


class Machine(AnimatedSprite):
    def __init__(self, sheet, group, group2, columns, raws, x, y):
        super().__init__(sheet, group, group2, columns, raws, x, y)
        self.working = False
        self.rest = 0

    def update(self):
        if self.working and self.rest == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.cur_frame + 1 == len(self.frames):
                Paper('news', self.group, self.rect.x + 12, self.rect.y - 15)
                self.working = False
                pm_work.stop()
                self.rest = 150
            self.image = self.frames[self.cur_frame]
        else:
            if self.rest > 0:
                self.rest -= 1


class Paper(Brick):
    pass


class Car(Brick):
    def update(self):
        self.image = lenin_car
        self.rect.x -= 5
        self.move_able = True


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
            self.image = ydoor_image
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
        if self.rect.collidepoint(event.pos):
            self.update()


class YDoor(Door):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.image = ydoor_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.now == 0:
            self.rect.x += TILE_SIZE
            copy = self.rect
            self.image = door_image
            self.rect = self.image.get_rect()
            self.rect.x = copy.x - 50
            self.rect.y = copy.y - 10
            self.now = 1
            open_door.play()
        else:
            copy = self.rect
            self.image = ydoor_image
            self.rect.x -= TILE_SIZE
            self.rect = self.image.get_rect()
            self.rect.x += copy.x + 50
            self.rect.y += copy.y + 10
            self.now = 0
            close_door.play()


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
        self.status = 1

    def update(self):
        if self.status == 1:
            self.change()
        else:
            self.back()
        self.rect.x += 7

    def change(self):
        self.image = images['dead_worker']
        self.status = 2

    def back(self):
        self.image = images['worker']
        self.status = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y):
        super().__init__()
        self.group = group
        self.image = images[image]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = True
        self.updating = True
        self.money = 0
        self.health = 100
        self.inventory = {'news': 0}
        self.goals = {'news': 10, 'meters': 1000}

        group.add(self)

    def possible_move(self):
        info = pygame.sprite.spritecollide(self, self.group, False)
        if len(info) == 1:
            return True
        for i in info:
            if type(i) == Machine:
                if i.rest == 0 and i.working == False:
                    i.working = True
                    pm_work.play()
            elif type(i) == Paper:
                i.kill()
                self.inventory['news'] += 1
                if self.goals['news'] > 0:
                    self.goals['news'] -= 1
            elif type(i) == Car:
                self.inventory['news'] = 0
                if self.goals['news'] == 0:
                    self.kill()
                    self.updating = False
                    car_driving.play()
                    i.update()

        return False

    def move(self, direction):
        if self.moving:
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


class DrivingCar(Player):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)
        self.crashed = False
        self.win = False

    def crash(self):
        if not self.crashed:
            crash.play()
            self.crashed = True

    def show_win(self):
        if not self.win:
            self.win = True
            car_driving.play()

    def possible_move(self):
        info = pygame.sprite.spritecollide(self, self.group, False)
        if len(info) == 1:
            return True
        else:
            return False

