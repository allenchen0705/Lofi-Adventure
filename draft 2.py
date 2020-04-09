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
ORANGE = (255, 178, 102)
BACKGROUND_COLOUR = ORANGE

player_size = 50
player_pos = [WIDTH/2, HEIGHT - player_size*2]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

SPEED = 10

clock = pygame.time.Clock()

my_font = pygame.font.SysFont("monospace", 35)
my_font.set_bold(True)


def set_level(score):
    speed = score/25 + 3
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


def start_screen():
    screen.fill(BACKGROUND_COLOUR)
    draw_text("Eludo.", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text('Move left and right with arrow keys to dodge enemies.', 22,
              WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text('Press any key to start.', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    game_over = wait_for_key()
    return game_over


def game_over_screen():
    screen.fill(BACKGROUND_COLOUR)
    draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
    draw_text('Score: ' + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
    draw_text('Press a key to play again', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    game_over = wait_for_key()
    return game_over


def wait_for_key():
    game_over = False
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                game_over = True
            if event.type == pygame.KEYUP:
                waiting = False
    return game_over


def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("monospace", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


game_over = start_screen()
play_again = True
while play_again:
    score = 0
    play_again = True
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BACKGROUND_COLOUR)

        x = player_pos[0]
        y = player_pos[1]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and 0 < x:
            x -= 8
            player_pos = [x, y]
        if keys[pygame.K_RIGHT] and x < WIDTH - player_size:
            x += 8
            player_pos = [x, y]

        drop_enemies(enemy_list)

        score = update_enemy_positions(enemy_list, score)
        SPEED = set_level(score)

        text = "Score:" + str(score)
        label = my_font.render(text, 1, WHITE)
        screen.blit(label, (0, HEIGHT - 40))

        draw_enemies(enemy_list)
        pygame.draw.rect(screen, MINT, (player_pos[0], player_pos[1],
                                        player_size, player_size))
        clock.tick(60)

        if collision_check(enemy_list, player_pos):
            game_over = True

        pygame.display.update()
    play_again = game_over_screen()

