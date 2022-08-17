import pygame
import pygame.draw
from pygame.math import *
from math import *
import pygame.mouse
from time import sleep

pygame.init()

screen = pygame.display.set_mode([500,500])
FPS = 120
fpsClock = pygame.time.Clock()
points = []
line_points = []

def curve(t):
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    # p1_weight = pow((1-t),3)
    # p2_weight = 3 * pow((1-t), 2) * t
    # p3_weight = 3 * (1-t) * (t*t) 
    # p4_weight = t*t*t
    # p = (p1 * p1_weight) 
    # + (p2 * p2_weight) 
    # + (p3 * p3_weight) 
    # + (p4 * p4_weight)

    pa = p1.lerp(p2, t)
    pb = p2.lerp(p3, t)
    pc = p3.lerp(p4, t)

    pd = pa.lerp(pb, t)
    pe = pb.lerp(pc, t)

    pf = pd.lerp(pe, t)
    

    draw_vec(p1,p2)
    draw_vec(p2,p3)
    draw_vec(p3,p4)

    draw_vec(pa, pb)
    draw_vec(pb, pc)

    draw_vec(pd, pe)

    draw_point(pf)

    for i in range(len(line_points)-1):
        p0 = line_points[i]
        p1 = line_points[i + 1]
        pygame.draw.line(screen, (0,0,255), (p0.x,p0.y), (p1.x, p1.y))

    return pf

def add_point(x: int = None, y: int = None, vec: Vector2 = None):
    if x is not None and y is not None:
        yee = Vector2(x,y)
        points.append(yee)
        return yee
    points.append(vec)
    return vec

def draw_vec(start, end, color = (255,0,0)):
    pygame.draw.line(screen, (255,0,0), (start.x,start.y), (end.x, end.y))

def draw_point(point, color = (255,0,0)):
    pygame.draw.circle(screen, color, (point.x, point.y), 5)

def draw_points():
    for point in points:
        draw_point(point)

def init_curve_line():
    for i in range(250):
        line_points.append(curve(i/250))


run = True
time = 0
tDir = 1
getTicksLastFrame = 0
points_selected = False



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if not points_selected:
                add_point(pos[0],pos[1])
                if len(points) is 4:
                    points_selected = True
                    print(points[0])
                    print(points[1])
                    print(points[2])
                    print(points[3])
                    init_curve_line()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                print("yee")
                points_selected = False
                points.clear()
                line_points.clear()
                time = 0

    #   Timer
    t = pygame.time.get_ticks()
    time += (t - getTicksLastFrame) / 1000.0 * tDir
    if time > 1 or time < 0:
        if time > 1:
            time = 1
        else:
            time = 0
        tDir *= -1
    getTicksLastFrame = t

    screen.fill((255, 255, 255))

    draw_points()

    if points_selected:
        curve(time)
    
    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()