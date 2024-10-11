# 2D tic-tac-toe game 3 × 3 with random AI
# human starts

import random


def draw_the_field(_field_):
    print(f'{field[0]} {field[1]} {field[2]}')
    print(f'{field[3]} {field[4]} {field[5]}')
    print(f'{field[6]} {field[7]} {field[8]}')


def check_the_win(_player_, _field_):
    # check for a filled column/row
    for i in range(3):  # columns
        if sum(_field_[i + j] == _player_ for j in range(0, 7, 3)) == 3:
            draw_the_field(field)
            print(f'Player {"1" if _player_ == "X" else "2"} has won!')
            return True
    for i in range(0, 7, 3):  # rows
        if sum(_field_[i + j] == _player_ for j in range(3)) == 3:
            draw_the_field(field)
            print(f'Player {"1" if _player_ == "X" else "2"} has won!')
            return True

    # check for a filled diagonal
    if sum(_field_[i] == _player_ for i in range(0, 9, 4)) == 3:  # ↘
        draw_the_field(field)
        print(f'Player {"1" if _player_ == "X" else "2"} has won!')
        return True
    if sum(_field_[j] == _player_ for j in range(2, 8, 2)) == 3:  # ↗
        draw_the_field(field)
        print(f'Player {"1" if _player_ == "X" else "2"} has won!')
        return True

    return False


def player_turn():
    turn = int(input())
    field[turn - 1] = 'X'
    free_tiles.remove(turn)


def computers_turn():
    turn_ai = random.choice(free_tiles)
    field[turn_ai - 1] = 'O'
    free_tiles.remove(turn_ai)


free_tiles = [n + 1 for n in range(9)]
field = [n + 1 for n in range(9)]
game_over = False

players = ('player', 'computer')
who_starts = random.choice(players)

if who_starts == 'player':
    while not game_over:
        draw_the_field(field)

        if not free_tiles:
            print('It\'s a draw!')
            break

        player_turn()
        game_over = check_the_win('X', field)
        if game_over:
            break

        computers_turn()
        game_over = check_the_win('O', field)
else:
    while not game_over:
        if not free_tiles:
            print('It\'s a draw!')
            break

        computers_turn()
        game_over = check_the_win('O', field)
        if game_over:
            break

        draw_the_field(field)

        player_turn()
        game_over = check_the_win('X', field)
