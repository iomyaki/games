# 2D tic-tac-toe game n × n for 2 human players

def draw_the_field(_field_):
    for y in range(size):
        print(f'{size - 1 - y} {" ".join(_field_[x][size - 1 - y] for x in range(size))}')
    print(f'  {" ".join(map(str, range(size)))}')


def make_a_turn(_player_, _field_):
    inlet = input(f'Player {"1" if _player_ == "X" else "2"}, it\'s your turn: ')

    # exit the game check NOT WORKING
    #if inlet == 'stop':
        #game_over = True
        #return exec('break')

    # check the input format correctness
    try:
        coord = tuple(map(int, inlet.split(' ')))
    except ValueError:
        print('Incorrect input format! Try again')
        return make_a_turn(_player_, _field_)

    if coord[0] > size - 1 or coord[1] > size - 1:
        print('Incorrect input format! Try again')
        return make_a_turn(_player_, _field_)

    # check if this tile is free
    if _field_[coord[0]][coord[1]] != '□':
        print('This tile is already taken! Try another one')
        return make_a_turn(_player_, _field_)

    # put a symbol into the corresponding tile
    _field_[coord[0]][coord[1]] = _player_


def check_the_win(_player_, _field_):
    # check for a filled column/row
    for column in _field_:
        if sum(column[x] == _player_ for x in range(size)) == size:
            print(f'Player {"1" if _player_ == "X" else "2"} has won!')
            return True
    for row in zip(*_field_):
        if sum(row[y] == _player_ for y in range(size)) == size:
            print(f'Player {"1" if _player_ == "X" else "2"} has won!')
            return True

    # check for a filled diagonal
    count_dgn1, count_dgn2 = 0, 0
    for i in range(size):
        count_dgn1 += (_field_[i][i] == _player_)
        count_dgn2 += (_field_[i][size - 1 - i] == _player_)
    if count_dgn1 == size or count_dgn2 == size:
        print(f'Player {"1" if _player_ == "X" else "2"} has won!')
        return True

    return False


# side of the field square
size = 3

field = [['□'] * size for x in range(size)]
player = 'X'
game_over = False
turn = 0

print('Let\'s play tic-tac-toe!\nTo make a turn, set tile\'s Ox and Oy coordinates separated by space: x y')
draw_the_field(field)
while not game_over:
    turn += 1

    # receive and check coordinates of a tile
    make_a_turn(player, field)

    # visualise the field
    draw_the_field(field)

    # check if the player has won
    if turn > 4:
        game_over = check_the_win(player, field)

    # check for a draw
    if turn == (size - 1) * 4 + 1:
        print('It\'s a draw!')
        game_over = True

    # change the player
    player = 'O' if player == 'X' else 'X'

# "Must have" improvements:
# 1) when entering an already taken tile; DONE
# 2) when input's format is incorrect; DONE
# 3) check if draw condition is correct for size > 3.

# Optional improvements:
# 1) sometimes a draw is obvious before the last turn (in case of 3x3 field);
# 2) maybe more elegant diagonal condition.
