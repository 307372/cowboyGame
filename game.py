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
font = pygame.font.SysFont("geneva", 20)
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
        self.frameCounter = 0
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
        self.screen.blit(self.background_texture, (0, 0))
        cameraOffset = self.getCameraOffset()
        self.player.draw(cameraOffset)
        for enemy in self.enemies:
            enemy.draw(cameraOffset)
        for rock in self.rocks:
            rock.draw(cameraOffset)
        for bullet in self.bullets:
            bullet.draw(cameraOffset)
        for cowIndex in range(len(self.cows)):
            self.cows[cowIndex].draw(cameraOffset)

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
        self.removeCows(cowsToRemove)
        self.removeEnemies(enemiesToRemove)



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
            self.bullets.append(Bullet(self.player.pos, bulletDirection, self.frameCounter))
        elif bulletDirection.len() == 0 and keys[pygame.K_UP]:
            self.bullets.append(Bullet(self.player.pos, self.lastShootingDirection, self.frameCounter))



    def bulletAi(self):
        bulletsToRemove = []
        for bulletIndex in range(len(self.bullets)):
            self.bullets[bulletIndex].move()

            for rock in self.rocks:
                if Pos.len(rock.pos - self.bullets[bulletIndex].pos) < rock.hitboxRadius:
                    bulletsToRemove.append(bulletIndex)

            enemiesToRemove = []
            for enemyIndex in range(len(self.enemies)):
                if Pos.len(self.enemies[enemyIndex].pos - self.bullets[bulletIndex].pos) < self.enemies[enemyIndex].hitboxRadius:
                    enemiesToRemove.append(enemyIndex)

            self.removeEnemies(enemiesToRemove)
        self.removeBullets(bulletsToRemove)

    def removeBullets(self, bulletsToRemove):
        if len(bulletsToRemove):
            bulletsToRemove = sorted(list(dict.fromkeys(bulletsToRemove)), reverse=True)
            for bulletIndex in bulletsToRemove:
                self.bullets.pop(bulletIndex)

    def removeEnemies(self, enemiesToRemove):
        if len(enemiesToRemove):
            enemiesToRemove = sorted(list(dict.fromkeys(enemiesToRemove)), reverse=True)
            for enemyIndex in enemiesToRemove:
                self.enemies.pop(enemyIndex)

    def removeCows(self, cowsToRemove):
        if len(cowsToRemove):
            cowsToRemove = sorted(list(dict.fromkeys(cowsToRemove)), reverse=True)
            for cowIndex in cowsToRemove:
                self.cows.pop(cowIndex)

    def updateMilk(self):
        start_time = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        text = font.render(f"{elapsed_time} milk", True, (245, 255, 230))
        self.screen.blit(text, (text.get_width() // 2, text.get_height() // 2))

    def removeExpiredBullets(self):
        bulletsToRemove = []
        for bulletIndex in range(len(self.bullets)):
            if self.bullets[bulletIndex].isExpired(self.frameCounter):
                bulletsToRemove.append(bulletIndex)
        self.removeBullets(bulletsToRemove)
    def run(self):
        self.player.move()
        self.shoot()
        self.bulletAi()
        self.removeExpiredBullets()
        self.allyAi()
        self.enemyAi()
        self.draw()
        self.updateMilk()
        self.frameCounter += 1
