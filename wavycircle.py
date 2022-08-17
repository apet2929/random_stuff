import pygame
from pygame.locals import *
from math import *

def yee():
    print("Yee")

print("yee")
yee()

pygame.init()

screen = pygame.display.set_mode([500,500])
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    screen.fill((255, 255, 255))
    
    for yee in range(10000):
        t = yee / (10000)

        r = 50
        a = 5
        n = 20
        x = (r + a * sin(n * t * 360 )) * cos (t * 360 )
        y = (r + a * sin(n * t * 360 )) * sin (t * 360 )
        
        xPoint = 250 + (x *2)
        yPoint = 250 - (y *2)

       
        pygame.draw.circle(screen, (0,0,0), (xPoint, yPoint), 1)

    pygame.display.flip()


pygame.quit()