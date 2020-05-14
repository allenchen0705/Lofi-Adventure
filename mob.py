import pygame
import random
from os import path

WIDTH = 800
HEIGHT = 585
FPS = 60
POWERUP_TIME = 5000

# define color
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LILAC = (229, 204, 255)
MINT = (204, 255, 229)
WHITE = (255, 255, 255)
ORANGE = (255, 178, 102)
BACKGROUND_COLOUR = ORANGE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#need to update this speed from the main loop, maybe changing the game to a class would help
speed = 3

game_folder = path.dirname(__file__)

shuriken_img = pygame.image.load(path.join(game_folder, 'ninjastar.jpg')).convert()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(shuriken_img, (80, 80))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .35 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 3
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(80, 120)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            # make rotation smoother by changing the center of the image
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 20 or self.rect.left < -75 or \
                self.rect.right > WIDTH + 75:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = speed + 3
