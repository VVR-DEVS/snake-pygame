from utils import Position
from utils.settings import *
from screens.screen import Screen
import pygame as pg
from screens.local_game_screen import LocalGameScreen
from screens.game_screen import MultiPlayerGameScreen


class StartScreen(Screen):

    def __init__(self):
        self.font = pg.font.SysFont('arial', 40)
        self.button_play_multiplayer = Button(300, 150, 'PLAY', self.font)
        

    def run(self, context):
        def start_game():
            context.push_screen(LocalGameScreen())

        context.window.fill(BLUE)

        text_credits = pg.font.SysFont('sans', 20).render('developed by: Mateus Rosario and Wercton Barbosa', True,
                                                          GREY)

        # TODO solve conflict
        self.button_play_multiplayer.run(context.window, start_game)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                context.exit_app()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    context.exit_app()

        context.window.blit(text_credits, (WIDTH / 2 + 40, HEIGHT - 90))
        pg.display.update()

class Button:
    def __init__(self, x, y, label, font):
        self.rect = pg.rect.Rect(23 * TILESIZE, HEIGHT / 2.5, x, y)
        self.text = font.render(label, True, BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def run(self, window, on_click):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.rect.collidepoint(mouse_pos):
                    on_click()
        
        self.draw(window)

    def draw(self, window):
        mouse = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            pg.draw.rect(window, GREY, self.rect)
        else:
            pg.draw.rect(window, BLACK, self.rect)
        window.blit(self.text, self.text_rect)