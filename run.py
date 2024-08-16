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


class App:
    running = True
    screens = []
    window = None
    settings = None

    def __init__(self):
        pg.init()
        self.settings = Setting.load_settings()
        self.window = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)

        self.screens.append(StartScreen())

        self.run_app()

    def push_screen(self, screen):
        self.screens.append(screen)
    
    def pop_screen(self):
        self.screens.pop()
    
    def exit_app(self):
        self.running = False

    def run_app(self):
        while self.running:
            try:
                self.clock.tick(FPS)
                # runs screen on top of the screens pile and pass App as context
                self.screens[-1].run(self)
            except IndexError:
                self.push_screen(StartScreen())
                self.screens[-1].run(self)


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
        App()
