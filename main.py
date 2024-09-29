from config import *
from Tetris import *
import sys
import pygame as pg


class Juego:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris")
        self.pantalla = pg.display.set_mode(WIN_RES)  # Configura la pantalla del juego.
        self.reloj = pg.time.Clock()
        self.timer()
        self.Tetris = Tetris(self)  # Inicializa la instancia de Tetris.
        self.text = Text(self)

    def timer(self):
        self.user_event=pg.USEREVENT + 0
        self.fast_user_event=pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, INTERVALO_TIEMPO)
        pg.time.set_timer(self.fast_user_event, INTERVALO_X2)

    def update(self):
        self.Tetris.update()  # Actualiza el estado del juego (piezas, colisiones, etc.).
        self.reloj.tick(FPS)  # Limita la velocidad de fotogramas del juego.

    def draw(self): 
        self.pantalla.fill(color=BG_COLOR)  # Rellena la pantalla con el color de fondo.
        self.pantalla.fill(color=COLOR_FONDO, rect=(0,0,*FIELD_RES))
        self.Tetris.draw()  # Dibuja los elementos del juego (piezas, campo, etc.).
        self.text.draw()  # Dibuja los textos en la pantalla.
        pg.display.flip()  # Actualiza la pantalla.

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()  # Cierra la aplicación si se presiona ESC o se cierra la ventana.
            elif event.type == pg.KEYDOWN:
                self.Tetris.control(pressed_key=event.key)  # Controla las acciones de las teclas.
            elif event.type == self.user_event:
                self.anim_trigger= True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger= True
                
    def run(self):
        while True:
            self.check_events()  # Verifica eventos del usuario.
            self.update()  # Actualiza el juego.
            self.draw()  # Dibuja en la pantalla.

# Punto de entrada del programa.
if __name__ == "__main__":
    app = Juego()  # Crea una instancia del juego.
    app.run()  # Inicia el bucle principal del juego.
