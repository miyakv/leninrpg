import pygame
from lib_board import Board
from lib_location import Location
from lib_sprites import Player, make_room, Brick

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites, 1, 1)
        self.locations = {'home': Location(screen, 5, 5, make_room(Brick, (5, 5), 7, 5, 1), (1, 2))}
        self.current_location = self.locations['home']
        # all game info here

jeu = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                jeu.player.move('up')
            if event.key == pygame.K_a:
                jeu.player.move('left')
            if event.key == pygame.K_s:
                jeu.player.move('down')
            if event.key == pygame.K_d:
                jeu.player.move('right')
    screen.fill((0, 0, 0))
    jeu.current_location.render_sprites(jeu.all_sprites) # unfinished!!1!
    pygame.display.flip()
pygame.quit()
