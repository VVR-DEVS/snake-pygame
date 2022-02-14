from client.spiel import *
from server.server import start_server
import sys

print(sys.argv)
if len(sys.argv) > 1:
    if sys.argv[1] == 'runserver':
        start_server()
    else:
        raise Exception('Argumento inválido recebido')
else:
    g = Spiel()
    g.startbildschirm()

    while g.running:
        g.neueSpiel()

    pg.quit()
