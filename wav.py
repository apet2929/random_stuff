import math
import pygame
from pygame import draw
from pygame.locals import *
from math import *
from button import Button
import pygame.display
import pygame.sprite
import pygame.font
import pygame.time
from color import Color
import pygame.draw

pygame.init()

screen = pygame.display.set_mode([500,500])
run = True

def removezero(num:float) -> float:
    if abs(num) < 0.0001:
        return 0.0001
    return num

def get_func(equation) -> tuple:
    x_func = eval(f"lambda t: {equation[0]}")
    y_func = eval(f"lambda t: {equation[1]}")
    return (x_func, y_func)


def calc_points(resolution) -> list:
    global points, x_extrema, y_extrema, x_avg, y_avg
    points.clear()
    x_max = 0
    x_min = math.inf
    y_max = 0
    y_min = math.inf
    x_avg = 0
    y_avg = 0
    
    for yee in range(int(TWOPI*resolution)):
        t = yee / resolution

        x = eq_func[0](t) * SCALE
        y = eq_func[1](t) * SCALE

        x_max = max(x_max, x)
        x_min = min(x_min, x)
        x_avg += x
        y_avg += y

        y_max = max(y_max, y)
        y_min = min(y_min, y)
        
        points.append((x, y))

    # x_avg /= resolution*TWOPI
    # y_avg /= resolution*TWOPI

    x_extrema = [x_min, x_max]
    y_extrema = [y_min, y_max]


def set_setting(setting):
    global eq_func, equation
    print(setting)
    equation = EQUATIONS[setting]
    eq_func = get_func(equation)

def get_text() -> str:
    global equation
    x_text = equation[0].replace("xOffset", STR_FORMAT.format(xOffset))
    y_text = equation[1].replace("yOffset", STR_FORMAT.format(yOffset))
    return (x_text, y_text)


def key_pressed(key):
    global xOffset, yOffset, spacePressed, run, menu
    if key == pygame.K_LEFT:
        xOffset -= STEP_SIZE
    elif key == pygame.K_RIGHT:
        xOffset += STEP_SIZE
    elif key == pygame.K_UP:
        yOffset += STEP_SIZE
    elif key == K_DOWN:
        yOffset -= STEP_SIZE
    elif key == K_LSHIFT:
        # Round down to the nearest int
        xOffset = int(xOffset)
        yOffset = int(yOffset)
    elif key in range(pygame.K_0, pygame.K_9+1):
        set_setting(key - pygame.K_0)
    else:
        # No need to recalculate points for these
        if key == pygame.K_SPACE:
            spacePressed = not spacePressed
        elif key == pygame.K_RETURN:
            print("xOffset: " + str(xOffset))
            print("yOffset: " + str(yOffset))
        elif key == pygame.K_ESCAPE:
            run = False
        elif key == pygame.K_d:
            menu = not menu
        return
    
    # Recalculate points
    calc_points(RESOLUTION)

def gen_colors(length):
    colors = []
    print("Generating colors start")
    for i in range(int(length+1)):
        hue = i / length * 360
        colors.append(Color(hsv=(hue, 0.7, 0.8)))
    print("Generating colors end")
    return colors

def draw_gui(screen):
    leftButton.draw(screen)
    rightButton.draw(screen)
    upButton.draw(screen)
    downButton.draw(screen)

    eq_text = get_text()
    text = FONT.render(f"x = {eq_text[0]}", True, (0,0,0))
    screen.blit(text, (0,50))
    text = FONT.render(f"y = {eq_text[1]}", True, (0,0,0))
    screen.blit(text, (0,100))

    text = FONT.render(str(CLOCK.get_fps())[0:5], False, (0,0,0))
    screen.blit(text, (400, 0))

def draw_points(moveby, points):
    for i, point in enumerate(points):
        pygame.draw.circle(screen, colors[i].rgb, (point[0] + moveby[0], point[1] + moveby[1]), 1)

def draw_colorful_lines(surf, colors, closed, points, moveby, width=1):
    for i in range(len(points)-1):
        pygame.draw.line(surf, colors[i].rgb, (points[i][0] + moveby[i], points[i][1] + moveby[1]), (points[i+1][0] + moveby[i], points[i+1][1] + moveby[1]), width)
    if closed:
        pygame.draw.line(surf, colors[-1].rgb, points[-1], points[0], width)

leftButton = Button(300,350,100,50, "<-")
rightButton = Button(400,350,100,50, "->")
upButton = Button(350, 300, 100, 50, "^")
downButton = Button(350, 400, 100, 50, "V")

TWOPI = 2 * pi
FPS = 200
STR_FORMAT = "{0:.2f}"
STEP_SIZE = 1
RESOLUTION = 1000
SCALE = 100
ROTATE_SPEED = 5
FONT = pygame.font.SysFont("Courier", 20, False)
CLOCK = pygame.time.Clock()

