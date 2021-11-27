import socket
from threading import Thread
from position import Position

from Settings import PORT, HOST


class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((HOST, PORT))
        self.spielen = []

    def run(self):
        try:
            self.soc.listen(5)
            print('Server Iniciado', 'Waiting Connection')
            while True:
                connection, adress = self.soc.accept()
                self.spielen.append(PlayerConnection(connection, adress, len(self.spielen), self.get_enemies_pos))
                self.spielen[-1].start()
        except Exception as e:
            print('Server:', e)
            self.close()

    def get_enemies_pos(self, id_spieler):
        positions = []
        for spieler in self.spielen:
            if spieler.id != id_spieler:
                positions.append(','.join([str(spieler.pos), str(spieler.id)]))
        return positions

    def close(self):
        print('Clossing Connections')
        self.soc.close()
        raise SystemExit()


class PlayerConnection(Thread):

    def __init__(self, connection, adress, id, get_enemies_pos):
        Thread.__init__(self)
        self.id = id
        self.connection = connection
        self.adress = adress
        self.get_enemies_pos = get_enemies_pos
        print('Connection Accepted with: ', adress)
        self.connection.send(b'10,10')
        self.pos = Position(10, 10)
        self.state = "waiting"

    def run(self):
        try:
            while self.state == 'waiting':
                msg = self.connection.recv(1024).decode('utf-8')
                print('Snake (' + str(self.id) + ') says :', msg)
                enemies_pos = self.get_enemies_pos(self.id)
                temp = self.format_spielen_pos(enemies_pos)
                if temp == '':
                    self.connection.send('NEY'.encode())
                else:
                    self.connection.send(temp.encode())

                if len(enemies_pos) + 1 == 2:
                    self.state = 'starting'

            while self.state == 'starting':
                msg = self.connection.recv(1024).decode('utf-8')
                print('Snake (' + str(self.id) + ') says :', msg)
                self.connection.send('start'.encode())
                self.state = 'playing'

            while self.state == 'playing':
                newPosX, newPosY = self.connection.recv(1024).decode('utf-8').split(',')  # Recebe posição Player
                print('Snake (' + str(self.id) + '):', newPosX, newPosY)
                self.pos.set(newPosX, newPosY)
                self.connection.send(self.format_spielen_pos(self.get_enemies_pos(self.id)).encode())  # manda posição inimigo "0,0,1; 0,012"

            self.connection.close()
        except Exception as e:
            print('Player', self.id, ':', e)
            self.connection.close()

    @staticmethod
    def format_spielen_pos(positions):
        return ';'.join(positions)


if __name__ == '__main__':
    serverObj = Server()
    try:
        serverObj.start()
    except Exception as e:
        print('Server :', e)
        serverObj.close()
