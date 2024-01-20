import pygame
from player import Player
from cow import Cow
import random

class Game:
    screen = 0

    def __init__(self, screen):
        self.screen = screen
        self.cows = [Cow(random.randrange(0, 1000), random.randrange(0, 1000)) for i in range(3)]
    player = Player()
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.player.draw()
        for cow in self.cows:
            cow.draw()

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

    def allyAi(self):
        for cow in self.cows:
            cow.moveTowards(self.player.pos)

    def run(self):
        self.readInput()
        self.allyAi()
        self.draw()

