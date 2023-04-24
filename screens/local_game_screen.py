from utils import Position
from utils import *
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

    def run(self, context):
        self.events(context)
        for snake in self.snakes:
            snake.update()
        self.verify_collisions()
        self.draw(context.window)
    
    def draw(self, window):
        window.fill(BLACK)
        self.draw_grid(window)
        self.draw_snakes(window)
        pg.display.flip()
    
    def verify_collisions(self):
        """verifies collisions between snakes and kills snake that is headed to the collision point
            it takes in to account snakes hitting itself
        :return: None
        """
        for snake in self.snakes:
            if snake.alive:
                for other_snake in self.snakes:
                    if other_snake.alive:
                        for section in other_snake:
                            if snake.head() == section and snake.head() is not section:
                                snake.kill()
                                if section is other_snake.head():
                                    other_snake.kill()

    def events(self, context):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                context.exit_app()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.snake.change_direction(Snake.UP)
                elif event.key == pg.K_DOWN:
                    self.snake.change_direction(Snake.DOWN)
                elif event.key == pg.K_RIGHT:
                    self.snake.change_direction(Snake.RIGHT)
                elif event.key == pg.K_LEFT:
                    self.snake.change_direction(Snake.LEFT)
                

                elif event.key == pg.K_w:
                    self.snakeP2.change_direction(Snake.UP)
                elif event.key == pg.K_s:
                    self.snakeP2.change_direction(Snake.DOWN)
                elif event.key == pg.K_d:
                    self.snakeP2.change_direction(Snake.RIGHT)
                elif event.key == pg.K_a:
                    self.snakeP2.change_direction(Snake.LEFT)
                elif event.key == pg.K_ESCAPE:
                    context.exit_app()
        