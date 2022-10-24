import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.178.43"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self):
        try:
            message = input(" -> ")
            self.client.send(message.encode())
        except socket.error as e:
            print(e)

    def recv(self):
        return self.client.recv(1024).decode()

    def close(self):
        self.client.close()
