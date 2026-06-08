#!/usr/bin/env python3

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 50, 50)
enemy = pygame.Rect(500, 500, 50, 50)

enemy_speed = 2

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5

    # enemy AI
    dx = player.x - enemy.x
    dy = player.y - enemy.y

    if dx > 0:
        enemy.x += enemy_speed
    if dx < 0:
        enemy.x -= enemy_speed
    if dy > 0:
        enemy.y += enemy_speed
    if dy < 0:
        enemy.y -= enemy_speed

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    pygame.display.update()

pygame.quit()