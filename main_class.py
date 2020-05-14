import pygame
from mob import Mob
from player import *
from screens import *
from setting import *

# initialize pygame and create window
pygame.init()
# sound
pygame.mixer.init()
pygame.display.set_caption("Eludo")


# helper functions
def new_mob(speed: int):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    m.speedy += speed


def new_powerup():
    p = Pow()
    all_sprites.add(p)
    powerups.add(p)


# debuffs
# slow speed
# become fat
# poison/bleeding effect

# game loop
start = True
game_over = False
last_update = 0
running = True
pause = False
while running:
    if start:
        show_start_screen()
        start = False
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
    if game_over:
        show_go_screen(score)
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


    # draw/render
    # screen.fill(BACKGROUND_COLOUR)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 100, 5, player.lives, lives_mini_img)

    # pause button
    pause_button = pygame.Rect(5, 5, 50, 50)
    pygame.draw.rect(screen, RED, pause_button)
    click = pygame.mouse.get_pressed()
    if button_hovered(pause_button, (255, 153, 153)):
        if click[0] == 1:
            pause = show_pause_screen()[0]
            start = show_pause_screen()[1]

    # update
    if not pause:
        all_sprites.update()
        player.unfreeze(mobs, speed + 3)

        # increase the number of shurikens with time
        now = pygame.time.get_ticks()
        if now - last_update > 6000:
            speed += 1
            new_mob(speed)
            for mob in mobs:
                mob.speedy += 1
            last_update = now

        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            new_mob(speed)
            if not player.shield and not player.invincible:
                player.hide()
                player.lives -= 1
                player.reset()
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
            if hit.type == 'slow' and not player.invincible:
                player.speed_slow_down()
                if player.speed < 2:
                    player.speed = 2
                new_powerup()
            if hit.type == 'invincible':
                player.time_invincible()
                new_powerup()

        if player.lives == 0: # and not death_explosion.alive():
            game_over = True

        score += 0.2

    pygame.display.flip()


pygame.quit()
