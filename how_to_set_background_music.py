#!/usr/bin/env python3

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# load background music
pygame.mixer.music.load("assets/fih.mp3")

# play background music forever
pygame.mixer.music.play(-1)

player = pygame.Rect(100, 100, 50, 50)
enemy = pygame.Rect(400, 400, 50, 50)

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    pygame.display.update()

pygame.quit()