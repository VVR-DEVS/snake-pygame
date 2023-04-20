from utils import Position
from utils.settings import *
from client import Client
from elements.snake import Snake
from screens.screen import Screen
import pygame as pg


class MultiPlayerGameScreen(Screen):
    PLAYING = 0
    CONNECTING = 1
    WAITING = 2

    def __init__(self):
        self.state = self.CONNECTING
        self.connection = Client()


        self.snake = None
        self.enemies = []

        self.num_players_match = 2

    def draw_grid(self, window):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(window, GREY, (x, 0), (x, HEIGHT))
            pg.draw.line(window, GREY, (0, x), (WIDTH, x))
    
    def draw_snakes(self, window):
        self.snake.draw(window)
        for snake in self.enemies:
            snake.draw(window)
    
    def draw(self, window):
        window.fill(BLACK)
        self.draw_grid(window)
        self.draw_snakes(window)
        # if self.verify_colissions() and self.moving:
        pg.display.flip()
    
    def run(self, window, context):
        if self.state == self.CONNECTING:
            self.try_connection(context[1])
        if self.state == self.WAITING:
            id_list = []
            while True:
                enemies_pos = self.connection.wait_start()
                if enemies_pos is None:
                    self.state = self.PLAYING
                    break
                for id_enemy in enemies_pos:
                    if id_enemy not in id_list:
                        id_list.append(id_enemy)
                        self.enemies.append(enemies_pos[id_enemy])
        if self.state == self.PLAYING:
            self.events()
            self.snake.update()
            self.update_enemies()
            self.draw(window)

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
                # if event.key == pg.K_ESCAPE:
                #     self.connection.disconnect()
                #     self.state = self.MENU
    
    def try_connection(self, on_no_connection):
        try:
            pos = self.connection.connect(self.num_players_match)
            if pos is None:
                on_no_connection()
            self.snake = Snake(pos, 3, Snake.UP)
            self.state = self.WAITING
        except Exception as e:
            print(f'Exceção: {str(e)}')
            on_no_connection()
    
    def update_enemies(self):
        enemies_pos = self.connection.update_data(str(self.snake))
        print('ENEMIES POS', enemies_pos)
        for id_enemy in enemies_pos:
            for enemy in self.enemies:
                if enemy.id == id_enemy:
                    enemy.set_body(enemies_pos[id_enemy])