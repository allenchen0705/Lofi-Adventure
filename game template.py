import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

# define color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LILAC = (229, 204, 255)
MINT = (204, 255, 229)
WHITE = (255, 255, 255)
ORANGE = (255, 178, 102)
BACKGROUND_COLOUR = ORANGE


# initialize pygame and create window
pygame.init()
# sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eludo")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update()

    # draw/render
    screen.fill(BACKGROUND_COLOUR)
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
