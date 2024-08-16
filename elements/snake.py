import pygame as pg
import random
import math
import re
from utils import *

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


    def __init__(self, head, size, direction, color=RED, id_player=None, body=None):
        self.id = id_player
        self.size = size
        self.direction = direction
        # has direction changed since last update
        self.direction_changed = False
        self.alive = True

        self.color = color

        if id_player is None:
            self.body = self.generate_body(3, head, self.LEFT)
        else:
            self.set_body(body)


    def generate_body(self, size, head, direction):
        if direction == self.UP:
            return [Position(head.x, head.y + i) for i in range(size)]
        elif direction == self.DOWN:
            return [Position(head.x, head.y - i) for i in range(size)]
        elif direction == self.LEFT:
            return [Position(head.x - i, head.y) for i in range(size)]
        elif direction == self.RIGHT:
            return [Position(head.x + i, head.y) for i in range(size)]
    
    def grow(self, size=1):
        self.size += size
        for i in range(size):
            self.body.append(Position(self.body[-1].x, self.body[-1].y))

    def draw(self, window, start_grid_x, start_grid_y, tile_size):
        snake_skin = pg.Surface((tile_size, tile_size))
        if self.alive:
            snake_skin.fill(self.color)
        else:
            snake_skin.fill((20, 50, 50))
        for pos in self.body:
            window.blit(snake_skin, (start_grid_x + int(pos[0]) * tile_size, start_grid_y + int(pos[1]) * tile_size))

    def update(self, grid_width, grid_height):
        self.direction_changed = False
        last_column = grid_width - 1
        last_row = grid_height - 1

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].set(self.body[i - 1][0], self.body[i - 1][1])

        if self.direction == self.LEFT:
            if self.body[0][0] == 0:
                self.body[0].set(last_column, self.body[0][1])
            else:
                self.body[0].set(self.body[0][0] - 1, self.body[0][1])
        elif self.direction == self.RIGHT:
            if self.body[0][0] == last_column:
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

    def set_body(self, body):
        if isinstance(body, str):
            """
            Using the re library to use regex to get the body parts and direction
            """
            try:
                self.direction = re.findall(r'/ (U|D|L|R) -', body)[0]
            except  IndexError:
                if self.direction == None:
                    self.direction = self.LEFT
            
            try:
                self.alive = False if re.findall(r'- (A|D) \[', body)[0] == 'D' else True
            except  IndexError:
                print('IndexError: Regex reading', re.findall(r'-(A|D)\[', body))

            body_parts = re.findall(r'\[(\d+), (\d+)\]', body)
            self.body = [Position(int(i[0]), int(i[1])) for i in body_parts]
        else:
            self.body = body

    def change_direction(self, move):
        if self.direction == move or self.direction_changed:
            return

        if self.direction == Snake.UP:
            if move == Snake.DOWN:
                return
        elif self.direction == Snake.DOWN:
            if move == Snake.UP:
                return
        elif self.direction == Snake.RIGHT:
            if move == Snake.LEFT:
                return
        elif self.direction == Snake.LEFT:
            if move == Snake.RIGHT:
                return
        
        self.direction = move
        self.direction_changed = True

    def bot_change_direction(self, other_snakes, foods, grid_width, grid_height, difficulty='Hard'):
        # method that to each call will verify position of the snakes on the grid and change direction based on the nearest food position
        if difficulty == 'easy':
            return self.change_direction(random.choice([Snake.UP, Snake.DOWN, Snake.RIGHT, Snake.LEFT]))
        else:
            self.change_direction(self.get_bot_direction(other_snakes, foods, grid_width, grid_height, difficulty))

    def get_bot_direction(self, other_snakes, foods, grid_width, grid_height, difficulty):
        free_directions = [Snake.UP, Snake.DOWN, Snake.RIGHT, Snake.LEFT]
        
        direction = self.get_nearest_food_direction(foods, grid_width, grid_height)
        if direction is None:
            # if direction is None or direction == self.direction: => this condition made a very interesting randomness effect
            direction = random.choice(free_directions)

        while len(free_directions) > 1:
            # calculates future position for every possible direction
            if direction == Snake.RIGHT:
                future_pos = Position(self.head().x + 1 if self.head().x + 1 < grid_width else 0, self.head().y)
            elif direction == Snake.LEFT:
                future_pos = Position(self.head().x - 1 if self.head().x - 1 >= 0 else grid_width - 1, self.head().y)
            elif direction == Snake.UP:
                future_pos = Position(self.head().x, self.head().y - 1 if self.head().y - 1 >= 0 else grid_height - 1)
            else:
                future_pos = Position(self.head().x, self.head().y + 1 if self.head().y + 1 < grid_height else 0)

            
            # verify collision with self body
            if future_pos in self.body:
                free_directions.remove(direction)
                direction = random.choice(free_directions)
                continue

            continue_outer_loop = False
            # verify collision with other snakes bodies
            for snake in other_snakes:
                if future_pos in snake.body:
                    free_directions.remove(direction)
                    direction = random.choice(free_directions)
                    continue_outer_loop = True
                    break
            
            if not continue_outer_loop:
                break

        if len(free_directions) == 1:
            print('Snake-bot says "Theres no other way"')
            return free_directions[0]

        return direction

    def get_nearest_food_direction(self, foods, grid_width, grid_height):
        # get the nearest food to the snake head position based on the grid size
        if len(foods) == 0:
            return None
        
        # searching the nearest food
        nearest_food = None
        nearest_food_distance = None
        nearest_food_distance_x = None
        nearest_food_distance_y = None
        nearest_food_index = None
        food_index = 0
        for food in foods:
            x_distance = self.unidimensional_distance_on_grid(self.head().x, food.x, grid_width)
            y_distance = self.unidimensional_distance_on_grid(self.head().y, food.y, grid_height)
            distance = math.sqrt(x_distance**2 + y_distance**2)

            if nearest_food is None:
                nearest_food = food
                nearest_food_index = food_index
                nearest_food_distance = distance
                nearest_food_distance_x = x_distance
                nearest_food_distance_y = y_distance
            else:
                if distance < nearest_food_distance:
                    nearest_food = food
                    nearest_food_index = food_index
                    nearest_food_distance = distance
                    nearest_food_distance_x = x_distance
                    nearest_food_distance_y = y_distance
            food_index += 1

        # print('Nearest Food Index:', nearest_food_index)
        
        # if distance X is bigger than distance Y (getting direction to head the snake), 
        #   takes into account if the nearest direction is through the limits of the grid
        if abs(nearest_food_distance_x) > abs(nearest_food_distance_y):
            if nearest_food.x > self.head().x:
                return Snake.RIGHT if nearest_food_distance_x > 0 else Snake.LEFT
            else:
                return Snake.LEFT if nearest_food_distance_x > 0 else Snake.RIGHT
        else:
            if nearest_food.y > self.head().y:
                return Snake.DOWN if nearest_food_distance_y > 0 else Snake.UP
            else:
                return Snake.UP if nearest_food_distance_y > 0 else Snake.DOWN

    def unidimensional_distance_on_grid(self, pos_1, pos_2, axis_length):
        """get the distance between two positions on the given unidimensional 
            axis of the grid (considering distance through the limits of the grid)

        Args:
            pos_1 (int): position of one item
            pos_2 (int): position of another item
            axis_length (int): length of the axis on grid

        Returns:
            int: a ind representing the distance between the two positions given 
                (if negative, the nearest distance is through the limits of the grid)
        """
        if axis_length == 1 or axis_length == 0:
            return 0
        elif axis_length == 2:
            if pos_1 == pos_2:
                return 0
            else:
                return 1
        else:
            if pos_1 == pos_2:
                return 0
            else:
                direct_dif = abs(pos_2 - pos_1)
                if direct_dif > axis_length / 2:
                    if pos_1 > pos_2:
                        return - (axis_length - pos_1 + pos_2)
                    else:
                        return - (axis_length - pos_2 + pos_1)
                else:
                    return direct_dif


    def head(self):
        return self.body[0]
    
    def kill(self):
        self.alive = False
    
    @staticmethod
    def id_str(snake_str):
        """
        Receives a representation of a snake as string and return the snake ids using regex
        """
        id_ = re.findall(r'/(\d+)/', snake_str)
        if id_ != None:
            if isinstance(id_, list):
                return id_[0]
            else:
                return id_
        else:
            return

    def __str__(self):
        body_pos = ''
        if self.id != None:
            body_pos = '/' + str(self.id)

        body_pos += '/ ' + self.direction + ' - ' + ('A' if self.alive else 'D')  +  ' ['
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