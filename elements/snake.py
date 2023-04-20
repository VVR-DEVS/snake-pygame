import pygame as pg
import re
from utils import Position, settings

class Snake:
    """This class represents the Snakes that will apear on Screen

    This class is a data structure to maintain and control the Snake's body

    Each body part is a Position object
    This class is Iterable
    """

    # directions that the snake can move
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


    def __init__(self, head, size, direction, id_player=None, body=None):
        self.snake_skin = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.id = id_player
        self.size = size
        self.direction = direction

        if id_player is None:
            self.body = self.generate_body(3, head, self.LEFT)
            self.snake_skin.fill((255, 0, 0))
        else:
            self.set_body(body)
            self.snake_skin.fill((0, 255, 0))


    def generate_body(self, size, head, direction):
        if direction == self.UP:
            return [Position(head.x, head.y + i) for i in range(size)]
        elif direction == self.DOWN:
            return [Position(head.x, head.y - i) for i in range(size)]
        elif direction == self.LEFT:
            return [Position(head.x - i, head.y) for i in range(size)]
        elif direction == self.RIGHT:
            return [Position(head.x + i, head.y) for i in range(size)]

    def draw(self, bildschirm):
        for pos in self.body:
            bildschirm.blit(self.snake_skin, (int(pos[0]) * settings.TILESIZE, int(pos[1]) * settings.TILESIZE))

    def update(self):
        last_collum = settings.WIDTH / settings.TILESIZE
        last_row = settings.HEIGHT / settings.TILESIZE

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].set(self.body[i - 1][0], self.body[i - 1][1])

        if self.direction == self.LEFT:
            if self.body[0][0] == 0:
                self.body[0].set(last_collum, self.body[0][1])
            else:
                self.body[0].set(self.body[0][0] - 1, self.body[0][1])
        elif self.direction == self.RIGHT:
            if self.body[0][0] == last_collum:
                self.body[0].set(0, self.body[0][1])
            else:
                self.body[0].set(self.body[0][0] + 1, self.body[0][1])
        elif self.direction == self.UP:
            if self.body[1][1] == 0:
                self.body[0].set(self.body[0][0], last_row)
            else:
                self.body[0].set(self.body[0][0], self.body[0][1] - 1)
        else:
            if self.body[1][1] == last_row:
                self.body[0].set(self.body[0][0], 0)
            else:
                self.body[0].set(self.body[0][0], self.body[0][1] + 1)

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

    def set_body(self, body):
        if isinstance(body, str):
            """
            Using the re library to use regex to get the body parts and direction
            """
            try:
                self.direction = re.findall(r'/(U|D|L|R)\[', body)[0]
            except  IndexError:
                if self.direction == None:
                    self.direction = self.LEFT
            body_parts = re.findall(r'\[(\d+), (\d+)\]', body)
            self.body = [Position(int(i[0]), int(i[1])) for i in body_parts]
        else:
            self.body = body

    def head(self):
        return self.body[0]
    
    @staticmethod
    def id_str(snake_str):
        """
        Receives a representation of a snake as string and return the snake ids using regex
        """
        id_ = re.findall(r'/(\d+)/', snake_str)
        if id_ != None:
            print(id_)
            if isinstance(id_, list):
                return id_[0]
            else:
                return id_
        else:
            return

    def __str__(self):
        if self.id == None:
            body_pos = '['
        else:
            body_pos = '/' + str(self.id) + '/ ' + self.direction + ' ['
        for i in self.body:
            body_pos += f'{i[0]}, {i[1]}] ['
        return body_pos[0: -1]

    def __getitem__(self, index):
        return self.body[index]


class SnakeIter:
    def __init__(self, snake):
        self.snake = snake
        self.index = 0

    def __next__(self):
        if self.index < self.snake.size:
            return self.snake.body[self.index]
        raise StopIteration

    def __iter__(self):
        return self