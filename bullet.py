import pygame
from pos import Pos


BULLET_LIFESPAN = 5 * 60
class Bullet:
    def __init__(self, position, directionVector, currentFrame):
        self.pos = position
        self.height = 5
        self.width = 5
        self.origin = Pos(self.width / 2, self.height / 2)
        self.direction = directionVector
        self.movementSpeed = 10
        self.despawnFrame = currentFrame + BULLET_LIFESPAN


    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), pygame.Rect(drawPos.x, drawPos.y, self.width, self.height))

    def move(self):
        self.pos += self.direction * self.movementSpeed

    def isExpired(self, currentFrame):
        return currentFrame > self.despawnFrame
