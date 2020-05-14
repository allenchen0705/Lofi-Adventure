import pygame


WIDTH = 800
HEIGHT = 585
FPS = 60
POWERUP_TIME = 5000
clock = pygame.time.Clock()
font_name = pygame.font.match_font("Arial")


screen = pygame.display.set_mode((WIDTH, HEIGHT))


# define color
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LILAC = (229, 204, 255)
MINT = (204, 255, 229)
WHITE = (255, 255, 255)
ORANGE = (255, 178, 102)
BACKGROUND_COLOUR = ORANGE


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def button_hovered(rectangle, hov_colour):
    mouse_pos = pygame.mouse.get_pos()
    hovered = False
    if rectangle.x <= mouse_pos[0] <= rectangle.x + rectangle.width \
            and rectangle.y <= mouse_pos[1] <= rectangle.y + rectangle.height:
        pygame.draw.rect(screen, hov_colour, rectangle)
        hovered = True

    return hovered


def show_go_screen():
    screen.fill(BLACK)
    play_again_button = pygame.Rect(int(WIDTH/2 - 85), int(2*HEIGHT/5 + 140), 180, 50)
    exit_button = pygame.Rect(int(WIDTH/2 - 50), int(2*HEIGHT/3 + 70), 100, 50)
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
    draw_text(screen, 'WELCOME', 64, int(WIDTH/2), int(2*HEIGHT/5))
    start_button = pygame.Rect(int(WIDTH/2 - 92), int(2*HEIGHT/5 + 140), 190, 50)
    draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(2*HEIGHT/3))

    waiting = True
    while waiting:

        clock.tick(FPS)

        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, GREEN, start_button)
        draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(2*HEIGHT/3))
        if button_hovered(start_button, (153, 255, 51)):
            draw_text(screen, 'START GAME', 28, int(WIDTH/2), int(2*HEIGHT/3))

            if click[0] == 1:
                waiting = False

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
