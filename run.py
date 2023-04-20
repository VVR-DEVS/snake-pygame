import pygame as pg
import sys
from server import start_server
from utils import Position
from utils.settings import *
from elements.snake import Snake
from screens.menus.start_screen import StartScreen


class AppContext:
    running = True
    screens = []
    window = None

    def __init__(self, window, home_screen):
        self.screens.append(home_screen)
        self.window = window

    def push_screen(self, screen):
        self.screens.append(screen)
    
    def exit_app(self):
        self.running = False

    def run_app(self):
        self.screens[-1].run(self)


def run():
    pg.init()
    window = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()
    pg.display.set_caption(TITLE)

    # context = AppContext(StartScreen(), window)

    running = True

    screens = []
    start_screen = StartScreen()
    screens.append(start_screen)

    def push_screen(screen):
        screens.append(screen)

    def exit_game():
        running = False

    while running:
        clock.tick(FPS)
        screens[-1].run(window, [push_screen, exit_game])


if __name__ == '__main__':
    print(sys.argv)
    # START SERVER
    if len(sys.argv) > 1:
        if sys.argv[1] == 'server':
                start_server()
        else:
            raise Exception('Argumento inválido recebido')
    
    # START GAME CLIENT
    else:
        run()
