from math import atan2, cos, degrees, radians, sin, sqrt
import pygame
from pygame import PixelArray, Rect, Surface, Vector2
import pygame.display
import pygame.event
import pygame.draw
from pygame.sprite import Sprite, Group
from color import Color
from ui import *
import pygame.transform
import pygame.time
import pygame.mouse

class Position:
    """
    Handles transforming between world and screen positions
    """
    def __init__(self, x, y) -> None:
        self.pos = [x, y]

    @property
    def screen_pos(self) -> tuple:
        return camera.t_world_to_screen_pos(self.pos)
    
    @screen_pos.setter
    def screen_pos(self, pos: tuple):
        world_pos = camera.t_screen_to_world_pos(pos)
        self.pos[0] = world_pos[0]
        self.pos[1] = world_pos[1]

    @screen_pos.getter
    def screen_pos(self):
        return camera.t_world_to_screen_pos(self.pos)


class Camera:
    def __init__(self, x, y, size: list) -> None:
        """
        x, y -> initial camera posiiton
        size -> list [width, height]
        """
        self.pos = Vector2(x, y)
        self.prev_pos = Vector2(x, y)
        # TODO : Implement zooming
        self.size = size
        self.world_rect = Rect(x, y, size[0], size[1])
        self.screen_rect = Rect(0,0,size[0], size[1])
        self.following: Sprite = None
    
    def update(self, delta):
        desired_pos = Vector2(self.following.rect.center)
        lerp = desired_pos.lerp(self.prev_pos, 0.03)
        self.prev_pos = self.pos
        self.pos = lerp

    def follow(self, sprite:Sprite):
        """
        Sets the camera to follow a sprite's position by lerping
        Camera position is updated in the update() method
        Only needs to be called once
        """
        self.following = sprite

    def t_screen_to_world_pos(self, pos: tuple = None):
        """
        Turns a point from screen pos to world pos 
        """
        return self.screen_to_world_pos(pos[0], pos[1])

    def screen_to_world_pos(self, x, y):
        """
        Turns a point from screen pos to world pos 
        """

        rX, rY = transform_pos((x, y))
        worldX = rX + self.pos.x
        worldY = rY + self.pos.y
        
        return (worldX, worldY)
    
    def world_to_screen_pos(self, x: float, y: float):
        """
        Turns a point from world pos to screen pos
        """

        return (x - self.pos.x, y - self.pos.y)

    def t_world_to_screen_pos(self, pos: tuple):
        """
        Turns a point from world pos to screen pos
        """
        
        return self.world_to_screen_pos(pos[0], pos[1])
    

    def on_screen(self, screen_pos: Rect = None, world_pos: Rect = None):
        """
        Idk if this will work
        """
        
        if screen_pos:
            return screen_pos.colliderect(self.screen_rect)
        else:
            result = world_pos.colliderect(self.world_rect)
            return result

    def move(self, x:float=None, y:float=None):
        self.prev_pos = self.pos
        # Handle x and y being None
        xm = 0
        ym = 0
        if x:
            self.pos.x += x
            xm = x
        if y:
            self.pos.y += y
            ym = y
        self.world_rect.topleft = (self.pos.x, self.pos.y)
        # self.world_rect.move_ip((xm, ym))

    def debug_draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.screen_rect, 4)
        pygame.draw.rect(screen, (0,255,0), self.world_rect, 4)      

class World:
    def __init__(self) -> None:
        # TODO : Come up with a better name for this
        # List of things the arrows collide with
        self.rects: list[Rect] = []

        # Ground
        self.rects.append(Rect(-1000000, HEIGHT, 1000000, HEIGHT*10))

        # Wall
        self.rects.append(Rect(WIDTH/2, HEIGHT/2, WIDTH * 3/2, HEIGHT/2))

    def draw(self, screen):
        for rect in self.rects:
            # Debug rects
            pygame.draw.rect(screen, (38, 182, 54), rect.move(-camera.pos.x, -camera.pos.y))
        
    def collide(self, other: Sprite):
        # Only bother checking for collision if the sprite is on screen
        if not camera.on_screen(world_pos=other.rect):
            return False
        for rect in self.rects:
            # Only bother checking for collision if the rect is on screen
            if camera.on_screen(world_pos=rect):
                if other.rect.colliderect(rect):
                    return True
                
            # Other not on screen

        return False

