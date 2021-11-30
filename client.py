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

    def send(self, pos):
        self.soc.send(str(pos).encode())
        enemies_pos = []
        resp = self.soc.recv(1024).decode('utf-8')
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(item[0], item[1])))
        return dict(enemies_pos)



