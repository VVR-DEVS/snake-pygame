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
        self.x = int(x)
        self.y = int(y)

    def get(self):
        return self.x, self.y

    def __str__(self):
        return str(self.x) + "," + str(self.y)


class BodyPosition:

    def __init__(self, body_pos):  # [(0, 1), (1, 1), (2, 1)]
        self.body = body_pos

    def set(self, body_pos):
        self.body = body_pos

    def get(self):
        return self.body

    def __str__(self):
        body_pos = ''
        for i in self.body:
            body_pos += f'{i[0]},{i[1]}-'  # '0,1-1,1-2,1-'
        return body_pos
