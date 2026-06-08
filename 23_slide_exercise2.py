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

class Enemy:
    def __init__(self, x, y):
        # position of the enemy
        self.x = x
        self.y = y

    def draw(self, screen):
        # draw the enemy as a red square
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))

cat = Player("assets/calico_car.png")

# create an empty enemy list
enemies = []

# make five enemies with the Enemy class
enemy1 = Enemy(200, 200)
enemy2 = Enemy(300, 200)
enemy3 = Enemy(400, 200)
enemy4 = Enemy(500, 200)
enemy5 = Enemy(600, 200)

# put them in the enemy list
enemies.append(enemy1)
enemies.append(enemy2)
enemies.append(enemy3)
enemies.append(enemy4)
enemies.append(enemy5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # loop through the enemy list and draw each enemy
    for enemy in enemies[:]:
        enemy.draw(screen)

    # update the display
    pygame.display.update()

pygame.quit()