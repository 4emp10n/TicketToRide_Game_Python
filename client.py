import socket
from network import Network

def client_program():

    net = Network()
    net.connect()

    while True:
        net.send()
        #client_socket.send(message.encode())  # send message
        #data = client_socket.recv(1024).decode()  # receive response
        data = net.recv()
        print('Received from server: ' + data)  # show in terminal
        net.send()
    net.close()

if __name__ == '__main__':
    client_program()