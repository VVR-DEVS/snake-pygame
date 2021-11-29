import pygame as pg
from Snake import Snake
from Settings import *
from client import Client


class Spiel:

    def __init__(self):

        pg.init()
        self.bildschirm = pg.display.set_mode(BILDSCHIRM_SIZE)
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.running = True
        self.state = MENU
        self.connection = None
        self.enemies = []
        self.spieler = None
        self.server = None

    def neueSpiel(self):
        self.run()

    def run(self):

        while self.running:
            if self.state == MENU:
                self.startbildschirm()
            elif self.state == CONNECTING:
                pos = self.connection.connect()
                self.spieler = Snake(pos)
                self.state = WAITING
            elif self.state == WAITING:
                id_list = []
                while True:
                    enemies_pos = self.connection.wait_start()
                    if enemies_pos is None:
                        self.state = PLAYING
                        break
                    for idEnemy in enemies_pos:
                        if idEnemy not in id_list:
                            id_list.append(idEnemy)
                            self.enemies.append(Snake(enemies_pos[idEnemy], idEnemy))

            elif self.state == PLAYING:
                while self.state == PLAYING:
                    self.clock.tick(10)
                    self.events()
                    self.aktualisieren()
                    self.draw()

    def aktualisieren(self):
        enemies_pos = self.connection.send(self.spieler.pos)
        for idEnemy in enemies_pos:
            next(filter(lambda enemy: idEnemy == enemy.id, self.enemies)).set_position(enemies_pos[idEnemy])

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.server.close()
                self.state = "OUT"
                self.running = False

            if event.type == pg.K_ESCAPE:
                self.state = MENU

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.spieler.change_direction('up')
                if event.key == pg.K_DOWN:
                    self.spieler.change_direction('down')
                if event.key == pg.K_RIGHT:
                    self.spieler.change_direction('right')
                if event.key == pg.K_LEFT:
                    self.spieler.change_direction('left')

    def draw(self):
        self.bildschirm.fill(BLACK)
        self.draw_grid()
        self.draw_snake()
        pg.display.flip()

    def draw_grid(self):
        self.spieler.update()
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.bildschirm, GREY, (x, 0), (x, HEIGHT))
            pg.draw.line(self.bildschirm, GREY, (0, x), (WIDTH, x))

    def draw_snake(self):
        # print('Draw', self.spieler.pos, self.enemies[0].pos)
        for pos in self.spieler.snake:
            self.bildschirm.blit(self.spieler.snake_skin, pos)

        for player in self.enemies:
            for pos in player.snake:
                self.bildschirm.blit(player.snake_skin, pos)

    def start_cliente(self):
        self.connection = Client()

    def startbildschirm(self):
        botao_client = pg.rect.Rect(23 * TILESIZE, HEIGHT / 2.5, 300, 150)
        text_client = pg.font.SysFont('arial', 40).render('PLAY', True, BLUE)
        text_client_rect = text_client.get_rect()
        text_client_rect.center = botao_client.center

        text_credits = pg.font.SysFont('sans', 20).render('developed by: Mateus Rosario and Wercton Barbosa', True,
                                                          GREY)

        while self.state == MENU:
            self.bildschirm.fill(BLUE)
            mouse = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.state = "OUT"
                    self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if botao_client.collidepoint(mouse_pos):
                        self.state = CONNECTING
                        self.start_cliente()
                        print("client")

            if botao_client.collidepoint(mouse):
                pg.draw.rect(self.bildschirm, GREY, botao_client)
            else:
                pg.draw.rect(self.bildschirm, BLACK, botao_client)
            self.bildschirm.blit(text_client, text_client_rect)
            self.bildschirm.blit(text_credits, (WIDTH / 2 + 40, HEIGHT - 90))
            pg.display.update()

    def endbildschirm(self):
        pass
