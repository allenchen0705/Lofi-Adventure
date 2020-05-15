import pygame
from mob import Mob
from player import *
from screens import *
from settings import *

# initialize pygame and create window
pygame.init()
# sound
pygame.mixer.init()
pygame.display.set_caption("Eludo")


# turning the game loop into a class
class Game:
    def __init__(self):
        self.running = True
        self.start = True
        self.game_over = False
        self.last_update = 0
        self.pause = False

    def new(self):
        self.start = False
        self.speed = 3
        self.score = 0
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.mobs = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        for i in range(5):
            self.new_mob(self.speed)
        for j in range(3):
            self.new_powerup()

    def update(self):
        self.all_sprites.update()
        self.player.unfreeze(self.mobs, self.speed + 3)

        # increase the number of shurikens with time
        now = pygame.time.get_ticks()
        if now - self.last_update > 6000:
            self.speed += 1
            self.new_mob(self.speed)
            for mob in self.mobs:
                mob.speedy += 1
            self.last_update = now

        # check to see if a mob hit the player
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)
        for hit in mob_hits:
            self.new_mob(self.speed)
            if not self.player.shield and not self.player.invincible:
                self.player.hide()
                self.player.lives -= 1
                self.player.reset()
            self.player.shield = False

        # check to see if player hit a powerup
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True, pygame.sprite.collide_circle)
        for hit in powerup_hits:
            if hit.type == 'extra life':
                self.player.lives += 1
                if self.player.lives >= 3:
                    self.player.lives = 3
                self.new_powerup()
            if hit.type == 'speed boost':
                self.player.speed_boost()
                if self.player.speed >= 11:
                    self.player.speed = 11
                self.new_powerup()
            if hit.type == 'shield' and not self.player.shield:
                self.player.shield = True
                self.new_powerup()
            if hit.type == 'time freeze':
                for mob in self.mobs:
                    mob.speedy = 1
                    mob.rot_speed = 8
                self.new_powerup()
            if hit.type == 'slow' and not self.player.invincible:
                self.player.speed_slow_down()
                if self.player.speed < 2:
                    self.player.speed = 2
                self.new_powerup()
            if hit.type == 'invincible':
                self.player.time_invincible()
                self.new_powerup()

        if self.player.lives == 0:
            self.game_over = True

    def new_mob(self, speed):
        m = Mob()
        self.all_sprites.add(m)
        self.mobs.add(m)
        m.speedy += speed

    def new_powerup(self):
        p = Pow()
        self.all_sprites.add(p)
        self.powerups.add(p)

    def draw(self):
        screen.blit(background, background_rect)
        self.all_sprites.draw(screen)

        # score on the top
        draw_text(screen, str(int(self.score)), 18, WIDTH / 2, 10)

        # lives on the top
        draw_lives(screen, WIDTH - 100, 5, self.player.lives, lives_mini_img)


g = Game()
while g.running:
    if g.start:
        show_start_screen()
        g.start = False
        g.new()

    if g.game_over:
        show_go_screen(g.score)
        g.game_over = False
        g.new()

    # keep loop running at the right speed
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g.running = False

    g.draw()

    # pause button
    pause_button = pygame.Rect(5, 5, 50, 50)
    pygame.draw.rect(screen, RED, pause_button)
    click = pygame.mouse.get_pressed()
    if button_hovered(pause_button, (255, 153, 153)):
        if click[0] == 1:
            g.pause = show_pause_screen()[0]
            g.start = show_pause_screen()[1]

    if not g.pause:
        g.update()
        g.score += 0.2

    pygame.display.flip()

pygame.quit()

# ------------------------------------------------------------------------------
# OLD VERSION (NO CLASSES)

# # helper functions
# def new_mob(speed: int):
#     m = Mob()
#     all_sprites.add(m)
#     mobs.add(m)
#     m.speedy += speed
#
#
# def new_powerup():
#     p = Pow()
#     all_sprites.add(p)
#     powerups.add(p)


# game loop
# start = True
# game_over = False
# last_update = 0
# running = True
# pause = False
# while running:
#     if start:
#         show_start_screen()
#         start = False
#         speed = 3
#         all_sprites = pygame.sprite.Group()
#         mobs = pygame.sprite.Group()
#         powerups = pygame.sprite.Group()
#         player = Player()
#         all_sprites.add(player)
#         for i in range(5):
#             new_mob(speed)
#         for j in range(3):
#             new_powerup()
#         score = 0
#     if game_over:
#         show_go_screen(score)
#         game_over = False
#         speed = 3
#         all_sprites = pygame.sprite.Group()
#         mobs = pygame.sprite.Group()
#         powerups = pygame.sprite.Group()
#         player = Player()
#         all_sprites.add(player)
#         for i in range(5):
#             new_mob(speed)
#         for j in range(3):
#             new_powerup()
#         score = 0
#     # keep loop running at the right speed
#     clock.tick(FPS)
#     # process input(events)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # draw/render
#     # screen.fill(BACKGROUND_COLOUR)
#     screen.blit(background, background_rect)
#     all_sprites.draw(screen)
#     draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)
#     draw_lives(screen, WIDTH - 100, 5, player.lives, lives_mini_img)
#
#     # pause button
#     pause_button = pygame.Rect(5, 5, 50, 50)
#     pygame.draw.rect(screen, RED, pause_button)
#     click = pygame.mouse.get_pressed()
#     if button_hovered(pause_button, (255, 153, 153)):
#         if click[0] == 1:
#             pause = show_pause_screen()[0]
#             start = show_pause_screen()[1]
#
#     # update
#     if not pause:
#         all_sprites.update()
#         player.unfreeze(mobs, speed + 3)
#
#         # increase the number of shurikens with time
#         now = pygame.time.get_ticks()
#         if now - last_update > 6000:
#             speed += 1
#             new_mob(speed)
#             for mob in mobs:
#                 mob.speedy += 1
#             last_update = now
#
#         # check to see if a mob hit the player
#         mob_hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
#         for hit in mob_hits:
#             new_mob(speed)
#             if not player.shield and not player.invincible:
#                 player.hide()
#                 player.lives -= 1
#                 player.reset()
#             player.shield = False
#
#         # check to see if player hit a powerup
#         powerup_hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
#         for hit in powerup_hits:
#             if hit.type == 'extra life':
#                 player.lives += 1
#                 if player.lives >= 3:
#                     player.lives = 3
#                 new_powerup()
#             if hit.type == 'speed boost':
#                 player.speed_boost()
#                 if player.speed >= 11:
#                     player.speed = 11
#                 new_powerup()
#             if hit.type == 'shield' and not player.shield:
#                 player.shield = True
#                 new_powerup()
#             if hit.type == 'time freeze':
#                 for mob in mobs:
#                     mob.speedy = 1
#                     mob.rot_speed = 8
#                 new_powerup()
#             if hit.type == 'slow' and not player.invincible:
#                 player.speed_slow_down()
#                 if player.speed < 2:
#                     player.speed = 2
#                 new_powerup()
#             if hit.type == 'invincible':
#                 player.time_invincible()
#                 new_powerup()
#
#         if player.lives == 0: # and not death_explosion.alive():
#             game_over = True
#
#         score += 0.2
#
#     pygame.display.flip()


# pygame.quit()
