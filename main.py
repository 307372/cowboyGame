# Simple pygame program

# Import and initialize the pygame library
import pygame
from player import Player
from game import Game
pygame.init()
FPS = 60

# Initialize Pygame mixer
file = 'music/1.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
pygame.event.wait()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000], vsync=1)
game = Game(screen)
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.run()
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()
