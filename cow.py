import pygame
from pos import Pos


class Cow:
    # Class attribute to store the loaded texture
    base_texture = None
    upgraded_texture = None

    def __init__(self, x, y, isUpgraded):
        self.pos = Pos(x, y)
        self.width = 50
        self.height = 50
        self.origin = Pos(self.width / 2, self.height / 2)
        self.isUpgraded = isUpgraded
        self.movementSpeed = 2 if not self.isUpgraded else 4

        if not Cow.base_texture:
            Cow.base_texture = pygame.image.load("img/cow.gif")
        if not Cow.upgraded_texture:
            Cow.upgraded_texture = pygame.image.load("img/cow_upgraded.png")

        self.base_texture = pygame.transform.scale(Cow.base_texture, (self.width, self.height))
        self.upgraded_texture = pygame.transform.scale(Cow.upgraded_texture, (self.width, self.height))

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.display.get_surface().blit(self.upgraded_texture if self.isUpgraded else self.base_texture, (drawPos.x, drawPos.y))

    def upgrade(self):
        self.movementSpeed = 4
        self.isUpgraded = True
    def moveTowards(self, target):
        movement = Pos(0, 0)
        if self.pos.x > target.x:
            movement.x -= self.movementSpeed
        elif self.pos.x < target.x:
            movement.x += self.movementSpeed
        if self.pos.y > target.y:
            movement.y -= self.movementSpeed
        elif self.pos.y < target.y:
            movement.y += self.movementSpeed
        if Pos.len(target - self.pos) > movement.len():
            self.pos += movement
        else:
            self.pos = target


