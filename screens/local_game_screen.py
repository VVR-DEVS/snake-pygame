from utils import Position
from utils.settings import *
from elements.snake import Snake
from screens.screen import Screen
import pygame as pg

class LocalGameScreen(Screen):
    def __init__(self):
        self.snake = Snake(Position(10, 10), 3, Snake.UP)
        self.snakeP2 = Snake(Position(40, 10), 3, Snake.DOWN)
        self.snakes = [self.snake, self.snakeP2]

    def draw_grid(self, window):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(window, GREY, (x, 0), (x, HEIGHT))
            pg.draw.line(window, GREY, (0, x), (WIDTH, x))
    
    def draw_snakes(self, window):
        for snake in self.snakes:
            snake.draw(window)

    def run(self, window, context):
        self.events()
        for snake in self.snakes:
            snake.update()
        self.draw(window)
    
    def draw(self, window):
        window.fill(BLACK)
        self.draw_grid(window)
        self.draw_snakes(window)
        # if self.verify_colissions() and self.moving:
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                context[1]()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.snake.change_direction(Snake.UP)
                if event.key == pg.K_DOWN:
                    self.snake.change_direction(Snake.DOWN)
                if event.key == pg.K_RIGHT:
                    self.snake.change_direction(Snake.RIGHT)
                if event.key == pg.K_LEFT:
                    self.snake.change_direction(Snake.LEFT)
                

                if event.key == pg.K_w:
                    self.snakeP2.change_direction(Snake.UP)
                if event.key == pg.K_s:
                    self.snakeP2.change_direction(Snake.DOWN)
                if event.key == pg.K_d:
                    self.snakeP2.change_direction(Snake.RIGHT)
                if event.key == pg.K_a:
                    self.snakeP2.change_direction(Snake.LEFT)
                # if event.key == pg.K_ESCAPE:
                #     self.connection.disconnect()
                #     self.state = self.MENU
        