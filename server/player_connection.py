from elements.snake import Snake
from threading import Thread
from utils import Position

class PlayerConnection(Thread):

    def __init__(self, connection, adress, id_player, max_player, get_enemies_pos, close_match):
        Thread.__init__(self)
        self.id = id_player
        self.connection = connection
        self.adress = adress
        self.max_player = max_player

        # CallBack to Match Object Functions
        self.get_enemies_pos = get_enemies_pos
        self.close_match = close_match

        # Placing first player
        self.snake = Snake(Position(id_player + 1 * 20, 10), 3, Snake.UP)
        self.snake.id = self.id
        print('Player ' + str(self.id) + ' placed and waiting', self.snake.head())
        # Sending player data
        self.send(self.snake.head())

        self.state = "waiting"

    def send(self, data):
        self.connection.send(str(data).encode())
    
    def receive(self):
        return self.connection.recv(1024).decode('utf-8')
    
    def waiting_update(self):
        msg = self.receive()

        enemies_pos = self.get_enemies_pos(self.id)

        enemies_player_snakes = self.join_players_data(enemies_pos)
        if enemies_player_snakes == '':
            self.send('NEY') # Not Enemies Yet
        else:
            self.send(enemies_player_snakes)

        if len(enemies_pos) + 1 == self.max_player:
            self.state = 'starting'
    
    def start_broadcast(self):
        self.receive()
        self.send('start')
        self.state = 'playing'
    
    def client_data_update(self):
        client_player_snake_data = self.receive()

        # updating server snake structure
        self.snake.set_body(client_player_snake_data)
    
    def sending_other_players_data(self):
        # sending other players body positions updated
        enemies_player_snakes = self.get_enemies_pos(self.id)
        enemies_player_snakes = self.join_players_data(enemies_player_snakes)
        self.send(enemies_player_snakes)

    def run(self):
        try:
            while self.state == 'waiting':
                self.waiting_update()

            while self.state == 'starting':
                self.start_broadcast()

            try:
                while self.state == 'playing':
                    self.client_data_update()
                    self.sending_other_players_data()
                    
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

    @staticmethod
    def join_players_data(players_data_list):
        return ';'.join(players_data_list)