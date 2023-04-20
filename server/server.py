import socket
from threading import Thread
from utils import Position
from elements.snake import Snake
from server.match import Match

from utils.settings import PORT, HOST


class Server:
    STARTING = 0
    RUNNING = 1
    CLOSING = 2

    def __init__(self):
        self.state = self.STARTING
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((HOST, PORT))

        self.next_match_id = 0
        self.matches = []

        self.state = self.RUNNING

        try:
            self.soc.listen(5)
            print('Server initialized.', '\nWaiting for conection...\n')
            while self.state == self.RUNNING:
                connection, adress = self.soc.accept()
                print('Connection Accepted with: ', adress)
                connection.send(b'connected')
                num_player_match = int(connection.recv(1024).decode('utf-8'))
                print('Searching Match...\n')
                encontrado = False
                for match in self.matches:
                    if num_player_match == match.num_players and len(match.players) < match.num_players and\
                            match.state != match.STARTED:
                        encontrado = True
                        match.add_player(connection, adress)
                        break

                if not encontrado:
                    self.matches.append(Match(self.next_match_id, num_player_match, connection, adress,
                                              self.close_match))
                    self.next_match_id += 1

        except Exception as e:
            print('Server:', e)
            self.close()

    def close_match(self, match_id):
        for i, match in enumerate(self.matches):
            if match.id == match_id:
                self.matches.pop(i)

    def close(self):
        print('Clossing Connections')
        self.soc.close()
        raise SystemExit()


def start_server():
    try:
        Server()
    except Exception as e:
        print('Server :', e)


if __name__ == '__main__':
    start_server()
