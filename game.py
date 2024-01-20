import pygame
from player import Player
from cow import Cow
from pos import Pos
import random
import math

class Game:
    screen = 0

    def __init__(self, screen):
        self.screen = screen
        self.cows = [Cow(random.randrange(0, 1000), random.randrange(0, 1000)) for i in range(60)]
    player = Player()
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.player.draw()
        for cow in self.cows:
            cow.draw()

    def allyAi(self):
        for i in range(len(self.cows)):
            self.cows[i].moveTowards(self.player.pos + self.getCowRingFormationPlayerOffset(len(self.cows), i))

    def getCowRingFormationPlayerOffset(self, amountOfCows, cowNumber):
        radius = 200
        deg = 360/amountOfCows
        angle = deg*cowNumber
        offset = Pos(0,0)
        if angle <= 90:
            offset.x = math.cos(angle) * radius
            offset.y = math.sin(angle) * radius
        elif angle <= 180:
            offset.x = math.cos(angle - 90) * radius
            offset.y = -math.sin(angle - 90) * radius
        elif angle <= 270:
            pass
        else:
            pass
        return offset

    def run(self):
        self.player.move()
        self.allyAi()
        self.draw()

