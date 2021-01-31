import pygame as pg
from Settings import *

class Snake:

    def __init__(self):

        self.snake = [(11 * TILESIZE, 10 * TILESIZE), (10 * TILESIZE, 10 * TILESIZE), (9 * TILESIZE, 10 * TILESIZE)]
        self.snake_skin = pg.Surface((TILESIZE, TILESIZE))
        self.snake_skin.fill((255, 0, 0))

        self.up = 0
        self.down = 1
        self.right = 2
        self.left = 3
        self.direction = self.up

    def update(self, move):
        if move == 'left':
            pass
        elif move == 'right':
            pass
        elif move == 'up':
            pass
        else:
            pass

