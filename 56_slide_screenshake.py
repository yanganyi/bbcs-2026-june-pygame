#!/usr/bin/env python3

import pygame
import random

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

# player variables
player_x = 350
player_y = 350
player_width = 100
player_height = 100

# screen shake variables
shake_timer = 0
player_hit = False

running = True
while running:
    # make the game run at 60 frames per second
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # press space to pretend the player got hit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_hit = True

    # if player is hit, start screen shake
    if player_hit:
        shake_timer = 0.3
        player_hit = False

    # calculate screen shake offset
    if shake_timer > 0:
        shake_timer -= dt
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)

    else:
        offset_x = 0
        offset_y = 0

    # clear background
    screen.fill((255, 255, 255))

    # draw player with screen shake offset
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (
            player_x + offset_x,
            player_y + offset_y,
            player_width,
            player_height
        )
    )

    # update the display
    pygame.display.update()

pygame.quit()