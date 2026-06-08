#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

class Player:
    def __init__(self, img):
        self.x = 100
        self.y = 100
        self.health = 100

        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))

        # rectangle for collision
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50

        # rectangle for collision
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

cat = Player("assets/calico_car.png")

enemies = []

enemy1 = Enemy(200, 200)
enemy2 = Enemy(300, 200)
enemy3 = Enemy(400, 200)
enemy4 = Enemy(500, 200)
enemy5 = Enemy(600, 200)

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

    # update player's collision rectangle after moving
    cat.update_rect()

    # check collision between player and enemies
    for enemy in enemies[:]:
        enemy.update_rect()

        if cat.rect.colliderect(enemy.rect):
            cat.health -= 1
            enemy.health -= 1

        # remove enemy if health reaches 0
        if enemy.health <= 0:
            enemies.remove(enemy)

    screen.fill((255, 255, 255))

    cat.draw(screen)

    for enemy in enemies[:]:
        enemy.draw(screen)

    print("Player health:", cat.health)

    pygame.display.update()

pygame.quit()