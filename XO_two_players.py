from sys import exit


def draw_the_field(_field_):
    for i in range(3):
        print(f'{2 - i} {_field_[0][2 - i]} {_field_[1][2 - i]} {_field_[2][2 - i]}')
    print('  0 1 2')


def make_a_turn(_players_, _player_, _field_):
    inlet = input(f'Player {_players_.index(_player_) + 1}, it\'s your turn: ')

    # exit the game check
    if inlet == 'stop':
        exit()

    # check the input format correctness
    try:
        coord = tuple(map(int, inlet.split(' ')))
    except ValueError:
        print('Incorrect input format! Try again')
        return make_a_turn(_players_, _player_, _field_)

    if coord[0] > 2 or coord[1] > 2:
        print('Incorrect input format! Try again')
        return make_a_turn(_players_, _player_, _field_)

    # check if this tile is free
    if coord in _players_[0] or coord in _players_[1]:
        print('This tile is already taken! Try another one')
        return make_a_turn(_players_, _player_, _field_)

    # add the tile to player's list
    _player_.append(coord)

    # put a symbol into the corresponding tile
    _field_[coord[0]][coord[1]] = 'X' if _players_.index(_player_) == 0 else 'O'


def check_the_win(_players_, _player_):
    # check for a filled column/row
    for x in range(3):
        count_col, count_row = 0, 0
        for y in range(3):
            count_col += _player_.count((x, y))
            count_row += _player_.count((y, x))
        if count_col == 3 or count_row == 3:
            print(f'Player {_players_.index(_player_) + 1} has won!')
            exit()

    # check for a filled diagonal
    if (1, 1) in _player_ and ((0, 0) in _player_ and (2, 2) in _player_ or (0, 2) in _player_ and (2, 0) in _player_):
        print(f'Player {_players_.index(_player_) + 1} has won!')
        exit()


players = ([], [])
field = [['□'] * 3 for j in range(3)]

print('Let\'s play tic-tac-toe!')
print('To make a turn, set tile\'s Ox and Oy coordinates separated by space: x y\nTo stop the game, print: stop')
draw_the_field(field)
for k in range(5):
    # check for a draw
    if k == 4:
        print('It\'s a draw!')
        exit()

    for player in players:
        # receive and check coordinates of a tile
        make_a_turn(players, player, field)

        # visualise the field
        draw_the_field(field)

        # check if the player has won
        check_the_win(players, player)

# "Must have" improvements:
# 1) when entering an already taken tile; DONE
# 2) when input's format is incorrect. DONE

# Optional improvements:
# 1) sometimes a draw is obvious before the fifth round;
# 2) maybe smarter diagonal condition, not just enumeration of tiles.
