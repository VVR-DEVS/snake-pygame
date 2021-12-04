import pygame as pg
from utils.settings import *
from utils.position import Position


class Snake:
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

    def __init__(self, pos, id_player=None):
        self.id = id_player
        self.snake_skin = pg.Surface((TILESIZE, TILESIZE))
        if id_player is None:  # vem corpo inteiro como pos (pode mudar depois pra no primeiro vir só o pos)
            self.pos = pos
            self.body = self.generate_body(3, pos, self.LEFT)
            self.snake_skin.fill((255, 0, 0))
        else:
            self.pos = pos[0]
            self.body = pos
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
        for pos in self.body:  # TODO corrigir: body de enemy está vindo como str
            bildschirm.blit(self.snake_skin, (int(pos[0]) * TILESIZE, int(pos[1]) * TILESIZE))

    def update(self):  # TODO: Adaptar Coordenadas para não trabalhar com TALESIZE, WIDTH
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        if self.direction == self.LEFT:
            if self.body[0][0] == 0:
                self.body[0] = (63, self.body[0][1])
            else:
                self.body[0] = (self.body[0][0] - 1, self.body[0][1])
        elif self.direction == self.RIGHT:
            if self.body[0][0] == 63:
                self.body[0] = (0, self.body[0][1])
            else:
                self.body[0] = (self.body[0][0] + 1, self.body[0][1])
        elif self.direction == self.UP:
            if self.body[1][1] == 0:
                self.body[0] = (self.body[0][0], 47)
            else:
                self.body[0] = (self.body[0][0], self.body[0][1] - 1)
        else:
            if self.body[1][1] == 47:
                self.body[0] = (self.body[0][0], 0)
            else:
                self.body[0] = (self.body[0][0], self.body[0][1] + 1)

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
            if not self.id:
                body_pos += f'{i[0]},{i[1]}-'  # '0,1-1,1-2,1-'
            else:
                body_pos += f'{i.x},{i.y}-'
        return body_pos

    def __str__(self):
        body_pos = ''
        for i in self.body:
            body_pos += f'{i[0]},{i[1]}-'  # '0,1-1,1-2,1-'
        return body_pos
