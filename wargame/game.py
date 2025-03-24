# libaries

# pygame: https://www.pygame.org/
# math: https://docs.python.org/3/library/math.html
# random: https://docs.python.org/3/library/random.html

import pygame
import math
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1270, 720))
clock = pygame.time.Clock()
running = True
enemyspawning = True
immune = False
multiplier = 1
multiplierbar = 0
multiplierdecay = 0.001
multiplierdisplay = multiplierbar + 1
score = 0
dt = 0
difficulty = 1
firerate = 1
screencolour = "grey"
pygame.font.init()
pygame.font.Font("AudioWide-Regular.ttf", 16)
hp = 100
hptext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("HP: " + str(hp), True, (0, 0, 0))
projectilecd = 100
projectilecdtext = pygame.font.Font("AudioWide-Regular.ttf", 16).render(str(math.floor(projectilecd)) + " %", True, (0, 0, 0))
dash = 300
dash_pressed = False
dashtext = pygame.font.Font("AudioWide-Regular.ttf", 16).render(str(math.floor(dash)), True, (0, 0, 0))
scoretext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("Score: " + str(score), True, (0, 0, 0))
multipliertext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("x" + str(math.floor(multiplier)), True, (0, 0, 0))
music = pygame.mixer.music.load("blooddrain.mpeg")
pygame.mixer.music.play(-1)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

