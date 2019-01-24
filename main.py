import pygame
from lib_sprites import *

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites, 32, 32)
        self.bricks = set()
        for i in range(6):
            self.bricks.add(Brick(self.all_sprites, 0, i * config.TILE_SIZE))
        for i in range(8):
            self.bricks.add(Brick(self.all_sprites, i * config.TILE_SIZE, 0))
        for i in range(6):
            self.bricks.add(Brick(self.all_sprites, config.TILE_SIZE * 7, i * config.TILE_SIZE))
        for i in range(8):
            if i != 5:
                self.bricks.add(Brick(self.all_sprites, i * config.TILE_SIZE, config.TILE_SIZE * 5))
        self.doors = set()
        self.doors.add(Door(self.all_sprites, 80, 80))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for door in self.doors:
                            door.get_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.move('up')
                    if event.key == pygame.K_a:
                        self.player.move('left')
                    if event.key == pygame.K_s:
                        self.player.move('down')
                    if event.key == pygame.K_d:
                        self.player.move('right')
            screen.fill((202, 255, 255))
            self.all_sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()


game = Game()
