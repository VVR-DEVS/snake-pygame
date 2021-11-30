from Game import *

g = Spiel()
g.startbildschirm()

while g.running:
    g.neueSpiel()

pg.quit()
