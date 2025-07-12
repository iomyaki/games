import atexit
import random
import sys
import time
from collections import deque
from copy import deepcopy
from datetime import datetime

from colorama import Fore, init as colorama_init, Style

AROUND_ALL = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
AROUND_CROSS = ((0, -1), (-1, 0), (0, 1), (1, 0))
AROUND_SALTIRE = ((-1, -1), (-1, 1), (1, 1), (1, -1))
DIRECTIONS = deque(["up", "right", "down", "left"])
COMPUTER_DEFAULT_TARGETS = deque(
    [
        [(0, 3), (6, 0)],
        [(0, 6), (3, 0), (6, 9), (9, 3)],
        [(3, 9), (9, 6)],
        [(2, 0), (7, 0), (9, 2)],
        [(0, 2), (0, 7), (2, 9), (7, 9)],
        [(0, 4), (9, 4)],
        [(0, 5), (4, 0), (4, 9), (5, 0), (5, 9), (9, 5)],
        [(7, 2)],
        [(7, 7), (9, 7)],
        [(2, 2), (2, 7)],
        [(2, 3), (2, 6), (3, 2), (6, 2), (6, 7), (7, 6)],
        [(3, 7), (7, 3)],
        [(3, 3), (6, 6)],
        [(3, 6)],
        [(1, 2), (2, 1), (2, 8), (7, 1), (8, 2), (8, 7)],
        [(1, 7), (6, 3), (7, 8)],
        [(0, 1), (0, 8), (1, 0), (1, 9), (8, 0), (8, 9), (9, 1), (9, 8)],
        [(2, 5), (4, 7), (5, 7)],
        [(2, 4), (4, 2), (5, 2), (7, 4), (7, 5)],
        [(4, 6), (5, 6), (6, 4), (6, 5)],
        [(3, 4), (3, 5), (4, 3), (5, 3)],
        [(1, 3), (1, 6), (3, 1)],
        [(3, 8), (6, 8), (8, 3), (8, 6)],
        [(6, 1)],
        [(1, 1)],
        [(8, 1), (8, 8)],
        [(1, 8)],
        [(4, 4), (4, 5), (5, 4), (5, 5)],
        [(4, 1)],
        [(1, 4), (1, 5), (4, 8), (5, 1), (5, 8), (8, 4), (8, 5)],
        [(0, 0), (0, 9), (9, 9)],
        [(9, 0)]
    ]
)

colorama_init()


class Player:
    def __init__(self, name: str, board):
        self.name = name
        self.board = board
        self.ships = 10

    def lose_ship(self):
        self.ships -= 1

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_board(self):
        return self.board

    def get_ships_number(self):
        return self.ships


class Ship:
    def __init__(self, owner: Player, hp: int):
        self.owner = owner
        self.hp = hp
        self.length = hp
        self.orientation = None
        self.coordinates = []
        self.status = "online"

    def get_owner(self):
        return self.owner

    def lose_hp(self):
        self.hp -= 1
        if self.hp <= 0:
            self.die()

    def die(self):
        self.status = "kia"
        self.get_owner().lose_ship()

    def set_orientation(self, orientation):
        self.orientation = orientation

    def add_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def get_hp(self):
        return self.hp

    def get_status(self):
        return self.status

    def get_length(self):
        return self.length

    def get_coordinates(self):
        self.coordinates.sort(key=lambda c: (c[0], c[1]))
        return self.coordinates


class Board:
    def __init__(self):
        self.board_ships: list[list[Ship | None]] = [[None for _ in range(10)] for _ in range(10)]
        self.board_inner_repr: list[list[str]] = [["O" for _ in range(10)] for _ in range(10)]
        self.board_outer_repr: list[list[str]] = [["O" for _ in range(10)] for _ in range(10)]

    def place_ship(self, *, ship: Ship, row: int, col: int, orientation: str):
        ship.set_orientation(orientation)
        row_factor, col_factor = (1, 0) if orientation == "v" else (0, 1)

        for i in range(ship.get_length()):
            row_coord = row + i * row_factor
            col_coord = col + i * col_factor

            ship.add_coordinates((row_coord, col_coord))
            self.set_ship_part(row_coord, col_coord, ship)
            self.set_inner_tile(row_coord, col_coord, "W")
            self.draw_shade(row_coord, col_coord)

    def draw_shade(self, row, col):
        for shade_row, shade_col in AROUND_ALL:
            if (
                0 <= row + shade_row <= 9 and
                0 <= col + shade_col <= 9 and
                self.get_inner_repr(row + shade_row, col + shade_col) == "O"
            ):
                self.set_inner_tile(row + shade_row, col + shade_col, "V")

    def clear_shades(self):
        for i in range(10):
            for j in range(10):
                if self.get_inner_repr(i, j) == "V":
                    self.set_inner_tile(i, j, "O")

    def get_ships(self, row=None, col=None):
        if row is None or col is None:
            return self.board_ships
        else:
            return self.board_ships[row][col]

    def get_inner_repr(self, row=None, col=None):
        if row is None or col is None:
            return self.board_inner_repr
        else:
            return self.board_inner_repr[row][col]

    def get_outer_repr(self, row=None, col=None):
        if row is None or col is None:
            return self.board_outer_repr
        else:
            return self.board_outer_repr[row][col]

    def set_ship_part(self, row: int, col: int, ship: Ship):
        self.board_ships[row][col] = ship

    def set_inner_tile(self, row: int, col: int, tile: str):
        self.board_inner_repr[row][col] = tile

    def set_outer_tile(self, row: int, col: int, tile: str):
        self.board_outer_repr[row][col] = tile


