import pygame
from pygame.locals import *
from constants import *
import globals

WIDTH=100
HEIGHT=100
HITBOX_WIDTH = 60
HITBOX_HEIGHT = 100

ASSET_SIZE = 48

JUMP_POWER=12

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        #Aqui si explico lo de las animaciones.
        #Aqui definimos cosas simples, que estamos en la animacion 'run',
        #un diccionario que contendra el detalle de las animaciones,
        #y otro que indica, por cada una, un 'tipo'.
        #continuous: Se repite, o 'loopea'. once: No lo hace (e.g. para brincar)
        #que se queda en el ultimo frame como 'cayendo'
        self.current_animation = "run"
        self.animations = {}
        self.animation_behaviour = {
            "run": "continuous",
            "jump": "once",
            "doublejump": "once"
        }

        self.load_assets()
        
        #Indice del frame de la animacion
        self.idxAnimation = 0
        self.animationSpeed = .15
        self.surf = self.animations[self.current_animation][self.idxAnimation]
        self.surf = pygame.transform.scale(self.surf, (WIDTH,HEIGHT))
        self.rect = self.surf.get_rect()
        self.update_hitbox()
        self.update_mask()
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(100, 300)
        self.acc = pygame.math.Vector2(0, .022)

        #Cuantas veces has brincado
        self.jumpCount=0
        self.canJump = False
        self.doJump = False
        self.wantedToJump = False
        self.wantToJumpTime = -1
        self.lastJumpTime = pygame.time.get_ticks()
        #Cosas para mejorar el manejo de brincos (e.g. si quisiste brincar un poquito)
        #antes de tocar el suelo, al tocarlo brinca automaticamente, etc
        self.timeToHonorJumpAttempt = 100
        self.dead = False
        self.addScore = 0
        self.colliding_with_floor = False
        self.shield = True
        self.shieldSurf = pygame.image.load("my-sprites/shield-big.png")
        self.shieldSurf = pygame.transform.scale(self.shieldSurf, (WIDTH*1.1, HEIGHT*1.1))
        self.shieldRect = self.shieldSurf.get_rect()

        #Al salvar con el escudo, a veces te acaba de salvar y se gasta
        #un salto si lo haces sin querer, esto lo previene
        self.canOnlyJumpGoingDown = False

    #Cargar una animacion especifica en base al nombre
    #Como usamos al 'Punk', podemos usar solo las que estan en esa carpeta.
    #Toda la animacion esta en un solo PNG, asi que itera en la imagen
    #segun el ancho esperado de cada cuadro de la animacion, y lo carga
    #en self.animations[nombre]
    def load_animation(self, name):
        self.animations[name] = []
        asset = pygame.image.load("sprites/2 Punk/Punk_" + name + ".png").convert_alpha()
        width = asset.get_width()
        idx = 0
        while (idx*ASSET_SIZE < width):
            frame = pygame.Surface((ASSET_SIZE, ASSET_SIZE), pygame.SRCALPHA)
            frame.blit(asset, asset.get_rect(), Rect(idx*ASSET_SIZE, 0, ASSET_SIZE, ASSET_SIZE))
            self.animations[name].append(
                frame
            )
            idx+=1
            
    #Cargas las animaciones a usar
    def load_assets(self):
        self.load_animation("run")
        self.load_animation("jump")
        self.load_animation("doublejump")

    #Cambiar la animacion actual, reseteando el indice del frame
    def changeAnimation(self, name):
        if self.current_animation is not name:
            self.current_animation = name
            self.idxAnimation = 0

    #Brincar
    def jump(self):
        #Solo poder brincar si ya pasaron ciertos MS para evitar
        #gastar dos saltos de inmediato
        if pygame.time.get_ticks() - self.lastJumpTime < 100:
            return
        self.lastJumpTime = pygame.time.get_ticks()

        #Si me salvo el escudo y voy hacia arriba todavia, no permitir brincar
        if self.canOnlyJumpGoingDown and self.vel.y < 0:
            return

        #Solo brincar cuando se puede, etc
        if self.canJump:
            self.doJump = True
            self.wantedToJump = False
            if self.jumpCount == 2:
                self.canJump = False
        else:
            self.wantedToJump = True
            self.wantToJumpTime = pygame.time.get_ticks()

    #'Cancelar' el brinco para no brincar tan alto
    def cancel_jump(self):
        if self.vel.y < -3:
            self.vel.y = -3

    #Revisar colision con el piso. Para eso uso un 'hitbox', entonces
    #cambio temporalmente el rect por el hitbox, reviso usando spritecollide,
    #y luego lo regreso HOH
    def check_collisions_floor(self, spritegroup):
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, spritegroup, False)
        self.rect = oldRect
        self.colliding_with_floor = False

        if hits:
            #Ver si ponemos al jugador arriba de la plataforma (cuando le pega de lado)
            #y no esta mucho mas abajo que la plataforma, "salvandolo"...
            if self.rect.bottom - hits[0].rect.top < (ASSET_SIZE/2) and self.vel.y >= 0:
                self.vel.y = 0
                self.jumpCount=0
                self.canJump = True
                self.pos.y = hits[0].rect.top + 1
                self.changeAnimation("run")
                if self.wantedToJump:
                    self.jump()
                self.colliding_with_floor = True
        else:
            if self.jumpCount == 2:
                self.canJump = False

    #Colision con enemigos, si tengo escudo me lo quita, etc
    def check_collisions_enemies(self, enemies_group):
        hits = pygame.sprite.spritecollide(self, enemies_group, False, pygame.sprite.collide_mask)
        if hits:            
            if self.shield:
                self.shield = False
                hits[0].kill()
            else:
                self.dead = True

    #Tomar un escudo. Aqui usamos el hitbox que es mas grande a los lados y arriba
    #para agarrarlos mas facil
    def check_collisions_shields(self, group):
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = oldRect
        if hits:
            for hit in hits:
                self.shield = True
                self.addScore += 5
                hit.kill()

    #Tomar dinero. Aqui usamos el hitbox que es mas grande a los lados y arriba
    #para agarrarlos mas facil
    def check_collisions_powerups(self, group):
        oldRect = self.rect
        self.rect = self.hitbox
        hits = pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_rect_ratio(1))
        self.rect = oldRect
        if hits:
            for hit in hits:
                self.addScore += 10
                hit.kill()      

    #En cada frame del juego se llama esto para cambiar el cuadro de la animacion
    #y revisar si se va a repetir (continuous) o si nos quedamos en la ultima y ya
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
        self.update_hitbox()
        self.update_mask()

    def update(self, delta_time, collision_floor_group, collision_group_powerups, collision_group_enemies, collision_group_shields):
        self.check_collisions_floor(collision_floor_group)
        self.check_collisions_powerups(collision_group_powerups)
        self.check_collisions_enemies(collision_group_enemies)
        self.check_collisions_shields(collision_group_shields)

        if self.dead:
            return

        self.animate(delta_time)

        now = pygame.time.get_ticks()

        if self.wantedToJump and now - self.wantToJumpTime > self.timeToHonorJumpAttempt:
            self.wantedToJump = False

        if self.doJump:
            #Si no esta en el piso, ya "gastamos" un salto
            #esto es un tema cuando vas rapido y brincas
            #al final de la plataforma
            if self.jumpCount == 0 and not self.colliding_with_floor:
                self.jumpCount += 1

            if self.jumpCount == 0:
                self.vel.y = JUMP_POWER * -1
                self.changeAnimation("jump")
            elif self.jumpCount == 1:
                self.vel.y = JUMP_POWER * -1 * .8
                self.changeAnimation("doublejump")
            self.jumpCount += 1
            self.doJump = False

        #Gravedad
        self.vel += self.acc * delta_time
        self.pos += self.vel

        #Nos fuimos hasta abajo? Escudo = Salvar. No escudo = MORIR
        if self.rect.top > SCREEN_HEIGHT:
            if self.shield:
                self.shield = False
                self.pos.y = 50
            else:
                self.dead = True

        self.rect.midbottom = self.pos
        self.update_hitbox()
        self.update_mask()
        self.update_shield()
        
        if self.canOnlyJumpGoingDown and self.vel.y > 0:
            self.canOnlyJumpGoingDown = False
            
    #El escudo nos debe salvar de morir cayendo hacia abajo
    #Se hace un megasalto automatico
    def shield_save(self):
        if self.shield:
            self.shield = False
            self.canOnlyJumpGoingDown = True
            self.vel.y = JUMP_POWER * -1.5
            self.pos.y -= 20
            self.jumpCount = 0
            self.canJump = True
            self.changeAnimation("jump")
        else:
            self.dead = True

    def update_shield(self):
        self.shieldRect.center = (
            self.rect.center[0]-20,
            self.rect.center[1]+10,
        )

    #HITBOX para colisiones con el piso, dinero, escudos
    #Aumento .1 de ancho con cada game_speed
    def update_hitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.x * 1 + (.1 * globals.game_speed), self.rect.y,
            HITBOX_WIDTH, HITBOX_HEIGHT
        )
    
    #MASK (mascara) para colisiones con enemigos (un poco mas pequenas que
    # el jugador para que sea mas 'justo' o 'facil')
    def update_mask(self):
        self.maskSurface = self.surf
        self.maskSurface = pygame.transform.scale(self.maskSurface, (WIDTH*.8,HEIGHT*.8))
        self.mask = pygame.mask.from_surface(self.maskSurface)

    #Mostrar el hitbox en pantalla, para debug
    def display_hitbox(self):
        debugRect = pygame.Surface((self.hitbox.width,self.hitbox.height))
        debugRect.set_alpha(128)
        debugRect.fill((255,0,0))
        pygame.display.get_surface().blit(debugRect, (self.hitbox.x, self.hitbox.y))