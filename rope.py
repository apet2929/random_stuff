import pygame
from math import *
from pygame.constants import MOUSEMOTION
from pygame.event import get
from pygame.math import *
import pygame.draw
import pygame.mouse
import random

pygame.init()

class Point:
    pos: Vector2 = None
    prev_pos = []
    locked: bool = False
    def __init__(self, position, locked) -> None:
        self.pos = position
        self.prev_pos = [self.pos.x, self.pos.y]
        self.locked = locked
    
    def update(self):
        self.prev_pos[0] = self.pos.x
        self.prev_pos[1] = self.pos.y

    def get_vel(self):
        return self.pos - Vector2(self.prev_pos[0], self.prev_pos[1])

    def draw(self):
        if self.locked:
            color = (0,255,0)
        else:
            color = (0,0,255)
        pygame.draw.circle(screen, color, (self.pos.x * 2, self.pos.y * 2), 4)

    def __str__(self) -> str:
        return str(self.pos) + " locked = " + str(locked)

class Stick:
    pointA: Point = None
    pointB: Point = None
    length: float = None

    def __init__(self, pointA: Point = None, pointB: Point = None) -> None:
        if pointA and pointB:
            self.pointA = pointA
            self.pointB = pointB
            self.do_init()
        else:
            pass

    def do_init(self):
        if self.pointA and self.pointB:
            self.length = self.pointA
            self.length = self.pointA.pos.distance_to(self.pointB.pos)

    def draw(self):
        if self.pointA and self.pointB:
            pygame.draw.line(screen, (0,0,255), (self.pointA.pos.x * 2, self.pointA.pos.y * 2), (self.pointB.pos.x * 2, self.pointB.pos.y * 2))

    def __str__(self) -> str:
        return str(self.pointA) + " | " + str(self.pointB)

        
class Rope():
    points: list[Point] = []
    sticks: list[Stick] = []
    def __init__(self, points:list=None, sticks:list=None, offset: Vector2=None):
        
        if sticks and points:
            for stick in sticks:
                if stick.pointA and stick.pointB:
                    self.sticks.append(stick)
        elif points:
            self.points: list[Point] = points.copy()
        elif offset:
            points = [
                Point(Vector2(offset.x + random.randint(-10,10), offset.y), True),
                Point(Vector2(50+offset.x, offset.y + random.randint(-10,10)), False),
                Point(Vector2(60+offset.x + random.randint(-10,10), 40 + offset.y), False),
                Point(Vector2(80+offset.x, 60 + offset.y + random.randint(-10,10)), False)
            ]
            sticks = [
                Stick(points[0], points[1]),
                Stick(points[1], points[2]),
                Stick(points[2], points[3])
            ]
            self.points = points
            self.sticks = sticks
        else:
            self.points = []
            self.sticks = []

    def add_point(self, point:Point = None, x:float = None, y: float = None, locked: bool = False):
        if point:
            self.points.append(point)
        else:
            self.points.append(Point(Vector2(x,y), locked))
    def add_stick(self, stick:Stick = None, pA: Point = None, pB: Point = None):
        if stick:
            if stick.pointA and stick.pointB:
                self.sticks.append(stick)
        else:
            stick = Stick(pA, pB)
            stick.do_init()
            self.sticks.append(stick)
        self.sticks.append(Stick(pA, pB))
    def render(self):
        for point in self.points:
            point.draw()
        for stick in self.sticks:
            stick.draw()
    def __str__(self):
        return f"Rope with {len(points)} points and {len(sticks)} sticks"

    def update(self, delta):
        if not self.points and self.sticks:
            return

        g = Vector2(0,1) * gravity
        #used for type hints
        point: Point
        for point in self.points:
            if not point.locked:

                velocity = point.get_vel()
                point.update()

                point.pos += velocity
                point.pos += g * delta
                
        #used for type hints
        stick: Stick
        for i in range(3):
            for stick in self.sticks:
                # print(stick)
                if stick.pointA and stick.pointB:
                    # dist = (stick.pointA)
                    dist = (stick.pointA.pos - stick.pointB.pos).magnitude()
                    d_pos = (stick.pointA.pos - stick.pointB.pos)
                    dl = stick.length - dist
                    current = d_pos * 0.5 * (dl/dist)
                    
                    a = stick.pointA.locked
                    b = stick.pointB.locked
                    if not a and not b:
                        stick.pointA.pos += current
                        stick.pointB.pos -= current
                    elif b and not a:
                        stick.pointA.pos += (current * 2)
                    elif a and not b:
                        stick.pointB.pos -= (current * 2)


