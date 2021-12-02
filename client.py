import socket

from position import Position
from Settings import PORT, HOST


class Client(object):

    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, num_players_match):
        self.soc.connect((HOST, PORT))
        msg = self.soc.recv(1024).decode('utf-8')
        print('Recebido:', msg)
        if msg == 'connected':
            self.soc.send(str(num_players_match).encode())
        else:
            return None
        pos = Position(self.soc.recv(1024).decode('utf-8'))
        return pos

    def wait_start(self):
        self.soc.send(b"waiting")
        resp = self.soc.recv(1024).decode('utf-8')
        if resp == 'start':
            return None

        if resp == 'NEY':
            return {}

        enemies_pos = []
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(int(item[0]), int(item[1]))))
        return dict(enemies_pos)

    def send(self, body_pos):
        print('body pos recebindo em send clinet:', body_pos)
        self.soc.send(str(body_pos).encode())  # '0,1-1,1-2,1-' enviando para...
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')  # recebendo de...
        print('resp recebido no soc:', resp)
        for snake in resp.split(';'):
            coordinates = []
            snake_id = None
            for body_part in snake.split('-'):
                print('AQUIIIIII')
                if '|' in body_part:
                    print('?')
                    snake_id = body_part.replace('|', '')
                else:
                    print(body_part)
                    x, y = body_part.split(',')
                    coordinates.append((x, y))
            enemies_pos.append((int(snake_id), coordinates))
        print("ALLES GUT!")
        return dict(enemies_pos)

    def send_signal(self, signal):
        self.soc.send(signal.encode())  # 'collided'
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(item[0], item[1])))
        return dict(enemies_pos)

    def disconnect(self):
        self.soc.close()

