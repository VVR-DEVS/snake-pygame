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

    def update(self):

        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = (self.snake[i-1][0], self.snake[i-1][1])

        if self.direction == 'left':
            self.snake[0] = (self.snake[0][0] - TILESIZE, self.snake[0][1])
        elif self.direction == 'right':
            self.snake[0] = (self.snake[0][0] + TILESIZE, self.snake[0][1])
        elif self.direction == 'up':
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - TILESIZE)
        else:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + TILESIZE)

    def change_direction(self, move):
        if self.direction == 'up' and move is 'down':
            return
        if self.direction == 'down' and move is 'up':
            return
        if self.direction == 'right' and move is 'left':
            return
        if self.direction == 'left' and move is 'right':
            return
        self.direction = move
