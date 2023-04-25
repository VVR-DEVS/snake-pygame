import socket
import os
from time import sleep
from threading import Thread
from utils import Position
from elements.snake import Snake
from server.match import Match

from utils import PORT, HOST


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

        try:
            self.soc.listen(5)

            connections = Thread(target=self.receiving_connections)
            self.state = self.RUNNING
            connections.start()
        except KeyboardInterrupt:
            print('\nServer Initialization Closed By Keyboard')
            self.close()
        except Exception as e:
            print('Server Initialization Exception:', e)
            self.close()

        self.run()

    def receiving_connections(self):
        print('Server initialized.', '\nWaiting for connections...\n')
        try:
            while self.state == self.RUNNING:
                # Receiving Connection
                connection, address = self.soc.accept()
                print('Connection Accepted with: ', address)
                connection.send(b'connected')

                # Receiving Expected Type Match
                num_player_match = int(connection.recv(1024).decode('utf-8'))
                print('Searching Match...\n')
                encontrado = False
                for match in self.matches:
                    if num_player_match == match.num_players and len(match.players) < match.num_players and\
                            match.state != match.STARTED:
                        encontrado = True
                        match.add_player(connection, address)
                        break
                        
                # Start New Match
                if not encontrado:
                    self.matches.append(Match(self.next_match_id, num_player_match, connection, address,
                                              self.close_match))
                    self.matches[-1].start()
                    self.next_match_id += 1
        except Exception as e:
            print('Server Start Connections Exception:', e)

    def run(self):
        try:
            stop_print = False
            while self.state == self.RUNNING:
                sleep(5)
                if not stop_print:
                    if len(self.matches) == 0:
                        stop_print = True
                    print('\n====================================================>')
                    print('Running ', len(self.matches), ' matches:')
                    for match in self.matches:
                        print('    | ', match)
                    print('====================================================>')
                    print('\n')

                elif stop_print and len(self.matches) > 0:
                    stop_print = False
                
        except KeyboardInterrupt:
            print('\nServer Closed By Keyboard')
            self.close()
        except Exception as e:
            print('Server Run Exception:', e)

    def close_match(self, match_id):
        for i, match in enumerate(self.matches):
            if match.id == match_id:
                self.matches.pop(i)
                break

    def close(self):
        print('Closing Connections')
        self.state = self.CLOSING
        for match in self.matches:
            match.close_match()
        self.soc.close()
        print('Connections Closed')
        os._exit(1)


def start_server():
    try:
        Server()
    except Exception as e:
        print('Server :', e)
