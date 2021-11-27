import socket

from position import Position
from Settings import PORT


class Client(object):

    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.soc.connect(('localhost', PORT))
        pos = Position(self.soc.recv(1024).decode('utf-8'))
        return pos

    def wait_start(self):
        self.soc.send(b"waiting")
        resp = self.soc.recv(1024).decode('utf-8')
        if resp == 'start':
            return None

        enemies_pos = []
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(item[0], item[1])))
        return dict(enemies_pos)

    def send(self, pos):
        self.soc.send(str(pos).encode())
        enemies_pos = []
        resp = self.soc.recv(1024).decode()
        for i in resp.split(';'):
            item = i.split(',')
            enemies_pos.append((item[2], Position(item[0], item[1])))
        return dict(enemies_pos)
