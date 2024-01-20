import pygame
from pos import Pos

class Player:
    def __init__(self):
        self.pos = Pos(500, 500)
        self.movementSpeed = 5
    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), (255,255,0), pygame.Rect(self.pos.x, self.pos.y, 50, 100))

    def move(self):
        keys = pygame.key.get_pressed()
        movement = Pos(0, 0)
        if keys[pygame.K_w]:
            movement.y -= self.movementSpeed
        if keys[pygame.K_s]:
            movement.y += self.movementSpeed
        if keys[pygame.K_a]:
            movement.x -= self.movementSpeed
        if keys[pygame.K_d]:
            movement.x += self.movementSpeed
        self.pos += movement