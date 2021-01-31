import pygame as pg
from Snake import Snake
from Server import Server
from Settings import *


class Spiel:

    enemies = None
    
    def __init__(self):

        pg.init()
        self.bildschirm = pg.display.set_mode(BILDSCHIRM_SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.running = True
        self.jogador = Snake()
        self.server = Server(self.enemies)
        self.server.start()

    def neueSpiel(self):
        self.run()

    def run(self):
        self.server.run()
        self.playing = True
        while self.playing:
            self.clock.tick(10)
            self.events()
            self.aktualisieren()
            self.draw()

    def aktualisieren(self):
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.server.close()
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.jogador.change_direction('up')
                if event.key == pg.K_DOWN:
                    self.jogador.change_direction('down')
                if event.key == pg.K_RIGHT:
                    self.jogador.change_direction('right')
                if event.key == pg.K_LEFT:
                    self.jogador.change_direction('left')

    def draw(self):
        self.bildschirm.fill(BLACK)
        self.draw_grid()
        self.draw_snake()
        pg.display.flip()
        
    def draw_grid(self):
        self.jogador.update()
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.bildschirm, GREY, (x, 0), (x, HEIGHT))
            pg.draw.line(self.bildschirm, GREY, (0, x), (WIDTH, x))

    def draw_snake(self):
        for pos in self.jogador.snake:
            self.bildschirm.blit(self.jogador.snake_skin, pos)

    def startbildschirm(self):
        pass

    def endbildschirm(self):
        pass
