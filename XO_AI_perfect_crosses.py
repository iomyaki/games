# 2D tic-tac-toe game 3 × 3 with perfect AI, computer starts

from sys import exit
from random import choice


def draw_the_field(_field_):
    for n in range(0, 7, 3):
        print(f'{field[n]} {field[n + 1]} {field[n + 2]}')


def two_of_three(_mode_):
    for win_line in win_lines:
        if sum(field[i] == ('O' if _mode_ == 'defense' else 'X') for i in win_line) == 2 and \
                sum(field[i] == ('O' if _mode_ == 'offense' else 'X') for i in win_line) == 0:
            return win_line
    return False


field = [0, 1, 2, 3, 4, 5, 6, 7, 8]
free = {tile for tile in range(9)}
X_turns = []
win_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
corners = {0, 2, 6, 8}
opp_corner = {0: 8, 2: 6, 6: 2, 8: 0}
opp_tile = {1: 7, 3: 5, 5: 3, 7: 1}

for game_round in range(6):
    # computer's turn
    # # check the possibility to win this turn
    if two_of_three('offense'):
        for tile in two_of_three('offense'):
            if field[tile] != 'X':
                field[tile] = 'X'
                draw_the_field(field)
                print('Crosses have won!')
                exit()
    # # check the threat to lose next turn
    elif two_of_three('defense'):
        for tile in two_of_three('defense'):
            if field[tile] != 'X':
                field[tile] = 'O'
                free.remove(tile)
    # # tactics depending on player's previous turn(s)
    elif game_round == 0:
        field[4] = 'X'
        free.remove(4)
    else:
        turn = choice(list(free))
        field[turn] = 'X'
        free.remove(turn)
