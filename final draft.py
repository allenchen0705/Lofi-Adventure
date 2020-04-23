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


# set up assets folders
game_folder = path.dirname(__file__)

# initialize pygame and create window
pygame.init()
# sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eludo")
clock = pygame.time.Clock()


# helper functions
font_name = pygame.font.match_font("Arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_mob(speed: int):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    m.speedy += speed

def new_powerup():
    p = Pow()
    all_sprites.add(p)
    powerups.add(p)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    # sprite of the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (67, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 25
        self.speedx = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.speed = 5
        self.power_time = pygame.time.get_ticks()
        self.freeze_time = pygame.time.get_ticks()
        self.shield = False

    def update(self):
        # timeout for speed boost
        if pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            if self.speed > 5:
                self.speed -= 3
                self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 25
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -(self.speed)
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.speed
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def unfreeze(self, mobs, orig_speed):
        # timeout for freeze
        if pygame.time.get_ticks() - self.freeze_time > POWERUP_TIME:
            for mob in mobs:
                mob.speedy = orig_speed
                mob.rot_speed = random.randrange(80, 120)
            self.freeze_time = pygame.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def speed_boost(self):
        self.speed += 3
        self.power_time = pygame.time.get_ticks()


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


# power ups
# ideas:
# shields
# extra life
# boost speed
class Pow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'extra life', 'speed boost', 'time freeze'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 20 or self.rect.left < -75 or \
                self.rect.right > WIDTH + 75:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)


def show_go_screen():
    play_again_button = pygame.Rect(int(WIDTH/2 - 85), int(2*HEIGHT/5 + 140), 180, 50)
    exit_button = pygame.Rect(int(WIDTH/2 - 50), int(2*HEIGHT/3 + 70), 100, 50)
    pygame.draw.rect(screen, GREEN, exit_button)
    draw_text(screen, 'GAME OVER', 64, int(WIDTH/2), int(2*HEIGHT/5))
    draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
    draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 70))
    waiting = True
    while waiting:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        if play_again_button.x <= mouse_pos[0] <= play_again_button.x + play_again_button.width \
                and play_again_button.y <= mouse_pos[1] <= play_again_button.y + play_again_button.height:
            pygame.draw.rect(screen, (153, 255, 51), play_again_button)
            draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
        else:
            pygame.draw.rect(screen, GREEN, play_again_button)
            draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()




# debuffs
# slow speed
# become fat
# poison/bleeding effect


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


# game loop
running = True
game_over = True
last_update = 0

while running:
    if game_over:
        show_go_screen()
        game_over = False
        speed = 3
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(5):
            new_mob(speed)
        for j in range(3):
            new_powerup()

        score = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()
    player.unfreeze(mobs, speed + 3)

    # increase the number of shurikens with time
    now = pygame.time.get_ticks()
    if now - last_update > 6000:
        speed += 1
        new_mob(speed)
        last_update = now

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_mob(speed)
        if not player.shield:
            player.hide()
            player.lives -= 1
        player.shield = False

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type == 'extra life':
            player.lives += 1
            if player.lives >= 3:
                player.lives = 3
            new_powerup()
        if hit.type == 'speed boost':
            player.speed_boost()
            if player.speed >= 11:
                player.speed = 11
            new_powerup()
        if hit.type == 'shield' and not player.shield:
            player.shield = True
            new_powerup()
        if hit.type == 'time freeze':
            for mob in mobs:
                mob.speedy = 1
                mob.rot_speed = 8
            new_powerup()

    if player.lives == 0: # and not death_explosion.alive():
        game_over = True

    score += 0.2

    # draw/render
    # screen.fill(BACKGROUND_COLOUR)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 100, 5, player.lives, lives_mini_img)
    pygame.display.flip()

pygame.quit()
