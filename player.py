import pygame

class Player:
    pos = [0,0]
    def draw(self):
        print('drawowanie')
        pygame.draw.rect(pygame.display.get_surface(), (255,255,0), pygame.Rect(self.pos[0], self.pos[1], 50, 100))

    def move(self, deltaX, deltaY):
        self.pos[0] += deltaX
        self.pos[1] += deltaY