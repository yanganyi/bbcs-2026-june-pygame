#!/usr/bin/env python3

import pygame
import random
import math

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

class Player:
    def __init__(self, img):
        self.x = 350
        self.y = 350
        self.health = 100

        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (80, 80))

        self.rect = pygame.Rect(self.x, self.y, 80, 80)

        self.speed = 5
        self.shoot_timer = 0

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 30
        self.speed = 2

        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def chase_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        if dx > 0:
            self.x += self.speed
        if dx < 0:
            self.x -= self.speed
        if dy > 0:
            self.y += self.speed
        if dy < 0:
            self.y -= self.speed

        self.update_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = 10

        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.update_rect()

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 5)

# create player
cat = Player("assets/calico_car.png")

# create lists
enemies = []
bullets = []
particles = []

# create enemies
enemies.append(Enemy(100, 100))
enemies.append(Enemy(650, 100))
enemies.append(Enemy(100, 650))
enemies.append(Enemy(650, 650))
enemies.append(Enemy(350, 100))

def find_nearest_enemy():
    nearest_enemy = None
    nearest_distance = 999999

    for enemy in enemies:
        dx = enemy.x - cat.x
        dy = enemy.y - cat.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_enemy = enemy

    return nearest_enemy

def shoot_at_enemy(enemy):
    bullet_x = cat.x + 40
    bullet_y = cat.y + 40

    enemy_x = enemy.x + 25
    enemy_y = enemy.y + 25

    dx = enemy_x - bullet_x
    dy = enemy_y - bullet_y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        distance = 1

    dx = dx / distance
    dy = dy / distance

    bullet_speed = 400

    vx = dx * bullet_speed
    vy = dy * bullet_speed

    bullets.append(Bullet(bullet_x, bullet_y, vx, vy))

def create_particles(x, y):
    for i in range(25):
        particle = {
            "x": x,
            "y": y,
            "vx": random.randint(-200, 200),
            "vy": random.randint(-200, 200),
            "life": random.uniform(0.3, 0.8),
            "size": random.randint(3, 8)
        }

        particles.append(particle)

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        cat.x -= cat.speed
    if keys[pygame.K_RIGHT]:
        cat.x += cat.speed
    if keys[pygame.K_UP]:
        cat.y -= cat.speed
    if keys[pygame.K_DOWN]:
        cat.y += cat.speed

    cat.update_rect()

    # keep player inside the screen
    if cat.x < 0:
        cat.x = 0
    if cat.x > 720:
        cat.x = 720
    if cat.y < 0:
        cat.y = 0
    if cat.y > 720:
        cat.y = 720

    cat.update_rect()

    # auto shoot nearest enemy
    cat.shoot_timer -= dt

    if cat.shoot_timer <= 0 and len(enemies) > 0:
        target = find_nearest_enemy()
        shoot_at_enemy(target)
        cat.shoot_timer = 0.4

    # move enemies
    for enemy in enemies[:]:
        enemy.chase_player(cat)

        # contact damage
        if cat.rect.colliderect(enemy.rect):
            cat.health -= 1
            enemy.health -= 1

        if enemy.health <= 0:
            create_particles(enemy.x + 25, enemy.y + 25)
            enemies.remove(enemy)

    # move bullets
    for bullet in bullets[:]:
        bullet.move(dt)

        # remove bullets outside screen
        if bullet.x < 0 or bullet.x > 800 or bullet.y < 0 or bullet.y > 800:
            bullets.remove(bullet)
            continue

        # bullets damage enemies only
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= bullet.damage

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.health <= 0:
                    create_particles(enemy.x + 25, enemy.y + 25)
                    enemies.remove(enemy)

                break

    # update particles
    for particle in particles[:]:
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt
        particle["life"] -= dt

        if particle["life"] <= 0:
            particles.remove(particle)

    screen.fill((20, 20, 20))

    # draw player
    cat.draw(screen)

    # draw enemies
    for enemy in enemies[:]:
        enemy.draw(screen)

    # draw bullets
    for bullet in bullets[:]:
        bullet.draw(screen)

    # draw particles
    for particle in particles[:]:
        pygame.draw.circle(
            screen,
            (255, random.randint(100, 255), 0),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    pygame.display.update()

pygame.quit()