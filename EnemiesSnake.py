import socket
from threading import Thread


class EnemiesSnake(Thread):

    connection = None
    adress = None

    def __init__(self, connection, adress):
        Thread.__init__(self)
        self.connection = connection
        self.adress = adress
        print('Connection Accepted with: ', adress)
    
    def run(self):
        while True:
            newPosX, newPosY = self.connection.recv(1024).decode('utf-8').split(',')    
            print('Poss:', newPosX, newPosY)
        self.connection.close()