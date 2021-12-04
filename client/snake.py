import pygame as pg
from utils.settings import *


class Snake:
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

    def __init__(self, pos, id_player=None):
        self.id = id_player
        self.pos = pos
        self.body = self.generate_body(3, pos, self.LEFT)
        self.snake_skin = pg.Surface((TILESIZE, TILESIZE))
        if not id_player:
            self.snake_skin.fill((255, 0, 0))
        else:
            self.snake_skin.fill((0, 255, 0))
        self.direction = self.UP

    def generate_body(self, size, pos, direction):
        if direction == self.UP:
            return [(pos.x, pos.y + i) for i in range(size)]
        elif direction == self.DOWN:
            return [(pos.x, pos.y - i) for i in range(size)]
        elif direction == self.LEFT:
            return [(pos.x - i, pos.y) for i in range(size)]
        elif direction == self.RIGHT:
            return [(pos.x + i, pos.y) for i in range(size)]

    def draw(self, bildschirm):
        for pos in self.body:
            bildschirm.blit(self.snake_skin, pos * TILESIZE)

    def update(self):  # TODO: Adaptar Coordenadas para não trabalhar com TALESIZE, WIDTH
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        if self.direction == self.LEFT:
            if self.body[0][0] == 0:
                self.body[0] = (WIDTH - TILESIZE, self.body[0][1])
            else:
                self.body[0] = (self.body[0][0] - TILESIZE, self.body[0][1])
        elif self.direction == self.RIGHT:
            if self.body[0][0] == WIDTH - TILESIZE:
                self.body[0] = (0, self.body[0][1])
            else:
                self.body[0] = (self.body[0][0] + TILESIZE, self.body[0][1])
        elif self.direction == self.UP:
            if self.body[1][1] == 0:
                self.body[0] = (self.body[0][0], HEIGHT - TILESIZE)
            else:
                self.body[0] = (self.body[0][0], self.body[0][1] - TILESIZE)
        else:
            if self.body[1][1] == HEIGHT - TILESIZE:
                self.body[0] = (self.body[0][0], 0)
            else:
                self.body[0] = (self.body[0][0], self.body[0][1] + TILESIZE)

        self.pos.set(self.body[0][0], self.body[0][1])

    def change_direction(self, move):

        if self.direction == Snake.UP and move == Snake.DOWN:
            return
        if self.direction == Snake.DOWN and move == Snake.UP:
            return
        if self.direction == Snake.RIGHT and move == Snake.LEFT:
            return
        if self.direction == Snake.LEFT and move == Snake.RIGHT:
            return
        self.direction = move

    def set_position(self, pos):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        self.body[0] = (int(pos.x), int(pos.y))
        self.pos.set(self.body[0][0], self.body[0][1])

    def enemy_set_position(self, body_pos):
        self.body = body_pos

    def snake_body_pos(self):
        body_pos = ''
        for i in self.body:
            body_pos += f'{i[0]},{i[1]}-'  # '0,1-1,1-2,1-'
        print('Snake().snake_body_pos:', body_pos)
        return body_pos

    def __str__(self):
        body_pos = ''
        for i in self.body:
            body_pos += f'{i[0]},{i[1]}-'  # '0,1-1,1-2,1-'
        return body_pos
