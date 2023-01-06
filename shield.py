import pygame
from pygame.locals import *
import globals
from constants import *
import random

WIDTH=48
HEIGHT=48

class Shield(pygame.sprite.Sprite):

    def __init__(self):
        super(Shield, self).__init__()

        self.surf = pygame.image.load("my-sprites/shield-small.png")
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(
            SCREEN_WIDTH, 
            random.randrange(int(SCREEN_HEIGHT*.5), int(SCREEN_HEIGHT*.8))
        )
        self.speed = random.randrange (2,4) / 10

    def update(self, delta_time):
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        if (self.rect.x + WIDTH) < 0:
            self.kill()

    #Mostrar el hitbox, para debug
    def display_hitbox(self, dest):
        debugRect = pygame.Surface((self.rect.width,self.rect.height))
        debugRect.set_alpha(128)
        debugRect.fill((0,255,0))
        pygame.display.get_surface().blit(debugRect, (self.rect.x, self.rect.y))