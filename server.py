import socket
from _thread import *

# get the hostname
host = "192.168.178.43"
port = 5555  # initiate port no above 1024

server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(2)


# conn, address = server_socket.accept()  # accept new connection

def thread_client(conn, player):
    print("thread_client")
    print("Connection from: " + str(conn))
    while True:

        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    currentPlayer = 0
    while True:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        start_new_thread(thread_client, (conn, currentPlayer))
        currentPlayer += 1
