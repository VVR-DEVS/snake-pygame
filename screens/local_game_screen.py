from utils import Position
from utils import *
import random
import pygame as pg
from elements.snake import Snake
from screens.screen import Screen

class LocalGameScreen(Screen):

    def __init__(self, vs_comp=False):
        self.grid_width = GRIDWIDTH
        self.grid_height = GRIDHEIGHT

        if WIDTH < HEIGHT:
            self.tile_size  = int(WIDTH / self.grid_width)
        else:
            self.tile_size  = int(HEIGHT / self.grid_width)
        
        self.start_grid_x = int((WIDTH - self.grid_width * self.tile_size)/2)
        self.start_grid_y = int((HEIGHT - self.grid_height * self.tile_size)/2)

        self.grid_rect = pg.Surface((self.grid_width * self.tile_size + self.tile_size, self.grid_height * self.tile_size + self.tile_size))
        self.grid_rect.fill(GREY)
        self.grid_rect.fill(BLACK, self.grid_rect.get_rect().inflate(-self.tile_size/2, -self.tile_size/2))

        self.vs_comp = vs_comp
        self.snake = Snake(Position(10, int(self.grid_height/2)), 3, Snake.UP, color=RED)
        self.snakeP2 = Snake(Position(self.grid_width - 10, int(self.grid_height/2)), 3, Snake.DOWN, color=GREEN)
        self.snakes = [self.snake, self.snakeP2]
        self.foods = []
        self.max_food_qty = 3

    def draw_grid(self, window):
        window.blit(self.grid_rect, (self.start_grid_x - self.tile_size/2, self.start_grid_y - self.tile_size/2))

        # Drawing Horizontal Lines
        for y in range(1, self.grid_height):
            pg.draw.line(window, GREY, (self.start_grid_x, self.start_grid_y + y * self.tile_size), 
                (self.start_grid_x + self.grid_width * self.tile_size, self.start_grid_y + y * self.tile_size))

        # Drawing Vertical Lines
        for x in range(1, self.grid_width):
            pg.draw.line(window, GREY, (self.start_grid_x + x * self.tile_size, self.start_grid_y), 
                (self.start_grid_x + x * self.tile_size, self.start_grid_y + self.grid_height * self.tile_size))
    
    def draw_snakes(self, window):
        for snake in self.snakes:
            snake.draw(window, self.start_grid_x, self.start_grid_y, self.tile_size)
    
    def draw_food(self, window):
        surf = pg.Surface((self.tile_size, self.tile_size))
        surf.fill((255, 0, 0))
        for food in self.foods:
            window.blit(surf, (self.start_grid_x + food.x * self.tile_size, self.start_grid_y + food.y * self.tile_size))

    def run(self, context):
        self.events(context)
        for snake in self.snakes:
            snake.update(self.grid_width, self.grid_height)
        self.spawn_food()
        self.verify_collisions()
        self.draw(context.window)
    
    def draw(self, window):
        window.fill(BLACK)
        self.draw_grid(window)
        self.draw_food(window)
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
                
                for food in self.foods:
                    if snake.head() == food:
                        snake.grow(size=3)
                        self.foods.remove(food)
                        break
    
    def spawn_food(self):
        """spawns food at a random position on the grid
        :return: None
        """
        if len(self.foods) < self.max_food_qty:
            self.foods.append(Position.random_position(0, 0, self.grid_width, self.grid_height))


    def events(self, context):
        # defining snake to be controlled by secondary set of control keys
        if self.vs_comp:
            snakeC2 = self.snake
            self.comp_movement()
        else:
            snakeC2 = self.snakeP2

        for event in pg.event.get():
            if event.type == pg.QUIT:
                context.exit_app()
            if event.type == pg.KEYDOWN:
                # first set of control keys
                if event.key == pg.K_UP:
                    self.snake.change_direction(Snake.UP)
                elif event.key == pg.K_DOWN:
                    self.snake.change_direction(Snake.DOWN)
                elif event.key == pg.K_RIGHT:
                    self.snake.change_direction(Snake.RIGHT)
                elif event.key == pg.K_LEFT:
                    self.snake.change_direction(Snake.LEFT)
                
                # second set of control keys
                elif event.key == pg.K_w:
                    self.snakeC2.change_direction(Snake.UP)
                elif event.key == pg.K_s:
                    self.snakeC2.change_direction(Snake.DOWN)
                elif event.key == pg.K_d:
                    self.snakeC2.change_direction(Snake.RIGHT)
                elif event.key == pg.K_a:
                    self.snakeC2.change_direction(Snake.LEFT)
                
                # app control keys
                elif event.key == pg.K_ESCAPE:
                    context.exit_app()
                elif event.key == pg.K_BACKSPACE:
                    context.pop_screen()
    
    def comp_movement(self):
        self.snakeP2.bot_change_direction([self.snake], self.foods, self.grid_width, self.grid_height)

