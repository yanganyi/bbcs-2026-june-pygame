#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (400, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()