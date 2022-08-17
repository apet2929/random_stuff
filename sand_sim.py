import pygame
from math import *
from time import sleep
import pygame.event
import pygame.sprite
from pygame.sprite import Sprite
import pygame.draw
from pygame.rect import Rect
import pygame.mouse
from pygame.surface import Surface
from random import random

pygame.init()

def screen_coord_to_grid_coord(mouse_pos):
    grid_x = int(mouse_pos[0] / unit_width)
    grid_y = int(mouse_pos[1] / unit_height)
    grid_x = clamp(grid_x, 0, world_width)
    grid_y = clamp(grid_y, 0, world_height)
    return (grid_x, grid_y)

def grid_coord_to_screen_coord(x, y):
    return (x * unit_width, y * unit_height)

def draw_grid():
    for i in range(len(particles)):
        for j in range(len(particles[i])):
            p = particles[i][j]
            if p == 0:
                continue

            pos = grid_coord_to_screen_coord(i, j)
            w = unit_width + 1
            h = unit_height + 1
            if particles[i][j] == 1:
                pygame.draw.rect(screen, (0,0,200), Rect(pos[0], pos[1], w, h))
            elif p == 2:
                pygame.draw.rect(screen, (100,100,100), Rect(pos[0], pos[1], w, h))
            elif p == 3:
                pygame.draw.rect(screen, (200,200,0), Rect(pos[0], pos[1], w, h))
            elif p == 5:
                pygame.draw.rect(screen, (150,50,0), Rect(pos[0], pos[1], w, h))
                
def clamp(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    return val

def clamp_tuple(val:tuple, min: tuple, max: tuple) -> tuple:
    if val[0] < min[0]:
        val[0] = min[0]
    elif val[0] > max[0]:
        val[0] = max[0]
    if val[1] < min[1]:
        val[1] = min[1]
    elif val[1] > max[1]:
        val[1] = max[1]
    return val
    
def fall(l, i, j, favors_left):
    val = particles[i][j]

    if j is world_height - 1:
        return l
    if val == 2:
        return l
    if val > particles[i][j+1]:
        temp = particles[i][j+1]
        l[i][j+1] = val
        l[i][j] = temp
        return l
    if favors_left:
        if i is not world_width - 1:
            if val > particles[i+1][j+1]:
                temp = particles[i+1][j+1]
                l[i+1][j+1] = val
                l[i][j] = temp
                return l
        if i != 0:
            if val > particles[i-1][j+1]:
                temp = particles[i-1][j+1]
                l[i-1][j+1] = val
                l[i][j] = temp
                return l
    else:
        if i != 0:
            if val > particles[i-1][j+1]:
                temp = particles[i-1][j+1]
                l[i-1][j+1] = val
                l[i][j] = temp
                return l
        if i is not world_width - 1:
            if val > particles[i+1][j+1]:
                temp = particles[i+1][j+1]
                l[i+1][j+1] = val
                l[i][j] = temp
                return l
    if val == 1:
        water(l, i, j, favors_left)
        return l
    
def water(l, i, j, favors_left):
    if favors_left:
        if i != 0:
            if particles[i-1][j] == 0:
                l[i-1][j] = 1
                l[i][j] = 0
    else:
        if i != world_width-1:
            if particles[i+1][j] == 0:
                l[i+1][j] = 1
                l[i][j] = 0
    return l


    # if val == 1:
    #     if j is world_height-1:
    #         return
    #     elif particles[i][j+1] == 0:
    #         l[i][j] = 0
    #         l[i][j+1] = 1
    #         return
    #     favors_left = random() > 0.5
    #     if favors_left:
    #         if i is not world_width-1:
    #             if particles[i+1][j+1] == 0:
    #                 l[i][j] = 0
    #                 l[i+1][j+1] = 1
    #                 return
    #         if i != 0:
    #             if particles[i-1][j+1] == 0:
    #                 l[i][j] = 0
    #                 l[i-1][j+1] = 1
    #                 return    
    #     else:
    #         if i != 0:
    #             if particles[i-1][j+1] == 0:
    #                 l[i][j] = 0
    #                 l[i-1][j+1] = 1
    #                 return 
    #         if i != world_width-1:
    #             if particles[i+1][j+1] == 0:
    #                 l[i][j] = 0
    #                 l[i+1][j+1] = 1
    #                 return

def update():
    _particles = particles.copy()
    
    for i in range(len(_particles)-1, -1, -1):
        favors_left = random() > 0.5
        for j in range(len(_particles[i])-1, -1, -1):
            fall(_particles, i, j, favors_left)
    return _particles

WIDTH = 500
HEIGHT = 500
FPS = 60
fpsClock = pygame.time.Clock()
getTicksLastFrame = 0
screen: Surface = pygame.display.set_mode([WIDTH,HEIGHT])

# SIMULATION VARS

world_width = 60
world_height = 60
unit_width = WIDTH / world_width
unit_height = HEIGHT / world_height
particles = [ [0]*world_width for i in range(world_height)]
run = True
current_particle = 1

while run:
    t = pygame.time.get_ticks()
    delta = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                for row in particles:
                    print(row)
            if event.key >= pygame.K_0 and event.key <= pygame.K_9:
                current_particle = event.key - pygame.K_0
                print(current_particle)

        if pygame.mouse.get_pressed()[0]:
            try:
                mouse_pos = pygame.mouse.get_pos()
                pos = screen_coord_to_grid_coord(mouse_pos)
                particles[pos[0]][pos[1]] = current_particle
            except AttributeError or IndexError:
                print(pos[1])
                pass
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # mouse_pos = pygame.mouse.get_pos()
            # screen_coord_to_grid_coord(mouse_pos)
    
    update()

    draw_grid()



    pygame.display.flip()
    fpsClock.tick(FPS)


pygame.quit()