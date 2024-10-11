# 2D tic-tac-toe game 3 × 3 with perfect AI, player starts

from sys import exit
from random import choice


def draw_the_field(_field_):
    for n in range(0, 7, 3):
        print(f'{field[n]} {field[n + 1]} {field[n + 2]}')


def two_of_three(_mode_):
    for win_line in win_lines:
        if sum(field[i] == ('X' if _mode_ == 'defense' else 'O') for i in win_line) == 2 and \
                sum(field[i] == ('X' if _mode_ == 'offense' else 'O') for i in win_line) == 0:
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
    # visualise the field
    draw_the_field(field)

    # player's turn
    turn = int(input())
    field[turn] = 'X'
    free.remove(turn)
    if game_round < 3:
        X_turns.append(turn)

    # check for a draw
    if not free:
        draw_the_field(field)
        print('It\'s a draw!')
        break

    # computer's turn
    # # check the possibility to win this turn
    if two_of_three('offense'):
        for tile in two_of_three('offense'):
            if field[tile] != 'O':
                field[tile] = 'O'
                draw_the_field(field)
                print('Noughts have won!')
                exit()
    # # check the threat to lose next turn
    elif two_of_three('defense'):
        for tile in two_of_three('defense'):
            if field[tile] != 'X':
                field[tile] = 'O'
                free.remove(tile)
    # # tactics depending on player's previous turn(s)
    elif field[4] == 'X':
        if corners & free:
            turn = choice(list(corners & free))
            field[turn] = 'O'
            free.remove(turn)
        else:
            turn = choice(list(free))
            field[turn] = 'O'
            free.remove(turn)
    elif game_round == 0:  # round one
        field[4] = 'O'
        free.remove(4)
    elif game_round == 1:  # round two
        if {X_turns[0]} & corners:
            if field[opp_corner[X_turns[0]]] != 'X':
                field[opp_corner[X_turns[0]]] = 'O'
                free.remove(opp_corner[X_turns[0]])
            else:
                turn = choice((1, 3, 5, 7))
                field[turn] = 'O'
                free.remove(turn)
        else:
            if {X_turns[1]} & corners:
                field[opp_corner[X_turns[1]]] = 'O'
                free.remove(opp_corner[X_turns[1]])
            elif X_turns[1] == opp_tile[X_turns[0]]:
                turn = choice(list(corners & free))
                field[turn] = 'O'
                free.remove(turn)
            else:
                if field[1] == 'X':
                    if field[3] == 'X':
                        field[0] = 'O'
                        free.remove(0)
                    if field[5] == 'X':
                        field[2] = 'O'
                        free.remove(2)
                if field[7] == 'X':
                    if field[3] == 'X':
                        field[6] = 'O'
                        free.remove(6)
                    if field[5] == 'X':
                        field[8] = 'O'
                        free.remove(8)
    else:
        turn = choice(list(free))
        field[turn] = 'O'
        free.remove(turn)
