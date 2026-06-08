#!/usr/bin/env python3

import pygame
import random
import math

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

pygame.mixer.music.load("assets/fih.mp3")
pygame.mixer.music.play(-1)

class Player:
    def __init__(self, img):
        self.x = 350
        self.y = 350
        self.health = 100
        self.speed = 5
        self.shoot_timer = 0

        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (80, 80))

        self.rect = pygame.Rect(self.x, self.y, 80, 80)

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

class Gem:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 150, 255), (int(self.x), int(self.y)), 10)

cat = Player("assets/calico_car.png")

enemies = []
bullets = []
gems = []
particles = []

score = 0
level = 1
xp = 0
xp_needed = 5

spawn_timer = 1
survival_timer = 0

def spawn_enemy():
    side = random.randint(1, 4)

    if side == 1:
        x = random.randint(0, 800)
        y = -50
    elif side == 2:
        x = random.randint(0, 800)
        y = 850
    elif side == 3:
        x = -50
        y = random.randint(0, 800)
    else:
        x = 850
        y = random.randint(0, 800)

    enemies.append(Enemy(x, y))

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
    survival_timer += dt

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

    if cat.x < 0:
        cat.x = 0
    if cat.x > 720:
        cat.x = 720
    if cat.y < 0:
        cat.y = 0
    if cat.y > 720:
        cat.y = 720

    cat.update_rect()

    spawn_timer -= dt

    if spawn_timer <= 0:
        spawn_enemy()
        spawn_timer = max(0.2, 1 - survival_timer / 60)

    cat.shoot_timer -= dt

    if cat.shoot_timer <= 0 and len(enemies) > 0:
        target = find_nearest_enemy()
        shoot_at_enemy(target)
        cat.shoot_timer = max(0.15, 0.5 - level * 0.03)

    for enemy in enemies[:]:
        enemy.chase_player(cat)

        if cat.rect.colliderect(enemy.rect):
            cat.health -= 1
            enemy.health -= 1

        if enemy.health <= 0:
            score += 10
            gems.append(Gem(enemy.x + 25, enemy.y + 25))
            create_particles(enemy.x + 25, enemy.y + 25)
            enemies.remove(enemy)

    for bullet in bullets[:]:
        bullet.move(dt)

        if bullet.x < 0 or bullet.x > 800 or bullet.y < 0 or bullet.y > 800:
            bullets.remove(bullet)
            continue

        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= bullet.damage

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.health <= 0:
                    score += 10
                    gems.append(Gem(enemy.x + 25, enemy.y + 25))
                    create_particles(enemy.x + 25, enemy.y + 25)
                    enemies.remove(enemy)

                break

    for gem in gems[:]:
        if cat.rect.colliderect(gem.rect):
            xp += 1
            score += 5
            gems.remove(gem)

            if xp >= xp_needed:
                xp = 0
                level += 1
                xp_needed += 3
                cat.health += 10
                cat.speed += 0.3
                create_particles(cat.x + 40, cat.y + 40)

    for particle in particles[:]:
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt
        particle["life"] -= dt

        if particle["life"] <= 0:
            particles.remove(particle)

    screen.fill((20, 20, 20))

    for gem in gems[:]:
        gem.draw(screen)

    for bullet in bullets[:]:
        bullet.draw(screen)

    for enemy in enemies[:]:
        enemy.draw(screen)

    cat.draw(screen)

    for particle in particles[:]:
        pygame.draw.circle(
            screen,
            (255, random.randint(100, 255), 0),
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

    health_text = font.render("Health: " + str(cat.health), True, (255, 255, 255))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    xp_text = font.render("XP: " + str(xp) + "/" + str(xp_needed), True, (255, 255, 255))

    screen.blit(health_text, (20, 20))
    screen.blit(score_text, (20, 55))
    screen.blit(level_text, (20, 90))
    screen.blit(xp_text, (20, 125))

    if cat.health <= 0:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (330, 380))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    pygame.display.update()

pygame.quit()