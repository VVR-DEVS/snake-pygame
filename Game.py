import pygame as pg
from Settings import *

class Spiel:
    def __init__(self):

        pg.init()
        self.bildschirm = pg.display.set_mode(BILDSCHIRM_SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.running = True

    def neueSpiel(self):
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.aktualisieren()
            self.draw()

    def aktualisieren(self):
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.bildschirm.fill(BLACK)
        pg.display.flip()

    def startbildschirm(self):
        pass

    def endbildschirm(self):
        pass