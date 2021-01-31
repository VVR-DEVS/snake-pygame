import socket
from threading import Thread

from Settings import PORT

class Server(object):

    connections = []

    def __init__(self):
        
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('localhost', PORT))
        soc.listen(1)
        while True:
            connection, adress = soc.accept()
            self.connections.append(ServerConnection(connection, adress))
            self.connections[-1].start()
        soc.close()

class ServerConnection(Thread):

    connection = None
    adress = None

    def __init__(self, connection, adress):
        Thread.__init__(self)
        self.connection = connection
        self.adress = adress
        print('Connection Accepted with: ', adress)
    
    def run(self):
        while True:
            data = self.connection.recv(1024)
            print(self.adress, '>>', data.decode())
            if not data:
                break
        self.connection.close()


if __name__ == '__main__':
    serverObj = Server()