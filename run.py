import pygame as pg
import sys

from server import start_server
from utils import Position
from utils import Setting
from utils import WINDOW_SIZE
from utils import TITLE
from utils import FPS
from elements.snake import Snake
from screens.menus.start_screen import StartScreen


class AppContext:
    running = True
    screens = []
    window = None
    settings = None

    def __init__(self, window, settings, home_screen):
        self.screens.append(home_screen)
        self.window = window
        self.settings = settings

    def push_screen(self, screen):
        self.screens.append(screen)
    
    def exit_app(self):
        self.running = False

    def run_app(self):
        self.screens[-1].run(self)


def run():
    pg.init()
    settings = Setting.load_settings()
    window = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()
    pg.display.set_caption(TITLE)

    context = AppContext(window, settings, StartScreen())

    while context.running:
        clock.tick(FPS)
        context.run_app()


if __name__ == '__main__':
    print(sys.argv)
    # START SERVER
    if len(sys.argv) > 1:
        if sys.argv[1] == 'server':
                start_server()
        else:
            raise Exception('Argumento inválido recebido')
    
    # START GAME (CLIENT)
    else:
        run()
