import socket
import random


class PlayerHandler:
    def __init__(self, conn, players):
        self.conn = conn
        self.role = random.randint(0, 1) if(len(players) == 0) else 1 - players[0].role
        self.turn = random.randint(0, 1) if(len(players) == 0) else 1 - players[0].turn
        self.id = 0 if len(players) == 0 else 1

        # send the player his role (sprite) and whether he starts
        self.send(f"{self.role} {self.turn}")

    # send the player a 'start game' note
    def start(self):
        self.send("start")

    # send any data to player
    def send(self, data):
        self.conn.sendall(str.encode(data))

    # recieve data from player
    def recieve_stream(self):
        return self.conn.recv(1024).decode('utf-8')