EQUATIONS = [ # (x equation, y equation)
    ("(sin(xOffset * t))", "(cos(yOffset * t))"),
    ("(sin(xOffset * t) + cos(xOffset * t)/2)", "(cos(yOffset * t) + sin(yOffset * t)/2)"),
    ("(sin(xOffset * t) + cos(xOffset * t)/2)", "(cos(yOffset * t) - sin(yOffset * t)/2)"),
    
    ("(sin(tan(xOffset * t)))", "(sin(yOffset*t))"),
    ("(sin(xOffset * t) / removezero(cos(xOffset * t/8)))", "cos(yOffset * t/8)"),
    ("(sin(xOffset * t) + atan(xOffset * t))", "(cos(yOffset * t) + atan(yOffset * t))"),
    ("(sin(xOffset * t) + 1/removezero(cos(xOffset * t)))", "(cos(yOffset * t) + 1/removezero(sin(yOffset * t)))"),
    ("(t*2/TWOPI)", "tan(yOffset * t)"),
    ("(tan(xOffset * t) % SCALE - 3.5)", "sin(yOffset * t)"),
    # ("(tan(xOffset * t)) % SCALE","(atan(tan(yOffset * t)))"),
    ("sin(TWOPI/4*xOffset*t)+tan(xOffset*t/8)/2","cos(TWOPI/4*yOffset*t)+tan(yOffset*t/8)%SCALE")
]

# The coolest in animations
TAN_FUNCS = [
    ("(t*2/TWOPI)", "tan(yOffset * t)"),    #   Surprisingly simple for how cool it looks
    ("(sin(xOffset * t))", "(tan(yOffset * t) % SCALE - 3.5)"),   #   Would look good on an rgb wall, make sure x != y
    ("sin(TWOPI/4*xOffset*t)+tan(xOffset*t/8)/2","cos(TWOPI/4*yOffset*t)+tan(yOffset*t/8)%SCALE"),  #   Not super interesting
    ("(sin(xOffset * t) + atan(xOffset * t))", "(cos(yOffset * t) + atan(yOffset * t))"),  #    This one is cool if you have xOffset 1 less or more than yOffset
    ("sin(TWOPI*xOffset*t)+tan(xOffset*t/8)*0.05","cos(TWOPI*yOffset*t)+tan(yOffset*t/8)*0.05"),    
    ("sin(xOffset*t*0.005)+tan(xOffset*t)*0.005","cos(yOffset*t)+tan(yOffset*t*0.005)*0.005"),  #   Very cool, looks like a black hole or smth
    ("tan(xOffset*xOffset*t * 0.05)", "tan(yOffset * yOffset * t * 0.05)")
]


xOffset = 0
yOffset = 0
spacePressed = False

points = []    #    List of points for drawing, len=2*pi*resolution
x_extrema = [0,0]   #   Lowest and highest vals used to center the equation   
y_extrema = [0,0]   #   Lowest and highest vals used to center the equation   
x_avg = 0
y_avg = 0
equation = ""   #   String equation used in eval() function to generate eq_func
eq_func:tuple = None    #   Callable functions used to generate points
set_setting(0)
calc_points(RESOLUTION)
colors: list[Color] = gen_colors(TWOPI*RESOLUTION) #   Generates a list of colors from hue=0 to 360 
menu = False    #   Draw GUI?
line = False

while run:
    delta = CLOCK.tick(FPS) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            key_pressed(event.key)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if leftButton.rect.collidepoint(event.pos):
                key_pressed(pygame.K_LEFT)
            if rightButton.rect.collidepoint(event.pos):
                key_pressed(pygame.K_RIGHT)
            if downButton.rect.collidepoint(event.pos):
                key_pressed(pygame.K_DOWN)
            if upButton.rect.collidepoint(event.pos):
                key_pressed(pygame.K_UP)
              
    screen.fill((255, 255, 255))

    if spacePressed:
        yOffset += (delta * (ROTATE_SPEED/10))
        xOffset += (delta * (ROTATE_SPEED/10))
        calc_points(RESOLUTION)
    
    # Draw centered points
    # ex: function f is centered at (0,100), f width = 300, f height = 800
    # We would offset x by 300/2
    fw = x_extrema[1] - x_extrema[0]
    fh = y_extrema[1] - y_extrema[1]
    func_center = [0,0]
    if fw in range(1000) and fh in range(1000):
        func_center = [x_extrema[0] + fw/2, y_extrema[0] + fh/2]

    """
    function center = 50, we move every point to the right 200 to center it
    function center = 0, we move every point to the right 250 to center it
    moveby = 250 - function center
    """

    moveby = [200 - func_center[0], 200 - func_center[1]]
    if not line:
        draw_points(moveby, points)
    else:
        draw_colorful_lines(screen, colors, False, points, moveby, 1)
    if menu:
        draw_gui(screen)
    # pygame.draw.circle(screen, (255,0,0), (x_avg, y_avg), 50)
    # print(x_avg, y_avg)

    pygame.display.flip()


pygame.quit()