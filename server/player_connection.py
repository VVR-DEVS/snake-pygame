from elements.snake import Snake
from threading import Thread
from utils import Position

class PlayerConnection(Thread):
    WAITING = 0
    STARTING = 1
    PLAYING = 2

    def __init__(self, connection, address, id_player, max_player, get_enemies_pos, disconnected):
        Thread.__init__(self)
        self.id = id_player
        self.connection = connection
        self.address = address
        self.max_player = max_player

        # CallBack to Match Object Functions
        self.get_enemies_pos = get_enemies_pos
        self.disconnected = disconnected

        # Placing first player
        self.snake = Snake(Position(id_player + 1 * 20, 10), 3, Snake.UP)
        self.snake.id = self.id
        print('Player ' + str(self.id) + ' placed and waiting', self.snake.head())
        # Sending player data
        self.send(self.snake.head())

        self.isRunning = True
        self.state = self.WAITING

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
            self.state = self.STARTING
    
    def start_broadcast(self):
        self.receive()
        self.send('start')
        self.state = self.PLAYING
    
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
            while self.isRunning:
                if self.state == self.WAITING:
                    self.waiting_update()

                elif self.state == self.STARTING:
                    self.start_broadcast()

                elif self.state == self.PLAYING:
                    self.client_data_update()
                    self.sending_other_players_data()
                        
        except Exception as e:
            print('Player', self.id, ':', e)
            self.stop()
    
    def stop(self):
        self.connection.close()
        self.disconnected(self.id)
        self.isRunning = False

    @staticmethod
    def join_players_data(players_data_list):
        return ';'.join(players_data_list)