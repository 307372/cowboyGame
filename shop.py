from pos import Pos
import pygame


class Shop:
    texture = None
    def __init__(self, pos):
        self.pos = pos
        self.movementSpeed = 5
        self.width = 200
        self.height = 200

        self.origin = Pos(self.width / 2, self.height / 2)
        self.hitboxRadius = (self.width / 2 + self.origin.len()) / 2

        if not Shop.texture:
            Shop.texture = pygame.image.load("img/shop.png")
        self.texture = pygame.transform.scale(Shop.texture, (self.width, self.height))

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))
