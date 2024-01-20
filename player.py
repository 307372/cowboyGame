import pygame
from pos import Pos

class Player:
    pos = Pos(500,500)
    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), (255,255,0), pygame.Rect(self.pos.x, self.pos.y, 50, 100))

    def move(self, deltaX, deltaY):
        self.pos.x += deltaX
        self.pos.y += deltaY