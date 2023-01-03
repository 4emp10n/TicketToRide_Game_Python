import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "35.158.118.91"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = int(self.connect())

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, deckCards):
        try:
            self.client.send(pickle.dumps(deckCards))
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            self.client.settimeout(0.1)
            return pickle.loads(self.client.recv(2048))
        except:
            return -1
        finally:
            self.client.setblocking(True)

    def close(self):
        self.client.close()
