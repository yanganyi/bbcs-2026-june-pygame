#!/usr/bin/env python3

import pygame
import random

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

# create an empty particle list
particles = []

def create_particles(x, y):
    # create 10 particles at the mouse click position
    for i in range(10):
        particle = {
            "x": x,
            "y": y,
            "vx": random.randint(-100, 100),
            "vy": random.randint(-100, 100),
            "life": 1
        }

        particles.append(particle)

running = True
while running:
    # make the game run at 60 frames per second
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # when the mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # create particles at the mouse position
            create_particles(mouse_x, mouse_y)

    # clear background
    screen.fill((255, 255, 255))

    # update and draw particles
    for particle in particles[:]:
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt

        particle["life"] -= dt

        # remove particle when its life reaches 0
        if particle["life"] <= 0:
            particles.remove(particle)

        else:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (int(particle["x"]), int(particle["y"])),
                5
            )

    # update the display
    pygame.display.update()

pygame.quit()