class Player(Sprite):
    def __init__(self, worldX, worldY) -> None:
        super().__init__()
        self.pos:Vector2 = Vector2(worldX,worldY)
        
        self.size = (60,100)
        self.rect = Rect(self.pos.x, self.pos.y, self.size[0] ,self.size[1])
        self.IMAGE = Surface(self.size, pygame.SRCALPHA)
        self.init_image()
        self.image = self.IMAGE.copy()

        # MECHANICS
        # Arrows : You have a limited number of arrows
        self.arrows = 10

    def draw(self, screen: pygame.Surface):
        screen_pos = camera.world_to_screen_pos(self.pos.x, self.pos.y)
        screen.blit(self.image, screen_pos)
        pygame.draw.circle(screen, (0,255,0), screen_pos, 4)
        
    def init_image(self):
        # Draw self with rects
        black = (0,0,0)

        """
        ---------------OOOOOOOOO--------
        ---------------OOOOOOOOO--------
        ---------------OOOOOOOOO--------
        ---------------OOOOOOOOO--------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOOOOOOOOOOOO----------
        -----OOOOOOO----OOOOOO----------
        -----OOOOOOO----OOOOOO----------
        -----OOOOOOO----OOOOOO----------
        -----OOOOOOO----OOOOOO----------
        -----OOOOOOO----OOOOOO----------
        """
        head = Rect(30,0,20,25)
        body = Rect(10,20,30,50)
        leg1 = Rect(10,50,10,50)
        leg2 = Rect(30,50,10,50)
        pygame.draw.rect(self.IMAGE, black, head)
        pygame.draw.rect(self.IMAGE, black, body)
        pygame.draw.rect(self.IMAGE, black, leg1)
        pygame.draw.rect(self.IMAGE, black, leg2)

