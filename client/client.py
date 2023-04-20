import socket
from utils.position import Position
from utils.settings import PORT, HOST
from elements.snake import Snake


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
        position_str = self.soc.recv(1024).decode('utf-8')
        print('Client Snake Position', position_str)
        pos = Position(position_str)
        return pos

    def wait_start(self):
        self.soc.send(b"waiting")
        enemies_pos_data = self.soc.recv(1024).decode('utf-8')

        if enemies_pos_data == 'start':
            return None
        if enemies_pos_data == 'NEY':
            return {}

        enemies_pos = []
        for snake_str in enemies_pos_data.split(';'):
            id_enemy = Snake.id_str(snake_str)
            enemies_pos.append((id_enemy, Snake(None, None, None, id_player=id_enemy, body=snake_str)))
        return dict(enemies_pos)

    def update_data(self, body_pos):
        print('body pos recebindo em send client:', body_pos)
        self.soc.send(str(body_pos).encode())
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')
        print('resp recebido no soc:', resp)
        for snake_str in resp.split(';'):
            id_enemy = Snake.id_str(snake_str)
            enemies_pos.append((id_enemy, Snake(None, None, None, id_player=id_enemy, body=snake_str)))
        return dict(enemies_pos)

    def send_signal(self, signal):
        self.soc.send(signal.encode())
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(item[0], item[1])))
        return dict(enemies_pos)

    def disconnect(self):
        self.soc.close()

