import socket
import os
from _thread import *
import errno
import sys
from game_logic import GameLogic


class Server:
    def __init__(self, game_logic):
         self.host = '127.0.0.1'
         self.port = 1999
         self.sock = self.connect()
         self.players_count = 0
         self.logic = game_logic

    def connect(self):
        # create the server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try to allocate an address for the server
        try:
            sock.bind((self.host, self.port))
        except socket.error as e:
            if e.errno != errno.EADDRINUSE:
                err = str(e)
            else:
                err = "Server already running or port is pre-used."
            sys.exit(err)
        sock.listen()
        print('server is listening..')
        return sock

    # server loop
    def serve(self):
        while True:
            if self.players_count < 2:
                client, address = self.sock.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                try:
                    # create new thread for each new client
                    start_new_thread(self.client_thread, (client, ))
                except:
                    self.sock.close()
                self.players_count += 1
                print('Players Count: ' + str(self.players_count))

    def client_thread(self, client):
        self.logic.start_player(client)


if __name__ == '__main__':
    try:
        logic = GameLogic()
        Server(logic).serve()
    except KeyboardInterrupt:
        sys.exit("\nBye!")
