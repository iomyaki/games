import random
import sys
import time

from collections import deque
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


class Player:
    def __init__(self, name: str):
        self.name = name
        self.ships = 10

    def lose_ship(self):
        self.ships -= 1


class Ship:
    def __init__(self, owner: Player, hp: int):
        self.owner = owner
        self.hp = hp
        self.orient = None
        self.coords = []
        self.status = "online"

    def lose_hp(self):
        self.hp -= 1
        if self.hp <= 0:
            self.die()

    def die(self):
        self.status = "kia"
        self.owner.lose_ship()


class Board:
    def __init__(self):
        self.board_ships = [[None for _ in range(10)] for _ in range(10)]
        self.board_inner = [["O" for _ in range(10)] for _ in range(10)]
        self.board_outer = [["O" for _ in range(10)] for _ in range(10)]

    def place_ship(self, ship: Ship, row: int, col: int, orient: str):
        ship.orient = orient
        if orient == "v":
            a, b = 1, 0
        else:
            a, b = 0, 1

        for i in range(ship.hp):
            row_coord, col_coord = row + i * a, col + i * b

            ship.coords.append((row_coord, col_coord))
            self.board_ships[row_coord][col_coord] = ship
            self.board_inner[row_coord][col_coord] = "W"

        # draw the "shade" of the ship
        around = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for coord in ship.coords:
            for tile in around:
                if (
                    0 <= coord[0] + tile[0] <= 9 and
                    0 <= coord[1] + tile[1] <= 9 and
                    self.board_inner[coord[0] + tile[0]][coord[1] + tile[1]] == "O"
                ):
                    self.board_inner[coord[0] + tile[0]][coord[1] + tile[1]] = "V"

    def clear_shades(self):
        for i in range(10):
            for j in range(10):
                if self.board_inner[i][j] == "V":
                    self.board_inner[i][j] = "O"