class Arrow(Sprite):
    # Used for calculating launch angle
    ZERO = Vector2(0,0)

    # Affects how fast the arrow falls
    GRAVITY = Vector2(0,10)
    MASS = 100

    # How fast the arrows come out of the bow
    POWER_SCL = 10

    """
    launch angle is in degrees in constructor, radians afterwards
    rotation is in radians
    """
    def __init__(self, pos: Vector2, power: float, launch_angle: float, world: World) -> None:
        self.position: Vector2 = Vector2(pos.x, pos.y)
        
        launch_angle = radians(launch_angle)
        self.launch_angle = launch_angle
        self.velocity: Vector2 = Vector2(power * cos(launch_angle), power * sin(launch_angle))
        self.rotation: float = self.launch_angle
        self.IMAGE = Arrow.draw_arrow()
        self.image = self.IMAGE.copy()
        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.rotate() # Need this or else the arrow will draw at 0 degrees for the first frame

        self.time = 0 # Not needed yet but I might use later for something

        self.world = world # Used to keep track of the platforms to be collided with
        self.collided = False

        super().__init__()

    def update(self, delta) -> None:
        self.time += delta
        if self.collided:
            return
        self.velocity += Arrow.MASS * Arrow.GRAVITY * delta
        self.position += self.velocity * delta
        
        self.rotate()
        center = (self.position.x, self.position.y)
        self.rect = self.image.get_rect(center=center)  # Update bounding box

        collided = self.world.collide(self)
        if collided:
            print("yee")
            self.collided = True
            d = {
                "pos", self.position
            }
            
            event = pygame.event.Event(pygame.USEREVENT+1, d)
            pygame.event.post(event)
            # hit ground  
    
    def draw(self, screen: Surface, camera: Camera):
        pos = camera.t_world_to_screen_pos(self.rect.topleft)
        # if camera.on_screen(pos):
        screen.blit(self.image, pos)

    # Sets rotation variable and rotates the image
    def rotate(self) -> None:
        self.rotation = atan2(-self.velocity.y, self.velocity.x)
        # self.scale_img()
        self.image = pygame.transform.rotate(self.IMAGE, degrees(self.rotation))

    # WARNING: This doesn't work (yet)
    def get_head_point(self):
        unrotated = Vector2(50,10)
        rotated = unrotated.rotate_rad(self.rotation)
        return self.position

    def draw_arrow():
        arrow = Surface((140, 35), pygame.SRCALPHA)

        # Colors
        shaft1 = (120, 60, 35)
        shaft2 = (90, 40, 25)
        feather1 = (160, 60, 20)
        feather2 = (120, 30, 20)
        head1 = (120,120,120)
        head2 = (90,90,90)

        pygame.draw.line(arrow, shaft1, (0,16), (120,16), 10)
        pygame.draw.line(arrow, shaft2, (0,19), (120,19), 5)
        for i in range(21):
            if i < 12:
                pygame.draw.line(arrow, head1, (120, 6+i), (136, 16), 2)
            else:
                pygame.draw.line(arrow, head2, (120, 6+i), (136, 16), 2)
        for i in range(0,24,2):
            if i % 4 == 0:
                pygame.draw.line(arrow, feather1, (3+i, 3), (6+i, 12), 2)
                pygame.draw.line(arrow, feather1, (6+i, 20), (3+i, 29), 2)
            else:
                pygame.draw.line(arrow, feather2, (3+i, 3), (6+i, 12), 2)
                pygame.draw.line(arrow, feather2, (6+i, 20), (3+i, 29), 2)

        arrow = pygame.transform.smoothscale(arrow, (80,20))
        return arrow

    def draw_arrow_old():
        """
        POOPY- deprecated
        Looks bad
        """
        surf = Surface((160,40))
        surf = pygame.Surface.convert_alpha(surf)
        surf.fill((0,0,0,0))

        # pygame.draw.rect(surf, (155, 66, 26), Rect(5,5,30,7)) # Back end
        # pygame.draw.rect(surf, (80, 195, 235),  Rect(30,5,25,7)) # Front end
        brown = (155, 66, 26)
        tip_col = (77, 74, 80)
        feather_col = (218, 0, 237)
        pygame.draw.line(surf, brown, (0, 20), (150, 20), 8)

        tip_points = [
            (140, 30), (140, 10), (160, 20)
        ]

        feather_points_1 = [
            (10, 24), (10, 32), (50, 24)
        ]
        feather_points_2 = [
            (10, 16), (10, 8), (50, 16)
        ]
        pygame.draw.polygon(surf, tip_col, tip_points)
        pygame.draw.polygon(surf, feather_col, feather_points_1)
        pygame.draw.polygon(surf, feather_col, feather_points_2)

        # surf, ns = resize_aa(surf, 20)
        # surf.fill((155, 66, 26), Rect(5,5,50,10))
    
        # pygame.draw.rect(surf, (255,0,0), Rect(5,5,50,10), 2)
        return surf

    
    def get_flight_path(origin:Vector2, power:float, angle:float) -> list[tuple]:
        """
        Returns a list of points (tuple) along the arrow's flight path

        Parameters:
        origin  - Origin point
        power   - The magnitude of the initial velocity
        angle   - The initial angle (degrees)
        """
        scl = 10 # of points
        points = []
        acceleration = Arrow.GRAVITY * Arrow.MASS
        vel0 = Vector2(power,0).rotate(angle)
        for i in range(scl):
            t = i * 0.5 / scl # from t = 0 to 0.5
            x = origin.x + (vel0.x * t)
            y = origin.y + (vel0.y * t) + (0.5 * acceleration.y * t**2)
            points.append((x, y))

        return points
    
    
    def get_components(origin: Vector2, point1: tuple) -> tuple:
        """
        Returns (origin - Vec2, power - float, angle - float (degrees)) as a tuple
        """
        vec = Vector2(point1[0] - origin.x, point1[1] - origin.y)
        power = vec.magnitude() * Arrow.POWER_SCL
        angle = -1 * vec.angle_to(Arrow.ZERO) # Down = positive
        return (origin, power, angle)

