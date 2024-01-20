import pygame
from pos import Pos

pygame.font.init()
font_size = 50
font = pygame.font.SysFont("Comic Sans MS", font_size)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


class ShopOption:
    def __init__(self, name, cost):
        self.text = name + f' ({cost})'
        self.cost = cost
        self.isAvailable = True  # TODO: check

    def draw(self, availableMoney, pos, screen):
        color = GREEN if availableMoney >= self.cost else RED
        textSurface = font.render(self.text, True, color)
        screen.blit(textSurface, (pos.x, pos.y))

shopOptions = [ShopOption('Fire rate upgrade', 100),
               ShopOption('Guns for cows', 100)]
class ShopMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.margin = 100

    def reactToInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.isInShop = False
            self.game.moveShopToRandomLocation()
            return

    def draw(self):
        self.drawBackground()
        for optionIndex in range(len(shopOptions)):
            shopOptions[optionIndex].draw(self.game.milk, Pos(self.margin*1.5, self.margin*1.5 + (font_size*1.5*optionIndex)), self.screen)

    def drawBackground(self):
        [windowWidth, windowHeight] = pygame.display.get_window_size()
        backgroundRect = pygame.Rect(self.margin, self.margin, windowWidth - self.margin * 2, windowHeight - self.margin * 2)
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), backgroundRect)

    def run(self):
        self.reactToInput()
        self.draw()
    