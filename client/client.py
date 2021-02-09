import socket
import errno
import sys
from _thread import *


class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 1999
        self.connected, self.conn = self.connect()

    def send_choice(self, role, x, y):
        self.send(f"choice {role} {x} {y}")

    # get role and whether player is first (turn)
    def get_role_turn(self):
        role, turn = self.recieve().split()
        return int(role), int(turn)

    # wait for start game packet, and start game
    def start(self, game):
        if self.recieve() == "start":
            start_new_thread(self.play, (game, ))
        return True

    # separate threaded function to manage the game
    def play(self, game):
        while self.connected:
            data = self.recieve_stream()
            game.get_data(data)

    # connect to the server
    def connect(self):
        # create the client socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try connect to the server
        try:
            sock.connect((self.host, self.port))
        except socket.error as e:
            if e.errno != errno.ECONNREFUSED:
                err = str(e)
            else:
                err = "Server is not running yet."
            sys.exit(err)
        return True, sock

    def send(self, data):
        self.conn.sendall(str.encode(data))

    # recieve one packet
    def recieve(self):
        data = None
        while not data:
            data = self.conn.recv(1024).decode('utf-8')
        return data

    def recieve_stream(self):
        return self.conn.recv(1024).decode('utf-8')