class MainMenuPage(Page):
    def __init__(self) -> None:
        bPlay = Button("Play", SIZE, (50,50), (25,10), button1, button2, buttontxt, fonts["button"], 45)
        buttons = [bPlay]
        mainMenuText = Text("Archery Game", SIZE, (50,25), fonts["title"], txtCol)
        texts = [mainMenuText]
        super().__init__(buttons, texts, input_box=False)
    
    def handle_input(self, events):
        super().handle_input(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.on_click(event.pos)
    
    def on_click(self, mouse_pos) -> int or None:
        button_index = super().on_click(mouse_pos)
        if button_index == 0:
            global state
            # Play button
            state = 1

class GamePage(Page):
    def __init__(self,) -> None:
        self.tFPS = Text("", SIZE, (90,5), fonts["button"], txtCol)
        texts = [self.tFPS]

        bQuit = Button("Quit", SIZE, (10,5), (20,10), button1, button2, buttontxt, fonts["button"], 10)
        buttons = [bQuit]
        super().__init__(buttons, texts, input_box=False)

        # Game vars
        self.arrows = Group()
        self.mouse_drag = False
        self.world = World()
        self.player = Player(100,100)
        camera.follow(self.player)

    def update(self, delta):
        global clock
        self.arrows.update(delta)
        self.tFPS.set_text(str(clock.get_fps())[0:6])
        camera.update(delta)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(event.pos)
                pos = camera.t_screen_to_world_pos(event.pos)
                self.mouse_drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_drag = False
                pos = camera.t_screen_to_world_pos(event.pos)
                # Release arrow

                # Vector translated to (0,0)
                origin, power, angle = Arrow.get_components(self.player.pos, pos)
                arrow = Arrow(origin, power, angle, self.world)
                self.arrows.add(arrow)
            elif event.type == pygame.USEREVENT+1:
                self.player.pos = Vector2(event.pos)

    # TODO: Clicking and dragging to shoot arrows
    def on_click(self, mouse_pos) -> int or None:
        button_index = super().on_click(mouse_pos)
        if button_index == 0:
            # quit
            global run
            run = False

    def render(self, screen: Surface, camera: Camera):
        super().render(screen)

        self.world.draw(screen)
        self.player.draw(screen)

        # Draw arrows
        arrow: Arrow
        for arrow in self.arrows.sprites():
            arrow.draw(screen, camera)

        if self.mouse_drag:
            origin = self.player.pos
            mouse_pos = pygame.mouse.get_pos()
            target = camera.t_screen_to_world_pos(mouse_pos)

            pygame.draw.line(screen, (0,255,0),camera.world_to_screen_pos(origin.x, origin.y), mouse_pos)
            origin, power, angle = Arrow.get_components(self.player.pos, target)
            preview = Arrow.get_flight_path(origin, power, angle)
            for point in preview:
                pygame.draw.circle(screen, (50,50,50), camera.t_world_to_screen_pos(point), 2)

        # camera.debug_draw(screen)

pygame.init()

def transform_pos(pos: tuple or Vector2):
    """
    Transforms real pixels to pixels in [500, 500] space? Find a better description
    """
    global rWidth, rHeight
    if isinstance(pos, tuple):
        xPercent = pos[0] / rWidth
        yPercent = pos[1] / rHeight
    elif isinstance(pos, Vector2):
        xPercent = pos.x / rWidth
        yPercent = pos.y / rHeight

    return (xPercent * WIDTH, yPercent * HEIGHT)

def resize_aa(surf, size):
	    """
        Shrinks sprite by 1/2
	    Anti-aliasing by average of color code in four pixels
	    with subsequent use of the average in a smaller surface
	    """
	    new_surf = pygame.surface.Surface((size//2, size//2))

	    for j in range(0, size, 2):

	        for i in range(0, size, 2):

	            r1, g1, b1, a1 = surf.get_at((i, j))

	            r2, g2, b2, a2 = surf.get_at((i+1, j))

	            r3, g3, b3, a3 = surf.get_at((i, j+1))

	            r4, g4, b4, a4 = surf.get_at((i+1, j+1))

	 

	            r = (r1 + r2 + r3 + r4) / 4

	            g = (g1 + g2 + g3 + g4) / 4

	            b = (b1 + b2 + b3 + b4) / 4

	 

	            new_surf.set_at((i//2, j//2), (r, g, b, 255))

	    new_size = size // 2
	    return new_surf, new_size

def resize(w, h):
    global rWidth, rHeight, realScreen
    rWidth = w
    rHeight = h
    SIZE = (w, h)
    realScreen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
    # TODO: implement this later

def render():
    screen.fill(bgCol)
    pages[state].render(screen, camera)

def handle_input(events):
    for event in events:
        if event.type == pygame.QUIT:
            global run
            run = False
        elif event.type == pygame.VIDEORESIZE:
            resize(event.w, event.h)
    
    pages[state].handle_input(events)


WIDTH = 500 
HEIGHT = 500
rWidth = 500    # Real width
rHeight = 500   # Real height
SIZE = (WIDTH, HEIGHT)
FPS = 120
realScreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
screen = Surface((WIDTH, HEIGHT))
screen.convert_alpha()
clock = pygame.time.Clock()
state = 0

fonts = {
    "title": get_font(WIDTH),
    "button": get_font(WIDTH, 15)
}




# GAME VARS
# TODO : Make camera size do something
camera = Camera(0,0, [500,500])
# pages = [MainMenuPage(), GamePage()]
pages = [GamePage()]

run = True
while run:
    # delta = clock.tick() / 1000 # Used for stress testing
    delta = clock.tick(FPS) / 1000 # Capped FPS
    events = pygame.event.get()
    handle_input(events)

    pages[state].update(delta)

    render()

    # Draw and scale screen to real screen size
    pygame.transform.scale(screen, (rWidth, rHeight), realScreen)

    pygame.display.flip()
pygame.quit()