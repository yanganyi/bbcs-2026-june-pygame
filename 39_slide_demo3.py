#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

# create an empty enemy list
enemies = []

# enemy spawn variables
spawn_timer = 2
spawn_count = 0

def spawn_enemy():
    global spawn_count

    # spacing between enemies
    offset = 70

    # starting position of the first enemy
    start_x = 50
    start_y = 100

    # how many enemies per row
    enemies_per_row = 10

    # calculate enemy row and column
    row = spawn_count // enemies_per_row
    col = spawn_count % enemies_per_row

    x = start_x + col * offset
    y = start_y + row * offset

    # create enemy as a red square rectangle
    enemy = pygame.Rect(x, y, 50, 50)

    # add enemy to enemy list
    enemies.append(enemy)

    spawn_count += 1

running = True
while running:
    # make the game run at 60 frames per second
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # countdown the spawn timer
    spawn_timer -= dt

    # spawn an enemy every 2 seconds
    if spawn_timer <= 0:
        spawn_enemy()
        spawn_timer = 2

    # clear background
    screen.fill((255, 255, 255))

    # loop through enemy list and draw each enemy
    for enemy in enemies[:]:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    # update the display
    pygame.display.update()

pygame.quit()