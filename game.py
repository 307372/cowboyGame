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

    def allyAi(self):
        for cow in self.cows:
            cow.moveTowards(self.player.pos)

    def getCowRingFormationPlayerOffset(self, amountOfCows, cowNumber):
        radius = 50
        deg = 360/amountOfCows
        angle = deg*cowNumber
        if angle <= 90:
            pass
        elif angle <= 180:
            pass
        elif angle <= 270:
            pass
        else:
            pass


    def run(self):
        self.player.move()
        self.allyAi()
        self.draw()

