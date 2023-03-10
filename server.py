import socket
from _thread import *
from cards import *
import random
import pickle

# get the hostname
host = "192.168.178.43"
port = 5555  # initiate port no above 1024
server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together
# configure how many client the server can listen simultaneously
server_socket.listen(2)

# ===============DeckCards========================

deckCards = []


def randColor(colors):
    colorKey = random.choice(list(colors))
    return colors[colorKey]


for i in range(1, 6):
    deckCards.append(randColor(colors))

# ===============DeckCards========================

playersTurn = 1
wayName = ""


def thread_client(conn, player, clients):
    conn.send(pickle.dumps(player))  # send player id
    print("Sending player id({x})".format(x = player))
    global playersTurn
    global deckCards
    global wayName
    while True:
        request = pickle.loads(conn.recv(2048))
        print("Got request ({}) from player {}".format(request, player))
        if request == "Choose card":
            conn.send(pickle.dumps(playersTurn))
            print("Sending playerTurnInfo ({}) to player {}".format(playersTurn, player))
            clientsAnswer = pickle.loads(conn.recv(2048))
            print("Got clientsAnswer ({}) from player {}".format(clientsAnswer, player))
            if clientsAnswer == "OK" and playersTurn == 1:
                deckCards = pickle.loads(conn.recv(2048))
                print("Got deckCards ({}) from player {}".format(playersTurn, player))
            elif clientsAnswer == "OK" and playersTurn == 2:
                deckCards = pickle.loads(conn.recv(2048))
                print("Got deckCards ({}) from player {}".format(playersTurn, player))
            elif clientsAnswer == "NO":
                pass

        if request == "MakeMove":
            conn.send(pickle.dumps(playersTurn))
            print("Sending playerTurnInfo ({}) to player {}".format(playersTurn, player))
            clientsAnswer = pickle.loads(conn.recv(2048))
            print("Got clientsAnswer ({}) from player {}".format(clientsAnswer, player))
            if clientsAnswer == "OK" and playersTurn == 1:
                playersTurn = 2
                print("PlayersTurn changed to {}".format(playersTurn))
                wayName = pickle.loads(conn.recv(2048))
                print("Got wayName ({}) from player {}".format(wayName, player))
            elif clientsAnswer == "OK" and playersTurn == 2:
                playersTurn = 1
                print("PlayersTurn changed to {}".format(playersTurn))
                wayName = pickle.loads(conn.recv(2048))
                print("Got wayName ({}) from player {}".format(wayName, player))
            elif clientsAnswer == "NO":
                print("Player ({}) didn't select the way".format(player))
                pass
        if request == "GetWays":
            conn.send(pickle.dumps(wayName))
            print("Sending ways ({}) to player {}".format(wayName, player))
        if request == "GetCards":
            conn.send(pickle.dumps(deckCards))
            print("Sending cards ({}) to player {}".format(deckCards, player))
        if request == "GetTurn":
            conn.send(pickle.dumps(playersTurn))
            print("Sending PlayersTurn ({}) to player {}".format(playersTurn, player))

        # Doesnt use yet
        if request == "SendWay":
            wayName = pickle.loads(conn.recv(2048))
            print("Gow wayName ({}) from player {}".format(wayName, player))


    conn.close()  # close the connection


clients = []
if __name__ == '__main__':
    currentPlayer = 1

    while True:
        conn, addr = server_socket.accept()  # accept new connection
        clients.append(conn)
        print("Connected to:", addr)
        start_new_thread(thread_client, (conn, currentPlayer, clients))
        currentPlayer += 1
