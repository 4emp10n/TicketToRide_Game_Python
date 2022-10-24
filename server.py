import socket
from _thread import *
import pickle

server = "192.168.178.43"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")

#players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 255))]


def thread_client(conn, player):
    conn.send(str.encode("Connected"))
    #conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            #data = pickle.loads(conn.recv(2048))
            data = conn.receive(1024).decode()
            #players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = "Hello player 1"
                else:
                    reply = "Hello player 2"
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(reply)
        except:
            break

    print("Loss connection")
    conn.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(thread_client, (conn, currentPlayer))
    currentPlayer += 1
