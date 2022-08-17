import pygame
from math import *
from time import sleep

pygame.init()

screen = pygame.display.set_mode([500,500])
FPS = 5
fpsClock = pygame.time.Clock()


def wav():
    point = (250,250)
    for i in range(360):
        r = abs(sin(i) * 300)
        xlen = cos(i) * r
        ylen = sin(i) * r
        x = xlen + point[0]
        y = ylen + point[1]
        pygame.draw.line(screen, (0,0,0), (point[0], point[1]), (x, y))
        pygame.display.flip()
        sleep(.1)



run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    point = (250,250)
    wav()

    pygame.display.flip()
    fpsClock.tick(FPS)


pygame.quit()