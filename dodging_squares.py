from math import cos
import pygame
import pygame.event
import pygame.display
from pygame.math import Vector2
import pygame.surface
import pygame.draw
from pygame.time import Clock
from pygame import Rect
import random

class Player(Rect):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 5
        self.color = (255,255,0)
        self.health = 100
        self.trail = []

    def update(self, keys, enemies):
        y = 0
        x = 0
        if keys[pygame.K_w]:
            y -= self.speed
        if keys[pygame.K_s]:
            y += self.speed
        if keys[pygame.K_a]:
            x -= self.speed
        if keys[pygame.K_d]:
            x += self.speed
        self.move(x, y)

        for enemy in enemies:
            if Vector2.distance_to(Vector2(self.x, self.y), Vector2(enemy.x, enemy.y)) < 100:
                self.collision(enemy)

        self.trail.insert(0, (Vector2(self.centerx, self.centery)))
        if len(self.trail) == 25:
            self.trail.pop()
    
    def render(self, screen):

        trailRect = Rect(0,0,self.w/2,self.h/2)
        i = 0
        for element in list(self.trail.__reversed__()):
            trailRect.x = element.x - trailRect.w/2
            trailRect.y = element.y - trailRect.h/2
            alpha = 255 - (i / 25) * 255
            pygame.draw.rect(screen, (255-alpha, 255-alpha, 0), trailRect)
            i+=1
        pygame.draw.rect(screen, self.color, self, 3, 1)
    
    def collision(self, other: Rect):
        if self.colliderect(other):
            self.health -= 0.5

    def move(self, x, y):
        if not (self.y + self.h +  y > HEIGHT or self.y + y < 0):
            self.y += y
        if not (self.x + self.w +  x > WIDTH or self.x + x < 0):
            self.x += x
        

class Enemy(Rect):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alive: bool = True

        xvel = random.randrange(-4, 4)
        yvel = random.randrange(-4, 4)
        self.vel: Vector2 = Vector2(xvel, yvel)
        self.vel.scale_to_length(4)
    
    def update(self):
        self.x += self.vel.x
        self.y += self.vel.y

        # self.vel.x += cos(self.x) * 0.4
        # self.vel.y += cos(1-self.y) * 0.4

        if self.bottomright[0] > WIDTH or self.x < 0:
            self.vel.x *= -1
        if self.bottomright[1] > HEIGHT or self.y < 0:
            self.vel.y *= -1

    def render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self, 3, 1)

    def __str__(self):
        return f"Enemy @ ({self.x}, {self.y})"

def handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
    return True

def update(keys):
    player.update(keys, enemies)

    for enemy in enemies:
        enemy.update()

def on_screen(rect):
    if rect.x < 0 or rect.x + rect.w > WIDTH:
        return False
    if rect.y < 0 or rect.y + rect.h > HEIGHT:
        return False
    return True

# RENDER METHODS

def render():
    render_enemies(enemies)
    player.render(screen)
    render_ui(player.health)

def render_enemies(enemies: list[Enemy]):
    for enemy in enemies:
        if(on_screen(enemy)):
            enemy.render(screen)

def render_ui(player_health):
    # Health bar
    pygame.draw.rect(screen, (125,125,125), Rect(25, 25, 100, 25))
    health = player_health / 100
    # print(health)
    pygame.draw.rect(screen, (125,255,125), Rect(26, 26, 98 * health, 23))

pygame.init()

WIDTH = 640
HEIGHT = 480
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
clock = Clock()


# GAME VARS
player = Player(0,0,100,100)
enemy = Enemy(150,150,25,25)
enemies: list[Enemy] = []
enemies.append(enemy)

while run:
    clock.tick(FPS)
    run = handle_events(pygame.event.get())

    keys = pygame.key.get_pressed()

    update(keys)

    screen.fill((0,0,0))

    render()

    pygame.display.flip()

    