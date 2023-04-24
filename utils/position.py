import random
class Position:
    x = None
    y = None

    def __init__(self, *args):
        if len(args) == 1:
            self.x, self.y = map(int, args[0].split(','))
        elif len(args) == 2:
            self.x = int(args[0])
            self.y = int(args[1])
        else:
            raise Exception('Argumento inválido em Position')

    def set(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def get(self):
        return self.x, self.y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # indexing position
    def __getitem__(self, index):
        return self.x if index % 2 == 0 else self.y    

    def __str__(self):
        return str(self.x) + "," + str(self.y)
    
    @staticmethod
    def random_position(min_x, min_y, max_x, max_y):
        return Position(random.randint(min_x, max_x), random.randint(min_y, max_y))
