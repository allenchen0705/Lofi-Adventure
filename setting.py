import pygame
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

font_name = pygame.font.match_font("Arial")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# set up assets folders
game_folder = path.dirname(__file__)

# Load all game graphics
player_img = pygame.image.load(path.join(game_folder, 'bad-ninja1---drawing.png')).convert()
lives_img = pygame.image.load(path.join(game_folder, 'heart.jpg')).convert()
lives_mini_img = pygame.transform.scale(lives_img, (25, 25))
lives_mini_img.set_colorkey(WHITE)
shuriken_img = pygame.image.load(path.join(game_folder, 'ninjastar.jpg')).convert()
background = pygame.image.load(path.join(game_folder, 'background.jpg')).convert()
background_rect = background.get_rect()
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(game_folder, 'shield_gold.png')).convert()
powerup_images['extra life'] = pygame.image.load(path.join(game_folder, 'pill_red.png')).convert()
powerup_images['speed boost'] = pygame.image.load(path.join(game_folder, 'bold_silver.png')).convert()
powerup_images['time freeze'] = pygame.image.load(path.join(game_folder, 'freeze.png')).convert()
powerup_images['slow'] = pygame.image.load(path.join(game_folder, 'slow.png')).convert()
powerup_images['invincible'] = pygame.image.load(path.join(game_folder, 'invincible.png')).convert()


# helper
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def button_hovered(rectangle, hov_colour):
    mouse_pos = pygame.mouse.get_pos()
    hovered = False
    if rectangle.x <= mouse_pos[0] <= rectangle.x + rectangle.width \
            and rectangle.y <= mouse_pos[1] <= rectangle.y + rectangle.height:
        pygame.draw.rect(screen, hov_colour, rectangle)
        hovered = True

    return hovered

