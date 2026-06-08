#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

# starting game state
state = "menu"

running = True
while running:
    # make the game run at 60 frames per second
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # change game state when key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                state = "menu"

            if event.key == pygame.K_p:
                state = "playing"

            if event.key == pygame.K_g:
                state = "game over"

    # menu screen
    if state == "menu":
        screen.fill((30, 30, 80))

    # playing screen
    elif state == "playing":
        screen.fill((30, 80, 30))

    # game over screen
    elif state == "game over":
        screen.fill((80, 30, 30))

    pygame.display.update()

pygame.quit()