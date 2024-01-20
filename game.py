import pygame

import player
from player import Player
from cow import Cow
from enemy import Enemy
from pos import Pos
from rock import Rock
import random
import math

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_texture = pygame.image.load("img/grass_11.png")  # Replace with your background image path
        self.cows = [Cow(random.randrange(0, 1000) - 500, random.randrange(0, 1000) - 500) for i in range(12)]
        self.player = Player()
        self.enemies = [Enemy(self.getValidEnemySpawnLocation()) for i in range(12)]
        self.rocks = [Rock(self.getValidRockSpawnLocation()) for i in range(12)]

    def getValidEnemySpawnLocation(self):
        angle = random.randrange(0, 360)
        [x, y] = self.screen.get_size()
        halfScreenDiagonal = Pos(x/2, y/2).len()
        spawnOffset = self.getUnitaryVectorFromAngle(angle) * halfScreenDiagonal
        return self.player.pos + spawnOffset

    def getValidRockSpawnLocation(self):
        angle = random.randrange(0, 360)
        [x, y] = self.screen.get_size()
        halfScreenDiagonal = Pos(x/2, y/2).len()
        spawnOffset = self.getUnitaryVectorFromAngle(angle) * halfScreenDiagonal
        return self.player.pos + spawnOffset

    def getCameraOffset(self):
        [width, height] = self.screen.get_size()
        return Pos(width / 2, height / 2) - self.player.pos

    def draw(self):
        # Draw the background
        self.screen.blit(self.background_texture, (0, 0))

        # Draw player and cows on top of the background
        cameraOffset = self.getCameraOffset()
        self.player.draw(cameraOffset)
        for enemy in self.enemies:
            enemy.draw(cameraOffset)
        for rock in self.rocks:
            rock.draw(cameraOffset)
        for cow in self.cows:
            cow.draw(cameraOffset)

    def allyAi(self):
        for i in range(len(self.cows)):
            self.cows[i].moveTowards(self.player.pos + self.getCowRingFormationPlayerOffset(len(self.cows), i))

    def enemyAi(self):
        pass
        # for enemy in enemies:
        # for i in range(len(self.cows)):
        #     self.cows[i].moveTowards(self.player.pos + self.getCowRingFormationPlayerOffset(len(self.cows), i))

    def getCowRingFormationPlayerOffset(self, amountOfCows, cowNumber):
        radius = 200
        deg = 360/amountOfCows
        angle = deg*cowNumber
        return self.getUnitaryVectorFromAngle(angle) * radius


    def getUnitaryVectorFromAngle(self, angle):
        offset = Pos(0, 0)
        if angle <= 90:
            offset.x = math.cos(math.radians(angle))
            offset.y = -math.sin(math.radians(angle))
        elif angle <= 180:
            offset.x = math.cos(math.radians(angle - 90))
            offset.y = math.sin(math.radians(angle - 90))
        elif angle <= 270:
            offset.x = -math.sin(math.radians(angle - 180))
            offset.y = math.cos(math.radians(angle - 180))
        else:
            offset.x = -math.cos(math.radians(angle - 270))
            offset.y = -math.sin(math.radians(angle - 270))
        return offset

    def run(self):
        self.player.move()
        self.allyAi()
        self.enemyAi()
        self.draw()
