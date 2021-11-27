import pygame as pg
from Game import *

g = Spiel()
g.startbildschirm()

while g.running:
    g.neueSpiel()
    g.endbildschirm()

pg.quit()
