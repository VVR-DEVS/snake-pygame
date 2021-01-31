import socket
from threading import Thread

from EnemiesSnake import EnemiesSnake
from Settings import PORT

class Server(Thread):

    soc = None

    def __init__(self, enemies):
        Thread.__init__(self)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(('localhost', PORT))
        self.enemies = enemies

    def run(self):
        self.soc.listen(1)
        while True:
            connection, adress = self.soc.accept()
            self.enemies.append(EnemiesSnake(connection, adress))
            self.enemies[-1].start()

    def close(self):
        self.soc.close


if __name__ == '__main__':
    serverObj = Server([])
    serverObj.start()