class Logger:
    def __init__(self, filename):
        self.file = open(filename, "a")
        atexit.register(self.close)

    def write(self, message):
        self.file.write(message)
        self.file.flush()

    def close(self):
        if not self.file.closed:
            self.file.close()


class Game:
    def __init__(self):
        self.board_1 = Board()
        self.board_2 = Board()
        self.player_1 = Player("Human", self.board_1)
        self.player_2 = Player("Computer", self.board_2)

        self.p1_battleship = Ship(self.player_1, 4)
        self.p1_cruiser_1 = Ship(self.player_1, 3)
        self.p1_cruiser_2 = Ship(self.player_1, 3)
        self.p1_destroyer_1 = Ship(self.player_1, 2)
        self.p1_destroyer_2 = Ship(self.player_1, 2)
        self.p1_destroyer_3 = Ship(self.player_1, 2)
        self.p1_submarine_1 = Ship(self.player_1, 1)
        self.p1_submarine_2 = Ship(self.player_1, 1)
        self.p1_submarine_3 = Ship(self.player_1, 1)
        self.p1_submarine_4 = Ship(self.player_1, 1)

        self.p2_battleship = Ship(self.player_2, 4)
        self.p2_cruiser_1 = Ship(self.player_2, 3)
        self.p2_cruiser_2 = Ship(self.player_2, 3)
        self.p2_destroyer_1 = Ship(self.player_2, 2)
        self.p2_destroyer_2 = Ship(self.player_2, 2)
        self.p2_destroyer_3 = Ship(self.player_2, 2)
        self.p2_submarine_1 = Ship(self.player_2, 1)
        self.p2_submarine_2 = Ship(self.player_2, 1)
        self.p2_submarine_3 = Ship(self.player_2, 1)
        self.p2_submarine_4 = Ship(self.player_2, 1)

        self.human_ships = (
            self.p1_battleship,
            self.p1_cruiser_1,
            self.p1_cruiser_2,
            self.p1_destroyer_1,
            self.p1_destroyer_2,
            self.p1_destroyer_3,
            self.p1_submarine_1,
            self.p1_submarine_2,
            self.p1_submarine_3,
            self.p1_submarine_4
        )

        self.computer_ships = (
            self.p2_battleship,
            self.p2_cruiser_1,
            self.p2_cruiser_2,
            self.p2_destroyer_1,
            self.p2_destroyer_2,
            self.p2_destroyer_3,
            self.p2_submarine_1,
            self.p2_submarine_2,
            self.p2_submarine_3,
            self.p2_submarine_4
        )

        self.log = Logger(
            f"battleship/logs/game_{str(datetime.now())[:19].replace(' ', '').replace(':', '').replace('-', '')}.log",
        )

    @staticmethod
    def ship_fits(*, row: int, col: int, board: Board, ship: Ship, orientation: str):
        row_factor, col_factor = (1, 0) if orientation == "v" else (0, 1)
        ship_length = ship.get_length()

        # entirely inside the map
        if row + (ship_length - 1) * row_factor > 9 or col + (ship_length - 1) * col_factor > 9:
            return False

        # not overlaps with other ships and their shades
        for i in range(ship_length):
            if board.get_inner_repr(row + i * row_factor, col + i * col_factor) != "O":
                return False

        return True

    def cheat(self):
        print(45 * "=")
        print(" C H E A T C O D E ".center(45, "="))
        print(45 * "=")
        for ship in self.computer_ships:
            print(*ship.coordinates)
        print(3 * (45 * "=" + "\n"))

    def welcome_dialogue(self):
        print("Welcome to the Battleship game!")
        name = input("Please, introduce yourself: ")
        if name:
            if name.lower() == "iseeeverything":  # cheat code
                self.cheat()
                self.player_1.set_name("Human")
            else:
                self.player_1.set_name(name)

        print("If you would like to fill your board manually, type A. If you choose a random layout, type B below")
        option = input("Your choice: ")
        while option and option.lower() != "a" and option.lower() != "b":
            option = input("Please, make a sound choice: ")

        if option.lower() == "a":
            self.manual_placement()
        elif not option or option.lower() == "b":
            self.random_placement(self.player_1)

        # remove all shades from the human's board
        self.board_1.clear_shades()

        print("Whether you or the computer starts the game will be determined randomly.")
        print("To shoot, type the row and the column of the target separated by the space, e.g. 4 6")
        print("The cell that was shot on the last turn will be painted yellow.")

    def draw_board_row(self, *, row: int, board: list, is_last: bool, last_row: int | None, last_col: int | None):
        """
        Legend:
        O — empty or unknown (blue)
        M — missed (black)
        X — hit ship part (pink)
        D — destroyed ship part (red)
        V — prohibited (black)
        W — intact ship part (white)
        any — last turn (yellow)
        """

        print(row, end=" ")
        self.log.write(f"{row} ")
        for col in range(10):
            c = board[row][col]
            if is_last and (row, col) == (last_row, last_col):
                print(f"{Fore.YELLOW}{Style.BRIGHT}{c}{Style.RESET_ALL}", end=" ")
            elif c == "O":
                print(f"{Fore.BLUE}{c}{Style.RESET_ALL}", end=" ")
            elif c == "M":
                print(f"{Fore.BLACK}{c}{Style.RESET_ALL}", end=" ")
            elif c == "X":
                print(f"{Fore.MAGENTA}{c}{Style.RESET_ALL}", end=" ")
            elif c == "D":
                print(f"{Fore.RED}{c}{Style.RESET_ALL}", end=" ")
            elif c == "V":
                print(f"{Fore.BLACK}{c}{Style.RESET_ALL}", end=" ")
            else:
                print(c, end=" ")
            self.log.write(f"{c} ")

    def manual_placement(self):
        print(
            f"{self.player_1.get_name()}, to place a ship, type its head's row and column, and its orientation (v/h), e.g.: 4 6 v"
        )
        print("Your ships will be marked as W, and their vicinity will be marked as V")
        for ship in self.human_ships:
            print(f"{Fore.GREEN}Your field{Style.RESET_ALL}")
            print("  0 1 2 3 4 5 6 7 8 9")
            for i in range(10):
                self.draw_board_row(
                    row=i,
                    board=self.board_1.board_inner_repr,
                    is_last=False,
                    last_row=None,
                    last_col=None,
                )
                print()

            # handle input
            user_input = input(f"Place a {ship.get_hp()} HP ship: ")

            condition_1 = (
                len(user_input) == 5 and
                user_input[0].isdigit() and  # maybe row
                user_input[2].isdigit() and  # maybe column
                user_input[1] == user_input[3] == " " and  # maybe the first and the second space
                user_input[4] in {"v", "h"}  # maybe orientation
            )
            condition_2 = self.ship_fits(
                row=int(user_input[0]),
                col=int(user_input[2]),
                board=self.board_1,
                ship=ship,
                orientation=user_input[4],
            ) if condition_1 else False

            while not condition_1 or not condition_2:
                if not condition_1:
                    user_input = input(f"Your input is incorrect, try again: ")
                else:
                    user_input = input(f"The placement is unacceptable, try again: ")

                condition_1 = (
                    len(user_input) == 5 and
                    user_input[0].isdigit() and
                    user_input[2].isdigit() and
                    user_input[1] == user_input[3] == " " and
                    (user_input[4].lower() == "v" or user_input[4].lower() == "h")
                )
                condition_2 = self.ship_fits(
                    row=int(user_input[0]),
                    col=int(user_input[2]),
                    board=self.board_1,
                    ship=ship,
                    orientation=user_input[4],
                ) if condition_1 else False

            self.board_1.place_ship(
                ship=ship,
                row=int(user_input[0]),
                col=int(user_input[2]),
                orientation=user_input[4],
            )

    def random_placement(self, player: Player):
        if player == self.player_1:
            ships_list = self.human_ships
            board = self.board_1
        else:
            ships_list = self.computer_ships
            board = self.board_2

        for ship in ships_list:
            orientation = random.choice(["v", "h"])

            row, col = random.randint(0, 9), random.randint(0, 9)
            while not self.ship_fits(
                row=row,
                col=col,
                board=board,
                ship=ship,
                orientation=orientation,
            ):
                row, col = random.randint(0, 9), random.randint(0, 9)

            board.place_ship(
                ship=ship,
                row=row,
                col=col,
                orientation=orientation,
            )

    def play(self):
        def draw_frame(last_hit: tuple[int, int, Player]):
            print(f"{Fore.GREEN}Your field{Style.RESET_ALL}              {Fore.RED}Enemy field{Style.RESET_ALL}")
            self.log.write(f"Your field              Enemy field\n")
            print("  0 1 2 3 4 5 6 7 8 9 \t  0 1 2 3 4 5 6 7 8 9")
            self.log.write("  0 1 2 3 4 5 6 7 8 9 \t  0 1 2 3 4 5 6 7 8 9\n")

            last_row, last_col, player = last_hit if last_hit is not None else (None, None, None)
            for i in range(10):
                self.draw_board_row(
                    row=i,
                    board=self.board_1.get_inner_repr(),
                    is_last=self.player_1 == player,
                    last_row=last_row,
                    last_col=last_col,
                )
                print("\t", end="")
                self.log.write("\t")

                self.draw_board_row(
                    row=i,
                    board=self.board_2.get_outer_repr(),
                    is_last=self.player_2 == player,
                    last_row=last_row,
                    last_col=last_col,
                )
                print()
                self.log.write("\n")

        def make_turn(
            players_order: list,
            computer_default_targets: deque,
            computer_current_targets: list,
            is_seeking: bool,
            area_of_search: dict
        ):
            def seek_the_ship(area_of_search: dict[str, deque], direction: str) -> tuple[int, int]:
                row, col = area_of_search[direction].popleft()
                if (direction == "up" or direction == "down") and defending_board.get_ships(row, col):
                    if "left" in area_of_search:
                        del area_of_search["left"]
                    if "right" in area_of_search:
                        del area_of_search["right"]
                elif (direction == "left" or direction == "right") and defending_board.get_ships(row, col):
                    if "up" in area_of_search:
                        del area_of_search["up"]
                    if "down" in area_of_search:
                        del area_of_search["down"]
                else:
                    del area_of_search[direction]

                return row, col

            attacker = players_order[0]
            defending = players_order[1]
            attacker_name = attacker.get_name()
            defending_board = defending.get_board()

            if attacker == self.player_1:
                user_input = input(f"{attacker_name}, make your turn: ")

                condition_1 = (
                    len(user_input) == 3 and
                    user_input[0].isdigit() and
                    user_input[2].isdigit() and
                    user_input[1] == " "
                )
                condition_2 = (
                    self.board_2.get_outer_repr(int(user_input[0]), int(user_input[2])) == "O"
                ) if condition_1 else False

                while not condition_1 or not condition_2:
                    if not condition_1:
                        user_input = input(f"{attacker_name}, your input is incorrect, try again: ")
                    else:
                        user_input = input(f"{attacker_name}, you can't hit this tile, try again: ")

                    condition_1 = (
                        len(user_input) == 3 and
                        user_input[0].isdigit() and
                        user_input[2].isdigit() and
                        user_input[1] == " "
                    )
                    condition_2 = (
                        self.board_2.get_outer_repr(int(user_input[0]), int(user_input[2])) == "O"
                    ) if condition_1 else False

                row, col = int(user_input[0]), int(user_input[2])
            else:
                print(f"{attacker_name} makes its turn…")
                self.log.write(f"{attacker_name} makes its turn…\n")
                time.sleep(1.5)

                if is_seeking:
                    while True:
                        direction = DIRECTIONS.popleft()
                        DIRECTIONS.append(direction)
                        if direction in area_of_search and area_of_search[direction]:
                            row, col = seek_the_ship(area_of_search, direction)
                            break
                else:
                    if not computer_current_targets:
                        computer_current_targets = computer_default_targets.popleft()
                        random.shuffle(computer_current_targets)

                    row, col = computer_current_targets.pop()
                    while not self.board_1.get_outer_repr(row, col) == "O":
                        if computer_current_targets:
                            row, col = computer_current_targets.pop()
                        else:
                            computer_current_targets = computer_default_targets.popleft()
                            random.shuffle(computer_current_targets)
                            row, col = computer_current_targets.pop()

            if ship := defending_board.get_ships(row, col):  # hit
                if attacker == self.player_2:  # computer
                    if not is_seeking:
                        is_seeking = True
                        up, right, down, left = [], [], [], []

                        delta_row, delta_col = 1, 1
                        while row - delta_row >= 0 and delta_row <= 3:
                            if defending_board.get_outer_repr(row - delta_row, col) != "O":
                                break
                            up.append((row - delta_row, col))
                            delta_row += 1
                        while col + delta_col <= 9 and delta_col <= 3:
                            if defending_board.get_outer_repr(row, col + delta_col) != "O":
                                break
                            right.append((row, col + delta_col))
                            delta_col += 1

                        delta_row, delta_col = 1, 1
                        while row + delta_row <= 9 and delta_row <= 3:
                            if defending_board.get_outer_repr(row + delta_row, col) != "O":
                                break
                            down.append((row + delta_row, col))
                            delta_row += 1
                        while col - delta_col >= 0 and delta_col <= 3:
                            if defending_board.get_outer_repr(row, col - delta_col) != "O":
                                break
                            left.append((row, col - delta_col))
                            delta_col += 1

                        area_of_search.clear()
                        if up:
                            area_of_search["up"] = deque(up)
                        if right:
                            area_of_search["right"] = deque(right)
                        if down:
                            area_of_search["down"] = deque(down)
                        if left:
                            area_of_search["left"] = deque(left)

                # mark the tile as hit
                print(f"{attacker_name} hit the ship ({row} {col})!")
                self.log.write(f"{attacker_name} hit the ship ({row} {col})!\n")
                defending_board.get_ships(row, col).lose_hp()
                defending_board.set_inner_tile(row, col, "X")
                defending_board.set_outer_tile(row, col, "X")

                # prohibit tiles that are diagonal from the one that has been hit
                for delta_row, delta_col in AROUND_SALTIRE:
                    if (
                        0 <= row + delta_row <= 9 and
                        0 <= col + delta_col <= 9 and
                        defending_board.get_outer_repr(row + delta_row, col + delta_col) == "O"
                    ):
                        defending_board.set_outer_tile(row + delta_row, col + delta_col, "V")

                # prohibit terminal tiles and replace X to D if the ship has been destroyed
                if ship.get_status() == "kia":
                    print(f"{defending.get_name()}'s ship has been destroyed")
                    self.log.write(f"{defending.get_name()}'s ship has been destroyed\n")

                    ship_coordinates = ship.get_coordinates()
                    for r, c in ship_coordinates:  # avoid "row, col" naming to not allow the name conflict
                        defending_board.set_inner_tile(r, c, "D")
                        defending_board.set_outer_tile(r, c, "D")

                    ship_edges = (ship_coordinates[0], ship_coordinates[-1])
                    for r, c in ship_edges:
                        for delta_row, delta_col in AROUND_CROSS:
                            if (
                                0 <= r + delta_row <= 9 and
                                0 <= c + delta_col <= 9 and
                                defending_board.get_outer_repr(r + delta_row, c + delta_col) == "O"
                            ):
                                defending_board.set_outer_tile(r + delta_row, c + delta_col, "V")

                    # if computer, return to the pseudorandom shooting
                    if attacker == self.player_2 and is_seeking:
                        is_seeking = False

                # game over
                if defending.get_ships_number() <= 0:
                    nonlocal turns_cnt

                    draw_frame((row, col, defending))
                    print(f"{attacker_name} has won!\nThe game took {turns_cnt} turns")
                    self.log.write(f"{attacker_name} has won!\nThe game took {turns_cnt} turns\n")
                    sys.exit(0)

            else:  # missed
                print(f"{attacker_name} missed ({row} {col})")
                self.log.write(f"{attacker_name} missed ({row} {col})\n")
                defending_board.set_inner_tile(row, col, "M")
                defending_board.set_outer_tile(row, col, "M")
                players_order.reverse()

            last_hit = row, col, defending

            return players_order, computer_current_targets, is_seeking, area_of_search, last_hit

        # setup
        turns_cnt = 1
        players_order = [self.player_1, self.player_2]
        computer_default_targets = deepcopy(COMPUTER_DEFAULT_TARGETS)
        computer_current_targets = []
        is_seeking = False
        area_of_search = {}
        last_hit = None

        random.shuffle(players_order)
        while True:
            print(f"Turn {turns_cnt}")
            self.log.write(f"Turn {turns_cnt}\n")
            draw_frame(last_hit)
            players_order, computer_current_turns, is_seeking, area_of_search, last_hit = make_turn(
                players_order,
                computer_default_targets,
                computer_current_targets,
                is_seeking,
                area_of_search,
            )
            turns_cnt += 1


def main():
    game = Game()

    game.random_placement(game.player_2)  # computer
    game.welcome_dialogue()
    game.play()


if __name__ == "__main__":
    main()
