import pygame
from settings import *


def show_go_screen(score):
    screen.fill(BLACK)
    play_again_button = pygame.Rect(int(WIDTH/2 - 85), int(2*HEIGHT/5 + 140), 180, 50)
    exit_button = pygame.Rect(int(WIDTH/2 - 50), int(2*HEIGHT/3 + 70), 100, 50)
    draw_text(screen, 'SCORE: ' + str(int(score)), 40, int(WIDTH/2), int(1*HEIGHT/4))
    draw_text(screen, 'GAME OVER', 64, int(WIDTH/2), int(2*HEIGHT/5))
    draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
    draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 70))
    waiting = True
    while waiting:

        clock.tick(FPS)

        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, GREEN, play_again_button)
        draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
        pygame.draw.rect(screen, RED, exit_button)
        draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 70))
        if button_hovered(play_again_button, (153, 255, 51)):
            draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))

            if click[0] == 1:
                waiting = False

        elif button_hovered(exit_button, (255, 153, 153)):
            draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 70))

            if click[0] == 1:
                pygame.quit()
                quit()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, 'WELCOME', 64, int(WIDTH/2), int(HEIGHT/7))
    draw_text(screen, 'CHOOSE YOUR CHARACTER', 36, int(WIDTH/2), int(HEIGHT/5 + 40))
    start_button = pygame.Rect(int(WIDTH/2 - 92), int(HEIGHT - 150), 190, 50)
    sarah_button = pygame.Rect(int(WIDTH/2 - 150), int(2*HEIGHT/3 - 125), 100, 100)
    allen_button = pygame.Rect(int(WIDTH/2 + 50), int(2*HEIGHT/3 - 125), 100, 100)
    # draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(HEIGHT - 150))

    choice = 0
    sarah_selected = False
    allen_selected = False
    waiting = True
    while waiting:

        clock.tick(FPS)

        click_character = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, RED, sarah_button)
        draw_text(screen, 'SARAH', 28, int(WIDTH/2 - 100), int(2*HEIGHT/3 - 125))
        pygame.draw.rect(screen, ORANGE, allen_button)
        draw_text(screen, 'ALLEN', 28, int(WIDTH/2 + 100), int(2*HEIGHT/3 - 125))
        if button_hovered(sarah_button, (255, 153, 153)):
            draw_text(screen, 'SARAH', 28, int(WIDTH/2 - 100), int(2*HEIGHT/3 - 125))

            if click_character[0] == 1:
                sarah_selected = True
                allen_selected = False
                choice = 1

        elif button_hovered(allen_button, (255, 220, 0)):
            draw_text(screen, 'ALLEN', 28, int(WIDTH/2 + 100), int(2*HEIGHT/3 - 125))

            if click_character[0] == 1:
                allen_selected = True
                sarah_selected = False
                choice = 2

        if sarah_selected or allen_selected:
            click_start = pygame.mouse.get_pressed()
            pygame.draw.rect(screen, GREEN, start_button)
            draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(HEIGHT - 150))
            if button_hovered(start_button, (153, 255, 51)):
                draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(HEIGHT - 150))

                if click_start[0] == 1:
                    waiting = False
                    return choice

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def show_pause_screen():
    pause = True
    reset = False
    play_again_button = pygame.Rect(int(WIDTH/2 - 85), int(2*HEIGHT/5 + 140), 180, 50)
    exit_button = pygame.Rect(int(WIDTH/2 - 50), int(2*HEIGHT/3 + 50), 100, 50)
    resume_button = pygame.Rect(int(WIDTH/2 - 65), int(2*HEIGHT/3 + 110), 130, 50)
    draw_text(screen, 'PAUSE', 64, int(WIDTH/2), int(2*HEIGHT/5))
    draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
    draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 50))
    draw_text(screen, 'RESUME', 28, int(WIDTH/2), int(2*HEIGHT/3 + 120))
    waiting = True
    while waiting:

        clock.tick(FPS)

        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, GREEN, play_again_button)
        draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))
        pygame.draw.rect(screen, RED, exit_button)
        draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 50))
        pygame.draw.rect(screen, (255, 220, 0), resume_button)
        draw_text(screen, 'RESUME', 28, int(WIDTH/2), int(2*HEIGHT/3 + 120))
        if button_hovered(play_again_button, (153, 255, 51)):
            draw_text(screen, 'PLAY AGAIN', 28, int(WIDTH/2), int(2*HEIGHT/3))

            if click[0] == 1:
                waiting = False
                reset = True
                pause = False

        elif button_hovered(exit_button, (255, 153, 153)):
            draw_text(screen, 'EXIT', 28, int(WIDTH/2), int(2*HEIGHT/3 + 50))

            if click[0] == 1:
                pygame.quit()
                quit()

        elif button_hovered(resume_button, (255, 243, 0)):
            draw_text(screen, 'RESUME', 28, int(WIDTH/2), int(2*HEIGHT/3 + 120))

            if click[0] == 1:
                pause = False
                waiting = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    return pause, reset
