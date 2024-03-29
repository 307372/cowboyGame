import pygame
from pos import Pos

class Rock:
    # Class attribute to store the loaded texture
    texture = None
    def __init__(self, pos):
        self.pos = pos
        self.width = 100
        self.height = 100
        self.origin = Pos(self.width / 2, self.height / 2)
        self.hitboxRadius = (self.width / 2 + self.origin.len()) / 2

        if not Rock.texture:
            Rock.texture = pygame.image.load("img/rock.png")  # Replace with the actual path

        # Scale the texture to 200x200 pixels
        self.texture = pygame.transform.scale(Rock.texture, (self.width, self.height))

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))


