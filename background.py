import pygame
from constants import *

ASSET_WIDTH = 576
ASSET_HEIGHT = 324

"""
Esta clase Background (Fondo) puede inicializarse varias veces, segun
las 'capas' de paralaje que se quieren.

Una normalmente tendra add_background en true para agregar el fondo gris, y 
el resto en false para solo agregar los edificios.

Se especifica la velocidad (debe variar para que se vea el paralaje),
file_num define el numero de archivo dentro de cada una de las 8
carpetas que se va a cargar, y y_offset es para que por ejemplo
los edificios de mas adelante se vean mas abajo y los de atras un poco mas arriba
bla bla
"""
class Background(pygame.sprite.Sprite):
    def __init__(self, add_background, speed, file_num, y_offset):
        super(Background, self).__init__()

        self.add_background = add_background
        self.speed = speed
        self.y_offset = y_offset
        self.file_num = file_num
        if (self.add_background):
            self.background_surf = pygame.image.load("sprites/1 Backgrounds/1/Night/1.png").convert_alpha()
            self.background_surf = pygame.transform.scale(self.background_surf, (SCREEN_WIDTH,self.background_surf.get_height()))
            self.background_rect = self.background_surf.get_rect()
            self.background_rect.y = SCREEN_HEIGHT - self.background_rect.height

        self.surfaces = []
        self.rects = []
        self.positions = []

        self.load_assets()
        self.setup_assets()

    #Cargar los assets. Espera que la carpeta se llame de cierta manera, que haya
    #8 subcarpetas, etc. tal cual como se muestra en el video
    #Guarda surfaces, rects y posiciones en arreglos para tener todo
    def load_assets(self):
        dir = "sprites/1 Backgrounds/"
        for i in range(1,9):
            path = dir + str(i) + "/Night/" + str(self.file_num) + ".png"
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(surf, (ASSET_WIDTH, ASSET_HEIGHT))
            self.surfaces.append(surf)
            self.rects.append(surf.get_rect())
            self.positions.append(pygame.math.Vector2(0,0))

    #Pone la X original de todo (i * width)
    #La Y la pone con en base al offset y la altura de la imagen
    def setup_assets(self):
        for i, pos in enumerate(self.positions):
            pos.x = ASSET_WIDTH * i
            pos.y = SCREEN_HEIGHT - self.rects[i].height + self.y_offset
            self.rects[i].x = pos.x
            self.rects[i].y = pos.y

    #En cada actualizacion se reduce la X de todo
    #si ya no se ve en pantalla, lo "resetea", enviandolo de nuevo a la
    #derecha, asi uno por uno para que sean infinitos
    def update(self, delta_time):
        for i, rect in enumerate(self.rects):
            self.positions[i].x -= self.speed * delta_time
            rect.x = int(self.positions[i].x)
            if (rect.x + ASSET_WIDTH <= 0):
                self.positions[i].x = ASSET_WIDTH * len(self.rects)
                rect.x = int(self.positions[i].x)

    def render(self, dest):
        if self.add_background:
            dest.blit(self.background_surf, self.background_rect)

        for i, surface in enumerate(self.surfaces):
            dest.blit(surface, self.rects[i])

