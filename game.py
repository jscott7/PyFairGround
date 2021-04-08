import pygame

# Import pygame.locals for easier access to constants
from pygame.locals import (
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    QUIT
)

pygame.init()

# Setup the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# The main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
       
        elif event.type == QUIT:
            running = False

    # Flip the display
    pygame.display.flip()