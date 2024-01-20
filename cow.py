import pygame
from pos import Pos
class Cow:
    # Class attribute to store the loaded texture
    texture = None

    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.movementSpeed = 2

        # Load the texture only once if it's not already loaded
        if not Cow.texture:
            Cow.texture = pygame.image.load("img/cow.gif")  # Replace with the actual path

        # Scale the texture to 200x200 pixels
        self.texture = pygame.transform.scale(Cow.texture, (200, 200))

    def draw(self):
        pygame.display.get_surface().blit(self.texture, (self.pos.x, self.pos.y))

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


