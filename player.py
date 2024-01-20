import pygame
from pos import Pos

class Player:
    def __init__(self):
        self.pos = Pos(0, 0)
        self.movementSpeed = 5
        self.width = 50
        self.height = 100
        self.texture = pygame.image.load("img/sprite_05.png")
        self.origin = Pos(self.width / 2, self.height / 2)
        if not self.texture:
            # Load the texture only once if it's not already loaded
            Player.texture = pygame.image.load("img/sprite_05.png")  # Replace with the actual path

        # Scale the texture to 20x20 pixels
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))



    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))
        # pygame.draw.rect(pygame.display.get_surface(), (0,255,0), pygame.Rect(self.pos.x-1.25, self.pos.y-1.25, 5, 5))
        # pygame.draw.rect(pygame.display.get_surface(), (255,0,0), pygame.Rect(self.pos.x, self.pos.y, 1, 1))

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