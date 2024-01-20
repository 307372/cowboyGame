import pygame

import player
from player import Player
from cow import Cow
from enemy import Enemy
from pos import Pos
from rock import Rock
from bullet import Bullet
import random
import math

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_texture = pygame.image.load("img/grass_11.png")  # Replace with your background image path
        self.cows = [Cow(random.randrange(0, 1000) - 500, random.randrange(0, 1000) - 500) for i in range(12)]
        self.player = Player()
        self.enemies = [Enemy(self.getValidEnemySpawnLocation()) for i in range(12)]
        self.rocks = [Rock(self.getValidRockSpawnLocation()) for i in range(12)]
        self.bullets = []
        self.lastShootingDirection = Pos(0,1)
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
        for bullet in self.bullets:
            bullet.draw(cameraOffset)
        for cowIndex in range(len(self.cows)):
            text_surface = my_font.render(str(cowIndex), False, (0,0,0))
            self.cows[cowIndex].draw(cameraOffset)
            self.screen.blit(text_surface, (self.cows[cowIndex].pos.x+cameraOffset.x, self.cows[cowIndex].pos.y+cameraOffset.y))

    def allyAi(self):
        for i in range(len(self.cows)):
            self.cows[i].moveTowards(self.player.pos + self.getCowRingFormationPlayerOffset(len(self.cows), i))

    def enemyAi(self):
        cowsToRemove = []
        enemiesToRemove = []
        for enemyIndex in range(len(self.enemies)):
            minDist = 1000000
            minCowIndex = self.player.pos
            for cowIndex in range(len(self.cows)):
                dist = Pos.len(self.enemies[enemyIndex].pos - self.cows[cowIndex].pos)
                if dist < minDist:
                    minDist = dist
                    minCowIndex = cowIndex
            if minDist != 1000000:
                self.enemies[enemyIndex].moveTowards(self.cows[minCowIndex].pos)
                dist = Pos.len(self.enemies[enemyIndex].pos - self.cows[minCowIndex].pos)
                if dist < self.enemies[enemyIndex].range:
                    enemiesToRemove.append(enemyIndex)
                    cowsToRemove.append(minCowIndex)
        if len(cowsToRemove):
            cowsToRemove = sorted(list(dict.fromkeys(cowsToRemove)), reverse=True)
            for cowIndex in cowsToRemove:
                self.cows.pop(cowIndex)

        if len(enemiesToRemove):
            enemiesToRemove = sorted(list(dict.fromkeys(enemiesToRemove)), reverse=True)
            for enemyIndex in enemiesToRemove:
                self.enemies.pop(enemyIndex)



    def getCowRingFormationPlayerOffset(self, amountOfCows, cowNumber):
        radius = 75
        deg = 360/amountOfCows
        angle = deg*cowNumber
        return self.getUnitaryVectorFromAngle(angle) * radius


    def getUnitaryVectorFromAngle(self, angle):
        offset = Pos(0, 0)
        if angle <= 90:
            offset.x = math.sin(math.radians(angle))
            offset.y = -math.cos(math.radians(angle))
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

    def shoot(self):
        keys = pygame.key.get_pressed()
        bulletDirection = Pos(0, 0)
        if keys[pygame.K_UP]:
            bulletDirection.y -= 1
        if keys[pygame.K_DOWN]:
            bulletDirection.y += 1
        if keys[pygame.K_LEFT]:
            bulletDirection.x -= 1
        if keys[pygame.K_RIGHT]:
            bulletDirection.x += 1



        if bulletDirection.len() > 0:
            bulletDirection = bulletDirection.normalized()
            self.lastShootingDirection = bulletDirection
            self.bullets.append(Bullet(self.player.pos, bulletDirection))
        if bulletDirection.len() == 0 and keys[pygame.K_UP]:
            self.bullets.append(Bullet(self.player.pos, self.lastShootingDirection))



    def bulletAi(self):
        for bullet in self.bullets:
            bullet.move()

    def run(self):
        self.player.move()
        self.shoot()
        self.bulletAi()
        self.allyAi()
        self.enemyAi()
        self.draw()
