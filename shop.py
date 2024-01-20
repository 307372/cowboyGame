from pos import Pos
import pygame


class Shop():
    def __init__(self, pos):
        self.pos = pos
        self.movementSpeed = 5
        self.width = 200
        self.height = 200
        #self.texture = pygame.image.load("img/sprite_05.png")
        self.origin = Pos(self.width / 2, self.height / 2)
        self.hitboxRadius = (self.width / 2 + self.origin.len()) / 2

    def draw(self, cameraOffset):
        drawPos = self.pos - self.origin + cameraOffset
        # pygame.display.get_surface().blit(self.texture, (drawPos.x, drawPos.y))
        pygame.draw.rect(pygame.display.get_surface(), (0,0,0), pygame.Rect(drawPos.x, drawPos.y, self.width, self.height))
        # pygame.draw.rect(pygame.display.get_surface(), (255,0,0), pygame.Rect(self.pos.x, self.pos.y, 1, 1))