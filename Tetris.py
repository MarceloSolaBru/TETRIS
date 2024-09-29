from config import *
import math
from Tetromino import Tetromino
import sys
import pygame.freetype as ft

# Clase que representa el juego de Tetris.
class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()  # Grupo de sprites para los bloques del tetromino.
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)  # Inicializa el tetromino actual.
        self.rapidito = False
        self.next_tetromino = Tetromino(self,current=False)  # Inicializa el siguiente tetromino.
        self.score = 0
        self.full_lines=0
        self.points={0 :0 , 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points[self.full_lines]
        self.full_lines=0

    def check_full_lines(self):
        row = FIELD_H -1 
        for y in range (FIELD_H-1,-1,-1):
            for x in range(FIELD_W):
                self.field_array[row][x]= self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos=vec(x,y)
            if sum(map(bool,self.field_array[y])) < FIELD_W:
                row -= 1
            else: 
                for x in range(FIELD_W-1,-1,-1):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x]=0
                self.full_lines += 1

    def put_tetromin_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[ 0 for x in range(FIELD_W)] for y in range (FIELD_H)]
    
    def check_landing(self):
        if self.tetromino.landing:
            if self.game_over():
                self.__init__(self.app)
            else:
                self.rapidito = False
                self.put_tetromin_in_array()
                self.next_tetromino.current = True
                self.tetromino=self.next_tetromino
                self.next_tetromino = Tetromino(self,current=False)

    def control(self, pressed_key):
        # Controla las acciones del juego cuando se presionan las teclas izquierda o derecha.
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="izq")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="der")
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.rapidito = True    

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.rapidito]
        if trigger:     # Actualiza el estado del juego.
            self.check_full_lines()
            self.tetromino.update()  # Actualiza el tetromino actual.
            self.check_landing()
            self.get_score()
        self.sprite_group.update()  # Actualiza los bloques en el grupo de sprites.
        

    def draw_grid(self):
        # Dibuja una cuadrícula en la pantalla.
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.pantalla, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def draw(self):
        # Dibuja los elementos del juego en la pantalla.
        self.draw_grid()  # Dibuja la cuadrícula.
        self.sprite_group.draw(self.app.pantalla)  # Dibuja los bloques en el grupo de sprites.

    def game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(3000)
            return True
            

class Text: 
    def __init__(self,app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.pantalla, (WIN_W*0.615, WIN_H*(0.05+0.00)), text="TETRIS", fgcolor="green",size= TILE_SIZE*1.65, bgcolor="black")
        self.font.render_to(self.app.pantalla, (WIN_W*0.67, WIN_H*(0.25+0.1)), text="NEXT", fgcolor="green",size= TILE_SIZE*1.65, bgcolor="black")
        self.font.render_to(self.app.pantalla, (WIN_W*0.64, WIN_H*(0.67+0.05)), text="SCORE", fgcolor="green",size= TILE_SIZE*1.65, bgcolor="black")
        self.font.render_to(self.app.pantalla, (WIN_W*0.64, WIN_H*(0.8+0.05)), text=f'{self.app.Tetris.score}', fgcolor="green",size= TILE_SIZE*1.65, bgcolor="black")
        