import random
from copy import deepcopy
from math import floor
from ru_loto_cards_std import cards
from ru_loto_cards_rand import get_random_card


class Player:
    def __init__(self, name, score, n_cards):
        self.name = name
        self.score = score
        self.n_cards = n_cards
        self.cards = []

    def get_cards(self):
        global free_cards

        self.cards = []  # but what if player wants to save some cards?
        for _ in range(self.n_cards):
            self.cards.append(deepcopy(free_cards.pop()))

    def pay(self):
        global bank

        self.score -= self.n_cards
        bank += self.n_cards

    def get_half_bank(self):
        global bank

        amount = int(floor(bank / 2))
        self.score += amount
        bank -= amount

    def get_bank(self):
        global bank

        self.score += bank
        bank = 0


#random.seed(42)
random_cards = False
number_of_parties = 100
bank = 10
debug = False

player_1 = Player('Socrates', 500, 1 if debug else 3)  # but n_cards can change every party
player_2 = Player('Plato', 500, 1 if debug else 3)
player_3 = Player('Aristotle', 500, 18)

if debug:
    players = [player_1, player_2]
else:
    players = [player_1, player_2, player_3]

for _ in range(number_of_parties):
    if random_cards:
        for player in players:
            player.cards = []
            for i in range(player.n_cards):
                player.cards.append(get_random_card())
            player.pay()
    else:
        free_cards = deepcopy(cards)
        random.shuffle(free_cards)

        for player in players:
            player.get_cards()
            player.pay()

        del free_cards

    if debug:
        for player in players:
            print(f"{player.name}:")
            for card in player.cards:
                print(card.upper, card.middle, card.lower, sep='\n')
        print('==================================')

    numbers = [n for n in range(1, 91)]
    random.shuffle(numbers)

    someone_won = False

    while numbers:
        random.shuffle(players)  # to imitate the players' reaction speed
        checking = True

        keg = numbers.pop()

        if debug:
            print(f'Keg {keg} has been extracted')

        for player in players:
            if someone_won:
                break
            else:
                for card in player.cards:
                    if keg in card.lower:
                        card.lower.remove(keg)
                        if len(card.lower) == 0:
                            someone_won = True
                            player.get_bank()

                            if debug:
                                print(f'{player.name} has won in this party!')

                            break

        if someone_won:
            break

        for player in players:
            for card in player.cards:
                if keg in card.middle:
                    card.middle.remove(keg)
                    if len(card.middle) == 0 and checking:
                        checking = False
                        player.get_half_bank()
                        for other_player in players:
                            if other_player != player:
                                other_player.pay()

        for player in players:
            for card in player.cards:
                if keg in card.upper:
                    card.upper.remove(keg)
                    if len(card.upper) == 0 and checking:
                        checking = False
                        for other_player in players:
                            if other_player != player:
                                other_player.pay()

        if debug:
            for player in players:
                print(f"{player.name}:")
                for card in player.cards:
                    print(card.upper, card.middle, card.lower, sep='\n')
            print('==================================')
            print(f'Bank now: {bank}')
            print(f"Players' score now: {player_1.score}, {player_2.score}")

    if debug:  # after finishing the party
        print(f'After party — bank: {bank}')
        print(f"After party — players' score: {player_1.score}, {player_2.score}")

    '''
    for card in player_1.cards:
        print(card.number, end=' ')
    print()
    for card in player_2.cards:
        print(card.number, end=' ')
    print()
    for card in player_3.cards:
        print(card.number, end=' ')
    '''

print(f"In the end — players' score: {player_1.score}, {player_2.score}, {player_3.score}")
