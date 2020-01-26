import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND_COLOUR = (0, 0, 0)

player_size = 50
player_pos = [WIDTH/2, HEIGHT - player_size*2]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos, ]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

SPEED = 10

game_over = False

clock = pygame.time.Clock()


def drop_enemies(enemy_list):
    if len(enemy_list) < 10:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_lst):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, GREEN, (enemy_pos[0], enemy_pos[1], enemy_size,
                                         enemy_size))


def detect_collision(player_p, enemy_p):
    p_x = player_p[0]
    p_y = player_p[1]

    e_x = enemy_p[0]
    e_y = enemy_p[1]

    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < e_x + enemy_size):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < e_y + enemy_size):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= 50
            elif event.key == pygame.K_RIGHT:
                x += 50

            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOUR)

    # update position of the enemy
    if 0 <= enemy_pos[1] < HEIGHT:
        enemy_pos[1] += SPEED
    else:
        enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
        enemy_pos[1] = 0

    if detect_collision(player_pos, enemy_pos):
        game_over = True

    drop_enemies(enemy_list)
    draw_enemies(enemy_list)


    pygame.draw.rect(screen, GREEN, (enemy_pos[0], enemy_pos[1], enemy_size,
                                     enemy_size))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size,
                                   player_size))

    clock.tick(30)

    pygame.display.update()
