from config import *  # Importa las constantes y configuraciones desde un archivo 'config'

import random

# Define la clase 'Block' que representa un bloque individual en el juego.
class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        # Inicializa un bloque con el tetromino al que pertenece y su posición.
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetromino.tetris.sprite_group)

        # Crea una superficie (rectángulo) para representar visualmente el bloque.
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        pg.draw.rect(self.image, tetromino.color,(1,1, TILE_SIZE - 2, TILE_SIZE-2),border_radius=5)
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        # Establece la posición visual del rectángulo basado en la posición del bloque.
        pos= [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        # Actualiza la posición del rectángulo basado en la posición del bloque.
        self.set_rect_pos()
        self.is_alive()

    def collide(self, pos):
        # Comprueba si el bloque colisiona con una posición 'pos'.
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

# Define la clase 'Tetromino' que representa una pieza de tetris.
class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))  # Elige una forma aleatoria.
        self.color = random.choice(["green"])    #random.choice(["orange","green","blue","red","purple"])
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False  # Indica si la pieza ha aterrizado en la parte inferior.
        self.current = current  # Indica si la pieza es la actual.

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.collide(new_block_pos):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_pos[i]

    def collide(self, block_pos):
        # Comprueba si la pieza colisiona con las posiciones de los bloques.
        return any(map(Block.collide, self.blocks, block_pos))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_pos = [block.pos + move_direction for block in self.blocks]
        collide = self.collide(new_block_pos)

        if not collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == "down":
            self.landing=True

    def update(self):
        # Mueve la pieza hacia abajo y agrega un pequeño retardo de tiempo.
        self.move(direction="down")

