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
        self.cows = [Cow(random.randrange(0, 1000) - 500, random.randrange(0, 1000) - 500) for i in range(12)]
    player = Player()

    def getCameraOffset(self):
        [width, height] = self.screen.get_size()
        return Pos(width/2, height/2) - self.player.pos
    def draw(self):
        self.screen.fill((255, 255, 255))
        cameraOffset = self.getCameraOffset()
        self.player.draw(cameraOffset)
        for cow in self.cows:
            cow.draw(cameraOffset)

    def allyAi(self):
        for i in range(len(self.cows)):
            self.cows[i].moveTowards(self.player.pos + self.getCowRingFormationPlayerOffset(len(self.cows), i))

    def getCowRingFormationPlayerOffset(self, amountOfCows, cowNumber):
        radius = 200
        deg = 360/amountOfCows
        angle = deg*cowNumber
        offset = Pos(0,0)
        if angle <= 90:
            offset.x = math.cos(math.radians(angle)) * radius
            offset.y = -math.sin(math.radians(angle)) * radius
        elif angle <= 180:
            offset.x = math.cos(math.radians(angle - 90)) * radius
            offset.y = math.sin(math.radians(angle - 90)) * radius
        elif angle <= 270:
            offset.x = -math.sin(math.radians(angle - 180)) * radius
            offset.y = math.cos(math.radians(angle - 180)) * radius
        else:
            offset.x = -math.cos(math.radians(angle - 270)) * radius
            offset.y = -math.sin(math.radians(angle - 270)) * radius
        return offset




    def run(self):
        self.player.move()
        self.allyAi()
        self.draw()

