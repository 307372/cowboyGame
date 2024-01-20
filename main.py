# Simple pygame program

# Import and initialize the pygame library
import pygame
from player import Player
from game import Game
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])
game = Game(screen)

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.run()
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()
