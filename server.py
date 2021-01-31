import socket
from Settings import PORT

class Server(object):

    def __init__(self):
        
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('localhost', PORT))
        soc.listen(1)
        conection, adress = soc.accept()
        print('Connection Accepted with: ', adress)
        while True:
            data = conection.recv(1024)
            print(data)
            if not data:
                break


if __name__ == '__main__':
    serverObj = Server()