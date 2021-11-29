import pygame as pg
from Settings import *


class Snake:

    def __init__(self, pos, idPlayer=None):
        self.id = idPlayer
        self.pos = pos
        self.snake = [(pos.x * TILESIZE, pos.y * TILESIZE), ((pos.x - 1) * TILESIZE, pos.y * TILESIZE),
                      ((pos.x - 3) * TILESIZE, pos.y * TILESIZE)]
        self.snake_skin = pg.Surface((TILESIZE, TILESIZE))
        if not idPlayer:
            self.snake_skin.fill((255, 0, 0))
        else:
            self.snake_skin.fill((0, 255, 0))

        self.up = 0
        self.down = 1
        self.right = 2
        self.left = 3
        self.direction = self.up

    def update(self):

        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])

        if self.direction == 'left':
            self.snake[0] = (self.snake[0][0] - TILESIZE, self.snake[0][1])
        elif self.direction == 'right':
            self.snake[0] = (self.snake[0][0] + TILESIZE, self.snake[0][1])
        elif self.direction == 'up':
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - TILESIZE)
        else:
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + TILESIZE)

        self.pos.set(self.snake[0][0], self.snake[0][1])

        # print('Position >> ', self.snake[0])

    def change_direction(self, move):

        if self.direction == 'up' and move == 'down':
            return
        if self.direction == 'down' and move == 'up':
            return
        if self.direction == 'right' and move == 'left':
            return
        if self.direction == 'left' and move == 'right':
            return
        self.direction = move

    def set_position(self, pos):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = (self.snake[i - 1][0], self.snake[i - 1][1])

        self.snake[0] = (int(pos.x), int(pos.y))
        self.pos.set(self.snake[0][0], self.snake[0][1])
