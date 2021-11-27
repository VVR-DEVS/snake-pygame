import socket
from threading import Thread
from position import Position

from Settings import PORT


class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(('localhost', PORT))

    def run(self):
        self.soc.listen(1)
        while True:
            connection, adress = self.soc.accept()
            self.spielen.append(
                PlayerConnection(connection, adress, self.enemies, len(self.players), self.get_spieler_pos()))
            self.spielen[-1].start()

    def get_spielen_pos(idSpielen):
        positions = []
        for i in range(len(self.spielen)):
            pos.append(self.spielen[i].pos)
        return pos

    def close(self):
        self.soc.close


class PlayerConnection(Thread):

    def __init__(self, connection, adress, idSpieler, get_spielen_pos):
        Thread.__init__(self)
        self.idSpieler = idSpieler
        self.connection = connection
        self.adress = adress
        self.get_spielen_pos = get_spielen_pos
        print('Connection Accepted with: ', adress)
        self.connection.send(b'10,10')
        self.pos = Position('10,10')
        self.state = "waiting"

    def run(self):
        while self.state == 'waiting':
            msg = self.connection.recv(1024).decode('utf-8')
            self.connection.send(self.format_spielen_pos(self.get_spielen_pos()).decode())

            if len(self.get_spielen_pos()) is num_players_on_match:
                self.state = 'starting'

        while True:
            newPosX, newPosY = self.connection.recv(1024).decode('utf-8').split(',')  # Recebe posicão Player
            print('Snake (' + self.idSpieler + '):', newPosX, newPosY)
            self.pos = self.pos.set(newPosX, newPosY)
            self.connection.send(
                self.format_spielen_pos(self.get_spielen_pos()).decode())  # manda posição inimigo "0,0,1; 0,012"

        self.connection.close()

    def format_spielen_pos():
        pass


if __name__ == '__main__':
    serverObj = Server([])
    serverObj.start()
