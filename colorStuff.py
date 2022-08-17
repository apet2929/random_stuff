import pygame
import pygame.draw
from pygame.locals import *
from math import *
from pygame.math import Vector2
from pygame.pixelarray import PixelArray
import pygame.transform
from pygame.surface import Surface
from button import Button
import pygame.display
import pygame.sprite
import pygame.font
import pygame.time
from color import Color
import ui
import time

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH,HEIGHT], RESIZABLE)
run = True
FPS = 120
clock = pygame.time.Clock()


def resize(w, h):
    global screen
    oldScreen = screen
    WIDTH = w
    HEIGHT = h 
    screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    del oldScreen

def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    return value

def colorWheel(radius, value) -> Surface:
    colorWheel: list[Color] = []
    wheelSurface = pygame.Surface((radius * 2 + 1, radius * 2 + 1))
    wheelSurface = wheelSurface.convert_alpha()
    wheelSurface.fill((0,0,0,0))
    wheelPixels = pygame.PixelArray(wheelSurface)


    for hue in range(360):  
        # for value in range(6):  
        for saturation in range(51):  
            colorWheel.append(Color(hsv=(hue+300, saturation / 50, value)))

    # def sortWheel(color: Color):
    #     return color.value
    # colorWheel.sort(key=sortWheel)

    """
    Draw a circle where
    theta = hue
    pointLength (radius) = saturation
    point on circle = 
        x = saturation * sin(hue)
        y = saturation * cos(hue)
    """

    for i in range(len(colorWheel)):
        # print(colorWheel[i])
        color = colorWheel[i]
        rads = radians(color.hue)
        pointLength = color.saturation * (radius-1)

        x = 0
        y = 0
        # originX = (color.value * spacing) + radius
        originX = radius
        originY = radius
        
        x = int(pointLength * cos(rads) + originX)
        y = int(pointLength * sin(rads) + originY)
        
        wheelPixels[x,y] = color.rgb
        wheelPixels[x+1,y] = color.rgb
        wheelPixels[x,y+1] = color.rgb
        wheelPixels[x+1,y+1] = color.rgb
        # wheelPixels[x-1,y] = color.rgb
        # wheelPixels[x,y-1] = color.rgb
        # wheelPixels[x+1,y-1] = color.rgb
        # wheelPixels[x-1,y-1] = color.rgb

    wheelPixels.close()
    print("done")
    return wheelSurface

def createPath(speed, radius, offset):
    path = []
    forwards = 1
    x = 50
    for i in range(int(400 * pi)):
        rads = (i+offset) / 200

        #  Circle 
        # x = (radius * cos(rads)) + WIDTH/4
        # y = (radius * sin(rads)) + HEIGHT/4

        # Bounces in the middle for some reason
        # x += sin(rads) > 0 if speed/100 else speed/-100

        
        if forwards > 0:
            x += (speed+1)/10
        else:
            x -= (speed+1)/10

        if x >= 300 or x < 0:
            forwards *= -1   
        y = radius * sin(rads * speed) + HEIGHT/4
        path.append(Vector2(x, y))
    return path

# color = Color(hsv=(0, 0.5, 1))
# color2 = Color(hsv=(360/3, 0.5, 1))
# color3 = Color(hsv=(360/5, 0.5, 1))

# color = Color(hsv=(295, 0.5, 1))
# color2 = Color(hsv=(355 , 0.5, 1))
# color3 = Color(hsv=(35, 0.5, 1))

start = time.perf_counter()

bgCol = Color(rgb=(0,0,0))
for i in range(20):
    wheel = colorWheel(100, i/20)
wr = wheel.get_rect()

end = time.perf_counter()

print(start, end, start-end, sep="\n")

# wheelSurface = colorWheel(50, 1)

# rotationSpeed = 360 / 2
# speed = 1
# rotationDeg = 0

# wheelRotationSurface: Surface
# pathIndex = 0
# radius = WIDTH/8
# wheelSurfacePath: list[Vector2] = createPath(speed, radius)

# Gen wheels and paths
# wheels = []
# paths = []
# for i in range(6):
#     wheels.append(colorWheel(50, i / 5))
#     paths.append(createPath(speed*i, radius, i * radius))

# wheelRect = wheels[0].get_rect().copy()

while run:
    delta = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            print(event)
            resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            # print(wheelRotationSurface.get_rect().center)
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if wr.collidepoint(x, y):
                col = wheel.get_at((x, y))
                wheel.get_at_mapped
                bgCol.set_rgb(col)


    screen.fill(bgCol.rgb)
    screen.blit(wheel, (0,0))
    # for i in range(len(wheels)):
    #     wheelRotationSurface = pygame.transform.rotate(wheels[i], rotationDeg)

    #     # Centers color wheel in wheelRect
    #     # Move wheel
    #     pathIndex += 1
    #     if pathIndex >= len(paths[0]):
    #         pathIndex = 0
    #     wheelRect.center = paths[i][pathIndex].x, paths[i][pathIndex].y

    #     dx = wheelRect.centerx - wheelRotationSurface.get_rect().centerx
    #     dy = wheelRect.centery - wheelRotationSurface.get_rect().centery
    #     screen.blit(wheelRotationSurface, wheelRect.move((i - 3) * 5 + dx, (i - 3) * 5 + dy))
    # Debug rect drawing
    # pygame.draw.rect(screen, (0,0,0), wheelRotationSurface.get_rect(), 2)
    # pygame.draw.rect(screen, (0,0,0), wheelRect, 2)

    pygame.display.flip()


pygame.quit()