class Position:
    
    x = None
    y = None

    def __init__(self, pos):
        if pos is not None:
            self.x, self.y = map(int, pos.split(','))

    def set(x, y):
        self.x = x
        self.y = y
    
    def get():
        return self.x, self.y
    
    def __str__():
        return str(self.x) + "," + str(self.y)