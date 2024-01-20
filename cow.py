import pygame
from pos import Pos
class Cow:
    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.movementSpeed = 2

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), pygame.Rect(self.pos.x, self.pos.y, 50, 50))

    def moveTowards(self, target):
        # will follow player
        movement = Pos(0, 0)
        if self.pos.x > target.x:
            movement.x -= self.movementSpeed
        elif self.pos.x < target.x:
            movement.x += self.movementSpeed
        if self.pos.y > target.y:
            movement.y -= self.movementSpeed
        elif self.pos.y < target.y:
            movement.y += self.movementSpeed
        self.pos += movement


