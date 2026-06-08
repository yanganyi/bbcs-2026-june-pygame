#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

class Player:
    def __init__(self, img):
        self.x = 100
        self.y = 100
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

cat = Player("assets/calico_car.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check which keys are currently being pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        cat.x -= 5

    if keys[pygame.K_RIGHT]:
        cat.x += 5

    if keys[pygame.K_UP]:
        cat.y -= 5

    if keys[pygame.K_DOWN]:
        cat.y += 5


    screen.fill((255, 255, 255))
    cat.draw(screen)
    pygame.display.update()

pygame.quit()