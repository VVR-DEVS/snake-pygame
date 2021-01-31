import socket as sockt
from Settings import PORT

class Server(object):

    def __init__(self):
        
        with sockt.socket(sockt.AF_INET, sockt.SOCK_STREAM) as socket:
            socket.bind(('localhost', PORT))
            socket.listen()
            conection, adress = socket.accept()
            with conection:
                print(adress)
                while True:
                    data = conection.recv(1024)
                    if not data:
                        break
                    conection.sendall(data)
                    
   
if __name__ == '__main__':
    serverObj = Server()