import socket
from threading import Thread
from utils.position import Position, BodyPosition

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
                    if num_player_match == match.num_players and len(match.spielen) < match.num_players and\
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


class Match:
    WAITING = 0
    STARTED = 1

    def __init__(self, id_match, num_players, fist_player_connection, fist_player_adrres, close_match_function):
        self.id = id_match
        self.close_match_server = close_match_function
        print('New Match(' + str(self.id) + ') Initialized')
        self.num_players = num_players
        self.spielen = []
        self.spielen.append(PlayerConnection(fist_player_connection, fist_player_adrres, len(self.spielen),
                                             self.num_players, self.get_enemies_pos, self.close_match))
        print('Match(' + str(self.id) + ') ... 1/' + str(self.num_players) + ' players connected.\n')
        self.spielen[-1].start()
        self.state = self.WAITING

    def add_player(self, connection, adress):
        self.spielen.append(PlayerConnection(connection, adress, len(self.spielen), self.num_players, self.get_enemies_pos,
                                             self.close_match))
        print('Match(' + str(self.id) + ') ... ' + str(len(self.spielen)) + '/' + str(self.num_players) +
              ' players connected.')
        self.spielen[-1].start()
        if len(self.spielen) == self.num_players:
            self.state = self.STARTED
            print('Match(' + str(self.id) + ') started')
        print()

    def get_enemies_pos(self, id_spieler):
        positions = []
        for spieler in self.spielen:
            if spieler.id != id_spieler:
                for spieler_body_part in spieler.body.body:
                    positions.append(','.join([str(spieler.pos), str(spieler.id)]))
        return positions

    def close_match(self, id_spieler):
        if id_spieler is not None:
            print('Player (' + id_spieler + ') Disconnected')
            self.close_match_server(self.id)
            print('Match(' + self.id + ') Ended')
        else:
            print('Match(' + self.id + ') Ended')
            self.close_match_server(self.id)


class PlayerConnection(Thread):

    def __init__(self, connection, adress, id_player, max_player, get_enemies_pos, close_match):
        Thread.__init__(self)
        self.id = id_player
        self.connection = connection
        self.adress = adress
        self.max_player = max_player
        self.get_enemies_pos = get_enemies_pos
        self.close_match = close_match
        self.pos = Position(id_player + 1 * 20, 10)
        self.body = BodyPosition([(id_player + 1 * 20, 10)])
        self.connection.send(str(self.pos).encode())
        self.state = "waiting"

    def run(self):
        try:
            while self.state == 'waiting':
                self.connection.recv(1024).decode('utf-8')  # recebendo de Client().wait_start
                # print('Snake (' + str(self.id) + ') says :', msg)
                enemies_pos = self.get_enemies_pos(self.id)
                enemis_pos_data = self.format_spielen_pos(enemies_pos)
                if enemis_pos_data == '':
                    self.connection.send('NEY'.encode())
                else:
                    self.connection.send(enemis_pos_data.encode())

                if len(enemies_pos) + 1 == self.max_player:
                    self.state = 'starting'

            while self.state == 'starting':
                msg = self.connection.recv(1024).decode('utf-8')
                # print('Snake (' + str(self.id) + ') says :', msg)
                self.connection.send('start'.encode())
                self.state = 'playing'

            try:
                while self.state == 'playing':
                    # newPosX, newPosY = self.connection.recv(1024).decode('utf-8').split(',')  # Recebe posição Player
                    newPos = self.connection.recv(1024).decode('utf-8')  # Recebe pos completa do Player de client().send
                    # print('Snake (' + str(self.id) + '):', newPosX, newPosY)
                    # self.pos.set(newPosX, newPosY)
                    # self.connection.send(self.format_spielen_pos(self.get_enemies_pos(self.id)).encode())  # manda posição inimigo "0,0,1; 0,012"
                    self.connection.send(f'{newPos}-{self.id}'.encode())  # '0,1-1,1-2,1-|1' último número é o id | manda para...
            except Exception as e:
                print(e)
                print('Conexão com o cliente perdida.')
                self.close_match(self.id)

            self.connection.close()
            self.close_match(None)
        except Exception as e:
            print('Player', self.id, ':', e)
            self.connection.close()
            self.close_match(None)

    def format_spielen_body_pos(self, body_pos):  # '0,1-1,1-2,1-' -> [(0, 1), (1, 1), (2, 1)]
        body_pos_list = []
        for coordinate in body_pos.split('-'):
            posX, posY = coordinate.split(',')
            body_pos_list.append((posX, posY))
        return body_pos_list

    @staticmethod
    def format_spielen_pos(positions):
        return ';'.join(positions)


def start_server():
    try:
        Server()
    except Exception as e:
        print('Server :', e)


if __name__ == '__main__':
    start_server()