class Game:
    def __init__(self):
        self.player_1 = Player("Human")
        self.player_2 = Player("Computer")
        self.board_1 = Board()
        self.board_2 = Board()

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

    @staticmethod
    def ship_fits(row: int, col: int, board: Board, ship: Ship, orient: str):
        if orient == "v":
            a, b = 1, 0
        else:
            a, b = 0, 1

        # is fully inside the map
        length = ship.hp
        if row + (length - 1) * a > 9 or col + (length - 1) * b > 9:
            return False

        # not overlaps with other ships
        for i in range(length):
            if board.board_inner[row + i * a][col + i * b] != "O":
                return False

        return True

    def cheat(self):
        print("=============================================")
        print("============= C H E A T C O D E =============")
        print("=============================================")
        for ship in self.computer_ships:
            print(*ship.coords)
        for _ in range(3):
            print("=============================================")

    def welcome_dialogue(self):
        print("Welcome to the Battleship game!")
        name = input("Please, introduce yourself: ")
        if name:
            if name.lower() == "iseeeverything":  # cheat code
                self.cheat()
                self.player_1.name = "Human"
            else:
                self.player_1.name = name

        print("If you would like to fill your board manually, type A. If you choose a random layout, type B below")
        option = input("Your choice: ")
        while option and option.lower() != "a" and option.lower() != "b":
            option = input("Please, make a sound choice: ")

        if option.lower() == "a":
            self.manual_placement()
        elif not option or option.lower() == "b":
            self.random_placement("human")

        # remove all Vs from the board
        self.board_1.clear_shades()

        print("To shoot, type the row and the column of the target separated by the space, e.g. 4 6")

    @staticmethod
    def draw_board(i: int, board: list):
        """
        Legend:
        O — empty
        M — missed
        X — hit
        D — destroyed
        V — prohibited
        W — ship
        """

        print(i, end=" ")
        for c in board[i]:
            if c == "O":
                print(f"{Fore.BLUE}{c}{Style.RESET_ALL}", end=" ")
            elif c == "M":
                print(f"{Fore.BLACK}{c}{Style.RESET_ALL}", end=" ")
            elif c == "X":
                print(f"{Fore.YELLOW}{c}{Style.RESET_ALL}", end=" ")
            elif c == "D":
                print(f"{Fore.RED}{c}{Style.RESET_ALL}", end=" ")
            elif c == "V":
                print(f"{Fore.BLACK}{c}{Style.RESET_ALL}", end=" ")
            else:
                print(c, end=" ")

    def manual_placement(self):
        print(f"{self.player_1.name}, to place a ship, type its head's row and column, and its orientation (v/h), e.g.: 4 6 v")
        print("Your ships will be marked as W, and their vicinity will be marked as V")
        for ship in self.human_ships:
            print("Your field")
            print("  0 1 2 3 4 5 6 7 8 9")
            for i in range(10):
                self.draw_board(i, self.board_1.board_inner)
                print()

            # handle input
            inp = input(f"Place a {ship.hp} HP ship: ")

            cond_1 = (
                    len(inp) == 5 and
                    inp[0].isdigit() and
                    inp[2].isdigit() and
                    inp[1] == inp[3] == " " and
                    inp[4] in {"v", "h"}
            )
            cond_2 = self.ship_fits(int(inp[0]), int(inp[2]), self.board_1, ship, inp[4]) if cond_1 else False
            while not cond_1 or not cond_2:
                if not cond_1:
                    inp = input(f"Your input is incorrect, try again: ")
                else:
                    inp = input(f"The placement is unacceptable, try again: ")

                cond_1 = (
                        len(inp) == 5 and
                        inp[0].isdigit() and
                        inp[2].isdigit() and
                        inp[1] == inp[3] == " " and
                        inp[4].lower() == "v" or inp[4].lower() == "h"
                )
                cond_2 = self.ship_fits(int(inp[0]), int(inp[2]), self.board_1, ship, inp[4]) if cond_1 else False

            self.board_1.place_ship(ship, int(inp[0]), int(inp[2]), inp[4])

    def random_placement(self, player: str):
        if player == "human":
            ships_list = self.human_ships
            board = self.board_1
        else:
            ships_list = self.computer_ships
            board = self.board_2

        for ship in ships_list:
            orient = random.choice(["v", "h"])

            row, col = random.randint(0, 9), random.randint(0, 9)
            while not self.ship_fits(row, col, board, ship, orient):
                row, col = random.randint(0, 9), random.randint(0, 9)

            board.place_ship(ship, row, col, orient)

    def play(self):
        def frame():
            print(f"{Fore.GREEN}Your field{Style.RESET_ALL}              {Fore.RED}Enemy field{Style.RESET_ALL}")
            print("  0 1 2 3 4 5 6 7 8 9 \t  0 1 2 3 4 5 6 7 8 9")
            for i in range(10):
                self.draw_board(i, self.board_1.board_inner)
                print("\t", end="")

                self.draw_board(i, self.board_2.board_outer)
                print()

        def make_turn(
                order: list,
                comp_default_turns: deque,
                comp_current_turns: list,
                seeking: bool,
                search_area: dict
        ):
            if order[0][0] == self.player_1:
                inp = input(f"{order[0][0].name}, make your turn: ")

                condition_1 = len(inp) == 3 and inp[0].isdigit() and inp[2].isdigit() and inp[1] == " "
                condition_2 = self.board_2.board_outer[int(inp[0])][int(inp[2])] == "O" if condition_1 else False
                while not condition_1 or not condition_2:
                    if not condition_1:
                        inp = input(f"{order[0][0].name}, your input is incorrect, try again: ")
                    else:
                        inp = input(f"{order[0][0].name}, you can't hit this tile, try again: ")

                    condition_1 = len(inp) == 3 and inp[0].isdigit() and inp[2].isdigit() and inp[1] == " "
                    condition_2 = self.board_2.board_outer[int(inp[0])][int(inp[2])] == "O" if condition_1 else False

                row, col = int(inp[0]), int(inp[2])
            else:
                print(f"{order[0][0].name} makes its turn...")
                time.sleep(1.5)

                if seeking:
                    if "up" in search_area and search_area["up"]:
                        row, col = search_area["up"].popleft()
                        if order[1][1].board_ships[row][col]:
                            if "left" in search_area:
                                del search_area["left"]
                            if "right" in search_area:
                                del search_area["right"]
                        else:
                            del search_area["up"]
                    elif "right" in search_area and search_area["right"]:
                        row, col = search_area["right"].popleft()
                        if order[1][1].board_ships[row][col]:
                            if "up" in search_area:
                                del search_area["up"]
                            if "down" in search_area:
                                del search_area["down"]
                        else:
                            del search_area["right"]
                    elif "down" in search_area and search_area["down"]:
                        row, col = search_area["down"].popleft()
                        if order[1][1].board_ships[row][col]:
                            if "left" in search_area:
                                del search_area["left"]
                            if "right" in search_area:
                                del search_area["right"]
                        else:
                            del search_area["down"]
                    elif "left" in search_area and search_area["left"]:
                        row, col = search_area["left"].popleft()
                        if order[1][1].board_ships[row][col]:
                            if "up" in search_area:
                                del search_area["up"]
                            if "down" in search_area:
                                del search_area["down"]
                        else:
                            del search_area["left"]
                else:
                    if not comp_current_turns:
                        comp_current_turns = comp_default_turns.popleft()
                        random.shuffle(comp_current_turns)

                    row, col = comp_current_turns.pop()
                    while not self.board_1.board_outer[row][col] == "O":
                        if comp_current_turns:
                            row, col = comp_current_turns.pop()
                        else:
                            comp_current_turns = comp_default_turns.popleft()
                            random.shuffle(comp_current_turns)
                            row, col = comp_current_turns.pop()

            ship = order[1][1].board_ships[row][col]
            if ship:  # hit
                if order[0][0].name == "Computer":
                    if not seeking:
                        seeking = True
                        up, right, down, left = [], [], [], []

                        dr, dc = 1, 1
                        while row - dr >= 0 and dr <= 3:
                            if order[1][1].board_outer[row - dr][col] != "O":
                                break

                            up.append((row - dr, col))
                            dr += 1
                        while col + dc <= 9 and dc <= 3:
                            if order[1][1].board_outer[row][col + dc] != "O":
                                break

                            right.append((row, col + dc))
                            dc += 1

                        dr, dc = 1, 1
                        while row + dr <= 9 and dr <= 3:
                            if order[1][1].board_outer[row + dr][col] != "O":
                                break

                            down.append((row + dr, col))
                            dr += 1
                        while col - dc >= 0 and dc <= 3:
                            if order[1][1].board_outer[row][col - dc] != "O":
                                break

                            left.append((row, col - dc))
                            dc += 1

                        search_area = {}
                        if up:
                            search_area["up"] = deque(up)
                        if right:
                            search_area["right"] = deque(right)
                        if down:
                            search_area["down"] = deque(down)
                        if left:
                            search_area["left"] = deque(left)

                # mark the tile as hit
                print(f"{order[0][0].name} hit the ship ({row} {col})!")
                order[1][1].board_ships[row][col].lose_hp()
                order[1][1].board_inner[row][col], order[1][1].board_outer[row][col] = "X", "X"

                # prohibit tiles that are diagonal from the one has been hit
                around_diag = ((-1, -1), (-1, 1), (1, 1), (1, -1))
                for dr, dc in around_diag:
                    if (
                        0 <= row + dr <= 9 and
                        0 <= col + dc <= 9 and
                        order[1][1].board_outer[row + dr][col + dc] == "O"
                    ):
                        order[1][1].board_outer[row + dr][col + dc] = "V"

                # prohibit terminal tiles and replace X to D, if the ship has been destroyed
                if ship.status == "kia":
                    print(f"{order[1][0].name}'s ship has been destroyed")
                    for r, c in ship.coords:
                        order[1][1].board_inner[r][c], order[1][1].board_outer[r][c] = "D", "D"

                    ship_ends = (ship.coords[0], ship.coords[-1])
                    around_cross = ((0, -1), (-1, 0), (0, 1), (1, 0))
                    for r, c in ship_ends:
                        for dr, dc in around_cross:
                            if (
                                0 <= r + dr <= 9 and
                                0 <= c + dc <= 9 and
                                order[1][1].board_outer[r + dr][c + dc] == "O"
                            ):
                                order[1][1].board_outer[r + dr][c + dc] = "V"

                    # if computer, return to "random" shooting
                    if order[0][0].name == "Computer" and seeking:
                        seeking = False

                # endgame
                if order[1][0].ships <= 0:
                    frame()
                    print(f"{order[0][0].name} has won!")
                    sys.exit(0)

            else:  # missed
                print(f"{order[0][0].name} missed ({row} {col})")
                order[1][1].board_inner[row][col], order[1][1].board_outer[row][col] = "M", "M"

                order.reverse()

            return order, comp_current_turns, seeking, search_area

        comp_default_turns = deque([
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
        ])
        comp_current_turns = []
        seeking = False
        search_area = {}

        # setup
        order = [(self.player_1, self.board_1), (self.player_2, self.board_2)]
        random.shuffle(order)
        while True:
            if order[0][0] == self.player_1:
                frame()
            order, comp_current_turns, seeking, search_area = make_turn(
                order,
                comp_default_turns,
                comp_current_turns,
                seeking,
                search_area
            )


def main():
    game = Game()

    game.random_placement("Computer")
    game.welcome_dialogue()
    game.play()


if __name__ == "__main__":
    main()

# at the end show, how many turns the game took
# mark the last turn with different color
