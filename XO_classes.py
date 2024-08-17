from sys import exit


class Player:
    def __init__(self, name):
        self.name = name
        self.choices = []

    def choose(self):
        self.choices.append(tuple(map(int, input(f'{self.name}, make your turn: ').split(' '))))


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game_over = False

    def win_conditions(self, player):
        for x in range(3):
            count_col, count_row = 0, 0
            for y in range(3):
                count_col += player.choices.count((x, y))
                count_row += player.choices.count((y, x))
            if count_col == 3 or count_row == 3:
                print(f'Player {player.name} has won!')
                self.game_over = True
                exit()

        if (1, 1) in player.choices and ((0, 0) in player.choices and (2, 2) in player.choices or
                                         (0, 2) in player.choices and (2, 0) in player.choices):
            print(f'Player {player.name} has won!')
            self.game_over = True
            exit()

    def play(self):
        while not self.game_over:
            self.player1.choose()
            self.win_conditions(self.player1)
            self.player2.choose()
            self.win_conditions(self.player2)


player1 = Player("Игрок 1")
player2 = Player("Игрок 2")
game = Game(player1, player2)
game.play()
