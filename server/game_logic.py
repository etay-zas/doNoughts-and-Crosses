from player_handler import PlayerHandler


class GameLogic:
    def __init__(self):
        self.players = []
        self.squares = [[None for x in range(3)] for y in range(3)]
        self.finished = False

    # threaded function to start and add a new player
    def start_player(self, client):
        player = PlayerHandler(client, self.players)
        self.players.append(player)
        # wait untill two players are in the game
        while len(self.players) < 2:
            pass
        self.play(player)

    # check if a player won
    def check_win(self, player):
        for i in range(3):
            if player.role == self.squares[i][0] == self.squares[i][1] == self.squares[i][2] or player.role == self.squares[0][i] == self.squares[1][i] == self.squares[2][i]:
                return True
        if player.role == self.squares[0][0] == self.squares[1][1] == self.squares[2][2] or player.role == self.squares[2][0] == self.squares[1][1] == self.squares[0][2]:
            return True
        return False

    def check_board_full(self):
        for y in range(3):
            for x in range(3):
                if self.squares[x][y] == None:
                    return False
        return True


    # main loop for game server logic
    def play(self, player):
        player.start()
        while not self.finished:
            data = player.recieve_stream()
            if data:
                data_arr = data.split()
                key = data_arr[0]
                if key == "choice":
                    key, role, x, y = data.split()
                    role, x, y = int(role), int(x), int(y)
                    # check if the chosen square is empty
                    if self.squares[x][y] == None:
                        self.squares[x][y] = role
                        self.players[1-player.id].send(f"chose {x} {y}")
                        # check if current player won
                        if self.check_win(player):
                            self.players[player.id].send("finish 1")
                            self.players[1-player.id].send("finish 0")
                        # check if board is full. if so, finish with tie
                        elif self.check_board_full():
                            self.players[player.id].send("finish 2")
                            self.players[1-player.id].send("finish 2")
