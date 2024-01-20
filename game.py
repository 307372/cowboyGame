import pygame
from player import Player

class Game:
    screen = 0
    def __init__(self, screen):
        self.screen = screen
    player = Player()
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.player.draw()
        #self.screen.flip()

    def readInput(self):
        keys = pygame.key.get_pressed()
        movement = [0, 0]
        if keys[pygame.K_w]:
            movement[1] -= 1
        if keys[pygame.K_s]:
            movement[1] += 1
        if keys[pygame.K_a]:
            movement[0] -= 1
        if keys[pygame.K_d]:
            movement[0] += 1
        self.player.move(movement[0], movement[1])

    def run(self):
        self.readInput()
        self.draw()

