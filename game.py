import pygame
from pygame.locals import *
import random
from player import Player
from constants import *
from background import Background
from events import *
from gameplatform import GamePlatform
from money import Money
from enemy import Enemy
from shield import Shield
import globals

#Facemesh
import cv2
import mediapipe as mp
import math
from webcam import Webcam

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("Plataformas")

        #2 fondos para manejar el paralaje. El detalle puedes leerlo
        #en background.py
        self.background1 = Background(True, .05, "2", 0)
        self.background2 = Background(False, .2, "3", 40)

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)

        #Sonidillos
        self.powerup_sound = pygame.mixer.Sound("sound/powerup.wav")
        self.powerup_sound.set_volume(.1)
        self.death_sound = pygame.mixer.Sound("sound/grunt2.wav")

        self.initialize()

    def initialize(self):
        self.player = Player()
        self.no_face = False
        self.dead = False

        self.platforms = []

        #La primera plataforma grande
        #Descomentar para tener una gigante inicial y probar cosas
        #platform = GamePlatform(2000, 0)
        platform = GamePlatform(20, 0)
        self.platforms.append(platform)
        self.difficulty = 1
        self.group_platforms = pygame.sprite.Group()
        self.group_platforms.add(platform)
        self.platformWillBeCreated = False

        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = -1

        self.score = 0
        self.text_score = None
        self.text_score_rect = None

        #powerups = el dinero. se llama asi porque segun yo iba a agregar mas pero nunca lo hice
        self.powerups = []
        self.group_powerups = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_MONEY, 1000)

        self.enemies = []
        self.group_enemies = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_ENEMY, 15000)

        self.shields = []
        self.group_shields = pygame.sprite.Group()
        pygame.time.set_timer(CREATE_NEW_SHIELD, 10000)

        #Este tiene mas detalles de webcam para mostrar solo la boca en el cuadrito
        self.webcam = Webcam().start()
        self.webcamImage=None
        self.face_left_x=0
        self.face_right_x=0
        self.face_top_y=0
        self.face_bottom_y=0
        self.mouth_left_x=0
        self.mouth_right_x=0
        self.mouth_top_y=0
        self.mouth_bottom_y=0
        self.mouthWasOpen=False

        self.max_face_area_height=0

    def update(self, delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

        if self.dead:
            for event in events:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.initialize()

        if self.dead or self.no_face:
            return

        for event in events:
            #Descomentar estos primeros 2 si quieres que la barra
            #espaciadora NO brinque
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.player.jump()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    self.player.cancel_jump()
            elif event.type == MOUTH_OPENED:
                self.player.jump()
            elif event.type == MOUTH_CLOSED:
                self.player.cancel_jump()
            elif event.type == CREATE_NEW_PLATFORM:
                self.platformWillBeCreated = False
                #Basar el tamano en la dificultad
                min = 1
                if self.difficulty <= 3:
                    min = 3
                max = 12 - self.difficulty
                if max < 4:
                    max = 4
                tileNumber = random.randrange(min, max)

                #Basar el espacio entre plataformas en la dificultad
                min_space = 90 + (self.difficulty*2)
                if min_space > 150:
                    min_space = 150
                max_space = 200 + (self.difficulty*2)
                if max_space > 350:
                    max_space = 350

                space = random.randrange(min_space, max_space)
                
                platform = GamePlatform(tileNumber, SCREEN_WIDTH + space)
                self.platforms.append(platform)
                self.group_platforms.add(platform)
            elif event.type == CREATE_NEW_MONEY:
                money = Money()
                self.powerups.append(money)
                self.group_powerups.add(money)

                #Calculos para ver cuando crear mas dinero, segun la dificultad
                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000

                #TODO al final ni los use HOHOH revisar
                pygame.time.set_timer(CREATE_NEW_MONEY, random.randint(3000, 10000))
            elif event.type == CREATE_NEW_ENEMY:
                enemy = Enemy()
                self.enemies.append(enemy)
                self.group_enemies.add(enemy)

                #Cuando crear un nuevo enemigo? Basado en la dificultad
                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000
                pygame.time.set_timer(CREATE_NEW_ENEMY, random.randint(min_time, max_time))
            elif event.type == CREATE_NEW_SHIELD:
                shield = Shield()
                self.shields.append(shield)
                self.group_shields.add(shield)
                min_time = 4000 - self.difficulty*500
                if min_time < 2000:
                    min_time = 2000
                max_time = 10000 - self.difficulty*500
                if max_time < 4000:
                    max_time = 4000

                #TODO usar min_time y max_time, ajustarlos XD
                pygame.time.set_timer(CREATE_NEW_SHIELD, random.randint(10000, 20000))

        if not self.player.dead:
            self.background1.update(delta_time)
            self.background2.update(delta_time)
            self.player.update(delta_time, self.group_platforms, self.group_powerups, self.group_enemies, self.group_shields)
            if self.player.dead or self.player.rect.top > SCREEN_HEIGHT:
                if self.player.shield:
                    #Moriste pero tienes escudo? No morir!
                    self.player.shield_save()
                else:
                    #No tenias escudo. Dead
                    self.dead = True
                    pygame.mixer.Sound.play(self.death_sound)

            if self.player.addScore > 0:
                self.score += (self.player.addScore*1000)
                self.player.addScore = 0
                pygame.mixer.Sound.play(self.powerup_sound)

            for platform in self.platforms:
                platform.update(delta_time)

            self.group_powerups.update(delta_time)
            self.group_enemies.update(delta_time)
            self.group_shields.update(delta_time)

            #Generar nueva plataforma?
            if (SCREEN_WIDTH - self.platforms[-1].rect.right > 0) and not self.platformWillBeCreated:
                self.platformWillBeCreated = True
                pygame.event.post(pygame.event.Event(CREATE_NEW_PLATFORM))

            #Hacer mas dificil
            seconds = int( (pygame.time.get_ticks() - self.start_time) / 1000)
            self.difficulty = int( 1+(seconds/10) )
            globals.game_speed = 1 + (self.difficulty*.2)

            #Score
            self.score += globals.game_speed * delta_time
            self.text_score = self.font.render('Score: ' + str(int(self.score/1000)), True, (255,255,255))
            self.text_score_rect = self.text_score.get_rect()
            self.text_score_rect.y = 10
            self.text_score_rect.x = (SCREEN_WIDTH//2) - (self.text_score_rect.width//2)

    def render(self):
        self.screen.fill((92, 89, 92))

        #Fondo
        self.background1.render(self.screen)
        self.background2.render(self.screen)

        if self.webcam.lastFrame is not None:
            self.render_camera()

        #Plataformas
        for platform in self.platforms:
            self.screen.blit(platform.surf, platform.rect)

        self.screen.blit(self.player.surf, self.player.rect)
        if (self.player.shield):
            self.screen.blit(self.player.shieldSurf, self.player.shieldRect)

        for powerup in self.group_powerups:
            self.screen.blit(powerup.surf, powerup.rect)
        for enemy in self.group_enemies.sprites():
            self.screen.blit(enemy.surf, enemy.rect)
        for shield in self.group_shields:
            self.screen.blit(shield.surf, shield.rect)

        if self.text_score is not None:
            self.screen.blit(self.text_score, self.text_score_rect)
            
        if self.dead:
            self.dead = self.font.render('GAME OVER :(', True, (255,255,255), (0,0,0))
            dead_rect = self.dead.get_rect()
            dead_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(self.dead, dead_rect)
            self.retry = self.smaller_font.render('Presiona enter para reintentar', True, (200,200,200), (0,0,0))
            retry_rect = self.retry.get_rect()
            retry_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 40)
            self.screen.blit(self.retry, retry_rect)

        pygame.display.flip()

    def render_camera(self):
        webcamImageSurface = pygame.image.frombuffer(self.webcamImage, (int(self.webcam.width()), int(self.webcam.height())), "BGR")

        #Mostrar la boca
        self.mouth_left_x = self.mouth_left_x - .03
        if self.mouth_left_x < 0:
            self.mouth_left_x = 0
        self.mouth_right_x = self.mouth_right_x + .03
        if self.mouth_right_x > 1:
            self.mouth_right_x = 1

        self.mouth_top_y = self.mouth_top_y - .03
        if self.mouth_top_y < 0:
            self.mouth_top_y = 0
        self.mouth_bottom_y = self.mouth_bottom_y + .03
        if self.mouth_bottom_y > 1:
            self.mouth_bottom_y = 1
        mouthRect = pygame.Rect(
            int(self.mouth_left_x*self.webcam.width()),
            int(self.mouth_top_y*self.webcam.height()), 
            int(self.mouth_right_x*self.webcam.width()) - int(self.mouth_left_x*self.webcam.width()),
            int(self.mouth_bottom_y*self.webcam.height()) - int(self.mouth_top_y*self.webcam.height())
        )
        onlyMouthSurface = pygame.Surface((
            int(self.mouth_right_x*self.webcam.width()) - int(self.mouth_left_x*self.webcam.width()),
            int(self.mouth_bottom_y*self.webcam.height()) - int(self.mouth_top_y*self.webcam.height())
        ))

        onlyMouthSurface.blit(webcamImageSurface, (0,0), mouthRect)
        mouth_ratio = onlyMouthSurface.get_rect().height / onlyMouthSurface.get_rect().width

        mouth_area_width = 100
        mouth_area_height = 50
        onlyMouthSurface = pygame.transform.scale(onlyMouthSurface, (int(mouth_area_width),int(mouth_area_height)))
        self.screen.blit(onlyMouthSurface, onlyMouthSurface.get_rect())

    def loop(self):
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            refine_landmarks=True
        ) as self.face_mesh:
            while self.running:
                if not self.webcam.ready():
                    continue
                time = pygame.time.get_ticks()
                if self.last_frame_time == -1:
                    delta_time = 1
                else:
                    delta_time = time - self.last_frame_time

                self.last_frame_time = time
                self.process_camera()
                self.update(delta_time)
                self.render()
                self.clock.tick(60)
            pygame.quit()

    def process_camera(self):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(image)
            self.webcamImage = image
            if results.multi_face_landmarks is not None:
                self.no_face = False
                for face_landmarks in results.multi_face_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image,
                        face_landmarks,
                        self.mp_face_mesh.FACEMESH_CONTOURS,
                        self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                        self.mp_drawing.DrawingSpec(color=(150, 150, 150), thickness=1))

                    #Coordenadas del cuadro de la cara y de la boca
                    self.face_left_x = face_landmarks.landmark[234].x
                    self.face_right_x = face_landmarks.landmark[454].x
                    self.face_top_y = face_landmarks.landmark[10].y
                    self.face_bottom_y = face_landmarks.landmark[152].y

                    self.mouth_left_x = face_landmarks.landmark[57].x
                    self.mouth_right_x = face_landmarks.landmark[287].x
                    self.mouth_top_y = face_landmarks.landmark[0].y
                    self.mouth_bottom_y = face_landmarks.landmark[17].y

                    top = (int(face_landmarks.landmark[10].x * self.webcam.width()), int(face_landmarks.landmark[10].y * self.webcam.height()))
                    bottom = (int(face_landmarks.landmark[152].x * self.webcam.width()), int(face_landmarks.landmark[152].y * self.webcam.height()))

                    mouth_top = (int(face_landmarks.landmark[13].x * self.webcam.width()), int(face_landmarks.landmark[13].y * self.webcam.height()))
                    mouth_bottom = (int(face_landmarks.landmark[14].x * self.webcam.width()), int(face_landmarks.landmark[14].y * self.webcam.height()))

                    distanceBetweenMouthPoints = math.sqrt( 
                        pow(mouth_top[0] - mouth_bottom[0], 2) +
                        pow(mouth_top[1] - mouth_bottom[1], 2)
                    )
                    
                    face_height = (bottom[1] - top[1])

                    #Obtener la distancia real de la boca dividida entre la cara
                    #para que sea mas 'relativamente constante'
                    real_distance = distanceBetweenMouthPoints * self.webcam.height()
                    relative_distance = real_distance / face_height

                    #Quiza deberia ser mejor calibrar esto, ya que depende
                    #del angulo de la persona vs la camara :|
                    if not self.mouthWasOpen and relative_distance > 10:
                        pygame.event.post(pygame.event.Event(MOUTH_OPENED))

                        self.mouthWasOpen = True
                    elif self.mouthWasOpen and relative_distance < 6:
                        pygame.event.post(pygame.event.Event(MOUTH_CLOSED))
                        self.mouthWasOpen = False
            else:
                self.no_face = True

            #Descomenta esto si quieres ver tu cara fea en otra ventana
            #cv2.imshow("Frame", image)
            k = cv2.waitKey(1) & 0xFF