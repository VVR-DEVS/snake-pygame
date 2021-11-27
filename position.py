class Position:
    x = None
    y = None

    def __init__(self, *args):
        if len(args) == 1:
            self.x, self.y = map(int, args[0].split(','))
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise Exception('Argumento inválido em Position')

    def set(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y

    def __str__(self):
        return str(self.x) + "," + str(self.y)
