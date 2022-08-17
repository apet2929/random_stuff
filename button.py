import os
import pygame
import pygame.font
from pygame.sprite import Sprite
import pygame.image

pygame.init()

class Button(Sprite):
    def __init__(self, x, y, w, h, text=None) -> None:
        super().__init__()
        img =  pygame.image.load("button.png") 
        self.image = img
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.font = pygame.font.SysFont('Courier', 25, False)
        yee = pygame.Rect(0,0,0,0)
        self.onClick = None

    def setOnClick(self, func):
        self.onClick = func

    def onClick(self):
        if self.onClick is not None:
            self.onClick()
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.text is not None:
            textRect = pygame.rect.Rect(self.rect.x + self.rect.w/4, self.rect.y + self.rect.h/4, self.rect.w, self.rect.h)
            screen.blit(self.font.render(self.text, False, (0,0,0)), textRect)
            

btn = Button(0,0,100,100)

            
    
