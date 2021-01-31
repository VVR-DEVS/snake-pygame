import socket as sock
from Settings import PORT

class Client(object):

    def __init__(self):

        socket = sock.socket(sock.AF_NET, sock.SOCK_STREAM)
        socket.connect(('www.python.org', 80))
        



if __name__ == '__main__':
    clientObj = Client()