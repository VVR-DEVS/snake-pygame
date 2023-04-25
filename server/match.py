from time import sleep
from threading import Thread

from elements.snake import Snake
from server.player_connection import PlayerConnection
from utils import Position

class Match(Thread):
    WAITING = 0
    STARTED = 1
    STOPPED = 2

    def __init__(self, id_match, num_players, fist_player_connection, fist_player_address, close_match_function):
        Thread.__init__(self)
        self.id = id_match
        self.close_match_server = close_match_function

        print('New Match(' + str(self.id) + ') Initialized')

        self.num_players = num_players
        self.players = []
        self.players.append(PlayerConnection(fist_player_connection, fist_player_address, len(self.players),
                                             self.num_players, self.get_enemies_body, self.player_disconnected))

        print('Match(' + str(self.id) + ') ... 1/' + str(self.num_players) + ' players connected.\n')

        self.players[-1].start()
        self.state = self.WAITING

    def add_player(self, connection, address):
        self.players.append(PlayerConnection(connection, address, len(self.players), self.num_players, self.get_enemies_body,
                                             self.player_disconnected))
        print('Match(' + str(self.id) + ') ... ' + str(len(self.players)) + '/' + str(self.num_players) +
              ' players connected.')
        
        self.players[-1].start()
        if len(self.players) == self.num_players:
            self.state = self.STARTED
            print('Match(' + str(self.id) + ') started')
        print()

    def get_enemies_body(self, id_player):
        positions = []
        for player in self.players:
            if player.id != id_player:
                positions.append(str(player.snake))
        return positions
    
    def player_disconnected(self, id_player):
            print('Player (' + str(id_player) + ') Disconnected')
            for pl in self.players:
                if pl.id == id_player:
                    self.players.remove(pl)
                    break
            if len(self.players) == 1:
                self.close_match()

    def close_match(self):
        self.state = self.STOPPED
        for pl in self.players:
            pl.stop()
        print('Match(' + str(self.id) + ') Ended')
        self.close_match_server(self.id)
    
    def run(self):
        # while self.state != self.STOPPED:
        #     sleep(5)
        #     print('Match ' + str(self.id) + ' Running: ', str(len(self.players)), '/', str(self.num_players), 'players')
        pass
    
    def str_state(self):
        if self.state == self.WAITING:
            return 'Waiting'
        elif self.state == self.STARTED:
            return 'Started'
        else:
            return 'Stopped'

    def __str__(self):
        return 'Match(' + str(self.id) + ') - ' + self.str_state() + ' - ' + str(len(self.players)) + '/' + str(self.num_players) + ' players'