def get_closest_point(pos: Vector2):
    closest = None
    closest_dist = None
    point: Point

    for rope in ropes:
        for point in rope.points:
            distance = point.pos.distance_to(pos)
            if not closest:
                closest_dist = point.pos.distance_to(pos)
                closest = point
            else:
                if distance < closest_dist:
                    closest_dist = distance
                    closest = point

    return closest

def get_closest_stick(pos: Vector2):
    closest = None
    closest_dist = None
    stick: Stick = None
    rope: Rope = None

    for rope in ropes:
        for stick in rope.sticks:
            if stick and stick.pointA and stick.pointB:
                center = stick.pointA.pos.lerp(stick.pointB.pos, 0.5)
                distance = pos.distance_to(center)
                if not closest:
                    if not closest:
                        closest_dist = distance
                        closest = stick
                    else:
                        if distance < closest_dist:
                            closest_dist = distance
                            closest = stick
    
    return (rope, stick)

def update(delta):
    for rope in ropes:
        rope.update(delta)

def render():
    for rope in ropes:
        rope.render()

def setupSticksTemp():
    for i in range(len(points)-1):
        sticks.append(Stick(
            points[i], points[i+1]
        ))

def add_point(point):
    points.append(point)
    print(points)

screen = pygame.display.set_mode([500,500])
FPS = 120
fpsClock = pygame.time.Clock()

# SIMULATION VARS
points = []
sticks = []
ropes: list[Rope] = []
tempRope = Rope(offset=Vector2(50,50))
ropes.append(tempRope)
# ropes.append(Rope())
gravity = 20

run = True
setup = True
pause = True
setupPoints = False
setupSticks = False
setupRopes = False
locked = False
eraser = False
tempStick = Stick()


while run:
    delta = fpsClock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONUP:
            
            if setupPoints:
                point = Point(
                    Vector2(
                        mouse_pos[0] / 2,
                        mouse_pos[1] / 2
                    ),
                    locked
                )

                tempRope.add_point(point)
                
            elif setupSticks:
                c_point = get_closest_point(Vector2(
                    mouse_pos[0]/2, mouse_pos[1]/2
                ))
                print(c_point)
                if tempStick.pointA is None:
                    tempStick.pointA = c_point
                elif tempStick.pointB is None:
                    if c_point is tempStick.pointA:
                        print("Oops! Start and end point are the same!")
                    else:
                        tempStick.pointB = c_point
                        tempStick.do_init()

                        tempRope.add_stick(tempStick)
                        print(tempRope.sticks)

                        print("Added stick: " + str(tempStick))
                        tempStick = Stick()
            elif setupRopes:
                ropes.append(Rope(offset=Vector2(mouse_pos[0]/2, mouse_pos[1]/2)))
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                locked = not locked
                print("locked = " + str(locked))
            elif event.key == pygame.K_RETURN:
                # if setup:
                #     if setupSticks:
                #         temp = Rope(points, sticks)
                #         ropes.append(temp)
                #         points = []
                #         sticks = []
                #         print("Yee")

                #     else:
                #         points = []
                #         sticks = []
                #         setupPoints = True
                #         setupSticks = False

                setup = not setup
            
            if setup:
                if event.key == pygame.K_1:
                    print("Setting up points")
                    setupPoints = True
                    setupSticks = False
                    setupRopes = False
                elif event.key == pygame.K_2:
                    setupPoints = False
                    setupSticks = True
                    setupRopes = False
                    print("Setting up sticks")
                elif event.key == pygame.K_3:
                    print("Setting up ropes")
                    setupPoints = False
                    setupSticks = False
                    setupRopes = True
                elif event.key == pygame.K_0:
                    print("yee")
                    ropes = []
                    points = []
                    sticks = []
                elif event.key == pygame.K_BACKSPACE:
                    (rope, stick) = get_closest_stick(Vector2(mouse_pos[0]/2, mouse_pos[1]/2))
                    if rope and stick:
                        rope.sticks.remove(stick)

    screen.fill((255, 255, 255))
    if delta < 1 and delta != None:
        if not setup:
            update(delta)
    render()
    pygame.display.flip()
   


pygame.quit()