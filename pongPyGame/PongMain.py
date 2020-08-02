
# Importacion de los módulos
import pygame
from pygame.locals import *
import os
import sys

# ----------------------------------------------
# Constantes, como anchos y largo de pantalla, etc.
# ----------------------------------------------
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "img"
SONIDO_DIR = "sound"

# ----------------------------------------------
# Clases y Funciones utilizadas
# ----------------------------------------------

def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido:", ruta)
        sonido = None
    return sonido

# -----------------------------------------------
# Creamos los sprites de los objetos del juego:
# -----------------------------------------------

class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"

    def __init__(self, sonido_golpe, sonido_punto):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [3, 3]
        self.sonido_golpe = sonido_golpe
        self.sonido_punto = sonido_punto

    def update(self, marcadorJ1, marcadorJ2):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
            self.sonido_punto.play()  # Reproducir sonido de punto
            if self.rect.left < 0:
                marcadorJ2 += 1
            else:
                marcadorJ1 += 1
            self.rect.centerx = SCREEN_WIDTH / 2.0
            self.rect.centery = SCREEN_HEIGHT / 2.0

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
        
        return marcadorJ1,marcadorJ2

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0] = -self.speed[0]
            self.sonido_golpe.play()  # Reproducir sonido de rebote

class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT / 2.0

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

    def cpu(self, pelota):
        self.speed = [0, 2.5]
        if pelota.speed[0] >= 0 and pelota.rect.centerx >= SCREEN_WIDTH / 2:
            if self.rect.centery > pelota.rect.centery:
                self.rect.centery -= self.speed[1]
            if self.rect.centery < pelota.rect.centery:
                self.rect.centery += self.speed[1]
    #Perfect cpu
    #def cpu(self, objetivo):
    #    self.rect.centery = objetivo.rect.centery
    #    if self.rect.bottom >= SCREEN_HEIGHT:
    #        self.rect.bottom = SCREEN_HEIGHT
    #    elif self.rect.top <= 0:
    #        self.rect.top = 0

# ------------------------------
# Funcion principal del juego
# ------------------------------

def main():
    pygame.init()
    pygame.mixer.init()
    # Contiene principalmente loop del juego (el alma de este)
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong PyGame by July")

    # se define la letra por defecto
    fuente = pygame.font.Font(None, 20)

    # cargamos el fondo y los objetos
    fondo = load_image("fondo_pong.jpg", IMG_DIR, alpha=False)
    sonido_golpe = load_sound("golpeo.ogg", SONIDO_DIR)
    sonido_punto = load_sound("punto.ogg", SONIDO_DIR)

    bola = Pelota(sonido_golpe, sonido_punto)
    jugador1 = Paleta(40)
    jugador2 = Paleta(SCREEN_WIDTH - 40)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    # Variables de marcador
    marcadorJ1 = 0
    marcadorJ2 = 0

     # el bucle principal del juego
    while True:
        clock.tick(60)
        # Obtenemos la posicon del mouse
        pos_mouse = pygame.mouse.get_pos()
        mov_mouse = pygame.mouse.get_rel()

        # Actualizamos los obejos en pantalla
        jugador1.humano()
        jugador2.cpu(bola)
        marcadorJ1,marcadorJ2 = bola.update(marcadorJ1, marcadorJ2)

        # Comprobamos si colisionan los objetos
        bola.colision(jugador1)
        bola.colision(jugador2)

        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    jugador1.rect.centery -= 5
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 5
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador1.rect.centery += 0
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 0
            # Si el mouse no esta quieto mover la paleta a su posicion
            elif mov_mouse[1] != 0:
                jugador1.rect.centery = pos_mouse[1]

        text = "                     Jugador 1:  %d                                                               Jugador 2:  %d" % (marcadorJ1,marcadorJ2)
        mensaje = fuente.render(text, 1, (255, 255, 255))

        # actualizamos la pantalla
        #screen.fill((30, 0, 255))
        screen.blit(fondo, (0, 0))
        screen.blit(mensaje, (15, 5))
        pygame.draw.line(screen, (255, 255, 255), (0, 25), (640, 25), 2)
        todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
        todos.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()