import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
LILAC = (229, 204, 255)
MINT = (204, 255, 229)
WHITE = (255, 255, 255)
BACKGROUND_COLOUR = (255, 178, 102)

player_size = 50
player_pos = [WIDTH/2, HEIGHT - player_size*2]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

SPEED = 10

game_over = False

score = 0

clock = pygame.time.Clock()

my_font = pygame.font.SysFont("monospace", 35)
my_font.set_bold(True)


def set_level(score):
    speed = score/15 + 5
    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 20 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, LILAC, (enemy_pos[0], enemy_pos[1], enemy_size,
                                         enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False


def detect_collision(player_p, enemy_p):
    p_x = player_p[0]
    p_y = player_p[1]

    e_x = enemy_p[0]
    e_y = enemy_p[1]

    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            sys.exit()

        #if event.type == pygame.KEYDOWN:

        x = player_pos[0]
        y = player_pos[1]
        keys = pygame.key.get_pressed()
        while keys[pygame.K_LEFT] and 0 < x:
            x -= 10
            player_pos = [x, y]
        while keys[pygame.K_RIGHT] and x < WIDTH - player_size:
            x += 10
            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOUR)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score)

    text = "Score:" + str(score)
    label = my_font.render(text, 1, WHITE)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(enemy_list, player_pos):
        game_over = True

    draw_enemies(enemy_list)
    pygame.draw.rect(screen, MINT, (player_pos[0], player_pos[1], player_size,
                                   player_size))
    clock.tick(30)

    pygame.display.update()
