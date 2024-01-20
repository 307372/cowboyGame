import pygame
from pos import Pos

class Enemy:
    # Class attribute to store the loaded texture
    texture = None

    def __init__(self, pos):
        self.pos = pos
        self.width = 75
        self.height = 75
        self.origin = Pos(self.width / 2, self.height / 2)
        self.range = self.width / 2
        self.movementSpeed = 2

        if not Enemy.texture:
            Enemy.texture = pygame.image.load("img/howl.png")  # Replace with the actual path

        # Scale the texture to 200x200 pixels
        self.texture = pygame.transform.scale(Enemy.texture, (self.width, self.height))

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))

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
