# Simple pygame program

# Import and initialize the pygame library
import pygame
from player import Player

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])
player = Player()


# Run until the user asks to quit

def reactToKeyboardInputs():
    keys = pygame.key.get_pressed()
    movement = [0, 0]
    if keys[pygame.K_w]:
        movement[1] -= 1
    if keys[pygame.K_s]:
        movement[1] += 1
    if keys[pygame.K_a]:
        movement[0] -= 1
    if keys[pygame.K_d]:
        movement[0] += 1
    player.move(movement[0], movement[1])


running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    reactToKeyboardInputs()
    # Fill the background with white
    screen.fill((255, 255, 255))
    player.draw()
    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