projectiles = []
enemies = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(screencolour)

    # the player
    # draw the player as a blue rectangle
    pygame.draw.rect(screen, "blue", pygame.Rect(player_pos.x, player_pos.y, 20, 20))

    screen.blit(hptext, (10, 10))

    pygame.draw.rect(screen, "black", pygame.Rect(10, 30, 200, 10))
    pygame.draw.rect(screen, "red", pygame.Rect(10, 30, hp * 2, 10))

    screen.blit(projectilecdtext, (10, 50))

    pygame.draw.rect(screen, "pink", pygame.Rect(10, 70, 200, 10))
    pygame.draw.rect(screen, "#ADD8E6", pygame.Rect(10, 70, projectilecd * 2, 10))

    pygame.draw.rect(screen, "red", pygame.Rect(250, 30, 300, 10))
    pygame.draw.rect(screen, "white", pygame.Rect(250, 30, dash, 10))

    screen.blit(dashtext, (250,10))
    screen.blit(scoretext, (10, 90))

    multiplierdisplay = multiplierbar + 1
    multipliertext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("x" + str(math.floor(multiplierdisplay)), True, (0, 0, 0))
    screen.blit(multipliertext, (10, 120))
    pygame.draw.rect(screen, "black", pygame.Rect(10, 140, 100, 10))
    pygame.draw.rect(screen, "blue", pygame.Rect(10, 140, min(multiplierbar, multiplier) * 100, 10))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 200 * dt
    if keys[pygame.K_s]:
        player_pos.y += 200 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 200 * dt
    if keys[pygame.K_d]:
        player_pos.x += 200 * dt
    if keys[pygame.K_SPACE] and dash >= 100 and not dash_pressed:
        immune = True
        dash_pressed = True
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = (mouse_pos - player_pos).normalize()
        dash_distance = dash * 2  # Dash distance in pixels
        dash_time = 0.15  # Dash duration in seconds
        dash_speed = dash_distance / dash_time
        dash_end_time = pygame.time.get_ticks() + dash_time * 1000
        dash_start_pos = player_pos.copy()
        dash_target_pos = player_pos + direction * dash_distance

    if dash_pressed:
        current_time = pygame.time.get_ticks()
        if current_time < dash_end_time:
            progress = (current_time - (dash_end_time - dash_time * 1000)) / (dash_time * 1000)
            dash = max(0, dash - 100)
            player_pos = dash_start_pos.lerp(dash_target_pos, progress)
            immune = False
        else:
            dash_pressed = False
            immune = False  # Reset immunity after dash ends
    if not keys[pygame.K_SPACE]:
        dash_pressed = False
    if dash < 300:
        dash += 2.5
    if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
        if projectilecd >= 100:
            pygame.mixer.Sound("shot.mp3").play()
            projectile_pos = pygame.Vector2(player_pos.x, player_pos.y)
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - projectile_pos).normalize()
            projectile_speed = 400  # pixels per second
            projectiles.append((projectile_pos, direction, projectile_speed * firerate))
            projectilecd = 0  # Reset cooldown after firing

    for projectile in projectiles:
        projectile_pos, direction, projectile_speed = projectile
        projectile_pos += direction * projectile_speed * dt
        pygame.draw.rect(screen, "cyan", pygame.Rect(projectile_pos.x, projectile_pos.y, 10, 10))

    if projectilecd < 100:
        projectilecd += 2 * firerate
    projectilecdtext = pygame.font.Font("AudioWide-Regular.ttf", 16).render(str(projectilecd) + "%", True, (0, 0, 0))
    if projectilecd < 100:
        projectilecd += 2 * firerate
    projectilecdtext = pygame.font.Font("AudioWide-Regular.ttf", 16).render(str(math.floor(projectilecd)) + " %", True, (0, 0, 0))
    hptext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("HP: " + str(hp), True, (0, 0, 0))
    dashtext = pygame.font.Font("AudioWide-Regular.ttf", 16).render(str(math.floor(dash)), True, (0, 0, 0))
    scoretext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("Score: " + str(score), True, (0, 0, 0))
    multipliertext = pygame.font.Font("AudioWide-Regular.ttf", 16).render("x" + str(math.floor(multiplierdisplay)), True, (0, 0, 0))
    if hp <= 0:
        running = False
    if player_pos.x < 0:
        player_pos.x = 0
    if player_pos.y < 0:
        player_pos.y = 0
    if player_pos.x > screen.get_width() - 20:
        player_pos.x = screen.get_width() - 20
    if player_pos.y > screen.get_height() - 20:
        player_pos.y = screen.get_height() - 20
    
    # Spawn enemies at intervals
    if enemyspawning:
        if not hasattr(pygame, 'last_enemy_spawn_time'):
            pygame.last_enemy_spawn_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - pygame.last_enemy_spawn_time > random.uniform(500, 2000):  # Randomize spawn time between 0.5 and 2 seconds
            angle = math.radians(random.uniform(0, 360))
            distance = random.uniform(100, 500)
            enemy_x = player_pos.x + math.cos(angle) * distance
            enemy_y = player_pos.y + math.sin(angle) * distance
            enemies.append(pygame.Vector2(enemy_x, enemy_y))
            pygame.last_enemy_spawn_time = current_time

    for enemy in enemies:
        distance = (enemy - player_pos).length()
        if distance < 20:
            if immune:
                enemies.remove(enemy)
                hp += 5
                if multiplierbar > 0.99:
                    score += 2
                else:
                    score += 1
                multiplierbar += 0.25
                multiplierbar = min(multiplierbar + 0.25, 3)
            else:
                hp -= 20
                enemies.remove(enemy)
        for projectile in projectiles[:]:
            if pygame.Rect(enemy.x, enemy.y, 20, 20).colliderect(pygame.Rect(projectile[0].x, projectile[0].y, 10, 10)):
                try:
                    enemies.remove(enemy)
                except ValueError:
                    pass
                if multiplierbar > 0.99:
                    score += 2
                else:
                    score += 1
                hp += 1
                multiplierbar += 0.1
                projectiles.remove(projectile)
                break
        else:
            direction = (player_pos - enemy).normalize()
            enemy += direction * 225 * dt  # Faster than the player, so it can catch up
            pygame.draw.rect(screen, "red", pygame.Rect(enemy.x, enemy.y, 20, 20))
        
        # Prevent enemies from bunching up too close
        for other_enemy in enemies:
            if other_enemy != enemy:
                other_distance = (enemy - other_enemy).length()
                if other_distance < 20:
                    separation_direction = (enemy - other_enemy).normalize()
                    enemy += separation_direction * 50 * dt

        pygame.draw.rect(screen, "red", pygame.Rect(enemy.x, enemy.y, 20, 20))

    multiplierbar -= multiplierdecay
    if multiplierbar < 0:
        multiplierbar = 0
    if multiplierbar >= 1 and not hasattr(pygame, 'non_decay_start_time'):
        pygame.non_decay_start_time = pygame.time.get_ticks()
        multiplierdecay = 0
    if hasattr(pygame, 'non_decay_start_time'):
        if pygame.mouse.get_pressed()[2] and hasattr(pygame, 'non_decay_start_time'):  # Check if right mouse button is pressed during the decay grace time
            firerate += 0.1
            del pygame.non_decay_start_time
            pygame.mixer.Sound("upgrade.mp3").play()
            multiplierbar = 0
            hp += 10
    if hasattr(pygame, 'non_decay_start_time') and pygame.time.get_ticks() - pygame.non_decay_start_time >= 3000:
        multiplierdecay = 0.001
        del pygame.non_decay_start_time

    if hp > 100:
        hp  = 100
    if projectilecd > 100:
        projectilecd = 100

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()