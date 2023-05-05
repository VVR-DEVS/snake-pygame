from utils import Position
from utils import *
from screens.screen import Screen
import pygame as pg
from screens.local_game_screen import LocalGameScreen
from screens.game_screen import MultiPlayerGameScreen


class StartScreen(Screen):

    def __init__(self):
        self.font = pg.font.SysFont('arial', 40)
        self.button_play = Button(WIDTH / 2 - 185, HEIGHT / 2 - 200, 'LOCAL', self.font)
        self.button_play_multiplayer = Button(WIDTH / 2 - 185, HEIGHT / 2 - 50, 'ONLINE', self.font)
        self.button_configs = Button(WIDTH / 2 - 185, HEIGHT / 2 + 100, 'CONFIGURATIONS', self.font)
        

    def run(self, context):
        def start_game():
            context.push_screen(LocalGameScreen())
        
        def start_multiplayer_game():
            context.push_screen(MultiPlayerGameScreen())

        context.window.fill(BLUE)

        text_credits = pg.font.SysFont('sans', 20).render('developed by: Mateus Rosario and Wercton Barbosa', True,GREY)
        
        mouse_event = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                context.exit_app()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    context.exit_app()
                elif event.key == pg.K_RETURN:
                    start_game()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_event = True

        self.button_play.run(context.window, mouse_event, start_game)
        self.button_play_multiplayer.run(context.window, mouse_event, start_multiplayer_game)
        self.button_configs.run(context.window, mouse_event, lambda: None)

        context.window.blit(text_credits, (WIDTH / 2 + 40, HEIGHT - 30))
        pg.display.update()

class Button:
    def __init__(self, x, y, label, font):
        self.rect = pg.rect.Rect(x, y, 370, 100)
        self.text = font.render(label, True, BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def run(self, window, mouseevent, on_click):
        if mouseevent:
            mouse_pos = pg.mouse.get_pos()
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