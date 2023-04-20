from elements.snake import Snake
from server.player_connection import PlayerConnection
from utils import Position

class Match:
    WAITING = 0
    STARTED = 1

    def __init__(self, id_match, num_players, fist_player_connection, fist_player_adrres, close_match_function):
        self.id = id_match
        self.close_match_server = close_match_function
        print('New Match(' + str(self.id) + ') Initialized')
        self.num_players = num_players
        self.players = []
        self.players.append(PlayerConnection(fist_player_connection, fist_player_adrres, len(self.players),
                                             self.num_players, self.get_enemies_body, self.close_match))
        print('Match(' + str(self.id) + ') ... 1/' + str(self.num_players) + ' players connected.\n')
        self.players[-1].start()
        self.state = self.WAITING

    def add_player(self, connection, adress):
        self.players.append(PlayerConnection(connection, adress, len(self.players), self.num_players, self.get_enemies_body,
                                             self.close_match))
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
                print('Body of the enemy:', player.snake)
                positions.append(str(player.snake))
        return positions

    def close_match(self, id_player):
        if id_player is not None:
            print('Player (' + str(id_player) + ') Disconnected')
            self.close_match_server(self.id)
            print('Match(' +  str(self.id) + ') Ended')
        else:
            print('Match(' + str(self.id) + ') Ended')
            self.close_match_server(self.id)