import socket
from utils.position import Position
from utils.settings import PORT, HOST


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
        enemies_pos_data = self.soc.recv(1024).decode('utf-8')  # recebendo de server().run

        if enemies_pos_data == 'start':
            return None
        if enemies_pos_data == 'NEY':  # No Enemies Yet
            return {}

        enemies_pos = []
        for i in enemies_pos_data.split(';'):
            item = i.split('|')
            id_enemy = int(item[-1])
            position = []
            coordinates = item[0].split('-')
            for coordinate in coordinates:
                if coordinate:
                    x, y = coordinate.split(',')
                    position.append((x, y))
            enemies_pos.append((id_enemy, position))
        return dict(enemies_pos)  # {'0': [<utils.position.Position object at 0x7f8cc6206a00>, <utils.position.Position object at 0x7f8cc6206ac0>, <utils.position.Position object at 0x7f8cc6206b50>]}

    def update_data(self, body_pos):
        print('body pos recebindo em send client:', body_pos)
        self.soc.send(str(body_pos).encode())  # '0,1-1,1-2,1-' enviando para PlayerConnection().run
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')  # recebendo de...
        print('resp recebido no soc:', resp)
        for snake in resp.split(';'):
            snake_id = snake[-1]
            snake = snake[:-3]  # 1,10-20,10-19,10--1 -> 1,10-20,10-19,10
            print('snake body: ', snake)
            coordinates = []
            for body_part in snake.split('-'):
                x, y = body_part.split(',')
                coordinates.append((x, y))
            enemies_pos.append((int(snake_id), coordinates))
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

