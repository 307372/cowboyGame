import pygame
from pos import Pos

class Player:
    def __init__(self):
        self.pos = Pos(500, 500)
        self.movementSpeed = 5
        self.width = 50
        self.height = 100
        self.texture = pygame.image.load("img/sprite_05.png")
        if not self.texture:
            # Load the texture only once if it's not already loaded
            Player.texture = pygame.image.load("img/sprite_05.png")  # Replace with the actual path

        # Scale the texture to 20x20 pixels
        self.texture = pygame.transform.scale(self.texture, (200, 200))



    def draw(self):
        # pygame.draw.rect(pygame.display.get_surface(), (255, 255, 0), pygame.Rect(self.pos.x, self.pos.y, self.width, self.height))
        pygame.display.get_surface().blit(self.texture, (self.pos.x, self.pos.y))

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