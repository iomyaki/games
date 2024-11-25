import random


def main() -> None:
    """
    Redirect the stdout of this script to the stdin of battleship.py to brutally massacre its AI:
    python certain_win.py | python battleship.py
    """

    print("Victor Randomoff")
    print("A")
    print("3 8 v")
    print("3 4 h")
    print("5 4 h")
    print("1 4 h")
    print("8 4 h")
    print("4 2 v")
    print("0 0 v")
    print("9 0 h")
    print("0 9 v")
    print("9 9 h")

    turns = [(i, j) for i in range(10) for j in range(10)]
    random.shuffle(turns)
    for turn in turns:
        print(*turn)


if __name__ == "__main__":
    main()
