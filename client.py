import socket
from Settings import PORT


class Client(object):

    def __init__(self):

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(('localhost', PORT))
        while True:
            soc.send(input().encode())


if __name__ == '__main__':
    clientObj = Client()
