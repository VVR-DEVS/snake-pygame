from utils import Position
from utils import *
from client import Client
from elements.snake import Snake
from screens.screen import Screen
import pygame as pg


class MultiPlayerGameScreen(Screen):
    PLAYING = 0
    CONNECTING = 1
    WAITING = 2
    DISCONNECTED = 3

    def __init__(self):
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

        self.state = self.CONNECTING
        self.connection = Client()

        self.snake = None
        self.enemies = []

        self.num_players_match = 2
    
    def try_connection(self, on_no_connection):
        try:
            position = self.connection.connect(self.num_players_match)
            if position is None:
                on_no_connection()
            self.snake = Snake(position, 3, Snake.UP)
            self.state = self.WAITING
        except Exception as e:
            print(f'Exceção: {str(e)}')
            on_no_connection()
        
    def update_enemies(self):
        enemies_pos = self.connection.update_data(str(self.snake))

        if not enemies_pos:
            self.disconnect()
            return

        for id_enemy in enemies_pos:
            for enemy in self.enemies:
                if enemy.id == id_enemy:
                    enemy.set_body(enemies_pos[id_enemy])
    
    def disconnect(self):
        self.state = self.DISCONNECTED
        self.connection.disconnect()

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
        self.snake.draw(window, self.start_grid_x, self.start_grid_y, self.tile_size)
        for snake in self.enemies:
            snake.draw(window, self.start_grid_x, self.start_grid_y, self.tile_size)
    
    def draw(self, window):
        window.fill(BLACK)
        self.draw_grid(window)
        self.draw_snakes(window)
        pg.display.flip()
    
    def run(self, context):
        if self.state == self.CONNECTING:
            self.try_connection(context.exit_app)
        if self.state == self.WAITING:
            id_list = []
            while True:
                enemies_pos = self.connection.wait_start()
                if enemies_pos is True:
                    self.state = self.PLAYING
                    break
                elif enemies_pos == False:
                    self.disconnect()
                elif enemies_pos is not None:
                    for id_enemy in enemies_pos:
                        if id_enemy not in id_list:
                            id_list.append(id_enemy)
                            self.enemies.append(enemies_pos[id_enemy])
    
        if self.state == self.PLAYING:
            self.events(context)
            self.snake.update(self.grid_width, self.grid_height)
            self.update_enemies()
            self.draw(context.window)
        if self.state == self.DISCONNECTED:
            context.pop_screen()

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
                elif event.key == pg.K_ESCAPE:
                    context.exit_app()
                elif event.key == pg.K_BACKSPACE:
                    context.pop_screen()
