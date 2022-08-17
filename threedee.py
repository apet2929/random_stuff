from math import cos, degrees, radians, sin
import pygame
from pygame import draw
import pygame.display
import pygame.event
from pygame.draw import *
from color import Color
from pygame.surface import Surface

WIDTH = 500
HEIGHT = 500
pygame.init()

class Cube():
    def __init__(self, width:float, height:float, depth: float, x:float=0, y:float=0, z:float=0) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.x = x
        self.y = y
        self.z = z
        self.nodes: list[list[float]] = []
        self.edges:list[list[int]] = []

        xpw = x + width
        yph = y + height
        zpd = z + depth

        self.nodes = [
            [x, y, z], [x, y, zpd], [x, yph, z],
            [x, yph, zpd], [xpw, y, z], [xpw, y, zpd],
            [xpw, yph, z], [xpw, yph, zpd]
        ]
        self.edges = [[0, 1], [1, 3], [3, 2], [2, 0], [4, 5], [5, 7], [7, 6], [6, 4], [0, 4], [1, 5], [2, 6], [3, 7]]

"""
Rotate around Z Axis
"""
def rotateZ3D(nodes, rads):
    sinTheta = sin(rads)
    cosTheta = cos(rads)
    for i in range(len(nodes)):
        point = nodes[i]
        newX = point[0] * cosTheta - point[1] * sinTheta
        newY = point[1] * cosTheta + point[0] * sinTheta
        oldZ = point[2]
        nodes[i] = (newX, newY, oldZ)

"""
Rotate around Y Axis
"""
def rotateY3D(nodes, rads):
    sinTheta = sin(rads)
    cosTheta = cos(rads)
    for i in range(len(nodes)):
        point = nodes[i]
        newX = point[0] * cosTheta - point[2] * sinTheta
        newZ = point[2] * cosTheta + point[0] * sinTheta
        oldY = point[1]
        nodes[i] = (newX, oldY, newZ)

"""
Rotate around X Axis
"""
def rotateX3D(nodes, rads):
    sinTheta = sin(rads)
    cosTheta = cos(rads)
    for i in range(len(nodes)):
        point = nodes[i]
        newY = point[1] * cosTheta - point[2] * sinTheta
        newZ = point[2] * cosTheta + point[1] * sinTheta
        oldX = point[0]
        nodes[i] = (oldX, newY, newZ)

def offsetPoint(x, y) -> tuple:
    return (x + WIDTH/2, y + HEIGHT/2)

def render(screen: Surface):
    screen.fill(bgColor.rgb)

    for i in range(len(cube.edges)):
        edge = cube.edges[i]
        point1 = cube.nodes[edge[0]]
        point2 = cube.nodes[edge[1]]
        p1 = offsetPoint(point1[0], point1[1])
        p2 = offsetPoint(point2[0], point2[1])
        line(screen, edgeColor.rgb, p1, p2, 2)

    for point in cube.nodes:
        draw.circle(screen, nodeColor.rgb, offsetPoint(point[0], point[1]), nodeSize)


cube = Cube(100, 100, 100, x=-100, y=0, z=0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 120


rotateX3D(cube.nodes, radians(240))
rotateY3D(cube.nodes, radians(100))
rotateZ3D(cube.nodes, radians(350))

# Colors
bgColor = Color(hsv=(280, 0.1, 0.8))
nodeColor = Color(hsv=(330, 0.8, 0.7))
edgeColor = Color(hsv=(300, 0.8, 0.4))

nodeSize = 8

running = True
while running:
    delta = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    rotateX3D(cube.nodes, radians(360 * delta / 5))

    render(screen)


    pygame.display.flip()

pygame.quit()