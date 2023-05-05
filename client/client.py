import socket
from utils.position import Position
from utils import PORT, HOST, GREEN
from elements.snake import Snake


class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send(self, data):
        self.connection.send(str(data).encode())
    
    def receive(self):
        rec = self.connection.recv(1024).decode('utf-8')
        if not rec:
            print('Connection Closed or Lost')
            return False
        return rec

    def connect(self, num_players_match):
        self.connection.connect((HOST, PORT))
        msg = self.receive()
        print('Connection Tried With Game Server: ', msg)

        # If Connected - search a mach
        if msg == 'connected':
            self.send(num_players_match)
        else:
            return False

        # receiving player position after mach found
        position_str = self.receive()
        position = Position(position_str)
        print('Match Found, Player Start Position', position)
    
        return position

    def wait_start(self):
        self.send("waiting")
        enemies_pos_data = self.receive()
        print("Waiting for Match Start ... | ", end='')

        if enemies_pos_data == 'start':
            print("All Players Ready, Match Start")
            return True
        elif enemies_pos_data == 'NEY':
            print("Waiting for Other Players to Join")
            return {}
        elif not enemies_pos_data:
            return False

        enemies_positions = enemies_pos_data.split(';')
        print("Receiving Enemies Positions", len(enemies_positions), 'players data loaded')

        # Snakes Enemies Positions Dictionary mounting
        enemies_pos = []
        for snake_str in enemies_positions:
            id_enemy = Snake.id_str(snake_str)
            enemies_pos.append((id_enemy, Snake(None, None, None, color=GREEN, id_player=id_enemy, body=snake_str)))
        
        return dict(enemies_pos)

    def update_data(self, body_pos):
        self.send(body_pos)
        print("\n\n===================================================")
        print("Sending Player data to Server", body_pos)

        # Receiving Enemies Positions Update
        resp = self.receive()
        if not resp:
            return False

        positions = resp.split(';')
        print("Enemies positions Update:", len(positions), 'players data received >>', resp, end='\n\n')

        # Snakes Enemies Positions Dictionary mounting
        enemies_pos = []
        for snake_str in positions:
            id_enemy = Snake.id_str(snake_str)
            enemies_pos.append((id_enemy, Snake(None, None, None, id_player=id_enemy, body=snake_str)))
        return dict(enemies_pos)

    def disconnect(self):
        self.connection.close()

