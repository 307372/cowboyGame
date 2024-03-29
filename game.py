import pygame
from player import Player
from cow import Cow
from enemy import Enemy
from pos import Pos
from rock import Rock
from bullet import Bullet
from shop import Shop
import random
import math

pygame.font.init()
font = pygame.font.SysFont("geneva", 20)
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_texture = pygame.image.load("img/grass_11.png")  # Replace with your background image path
        self.cows = [Cow(random.randrange(0, 1000) - 500, random.randrange(0, 1000) - 500, False) for i in range(12)]
        self.player = Player()
        self.enemies = [Enemy(self.getValidEnemySpawnLocation()) for i in range(12)]
        self.rocks = [Rock(self.getValidRockSpawnLocation()) for i in range(12)]
        self.shop = Shop(self.getValidRockSpawnLocation())
        self.bullets = []
        self.lastShootingDirection = Pos(0,1)
        self.frameCounter = 0
        self.isInShop = False
        self.milk = 0
        self.cowShootingDelay = 10
        self.nextCowShootableFrame = 0
        self.isCowUpgradeBought = False


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
        for cow in self.cows:
            cow.draw(cameraOffset)

        self.shop.draw(cameraOffset)
        self.drawMilkCounter()

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

    def playerShoot(self):
        if self.player.nextShootableFrame < self.frameCounter:
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
                self.player.updateNextShootableFrame(self.frameCounter)
            elif bulletDirection.len() == 0 and keys[pygame.K_UP]:
                self.bullets.append(Bullet(self.player.pos, self.lastShootingDirection, self.frameCounter))
                self.player.updateNextShootableFrame(self.frameCounter)


    def cowShoot(self):
        if self.isCowUpgradeBought and self.nextCowShootableFrame < self.frameCounter:
            for cowIndex in range(len(self.cows)):
                bulletDirection = self.getCowRingFormationPlayerOffset(len(self.cows), cowIndex).normalized()
                self.bullets.append(Bullet(self.cows[cowIndex].pos, bulletDirection, self.frameCounter))
            self.nextCowShootableFrame = self.frameCounter + self.cowShootingDelay

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
        self.milk += len(self.cows) / 60

    def drawMilkCounter(self):
        text = font.render(f"{math.floor(self.milk)} milk", True, (245, 255, 230))
        self.screen.blit(text, (text.get_width() // 2, text.get_height() // 2))

    def removeExpiredBullets(self):
        bulletsToRemove = []
        for bulletIndex in range(len(self.bullets)):
            if self.bullets[bulletIndex].isExpired(self.frameCounter):
                bulletsToRemove.append(bulletIndex)
        self.removeBullets(bulletsToRemove)

    def spawnEnemies(self, amount):
        for i in range(amount):
            self.enemies.append(Enemy(self.getValidEnemySpawnLocation()))

    def moveShopToRandomLocation(self):
        self.shop = Shop(self.getValidRockSpawnLocation())


    def openShopIfClose(self):
        if Pos.len(self.shop.pos - self.player.pos) < self.shop.hitboxRadius:
            self.isInShop = True

    def upgradeFireRate(self):
        self.player.shootingDelay = 0

    def upgradeCows(self):
        self.isCowUpgradeBought = True
        for cow in self.cows:
            cow.upgrade()

    def spawnCowsInShop(self, amount):
        for i in range(amount):
            self.cows.append(Cow(self.shop.pos.x, self.shop.pos.y, self.isCowUpgradeBought))

    def run(self):
        self.player.move()
        self.playerShoot()
        self.cowShoot()
        self.bulletAi()
        self.removeExpiredBullets()
        self.allyAi()
        self.enemyAi()
        self.updateMilk()
        self.openShopIfClose()
        if self.frameCounter % 30 == 0 and len(self.enemies) < 30:
            self.spawnEnemies(1)

        self.draw()
        self.frameCounter += 1
