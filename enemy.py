import pygame
from pygame.locals import *
import globals
from constants import *
import random

WIDTH=80
HEIGHT=80

ASSET_SIZE = 48

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()

        #Lo de las animaciones es igual en todos lados.
        #lo explico en player.py
        self.current_animation = "walk"
        self.animations = {}
        self.animation_behaviour = {
            "walk": "continuous"
        }

        self.load_assets()

        self.idxAnimation = 0
        self.animationSpeed = .15
        self.surf = self.animations[self.current_animation][self.idxAnimation]
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.rect = self.surf.get_rect()
        self.pos = pygame.math.Vector2(
            SCREEN_WIDTH, 
            random.randrange(int(SCREEN_HEIGHT*.5), int(SCREEN_HEIGHT*.8))
        )
        #Velocidad aleatoria de los enemigos :)
        #TODO quiza deberia aumentar segun el game_speed hoh
        self.speed = random.randrange (2,4) / 10
        self.update_mask()

    #Lo de las animaciones es igual en todos lados.
    #lo explico en player.py
    def load_assets(self):
        self.animations["walk"] = []
        asset = pygame.image.load("sprites/City Enemies/5/Walk.png").convert_alpha()
        width = asset.get_width()
        idx = 0
        while (idx*ASSET_SIZE < width):
            frame = pygame.Surface((ASSET_SIZE, ASSET_SIZE), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(idx*ASSET_SIZE, 0, ASSET_SIZE, ASSET_SIZE))
            self.animations["walk"].append(
                frame.convert_alpha()
            )
            idx+=1

    #Lo de las animaciones es igual en todos lados.
    #lo explico en player.py
    def animate(self,delta_time):
        self.animationSpeed = .008 * delta_time
        self.idxAnimation += self.animationSpeed
        if int(self.idxAnimation)+1 >= len(self.animations[self.current_animation]):
            if self.animation_behaviour[self.current_animation] == "continuous":
                self.idxAnimation = 0
            else:
                self.idxAnimation = len(self.animations[self.current_animation])-1
        self.surf = self.animations[self.current_animation][int(self.idxAnimation)]
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.rect = self.surf.get_rect()

    #Solo moverlo a la izquierda segun la velocidad, etc
    def update(self, delta_time):
        self.animate(delta_time)
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        if (self.rect.x + WIDTH) < 0:
            self.kill()
        self.update_mask()

    #Colision se hace con mascaras, con el 90% del tamano del sprite
    def update_mask(self):
        self.maskSurface = self.surf
        self.maskSurface = pygame.transform.scale(self.maskSurface, (WIDTH*.9,HEIGHT*.9))
        self.mask = pygame.mask.from_surface(self.maskSurface)