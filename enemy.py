import pygame
from pos import Pos

class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.width = 100
        self.height = 100
        self.origin = Pos(self.width / 2, self.height / 2)
        self.movementSpeed = 2

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        #pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), pygame.Rect(drawPos.x, drawPos.y, 50, 50))

    def moveTowards(self, target):
        # will move towards target
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
