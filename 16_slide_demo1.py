#!/usr/bin/env python3

import pygame
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

class Player:
    def __init__(self, img):
        # position of the player
        self.x = 100
        self.y = 100

        # we define what the player looks like with the image provided
        self.img = pygame.image.load(img).convert_alpha()

        # we resize the image to 100x100 to have our player be a reasonable size
        self.img = pygame.transform.scale(self.img, (100, 100))

    def draw(self, screen):
        # screen.blit is used for images;
        # if you prefer a shape instead such as a rectangle you can use
        # pygame.draw.rect(screen, (0, 255, 0), (50, 50, 80, 40))
        screen.blit(self.img, (self.x, self.y))

# create an instance of the class Player, called cat
cat = Player("assets/calico_car.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear background
    # the three numbers is in rgb formatting (Google it!)
    screen.fill((255, 255, 255))

    # draw the player
    cat.draw(screen)

    # update the display
    pygame.display.update()

# quit the game if the user closes the window
pygame.quit()