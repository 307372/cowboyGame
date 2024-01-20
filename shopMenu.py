import pygame
from pos import Pos

pygame.font.init()
font_size = 50
font = pygame.font.SysFont("Comic Sans MS", font_size)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


class ShopOption:
    def __init__(self, name, cost, effectLambda):
        self.effectLambda = effectLambda
        self.name = name
        self.cost = cost
        self.isAvailable = True

    def getTextSurface(self, isBuyable, isSelected):
        color = GREEN if isBuyable or not self.isAvailable else RED
        text = self.name + (f' ({self.cost})' if self.isAvailable else ' >>> SOLD OUT <<<')
        selection = '> ' if isSelected else '  '
        return font.render(selection + text, True, color)
    def draw(self, availableMoney, pos, screen, isSelected):
        isBuyable = availableMoney >= self.cost
        textSurface = self.getTextSurface(isBuyable, isSelected)
        screen.blit(textSurface, (pos.x, pos.y))

    def useEffect(self):
        self.effectLambda()
        self.isAvailable = False



class ShopMenu:
    def __init__(self, game):
        self.selectedOptionIndex = 0
        self.game = game
        self.screen = game.screen
        self.margin = 100
        self.previouslyPressedKeys = pygame.key.get_pressed()
        self.shopOptions = [ShopOption('Fire rate upgrade', 100, self.game.upgradeFireRate),
                            ShopOption('Guns for cows', 200, self.game.upgradeCows),
                            ShopOption('10 cows', 150, lambda: self.game.spawnCowsInShop(10))]

    def reactToInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.isInShop = False
            self.game.moveShopToRandomLocation()
            return
        if keys[pygame.K_s] and not self.previouslyPressedKeys[pygame.K_s]:
            self.selectedOptionIndex = (self.selectedOptionIndex + 1) % (len(self.shopOptions))
        elif keys[pygame.K_w] and not self.previouslyPressedKeys[pygame.K_w]:
            self.selectedOptionIndex = (self.selectedOptionIndex - 1) % (len(self.shopOptions))
        if keys[pygame.K_RETURN] and not self.previouslyPressedKeys[pygame.K_RETURN]:
            self.attemptToBuy()
        self.previouslyPressedKeys = keys

    def attemptToBuy(self):
        if self.game.milk > self.shopOptions[self.selectedOptionIndex].cost and self.shopOptions[self.selectedOptionIndex].isAvailable:
            self.shopOptions[self.selectedOptionIndex].useEffect()
            self.game.milk -= self.shopOptions[self.selectedOptionIndex].cost

    def draw(self):
        self.drawBackground()
        self.drawExitInformation()
        for optionIndex in range(len(self.shopOptions)):
            self.shopOptions[optionIndex].draw(self.game.milk,
                                          Pos(self.margin*1.5, self.margin*1.5 + (font_size*1.5*optionIndex)),
                                          self.screen, optionIndex == self.selectedOptionIndex)

    def drawBackground(self):
        [windowWidth, windowHeight] = pygame.display.get_window_size()
        backgroundRect = pygame.Rect(self.margin, self.margin, windowWidth - self.margin * 2, windowHeight - self.margin * 2)
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), backgroundRect)

    def drawExitInformation(self):
        [windowWidth, windowHeight] = pygame.display.get_window_size()
        textSurface = font.render('Press ESC to exit shop', True, GREEN)
        self.screen.blit(textSurface, (self.margin*1.5, windowHeight - self.margin*1.5))


    def run(self):
        self.reactToInput()
        self.draw()
