import pygame
from constants import *
import globals
import random

platform_height=64
tile_width=64
tile_height=64

"""
Esto de las plataformas esta gracioso.
Tenemos muchas plataformas con distinto arte.
Algunas tienen continuidad hacia abajo, y otras no (son 'flotantes')
Las cargo e indico distintos sprites para cuando es uno solo (unique),
pero si es mas de 1, tenemos 'beginning', 'middle' y 'end'.
Los que dicen _bottom es para cuando continuan hacia abajo en lugar de flotar
"""
class GamePlatform(pygame.sprite.Sprite):
    def __init__(self, tileNumber, x):
        super(GamePlatform, self).__init__()

        width = tileNumber * tile_width
        self.height = random.randint(16,256)
        self.surf = pygame.Surface((width, self.height), pygame.SRCALPHA)

        tiles = []
        tiles.append({
            "unique": "IndustrialTile_25.png",
            "beginning": "IndustrialTile_04.png",
            "middle": "IndustrialTile_05.png",
            "end": "IndustrialTile_06.png",
            "beginning_bottom": "IndustrialTile_13.png",
            "middle_bottom": "IndustrialTile_14.png",
            "end_bottom": "IndustrialTile_15.png"
        })
        tiles.append({
            "unique": "IndustrialTile_81.png",
            "beginning": "IndustrialTile_81.png",
            "middle": "IndustrialTile_81.png",
            "end": "IndustrialTile_81.png"
        })
        tiles.append({
            "unique": "IndustrialTile_52.png",
            "beginning": "IndustrialTile_31.png",
            "middle": "IndustrialTile_32.png",
            "end": "IndustrialTile_33.png",
            "beginning_bottom": "IndustrialTile_40.png",
            "middle_bottom": "IndustrialTile_41.png",
            "end_bottom": "IndustrialTile_42.png"
        })
        
        #Tomar un indice randomio
        tile_idx = random.randrange(len(tiles))

        platformImageSurf_unique = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["unique"]).convert_alpha()
        platformImageSurf_beginning = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["beginning"]).convert_alpha()
        platformImageSurf_middle = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["middle"]).convert_alpha()
        platformImageSurf_end = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["end"]).convert_alpha()
        platformImageSurf_beginning_bottom = None
        platformImageSurf_middle_bottom = None
        platformImageSurf_end_bottom = None

        #Tiene continuidad hacia abajo? (es decir, no es flotante)
        if "beginning_bottom" in tiles[tile_idx]:
            platformImageSurf_beginning_bottom = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["beginning_bottom"]).convert_alpha()
            platformImageSurf_middle_bottom = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["middle_bottom"]).convert_alpha()
            platformImageSurf_end_bottom = pygame.image.load("sprites/1 Tiles/" + tiles[tile_idx]["end_bottom"]).convert_alpha()

        platformImageSurf_unique = pygame.transform.scale(platformImageSurf_unique, (tile_width,tile_height))
        platformImageSurf_beginning = pygame.transform.scale(platformImageSurf_beginning, (tile_width,tile_height))
        platformImageSurf_middle = pygame.transform.scale(platformImageSurf_middle, (tile_width,tile_height))
        platformImageSurf_end = pygame.transform.scale(platformImageSurf_end, (tile_width,tile_height))
        if "beginning_bottom" in tiles[tile_idx]:
            platformImageSurf_beginning_bottom = pygame.transform.scale(platformImageSurf_beginning_bottom, (tile_width,tile_height))
            platformImageSurf_middle_bottom = pygame.transform.scale(platformImageSurf_middle_bottom, (tile_width,tile_height))
            platformImageSurf_end_bottom = pygame.transform.scale(platformImageSurf_end_bottom, (tile_width,tile_height))

        if tileNumber == 1:
            #Si solo es uno, poner la version 'unique'
            self.surf.blit(platformImageSurf_unique, (0, 0))
        else:
            #No es solo uno, ir a la logica divertida
            tileX=0
            idx=0
            while True:
                if idx == 0:
                    #El primero siempre es _beginning
                    self.surf.blit(platformImageSurf_beginning, (tileX, 0))
                elif tileX + tile_width >= width:
                    #El ultimo siempre es _end
                    self.surf.blit(platformImageSurf_end, (tileX, 0))
                else:
                    #Los de enmedio siempre seran 'middle'
                    self.surf.blit(platformImageSurf_middle, (tileX, 0))

                if self.height > tile_height and "beginning_bottom" in tiles[tile_idx]:
                    #Si hay continuidad hacia abajo, misma logica para pintar los de
                    #abajo y que no 'flote' la plataforma
                    currentY = tile_height
                    while currentY < self.height:
                        if idx == 0:
                            self.surf.blit(platformImageSurf_beginning_bottom, (tileX, currentY))
                        elif tileX + tile_width >= width:
                            self.surf.blit(platformImageSurf_end_bottom, (tileX, currentY))
                        else:
                            self.surf.blit(platformImageSurf_middle_bottom, (tileX, currentY))
                        currentY += tile_height

                tileX += tile_width
                if tileX > width:
                    break
                idx += 1
        
        #Ya lo demas no tiene chiste
        self.pos = pygame.math.Vector2(x, SCREEN_HEIGHT-self.height)

        self.rect = self.surf.get_rect(
            topleft=(x, self.pos.y)
        )
        self.speed = .2

        self.surf = self.surf.convert_alpha()

    def update(self, delta_time):
        self.pos.x -= self.speed * globals.game_speed * delta_time
        self.rect.topleft = self.pos